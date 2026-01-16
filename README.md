# S130 Development tools V1.1.0

This repository contains high-level development tools for Sunswift embedded and DDS projects. It is separated into host/ and target/. host/ contains the dev tools we are using during development time on our host machines. target/ contains scripts that should be run on the target (NVIDIA Drive THOR computer). It is intended to be a submodule in the SR-Mjolnir repository.


It includes:

- `srpkg`: DDS package creation and management tool  
- `srbuild`: Build tool for compiling and deploying DDS packages  
- `srlaunch`: Tool for starting nodes
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
Then just `Ctrl-C` to shut down all nodes gracefully. It's that easy guys.
## Example Workflow

1. Create a new DDS package:
   ```bash
   cd /path/to/repo/src
   srpkg create my_dds_node
   ```

2. Add your source code to `my_dds_node/src/` and headers to `my_dds_node/include/`

3. Fill out the template CMakeLists.txt

3. Add `add_subdirectory(relative/path/to/my_dds_node)` to src/CMakeLists.txt to enable the build

4. Build the package:
   ```bash
   srbuild target my_dds_node
   # or
   srbuild all
   ```

5. Launch the node:
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
- `srlaunch` is used from the deploy directory
- `srdds` is currently work in progress

## Contributors
Ryan Wong || z5417983