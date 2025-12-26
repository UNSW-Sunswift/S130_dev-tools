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
#     build/
#     src/
#     include/
#     config/
#     launch/
#     CMakelists.txt
#     README.md
#
# build -> for CMakelists.txt to put artifacts and final binary
# src -> all your .cpp files
# include -> all your .hpp files
# config -> json files (probably) for node configs + params + choice of launch file
# launch -> containing one or more launch files
# 
# Usage in directory you want to create pkg in:
#   
###############################################################################

import argparse
import sys
import re
import shutil
import json
from typing import Optional, Tuple
from datetime import datetime
from pathlib import Path

CWD = Path.cwd()
# THIS ASSUMES THAT node_registry.json is 2 directories above this script and in the repo root...
REPO_ROOT = Path(__file__).resolve().parents[2]
NODE_REG_PATH = REPO_ROOT / "node_registry.json"


### HELPERS =====================================================================================

def die(msg: str) -> None:
    print(msg)
    sys.exit(1)
    
def dir_size(path: Path) -> int:
    return sum(
        p.stat().st_size
        for p in path.rglob("*")
        if p.is_file()
    )

def fill_readme(path: Path) -> bool:
    pass

def fill_cmakelists(path: Path) -> bool:
    pass

def fill_launch(path: Path) -> bool:
    pass

def fill_config(path: Path) -> bool:
    pass

def pkg_exist(pkg_name:str, abs_pkg_path: Path) -> tuple[bool, Optional[str]]:
    # Check if package already exists in cwd
    if abs_pkg_path.exists() and abs_pkg_path.is_dir():
        return (True, str(abs_pkg_path.relative_to(REPO_ROOT)))

    # Check if it already exists in node_registry.json somewhere else
    data = json.loads(NODE_REG_PATH.read_text())
    found_pkg = next((node for node in data["nodes"] if node["name"] == pkg_name), None)
    if found_pkg:
        return (True, found_pkg["path"])

    return (False, None)

def create_or_delete_entry(create: bool, pkg_name: str, abs_pkg_path: Path) -> bool:
    """Creates or deletes node_registry entry depending on a flag.
    ASSUMES ALL CHECKING HAS BEEN DONE BEFORE
    Args:
        create (bool): flag to create or del
        pkg_name (str): raw pkg name (not path)
        abs_pkg_path (Path): absolute path relative to fs root
    Returns:
        bool: if success or not
    """
    data = json.loads(NODE_REG_PATH.read_text())
    if create:
        # Add entry
        new_entry = {
            "name": pkg_name,
            "type": "rti_dds",
            "path": str(abs_pkg_path.relative_to(REPO_ROOT)),
            "target": "qnx"
        }
        data["nodes"].append(new_entry)
    else:
        # Delete entry
        index = next((i for i, node in enumerate(data["nodes"]) if node["name"] == pkg_name), None)
        if index is None:
            print("Package does not exist (failed previous checks...)")
            return False
        data["nodes"].pop(index)
    
    # Write to registry
    try:
        NODE_REG_PATH.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    except IOError as e:
        print(f"An error has occured: {e}")
        return False
    
    return True

### CORE LOGIC ==================================================================================

def pkg_create(pkg_name: str) -> None:
    """Creates directory based on structure in top comment if it doesn't already exist.
    Also registers it to node_registry.json.
    
    Args:
        pkg_name (str): pkg_name passed in from CL args
    """
    abs_pkg_path = CWD / pkg_name
    nested_dirs = ["build", "src", "include", "config", "launch"]
    files = ["CMakelists.txt", "README.md"]
    
    # Check if pkg already exists
    res, location = pkg_exist(pkg_name, abs_pkg_path)
    if res:
        die(f"Package: {pkg_name} already exists at '{location}'")

    # Create directories and files    
    for dir in nested_dirs:
        (abs_pkg_path / dir).mkdir(parents=True)
    for file in files:
        (abs_pkg_path / file).touch()
        
    # TODO: Populate CMakeLists.txt, README.md and create launch and config templates

    # Create node_registry entry
    res = create_or_delete_entry(True, pkg_name, abs_pkg_path)
    if not res:
        die("Error creating node registry entry\nExiting...")

    print("Package: create success")
    print(f"Package: '{pkg_name}' created at '{abs_pkg_path.relative_to(REPO_ROOT)}'")
    print(f"Package: registered in node_registry")


def pkg_delete(pkg_name: str) -> None:
    """Deletes directory with pkg_name if it's in the cwd, and it's a Sunswift DDS pkg
    Also unregisters it from node_registry.json
     
    Args:
        pkg_name (str): pkg_name passed in from CL args
    """ 
    abs_pkg_path = CWD / pkg_name
    
    res, location = pkg_exist(pkg_name, abs_pkg_path)
    if not res:
        die(f"Package: {pkg_name} not found")
    
    stats = abs_pkg_path.stat()
    print(f"Found Sunswift DDS package: {pkg_name}")
    print(f"Package size (bytes): {dir_size(abs_pkg_path)}")
    print(f"Created: {datetime.fromtimestamp(stats.st_ctime).strftime("%Y-%m-%d %H:%M:%S")}")
    res = input(f"Do you really want to delete {pkg_name} (y/n): ")
    print("-----")
    if res.lower() == "y":
        # TODO: MAKE THIS SAFER!
        shutil.rmtree(abs_pkg_path)
        
        res = create_or_delete_entry(False, pkg_name, abs_pkg_path)
        if not res:
            die(f"Error deleting node from registry\nExiting...")
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
        die("Invalid package name: must be in 'snake_case'")
        
    ### TODO: SANITY CHECK -> check node_registry.json exists and is in correct path. 
    # check that script is run in repo
    # warn if not in src/
    
    ### Logic based on flags
    if args.create:
        pkg_create(pkg_name)
    elif args.delete:
        pkg_delete(pkg_name)
    # TODO: find and mv flags

if __name__ == "__main__":
    main()