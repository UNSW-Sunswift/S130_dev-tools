"""Common utilities shared by srbuild/srpkg."""

from typing import NoReturn
import sys


def die(msg: str) -> NoReturn:
    print(msg)
    sys.exit(1)
