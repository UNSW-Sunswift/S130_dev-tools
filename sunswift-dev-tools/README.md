# Sunswift Dev Tools V1.0

This repository contains high-level development tools for Sunswift embedded and DDS projects. It is separated into host/ and target/. host/ contains the dev tools we are using during development time on our host machines. target/ contains scripts that should be run on the target (NVIDIA Drive THOR computer). It is intended to be a submodule in the SR-Mjolnir repository.


It includes:

- `srpkg`: DDS package creation and management tool  
- `srbuild`: Build tool for compiling and deploying DDS packages  
- `srlaunch`: (WORK IN PROGRESS) Tool for starting nodes
- `srdds`: (WORK IN PROGRESS) Tool for managing active nodes

## Getting Started

### 1. Add host dev tools to your PATH

To make `srpkg` and `srbuild` available globally:

```bash
export PATH="$PATH:<absolute_path_to_repo>/sunswift-dev-tools/host"
```
Recommend adding this to your .bashrc
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
├── .srpkg              # Package metadata file
├── src/                # Source files (.cpp)
├── include/            # Header files (.hpp)
├── param/              # Parameter files (JSON)
├── param/param.json    # Default parameter template
├── CMakeLists.txt      # Build configuration template
└── README.md           # Package documentation
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

`srbuild` is a wrapper around CMake that simplifies building DDS packages and targets. It must be run from within the repository, but can be used from anywhere, not necessarily root.

#### Output:
`srbuild` automatically creates or overwrites root level `build/` `deploy/` and `lib/` directories. It outputs all static libraries into `lib/`, all user executables to `deploy/bin/`, and CMake-required files in `build/`.
```
SR-Mjolnir/
├── build/          # CMake-required files
├── deploy/         # Package metadata file
│     ├─ bin/       # Node executables
│     ├─ param/
│     └─ logs/       
├── lib/            # Static libraries
└── ...
```
#### Building all targets:

To build all available targets in the repository:

```bash
srbuild --all
# or
srbuild -a
```

#### Building specific targets:

To build only specific packages or libraries:

```bash
srbuild --target package1 package2 lib1
# or
srbuild -t package1 package2 lib1
```
This automatically builds dependencies if required.
#### Cleaning the build:

To clean the build directory and re-initialize CMake:

```bash
srbuild --clean
```

This will delete the `/deploy`, `/build` and `/lib` directories and reset the build configuration.

#### Parallel jobs:

By default, `srbuild` uses 8 parallel jobs for compilation. You can customize this:

```bash
srbuild --all --jobs 4
srbuild -t package1 -j 16
```

## Example Workflow

1. Create a new DDS package:
   ```bash
   cd /path/to/repo/src
   srpkg create my_dds_node
   ```

2. Add your source code to `my_dds_node/src/` and headers to `my_dds_node/include/`

3. Add `add_subdirectory(my_dds_node)` to src/CMakeLists.txt to enable the build

4. Build the package:
   ```bash
   srbuild -t my_dds_node
   # or
   srbuild --all
   ```

5. Add the binary and config locations (in deploy/) to `launch/launch_config.json`

6. Run the executable (from repo root):
   ```bash
   ./deploy/bin/my_dds_node
   ```

## Notes

- Both tools must be run from within the SR-Mjolnir repository
- `srpkg` creates packages in the current working directory
- `srbuild` operates on the entire repository build system
- `srlaunch` and `srdds` are currently work in progress

## Contributors
Ryan Wong || z5417983