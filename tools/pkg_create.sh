#!/usr/bin/env bash
set -ueo pipefail

###############################################################################
# Sunswift High Level DDS Package generator
# Version: V0.1
# Date: 22/12/2025
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
#     Makefile # or CMakeLists.txt, haven't decided yet
#     README.md
#
# src -> all your .cpp files
# include -> all your .hpp files
# config -> json files (probably) for node configs + params + choice of launch file
# launch -> containing one or more launch files
# logs -> directory for node output logs
# 
# Usage:
###############################################################################

### Handle command line args and error checks
if [[ $# -ne 1 ]]; then
    echo "ERR: Missing parameters"
    echo "Usage: $0 <package_name>"
    exit 1
fi

pkg_name="$1"

if [[ -d "$pkg_name" ]]; then
    echo "ERR: Package already exists" # will do more error checking later
    exit 1
fi

### Create package
mkdir -p "$pkg_name"/{src,include,config,launch,logs}
touch "$pkg_name"/{Makefile,README.md}

echo "Package $pkg_name created successfully"
