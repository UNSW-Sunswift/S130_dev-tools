# S130 Development tools V1.3.0

## Version Notes: v1.3.0
srpkg:
- Added `--linux` and `--qnx` flags to `srpkg create` which adds a conditional compile statement to the top of the CMakeLists.txt. Defaults to qnx. The compiler cache variable is set in the toolchain file in SR-Mjolnir.
- Refactored to remove ugly globals and update docstrings

srbuild:
- Added `--linux` and `--qnx` flags to all `srbuild` subcommands which initialises cmake with qnx toolchain file or doesn't. Defaults to qnx. For `srbuild clean` it deletes both `build/qnx` and `build/linux`
- `srbuild` now generates `build/linux` or `build/qnx` instead of just `build`
- Also refactored to remove globals
- Updated and added new pytests

common_helpers.py:
- Renamed from srutils.py


## Introduction
This repository contains high-level development tools for Sunswift embedded and DDS projects. It is separated into host/ and target/. host/ contains the dev tools we are using during development time on our host machines. target/ contains scripts that should be run on the target. It is intended to be a submodule in the SR-Mjolnir repository. Because of this, `srbuild` and `srpkg` are tightly coupled to SR-Mjolnir. If future maintainers want to generalise this tool, please change the logic which verifies/depends on repository structure and build/CMakeLists.txt layout.

> **TARGET/SRLAUNCH IS NOW DEPRECATED AS WE WILL USE QNX'S OWN PROCESS MANAGEMENT TOOL**

It includes:

- `srpkg`: DDS package creation and management tool
- `srbuild`: Build tool for compiling and deploying DDS packages


## Getting Started

### 1. Add host dev tools to your PATH

To make `srpkg` and `srbuild` available globally:

```bash
export PATH="$PATH:<absolute_path_to_repo>/sunswift-dev-tools/host"
```
I recommend adding this to your .bashrc
### 2. Using srpkg

`srpkg` is a tool for creating and managing DDS packages. It must be run from within the repository.

#### Creating a new DDS package:
To create a new DDS package in the **current working directory**:

```bash
srpkg create <package_name> [--linux | --qnx]
```

This will create a new directory with the following structure:

```
<package_name>/
├── .srpkg                             # Package metadata file
├── src/                               # Source files (.cpp)
├── include/                           # Header files (.hpp)
├── test/                              # Unit tests
├── param/                             # Parameter files
├── param/<package_name>_param.toml    # Default parameter template
├── CMakeLists.txt                     # Build configuration template
└── README.md                          # Package documentation
```

The package will be created in your **current working directory**. Packages default to QNX as the build target, but you can specify `--linux` instead. Technically `--qnx` is redundant, but for clarity's sake it's there.

#### Package information and listing:
These commands may be used from anywhere in the repository

```bash
# Show information about a specific package
srpkg info <package_name>

# List all packages in the repository
srpkg list
```

### 3. Using srbuild

`srbuild` is a wrapper around CMake that simplifies building DDS packages and targets. It must be run from within the repository, but can be used from anywhere within, not necessarily root.

#### Output:
`srbuild` automatically creates or overwrites root level `build/[qnx | linux]` and `deploy/[qnx | linux]` directories. It builds all objects, libraries and binaries into `build/[qnx | linux]` (don't bother touching this, it's needed for CMake), then installs all runtime files into `deploy/[qnx | linux]` for easy deployment (use this). By default, it builds using the qnx toolchain file which is hardcoded to live at `SR-Mjolnir/cmake/qnx.toolchain.cmake`.
```
SR-Mjolnir/
├── cmake/
│     └── qnx.toolchain.cmake    # QNX toolchain file
├── build/                       # CMake-required files
│     ├── qnx/
│     └── linux/
├── deploy/
│     ├── qnx/
│     │     ├── bin/
│     │     └── param/
│     └── linux/
│           ├── bin/
│           └── param/
└── ...
```
#### Building all targets:

To build and install all available targets in the repository:

```bash
srbuild all [--linux | --qnx]
```

#### Building specific targets:

To build only specific packages or libraries:

```bash
srbuild target node1 node2 ... [--linux | --qnx]
```
This automatically builds dependencies if required.
#### Cleaning the build:

To delete the entire build directory (including `build/qnx` and `build/linux`):

```bash
srbuild clean
```

#### Parallel jobs:

By default, `srbuild` uses 8 parallel jobs for compilation. You can customize this:

```bash
srbuild all --jobs 4
srbuild target package1 -j 16
```

## Example Workflow

1. Create a new DDS package:
   ```bash
   cd /path/to/repo/src
   srpkg create my_dds_node
   ```

2. Add your source code to `my_dds_node/src/`, headers to `my_dds_node/include/` and unit tests to `my_dds_node/test/`

3. Fill out the template CMakeLists.txt

4. Build the package:
   ```bash
   srbuild target my_dds_node
   # or
   srbuild all
   ```

5. Ready to deploy or test!
## Notes

- Both tools must be run from within the SR-Mjolnir repository
- `srpkg` creates packages in the current working directory
- `srbuild` operates on the entire repository build system

## Contributors
- Ryan Wong || z5417983
- Henry Jiang || z5416365
