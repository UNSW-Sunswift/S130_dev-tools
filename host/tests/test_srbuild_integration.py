###############################################################################
# Integration tests for srbuild CLI
# Author: Ryan Wong
#
# Made to run automatically on CI. Tests srbuild end to end by mocking a repository
# and running the CLI commands. Uses pytest. Assumes srbuild is one level above this.
# Uses fixtures from conftest.py to set up a temporary git repository with the expected structure.
###############################################################################

import pytest
import subprocess
from pathlib import Path

# =================================================================================================
# HELPER FUNCTIONS
# =================================================================================================
def run(*args: str, cwd: Path, stdin: str = "") -> subprocess.CompletedProcess:
    """Run srbuild CLI and return the CompletedProcess object."""
    srbuild_path = Path(__file__).resolve().parent.parent / "srbuild"
    return subprocess.run(
        [str(srbuild_path), *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        input=stdin,
    )


def assert_success(r: subprocess.CompletedProcess) -> None:
    assert r.returncode == 0, f"Expected success.\nstdout: {r.stdout}\nstderr: {r.stderr}"


def assert_failure(r: subprocess.CompletedProcess) -> None:
    assert r.returncode != 0, f"Expected failure.\nstdout: {r.stdout}\nstderr: {r.stderr}"


# =================================================================================================
# SANITY CHECK TESTS
# =================================================================================================

def test_rejects_outside_repo(repo: Path) -> None:
    """Must fail when run outside a valid git repository."""
    r = run("all", cwd=repo.parent)
    assert_failure(r)

def test_rejects_missing_marker(repo: Path) -> None:
    """Must fail when .sunswift-evsn marker is missing."""
    (repo / ".sunswift-evsn").unlink()
    r = run("all", cwd=repo)
    assert_failure(r)
    assert "marker" in r.stdout or "marker" in r.stderr

def test_rejects_missing_cmake(repo: Path) -> None:
    """Must fail when CMakeLists.txt is missing."""
    r = run("all", cwd=repo)
    assert_failure(r)
    assert "CMakeLists.txt" in r.stdout or "CMakeLists.txt" in r.stderr

def test_accepts_valid_repo(configured_repo: Path) -> None:
    """Should pass all srbuild sanity checks with a fully configured repo."""
    # Have to add linux flag because we don't have a toolchain file
    r = run("all", "--linux", cwd=configured_repo)
    assert_success(r)
    assert "not a git repository" not in r.stdout
    assert "marker" not in r.stdout
    assert "CMakeLists.txt does not exist" not in r.stdout


# =================================================================================================
# TARGET TESTS
# =================================================================================================

def test_target_requires_at_least_one(repo: Path) -> None:
    """srbuild target with no targets specified should fail."""
    r = run("target", cwd=repo)
    assert_failure(r)

def test_target_accepts_single(configured_repo: Path) -> None:
    """srbuild target with one target should pass sanity checks."""
    r = run("target", "my_node", cwd=configured_repo)
    assert "CMakeLists.txt does not exist" not in r.stdout

def test_target_accepts_multiple(configured_repo: Path) -> None:
    """srbuild target with multiple targets should pass sanity checks."""
    r = run("target", "node_a", "node_b", cwd=configured_repo)
    assert "CMakeLists.txt does not exist" not in r.stdout


# =================================================================================================
# PLATFORM FLAG TESTS
# =================================================================================================

def test_all_accepts_linux_flag(configured_repo: Path) -> None:
    """--linux flag should be accepted and result in a successful build of an empty project."""
    r = run("all", "--linux", cwd=configured_repo)
    assert_success(r)

def test_all_accepts_qnx_flag(configured_repo: Path) -> None:
    """--qnx flag should be accepted without argparse error (cmake will fail without toolchain)."""
    r = run("all", "--qnx", cwd=configured_repo)
    assert "unrecognized arguments" not in r.stderr

def test_target_accepts_linux_flag(configured_repo: Path) -> None:
    """--linux flag should be accepted on the target subcommand without argparse error."""
    r = run("target", "my_node", "--linux", cwd=configured_repo)
    assert "unrecognized arguments" not in r.stderr

def test_all_accepts_jobs_flag(configured_repo: Path) -> None:
    """-j flag should be accepted and not cause an argparse error."""
    r = run("all", "--linux", "-j", "4", cwd=configured_repo)
    assert_success(r)

def test_all_rejects_invalid_jobs(configured_repo: Path) -> None:
    """-j with a non-integer value should be rejected by argparse."""
    r = run("all", "--linux", "-j", "fast", cwd=configured_repo)
    assert_failure(r)
    assert "invalid int value" in r.stderr


# =================================================================================================
# UNKNOWN SUBCOMMAND TESTS
# =================================================================================================

def test_rejects_unknown_subcommand(configured_repo: Path) -> None:
    """An unrecognised subcommand should fail."""
    r = run("bogus", cwd=configured_repo)
    assert_failure(r)


# =================================================================================================
# CLEAN TESTS
# =================================================================================================

def test_clean_cancels_on_no(configured_repo: Path) -> None:
    """Answering 'n' to the clean prompt should cancel and leave build dirs intact."""
    (configured_repo / "build" / "linux").mkdir(parents=True)
    (configured_repo / "build" / "qnx").mkdir(parents=True)
    r = run("clean", cwd=configured_repo, stdin="n\n")
    assert_failure(r)
    assert (configured_repo / "build" / "linux").exists()
    assert (configured_repo / "build" / "qnx").exists()

def test_clean_removes_both_by_default(configured_repo: Path) -> None:
    """Answering 'y' with no flag should remove both build/linux and build/qnx."""
    (configured_repo / "build" / "linux").mkdir(parents=True)
    (configured_repo / "build" / "qnx").mkdir(parents=True)
    r = run("clean", cwd=configured_repo, stdin="y\n")
    assert_success(r)
    assert not (configured_repo / "build" / "linux").exists()
    assert not (configured_repo / "build" / "qnx").exists()

def test_clean_removes_only_linux(configured_repo: Path) -> None:
    """--linux flag should remove only build/linux and leave build/qnx intact."""
    (configured_repo / "build" / "linux").mkdir(parents=True)
    (configured_repo / "build" / "qnx").mkdir(parents=True)
    r = run("clean", "--linux", cwd=configured_repo, stdin="y\n")
    assert_success(r)
    assert not (configured_repo / "build" / "linux").exists()
    assert (configured_repo / "build" / "qnx").exists()

def test_clean_removes_only_qnx(configured_repo: Path) -> None:
    """--qnx flag should remove only build/qnx and leave build/linux intact."""
    (configured_repo / "build" / "linux").mkdir(parents=True)
    (configured_repo / "build" / "qnx").mkdir(parents=True)
    r = run("clean", "--qnx", cwd=configured_repo, stdin="y\n")
    assert_success(r)
    assert (configured_repo / "build" / "linux").exists()
    assert not (configured_repo / "build" / "qnx").exists()

def test_clean_handles_missing_build(configured_repo: Path) -> None:
    """Clean should succeed gracefully when neither build/linux nor build/qnx exist."""
    r = run("clean", cwd=configured_repo, stdin="y\n")
    assert_success(r)
