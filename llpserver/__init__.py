from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

__all__ = []

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    # package is not installed
    __version__ = "<unknown>"