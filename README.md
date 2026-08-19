# Sunswift Dev Tools

Developer tooling for SR-Mjolnir and SR-Gungnir, SR8's high level repositories.
Includes:

- `srpkg`: creates a new DDS package in your current working directory
- `srbuild`: wraps CMake to configure, build, and install targets

Both tools are installed as a [uv](https://docs.astral.sh/uv/) tool.

`srlaunch` (process launcher) has moved to [`deprecated/`](deprecated/). QNX targets should use QNX's own process management. It is being replaced by a cross-platform orchestrator (Seb's thesis).

## Installation

Install globally as a uv tool (recommended):

```bash
uv tool install git+https://github.com/UNSW-Sunswift/SR-Dev-Tools.git
```

This puts `srbuild` and `srpkg` on your PATH. To upgrade later:

```bash
uv tool upgrade sr-dev-tools
```

For local development on this repo itself:

```bash
git clone git@github.com:UNSW-Sunswift/SR-Dev-Tools.git
cd SR-Dev-Tools
uv tool install --editable .
```

From a Dockerfile:

```dockerfile
RUN uv tool install git+https://github.com/UNSW-Sunswift/SR-Dev-Tools.git
```

## `srpkg`

Creates a new DDS package in the **current working directory**. Same idea as `ros2 pkg create`.

```bash
srpkg create <package_name>
```

This creates:

```
<package_name>/
├── .srpkg                             # Package metadata marker
├── src/
│   └── main.cpp
├── include/
├── test/
├── param/
│   └── <package_name>_param.toml
├── CMakeLists.txt                     # Build configuration template
└── README.md
```

Package names must be `snake_case`. `srpkg` only checks for a duplicate name in the current directory and does not search the rest of your repository. If you have a build system which builds multiple executables from different directories, it is on you to make sure no packages (and so executables) share a name.

## `srbuild`

Invokes CMake to configure, build, and install targets. Assumes top level CMakeLists is at your current working directory, or discovers the repository root (see below).

### Repository root discovery

`srbuild` looks for a `.sunswift-evsn` marker file, walking up from your current directory. If found, that directory is treated as the root and assumes your top-level `CMakeLists.txt` lives here. If no marker is found anywhere above the current directory, `srbuild` just uses the current directory as the root instead.. The marker is optional.

### Building

```bash
# Build and install everything
srbuild all

# Build and install specific targets
srbuild target node1 node2 ...

# Delete the entire build/ directory
srbuild clean
```

### Platform / toolchain selection

```bash
srbuild all --linux                              # native build, no toolchain file
srbuild all --qnx=cmake/qnx_toolchain.cmake       # cross-compile using the given toolchain file
srbuild all                                       # no flag: native build
```

`--qnx` and `--linux` are mutually exclusive. `--qnx` takes a path to a CMake toolchain file, resolved **relative to your current working directory** (not the discovered repo root). `srbuild` has no built-in opinion on where that file lives — pass whatever path is correct for your project.

### Output layout

Given a discovered/assumed root, `srbuild` produces:

```
<root>/
├── CMakeLists.txt
├── build/
│   ├── native/   (or linux/, qnx/, depending on the flag used)
├── deploy/
│   └── native/   (or linux/, qnx/)
│       ├── bin/
│       └── param/
```

`build/` holds CMake's intermediate files (don't touch it directly). `deploy/` holds the installed, runnable output.

### Parallel jobs

```bash
srbuild all --jobs 4
srbuild target node1 -j 16
```

Defaults to 8 parallel jobs.

## Example workflow

```bash
cd path/to/your/project/src
srpkg create my_dds_node
# fill in my_dds_node/src, include/, and CMakeLists.txt

cd path/to/your/project
srbuild target my_dds_node
# or
srbuild all
```

## Contributors
- Ryan Wong || z5417983
- Henry Jiang || z5416365
