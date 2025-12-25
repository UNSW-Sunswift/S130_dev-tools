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
import json
from pathlib import Path

cwd = Path.cwd()

def pkg_create(pkg_name: str) -> bool:
    """Creates directory based on structure in top comment if it doesn't already exist
    Args:
        pkg_name (str): pkg_name passed in from CL args
    Returns:
        bool: If pkg_creation was successful
    """
    nested_dirs = ["src", "include", "config", "launch", "logs"]
    files = ["CMakelists.txt", "README.md"]
    new_pkg_path = cwd / pkg_name
    
    for dir in nested_dirs:
        (new_pkg_path / dir).mkdir(parents=True)
        
    for file in files:
        (new_pkg_path / file).touch()

    return True
    

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


if __name__ == "__main__":
    main()