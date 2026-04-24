"""
pyxxdi public API.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("pyxxdi")
except PackageNotFoundError:
    __version__ = "0.0.0"


# ---------------------------------------------------------------------
# IO layer
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Cleaning layer
# ---------------------------------------------------------------------
from pyxxdi.cleaning import (
    clean_affiliations,
    clean_keywords,
    clean_publications,
    deduplicate,
    drop_duplicate_doi,
    drop_duplicate_title_year,
)
from pyxxdi.io import (
    read_csv,
    read_excel,
    read_openalex,
    read_scopus,
    read_wos,
)

# ---------------------------------------------------------------------
# Utils layer
# ---------------------------------------------------------------------
from pyxxdi.utils import (
    CANONICAL_COLUMNS,
    DTYPE_MAP,
    INSTITUTION_REQUIRED_COLUMNS,
    METRIC_REQUIRED_COLUMNS,
    REQUIRED_COLUMNS,
    ValidationError,
    ValidationReport,
    add_missing_canonical_columns,
    reorder_canonical_columns,
    schema_report,
    validate,
)

# ---------------------------------------------------------------------
# Public namespace
# ---------------------------------------------------------------------

__all__ = [
    "__version__",
    # IO
    "read_csv",
    "read_excel",
    "read_scopus",
    "read_wos",
    "read_openalex",
    # schema
    "CANONICAL_COLUMNS",
    "REQUIRED_COLUMNS",
    "METRIC_REQUIRED_COLUMNS",
    "INSTITUTION_REQUIRED_COLUMNS",
    "DTYPE_MAP",
    # validation
    "ValidationError",
    "ValidationReport",
    "validate",
    "schema_report",
    "add_missing_canonical_columns",
    "reorder_canonical_columns",
    # cleaning
    "clean_publications",
    "deduplicate",
    "drop_duplicate_doi",
    "drop_duplicate_title_year",
    "clean_affiliations",
    "clean_keywords",
]
