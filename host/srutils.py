"""Common repo utilities for srbuild/srpkg."""

from pathlib import Path
import subprocess
import sys

MARKER_FILE = ".sunswift-evsn"

def die(msg: str) -> None:
    print(msg)
    sys.exit(1)

def git_toplevel(path: Path) -> Path:
    try:
        result = subprocess.run(
            ["git", "-C", str(path), "rev-parse", "--show-toplevel"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except FileNotFoundError:
        raise RuntimeError("Error: git not found; cannot determine repository root")
    except subprocess.CalledProcessError:
        raise RuntimeError("Error: not a git repository (or any of the parent directories)")

    root = result.stdout.strip()
    if not root:
        raise RuntimeError("Error: git returned empty repository root")
    return Path(root).resolve()

def resolve_repo_root(cwd: Path = Path.cwd()) -> Path:
    candidate = git_toplevel(cwd)
    if not candidate.exists() or not candidate.is_dir():
        raise RuntimeError("Error: repo root does not exist or is not a directory")
    return candidate

def validate_repo_root(repo_root: Path, marker_file: str = MARKER_FILE) -> None:
    if not ((repo_root / "src").exists() and (repo_root / "core").exists()):
        raise RuntimeError("Error: repository root missing src/ or core/\nYou may be running this in a submodule")
    if not (repo_root / marker_file).exists():
        raise RuntimeError(f"Error: marker file '{marker_file}' not found in repository root")
