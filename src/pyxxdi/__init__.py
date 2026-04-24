"""
pyxxdi

Modern bibliometric analytics package for x-index, xd-index,
research evaluation, benchmarking, and expertise intelligence.
"""

from importlib.metadata import version, PackageNotFoundError

__all__ = [
    "__version__",
]

try:
    __version__ = version("pyxxdi")
except PackageNotFoundError:
    __version__ = "0.1.0"