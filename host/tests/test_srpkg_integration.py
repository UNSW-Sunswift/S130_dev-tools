###############################################################################
# Integration tests for srpkg CLI
# Version: V1.0
# Date: 16/03/2026
# Author: Ryan Wong
#
# Made to run automatically on CI. Tests srpkg end to end by mocking a repository 
# and running the CLI commands. Uses pytest. Assumes srpkg is one level above this
# Uses fixtures from conftest.py to set up a temporary git repository with the expected structure.
###############################################################################

import pytest
import subprocess
import os
from pathlib import Path

# =================================================================================================
# HELPER FUNCTIONS
# =================================================================================================
def run(*args: str, cwd: Path) -> subprocess.CompletedProcess:
    """Run srpkg CLI and returns CompletedProcess object."""
    env = os.environ.copy()
    srpkg_path = Path(__file__).resolve().parent.parent / "srpkg"
    result = subprocess.run(
        [str(srpkg_path), *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        env=env
    )
    return result


# =================================================================================================
# TESTS
# =================================================================================================

### srpkg create tests
def test_create_basic(repo: Path, src: Path) -> None:
    """Create package in src called my_node and verify creation"""
    r = run("create", "my_node", cwd=src)
    assert r.returncode == 0

    pkg = src / "my_node"
    assert (pkg / ".srpkg").exists()
    assert (pkg / "src").is_dir()
    assert (pkg / "include").is_dir()
    assert (pkg / "param").is_dir()
    assert (pkg / "CMakeLists.txt").exists()
    assert (pkg / "README.md").exists()

def test_create_rejects_local_duplicate(repo, src):
    run("create", "my_node", cwd=src)
    r = run("create", "my_node", cwd=src)
    assert r.returncode != 0
    assert "already exists" in r.stdout

def test_create_rejects_duplicate_in_other_dir(repo, src):
    sub = src / "subsystem"
    sub.mkdir()
    run("create", "my_node", cwd=sub)

    r = run("create", "my_node", cwd=src)
    assert r.returncode != 0
    assert "already exists" in r.stdout

def test_create_rejects_outside_src(repo):
    r = run("create", "my_node", cwd=repo)
    assert r.returncode != 0
    assert "src" in r.stdout

def test_create_rejects_outside_repo(repo):
    r = run("create", "my_node", cwd=repo.parent)
    assert r.returncode != 0

def test_create_rejects_bad_name(repo, src):
    for bad in ["MyNode", "my-node", "my node", "my.node"]:
        r = run("create", bad, cwd=src)
        assert r.returncode != 0, f"Expected failure for name: {bad}"


### srpkg info tests
def test_info_found(repo, src):
    run("create", "my_node", cwd=src)
    r = run("info", "my_node", cwd=src)
    assert r.returncode == 0
    assert "my_node" in r.stdout
    assert "Location" in r.stdout

def test_info_not_found(repo, src):
    r = run("info", "ghost_node", cwd=src)
    assert r.returncode != 0

def test_info_shows_cpp_files(repo, src):
    run("create", "my_node", cwd=src)
    (src / "my_node" / "src" / "helper.cpp").write_text("// helper")
    r = run("info", "my_node", cwd=src)
    assert "helper.cpp" in r.stdout

def test_info_shows_hpp_files(repo, src):
    run("create", "my_node", cwd=src)
    (src / "my_node" / "include" / "helper.hpp").write_text("// header")
    r = run("info", "my_node", cwd=src)
    assert "helper.hpp" in r.stdout


### srpkg list tests
def test_list_finds_packages(repo, src):
    run("create", "node_a", cwd=src)
    run("create", "node_b", cwd=src)
    r = run("list", cwd=src)
    assert r.returncode == 0
    assert "node_a" in r.stdout
    assert "node_b" in r.stdout

def test_list_finds_packages_other_dir(repo, src):
    sub = src / "subsystem"
    sub.mkdir()
    run("create", "node_a", cwd=src)
    run("create", "node_b", cwd=sub)
    r = run("list", cwd=repo)
    assert r.returncode == 0
    assert "node_a" in r.stdout
    assert "node_b" in r.stdout
    
def test_list_empty(repo, src):
    r = run("list", cwd=src)
    assert r.returncode == 0
    assert "No packages found" in r.stdout

def test_list_ignores_dirs_without_marker(repo, src):
    (src / "not_a_package").mkdir()
    r = run("list", cwd=src)
    assert "not_a_package" not in r.stdout