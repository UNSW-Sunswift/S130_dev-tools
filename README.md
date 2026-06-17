# S130 Development tools V1.2.0

## Version Notes: v1.3.0 
- Upgraded `srpkg` to V3.1 with decoupled logic/node architecture and native unit test generation.
- Added `srtest` testing engine with native coverage, AddressSanitizer (ASan), and CI/CD XML/JSON logging.
- Upgraded `srbuild` with improved repository root validation and safer clean removal.

## Introduction
This repository contains high-level development tools for Sunswift embedded and DDS projects. It is separated into host/ and target/. host/ contains the dev tools we are using during development time on our host machines. target/ contains scripts that should be run on the target (NVIDIA Drive THOR computer). It is intended to be a submodule in the SR-Mjolnir repository.


It includes:

- `srpkg`: DDS package creation and management tool
- `srbuild`: Build tool for compiling and deploying DDS packages
- `srlaunch`: Tool for starting nodes
- `srtest`: Complete dynamic testing engine for executing unit tests, memory checks, and code coverage
- `srdds`: (WORK IN PROGRESS) Tool for managing active nodes

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
srpkg create <package_name>
```

This will create a new directory with the following structure:

```
<package_name>/
├── .srpkg                                # Package metadata file
├── CMakeLists.txt                        # Build configuration template
├── README.md                             # Package documentation
├── include/
│   ├── <package_name>_logic.hpp          # Math/Logic definitions
│   └── <package_name>_node.hpp           # DDS Node definitions
├── param/
│   └── <package_name>_param.toml         # Default TOML parameter template
├── src/
│   ├── <package_name>_logic.cpp          # Math/Logic implementation
│   ├── <package_name>_node.cpp           # DDS Node implementation
│   └── main.cpp                          # Executable entry point
└── test/
    └── unit/
        └── test_<package_name>_unit.cpp  # GoogleTest suite block
```

The package will be created in your current working directory.

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
`srbuild` automatically creates or overwrites root level `build/` and `deploy/` directories. It builds all objects, libraries and binaries into `build/` (don't bother touching this, it's needed for CMake), then installs all runtime files into `deploy/` for easy deployment (use this).
```
SR-Mjolnir/
├── build/          # CMake-required files
├── deploy/
│     ├── bin/       # Node executables
│     ├── param/
│     └── tools/     # srlaunch, srdds
└── ...
```
#### Building all targets:

To build and install all available targets in the repository:

```bash
srbuild all
```

#### Building specific targets:

To build only specific packages or libraries:

```bash
srbuild target node1 node2 ...
```
This automatically builds dependencies if required.
#### Cleaning the build:

To delete the build directory:

```bash
srbuild clean
```

#### Parallel jobs:

By default, `srbuild` uses 8 parallel jobs for compilation. You can customize this:

```bash
srbuild all --jobs 4
srbuild target package1 -j 16
```
### 4. Using srlaunch
Run `srlaunch` from the `deploy/tools` directory only. The version in the submodule repo is for version control.
```bash
cd deploy/tools
./srlaunch all
./srlaunch target node1 node2
```

### 5. Using srtest
`srtest` is a zero-config testing engine that discovers compiled unit tests, calculates exact line and function coverage, and monitors runtime memory safety using AddressSanitizer (ASan).

Ensure you have run `srbuild all` (with testing enabled in CMake) before executing tests.

#### Running tests:
```bash
# Runs all available test executables 
srtest all

# Run everything except specific nodes
srtest all --except tpms motor

# Run only the specific nodes you are working on
srtest node pedal_box

# Run only test cases matching a specific name pattern
srtest -f "*Parse*" node pedal_box

# Export structured XML/JSON reports to a target directory
srtest -o build/test-results all
```

Then just `Ctrl-C` to shut down all nodes gracefully. It's that easy guys.
## Example Workflow

1. Create a new DDS package:
   ```bash
   cd /path/to/repo/src
   srpkg create my_dds_node
   ```

2. Add your source code to `my_dds_node/src/` and headers to `my_dds_node/include/`

3. Fill out the template CMakeLists.txt

4. Add `add_subdirectory(relative/path/to/my_dds_node)` to src/CMakeLists.txt to enable the build

5. Build the package and test suite:
   ```bash
   srbuild target my_dds_node
   # or
   srbuild all
   ```

6. Verify your logic and memory safety: 
   ```bash 
   srtest node my_dds_node
   ```

7. Launch the node:
   ```bash
   # in deploy/tools
   ./srlaunch target my_dds_node
   # OR
   ./srlaunch all
   ```
## Notes

- Both tools must be run from within the SR-Mjolnir repository
- `srpkg` creates packages in the current working directory
- `srbuild` operates on the entire repository build system
- `srtest` discovers and runs test binaries from the build directory
- `srlaunch` is used from the deploy directory
- `srdds` is currently work in progress

## Contributors
Ryan Wong || z5417983
Henry Jiang || z5416365
Vipul Kumar Chiluvery || z5476881