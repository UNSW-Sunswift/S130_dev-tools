#!/usr/bin/env python3

###############################################################################
# Sunswift High Level DDS Package generator
# Version: V0.1
# Date: 24/12/2025
# Author: Ryan Wong
#
# Creates a new package according to this structure in the directory which you
# run this script from
# 
# <package_name>/
#     src/
#     include/
#     config/
#     launch/
#     logs/
#     CMakeLists.txt
#     README.md
#
# src -> all your .cpp files
# include -> all your .hpp files
# config -> json files (probably) for node configs + params + choice of launch file
# launch -> containing one or more launch files
# logs -> directory for node output logs
# 
# Usage in directory you want to create pkg in:
#   
###############################################################################

import argparse
import sys
import re
import shutil
import json
from datetime import datetime
from pathlib import Path

cwd = Path.cwd()

### CORE LOGIC ==================================================================================

def pkg_create(pkg_name: str) -> None:
    """Creates directory based on structure in top comment if it doesn't already exist
    Also registers it to node_registry.json
    
    Args:
        pkg_name (str): pkg_name passed in from CL args
    """
    pkg_path = cwd / pkg_name
    nested_dirs = ["src", "include", "config", "launch", "logs"]
    files = ["CMakelists.txt", "README.md"]
    
    # TODO: Check if package already exists in cwd
    
    # TODO: Check if it already exists in node_registry.json somewhere else
    
    for dir in nested_dirs:
        (pkg_path / dir).mkdir(parents=True)
    for file in files:
        (pkg_path / file).touch()
        
    # TODO: Register this package in node_registry.json
    print("Package: create success")
    print(f"Package: {pkg_name} created at {pkg_path}")


def pkg_delete(pkg_name: str) -> None:
    """Deletes directory with pkg_name if it's in the CWD, and it's a Sunswift DDS pkg
    Also unregisters it from node_registry.json
     
    Args:
        pkg_name (str): pkg_name passed in from CL args
    """ 
    pkg_path = cwd / pkg_name
    
    if not (pkg_path.exists() and pkg_path.is_dir()):
        print(f"Package with name: '{pkg_name}' not found in current directory")
        sys.exit(1)
    
    # TODO check if it is a valid Sunswift DDS package from node_registry
    
    stats = pkg_path.stat()
    print(f"Found Sunswift DDS package: {pkg_name}")
    print(f"Package size (bytes): {stats.st_size}")
    print(f"Created: {datetime.fromtimestamp(stats.st_ctime).strftime("%Y-%m-%d %H:%M:%S")}")
    res = input(f"Do you really want to delete {pkg_name} (y/n): ")
    print("-----")
    if res.lower() == "y":
        shutil.rmtree(pkg_path)
        print(f"Package: {pkg_name} deleted")
        print(f"Package: {pkg_name} removed from node registry")
    else:
        print("Stopping delete...")
        sys.exit(0)
                
    
### MAIN =======================================================================================
def main():
    ### Command line arguments
    parser = argparse.ArgumentParser(
            description="Sunswift DDS package management tool. \
            To create and delete packages, you must be in the same directory as the package"
        )
    group = parser.add_mutually_exclusive_group(required=True)

    parser.add_argument("pkg_name", help="Name of package to be created/deleted")
    group.add_argument("-c", "--create", action="store_true", help="Create specified package")
    group.add_argument("-d", "--delete", action="store_true", help="Remove specified package")
    group.add_argument("-f", "--find", action="store_true", help="Find specified package")
    args = parser.parse_args()
    
    pkg_name = args.pkg_name
    
    ### Validate package name
    pattern = r"^[a-z0-9_]*$"
    if not re.match(pattern, pkg_name):
        print("Invalid package name: must be in 'snake_case'")
        sys.exit(1)
    
    ### Logic based on flags
    if args.create:
        pkg_create(pkg_name)
    elif args.delete:
        pkg_delete(pkg_name)


if __name__ == "__main__":
    main()