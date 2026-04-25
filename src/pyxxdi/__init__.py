"""pyxxdi public API."""

from importlib.metadata import PackageNotFoundError, version

from pyxxdi.affiliations import clean_affiliations
from pyxxdi.analytics import (
    author_profile,
    collaboration_network,
    compare_institutions,
    compare_researchers,
    export_report,
    institution_profile,
    researcher_dashboard,
    temporal_trends,
)
from pyxxdi.classify import classify_subjects
from pyxxdi.cleaning import (
    clean_publications,
    deduplicate,
    drop_duplicate_doi,
    drop_duplicate_title_year,
)
from pyxxdi.io import read_csv, read_excel, read_openalex, read_scopus, read_wos
from pyxxdi.keywords import clean_keywords, normalize_keywords
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
from pyxxdi.schemas import SchemaValidationError, harmonize_schema, validate_schema
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

try:
    __version__ = version("pyxxdi")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = [
    "__version__",
    # Parsing / IO
    "read_csv",
    "read_excel",
    "read_scopus",
    "read_wos",
    "read_openalex",
    # Schema / validation
    "CANONICAL_COLUMNS",
    "REQUIRED_COLUMNS",
    "METRIC_REQUIRED_COLUMNS",
    "INSTITUTION_REQUIRED_COLUMNS",
    "DTYPE_MAP",
    "harmonize_schema",
    "validate_schema",
    "SchemaValidationError",
    "ValidationError",
    "ValidationReport",
    "validate",
    "schema_report",
    "add_missing_canonical_columns",
    "reorder_canonical_columns",
    # Cleaning
    "clean_publications",
    "deduplicate",
    "drop_duplicate_doi",
    "drop_duplicate_title_year",
    "clean_keywords",
    "normalize_keywords",
    "clean_affiliations",
    # Metrics
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
    # Classification
    "classify_subjects",
    # Analytics
    "institution_profile",
    "author_profile",
    "collaboration_network",
    "temporal_trends",
    "researcher_dashboard",
    "compare_researchers",
    "compare_institutions",
    "export_report",
]
