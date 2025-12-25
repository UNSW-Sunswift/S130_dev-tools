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


### Helpers ==================================================================
die() {
    echo -e "$*" >&2
    exit 1
}

cleanup() {
    echo "ERR: pkg_create failed at: $BASH_COMMAND" >&2
    echo "Line number: $LINENO" >&2
    echo "Cleaning up..." >&2
    [[ -d "$pkg_name" ]] && rm -rf "$pkg_name"
}


### Core functions ===========================================================
template_readme() {
    cat > "$pkg_name"/README.md <<EOF
# $pkg_name DDS Package

## Description
Briefly describe the purpose of this DDS node.

## Topics Published to
Enter topics published to below
Topic | C++ Type | Description
------|------|------------
/domain/subsystem/topic|\`C++ Type\`|BMS Voltage

## Topics Subscribed to
Enter topics subscribed to below
Topic | C++ Type | Description
------|----------|------------
/domain/subsystem/topic|\`C++ Type\`|BMS Voltage


## Parameters
Under construction!

## Acknowledgements
Written by \`Your name here\` | \`Your zID here\`
EOF
}

# Creates pkg given a name. No error handling
create_pkg() {
    mkdir -p "$pkg_name"/{src,include,config,launch,logs}
    touch "$pkg_name"/{Makefile,README.md}

    # Fill out templates
    template_readme
}


### Main function=============================================================
main() {
    pkg_name=""
    mode=""
    # command line args handling
    while [[ "$#" -ne 0 ]]; do
        case "$1" in
            -n|--name) 
                pkg_name="$2"
                shift 2
                ;;
            -i|--install)
                mode="install"
                shift
                ;;
            -d|--delete)
                mode="delete"
                shift
                ;;
            *)
                echo "Unknown option: $1" >&2
                die "Usage: "
                ;;
        esac
    done

    # global pkg_name
    pkg_name="$1"
    trap cleanup ERR

    if [[ -d "$pkg_name" ]]; then
        die "ERR: Package already exists" # will do more error checking later
    fi

    # create package
    create_pkg
    echo "Package $pkg_name created successfully"
}

# Call main and pass in all command-line args
main "$@"
