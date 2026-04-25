"""
pyxxdi public API.
"""

from importlib.metadata import PackageNotFoundError, version

from .analytics import (
    author_profile,
    collaboration_network,
    compare_institutions,
    compare_researchers,
    export_report,
    institution_profile,
    researcher_dashboard,
    temporal_trends,
)
from .classify import classify_subjects

try:
    __version__ = version("pyxxdi")
except PackageNotFoundError:
    __version__ = "0.0.0"

from pyxxdi.affiliations import clean_affiliations

# ---------------------------------------------------------------------
# Cleaning layer
# ---------------------------------------------------------------------
from pyxxdi.cleaning import (
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
from pyxxdi.keywords import (
    clean_keywords,
    normalize_keywords,
)

# ---------------------------------------------------------------------
# Metrics layer
# ---------------------------------------------------------------------
from pyxxdi.metrics import (
    g_index,
    h_index,
    metric,
    x_index,
    xc_index,
    xd_field_normalized_index,
    xd_fractional_index,
    xd_index,
    xd_ivw_index,
    xo_index,
    xx_index,
    xxd_index,
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
# Schema layer
# ---------------------------------------------------------------------
from .schemas import (
    SchemaValidationError,
    harmonize_schema,
    validate_schema,
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
    # schema constants
    "CANONICAL_COLUMNS",
    "REQUIRED_COLUMNS",
    "METRIC_REQUIRED_COLUMNS",
    "INSTITUTION_REQUIRED_COLUMNS",
    "DTYPE_MAP",
    # schema functions
    "harmonize_schema",
    "validate_schema",
    "SchemaValidationError",
    # validation utils
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
    "clean_keywords",
    # metrics
    "metric",
    "h_index",
    "g_index",
    "x_index",
    "xd_index",
    "xd_fractional_index",
    "xd_field_normalized_index",
    "xd_ivw_index",
    "xc_index",
    "xo_index",
    "xx_index",
    "xxd_index",
    # Cleaning
    "normalize_keywords",
    # affiliations
    "clean_affiliations",
    # subjects
    "classify_subjects",
    # analytics
    "institution_profile",
    "author_profile",
    "collaboration_network",
    "temporal_trends",
    "researcher_dashboard",
    "compare_researchers",
    "compare_institutions",
    "export_report",
]
