### This file contains pytest fixtures for the srpkg and srbuild tests.
import pytest
import subprocess
from pathlib import Path

@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """Real git repo with the expected Sunswift structure."""
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    (tmp_path / "src").mkdir()
    (tmp_path / "core").mkdir()
    (tmp_path / ".sunswift-evsn").touch()
    return tmp_path

@pytest.fixture
def src(repo: Path) -> Path:
    return repo / "src"