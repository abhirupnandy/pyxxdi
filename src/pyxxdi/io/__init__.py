"""
Input / output readers for pyxxdi.
"""

from pyxxdi.io.csv import read_csv
from pyxxdi.io.excel import read_excel
from pyxxdi.io.openalex import read_openalex
from pyxxdi.io.wos import read_wos
from pyxxdi.parsing import read_scopus

__all__ = [
    "read_csv",
    "read_excel",
    "read_scopus",
    "read_wos",
    "read_openalex",
]
