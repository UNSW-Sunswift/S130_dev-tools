###############################################################################
# Integration tests for srbuild CLI
# Version: V1.0
# Date: 21/03/2026
# Author: Ryan Wong
#
# Made to run automatically on CI. Tests srbuild end to end by mocking a repository 
# and running the CLI commands. Uses pytest. Assumes srbuild is one level above this
# Uses fixtures from conftest.py to set up a temporary git repository with the expected structure.
###############################################################################

import pytest
import subprocess
from pathlib import Path

# =================================================================================================
# HELPER FUNCTIONS
# =================================================================================================
def run(*args: str, cwd: Path) -> subprocess.CompletedProcess:
    """Run srbuild CLI and returns CompletedProcess object."""
    srbuild_path = Path(__file__).resolve().parent.parent / "srbuild"
    result = subprocess.run(
        [str(srbuild_path), *args],
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    return result


### srbuild sanity check tests ----------------------------------------------------------------

def test_rejects_outside_repo(repo: Path) -> None:
    """Must fail when run outside a valid repository."""
    r = run("all", cwd=repo.parent)
    assert r.returncode != 0

def test_rejects_missing_marker(repo: Path) -> None:
    """Must fail when .sunswift-evsn marker is missing."""
    (repo / ".sunswift-evsn").unlink()
    r = run("all", cwd=repo)
    assert r.returncode != 0

def test_rejects_missing_src(repo: Path) -> None:
    """Must fail when src/ is missing."""
    import shutil
    shutil.rmtree(repo / "src")
    r = run("all", cwd=repo)
    assert r.returncode != 0

def test_rejects_missing_core(repo: Path) -> None:
    """Must fail when core/ is missing."""
    import shutil
    shutil.rmtree(repo / "core")
    r = run("all", cwd=repo)
    assert r.returncode != 0

def test_accepts_valid_repo(repo: Path) -> None:
    """Should pass sanity checks and fail only on missing CMakeLists.txt, not repo structure."""
    r = run("all", cwd=repo)
    # CMakeLists.txt doesn't exist so cmake will fail, but the repo check should pass
    assert "not a git repository" not in r.stdout
    assert "marker file" not in r.stdout
    assert "missing src" not in r.stdout

def test_rejects_no_cmake(repo: Path) -> None:
    """Should fail when CMakeLists.txt is missing."""
    r = run("all", cwd=repo)
    assert r.returncode != 0
    assert "CMakeLists.txt" in r.stdout

def test_accepts_cmake(repo: Path) -> None:
    """Should get past CMakeLists check when it exists."""
    (repo / "CMakeLists.txt").touch()
    r = run("all", cwd=repo)
    # Will fail because cmake isn't configured, but not because of our checks
    assert "CMakeLists.txt does not exist" not in r.stdout


### srbuild target tests ----------------------------------------------------------------------

def test_target_requires_at_least_one(repo: Path) -> None:
    """srbuild target with no targets should fail."""
    r = run("target", cwd=repo)
    assert r.returncode != 0

def test_target_accepts_single(repo: Path) -> None:
    """srbuild target with one target should pass sanity checks."""
    (repo / "CMakeLists.txt").touch()
    r = run("target", "my_node", cwd=repo)
    assert "CMakeLists.txt does not exist" not in r.stdout

def test_target_accepts_multiple(repo: Path) -> None:
    """srbuild target with multiple targets should pass sanity checks."""
    (repo / "CMakeLists.txt").touch()
    r = run("target", "node_a", "node_b", cwd=repo)
    assert "CMakeLists.txt does not exist" not in r.stdout