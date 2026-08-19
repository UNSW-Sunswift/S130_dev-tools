#!/usr/bin/env python3

###############################################################################
# Sunswift High Level DDS Package generator
# Author: Ryan Wong
#
# Creates a new package according to this structure in the directory which you
# run this script from
#
# <package_name>/
#     .srpkg
#     src/
#     include/
#     test/
#     param/
#     CMakeLists.txt
#     README.md
#
# src -> all your .cpp files
# include -> all your .hpp files
# test -> all your test files
# param -> files for static params
#
# Usage in directory you want to create package in:
#   - srpkg create <name>
###############################################################################

import argparse
import re
import shutil
from pathlib import Path
from dataclasses import dataclass
from sr_dev_tools.common_helpers import die

# =================================================================================================
# CONSTANTS
# =================================================================================================
CWD = Path.cwd().resolve()

# All of these are relative to pkg top level
NESTED_DIRS = {
    "src": "src",
    "include": "include",
    "param": "param",
    "test": "test"
}
FILES = {
    "metadata": ".srpkg",
    "make": "CMakeLists.txt",
    "readme": "README.md",
    "param": "param/{pkg_name}_param.toml",
    "main": "src/main.cpp"
}

@dataclass
class PkgPaths:
    pkg_name: str
    abs_pkg_path: Path

# =================================================================================================
# HELPERS
# =================================================================================================

def fill_readme(paths: PkgPaths) -> None:
    text = f"""# {paths.pkg_name} DDS Package

## Description
Briefly describe the purpose of this DDS node.

## Topics Published to
Enter topics published to below
Topic | Topic Type | Description
------|----------|------------
/domain/subsystem/topic|`Topic Type`|BMS Voltage

## Topics Subscribed to
Enter topics subscribed to below
Topic | Topic Type | Description
------|----------|------------
/domain/subsystem/topic|`Topic Type`|BMS Voltage

## Parameters
Under construction!

## Contributors
Written by `Your name here` | `Your zID here`"""
    with (paths.abs_pkg_path / FILES["readme"]).open("w") as file:
        file.write(text)

def fill_cmakelists(paths: PkgPaths) -> None:
    text = f"""# Per-node info
set(TARGET_NAME {paths.pkg_name})
set(SOURCES
    src/main.cpp
    # Add your sources here
)
set(INCLUDE_DIRS
    include
)
set (LIBS
    sr_node
    # add your type libraries here
    # add other dependencies here
)
set(PARAM_FILE param/{paths.pkg_name}_param.toml)

# Compile and link
add_executable(${{TARGET_NAME}} ${{SOURCES}})
target_include_directories(${{TARGET_NAME}} PRIVATE ${{INCLUDE_DIRS}})
target_link_libraries(${{TARGET_NAME}} PRIVATE ${{LIBS}})

# Install time
install(
    TARGETS ${{TARGET_NAME}}
    RUNTIME DESTINATION bin
    COMPONENT ${{TARGET_NAME}}
)
if(PARAM_FILE)
    install(
        FILES ${{PARAM_FILE}}
        DESTINATION param
        COMPONENT ${{TARGET_NAME}}
    )
endif()
"""
    with (paths.abs_pkg_path / FILES["make"]).open("w") as file:
        file.write(text)

def fill_param(paths: PkgPaths) -> None:
    text = f"""# {paths.pkg_name}_param.toml
# Parameter file for {paths.pkg_name}
# All parameters are optional. Missing keys fall back to declared defaults in the node.
# Undeclared parameters are ignored

[params]
# example_string = "hello"
# example_int    = 42
# example_float  = 3.14
# example_bool   = true

"""
    with (paths.abs_pkg_path / FILES["param"].format(pkg_name=paths.pkg_name)).open("w") as file:
        file.write(text)

def fill_main(paths: PkgPaths) -> None:
    text = f"""// #include "my_node.hpp" TODO: change to your node

int main(int argc, char* argv[]) {{
    // TODO: initialise SRNode
    // TODO: Spin SRNode and catch exceptions
    return 0;
}}

"""
    with (paths.abs_pkg_path / FILES["main"]).open("w") as file:
        file.write(text)

def validate_name(name: str) -> PkgPaths:
    pattern = r"^[a-z0-9_]+$"
    if not re.match(pattern, name):
        die("[srpkg] Invalid package name: must be in 'snake_case'")
    return PkgPaths(name, CWD / name)

# =================================================================================================
# CORE LOGIC
# =================================================================================================

def parse_args() -> argparse.Namespace:
    """Build the CLI parser and return parsed arguments."""
    root_parser = argparse.ArgumentParser(
        description="Sunswift DDS package management tool. "
                    "Packages are created in your current working directory."
    )
    level1_junction = root_parser.add_subparsers(dest="command", required=True)
    command_create = level1_junction.add_parser("create")
    command_create.add_argument("name", help="Name of package to create (snake_case)")

    return root_parser.parse_args()

def mkdir_package(paths: PkgPaths) -> None:
    """Create the package directory tree and empty files."""
    paths.abs_pkg_path.mkdir()
    for dir in NESTED_DIRS.values():
        (paths.abs_pkg_path / dir).mkdir()
    for file in FILES.values():
        new_file = file
        if "{pkg_name}" in file:
            new_file = file.format(pkg_name=paths.pkg_name)
        (paths.abs_pkg_path / new_file).touch()

def pkg_create(paths: PkgPaths) -> None:
    """Create a new package in CWD if no directory with that name already exists.

    Args:
        paths: Package name and absolute destination path.
    """
    if paths.abs_pkg_path.exists():
        die(f"[srpkg] Error: '{paths.pkg_name}' already exists at '{paths.abs_pkg_path}'")

    try:
        mkdir_package(paths)
        fill_readme(paths)
        fill_cmakelists(paths)
        fill_param(paths)
        fill_main(paths)
    except Exception as e:
        if paths.abs_pkg_path.exists():
            shutil.rmtree(paths.abs_pkg_path)
        die(f"[srpkg] Error creating package: {e}")

    print(f"[srpkg] Package '{paths.pkg_name}' created successfully!")
    print(f"[srpkg] Location: {paths.abs_pkg_path}\n")

    print("[srpkg] Created structure:")
    for dir in NESTED_DIRS.values():
        print(f"  {dir}")
    for file_name in FILES.values():
        if "{pkg_name}" in file_name:
            file_name = file_name.format(pkg_name=paths.pkg_name)
        print(f"  {file_name}")

# =================================================================================================
# MAIN
# =================================================================================================
def main():
    args = parse_args()

    if args.command == "create":
        paths = validate_name(args.name)
        pkg_create(paths)


if __name__ == "__main__":
    main()
