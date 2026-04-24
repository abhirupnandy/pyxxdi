"""
Canonical schema definitions for pyxxdi.

This module defines the internal bibliometric dataframe schema used across
all readers, cleaners, validators, and metric engines.

Every importer should map source-specific columns into these canonical names.
"""

from __future__ import annotations

from typing import Final

# ---------------------------------------------------------------------
# Core canonical columns
# ---------------------------------------------------------------------

CANONICAL_COLUMNS: Final[list[str]] = [
    "record_id",
    "source_db",
    "title",
    "authors",
    "year",
    "source",
    "doi",
    "affiliations",
    "institution",
    "country",
    "author_keywords",
    "index_keywords",
    "abstract",
    "citations",
    "document_type",
    "volume",
    "issue",
    "pages",
    "publisher",
    "issn",
    "isbn",
    "language",
    "open_access",
    "url",
    "date_added",
    "raw_source_id",
]

# ---------------------------------------------------------------------
# Validation tiers
# ---------------------------------------------------------------------

REQUIRED_COLUMNS: Final[list[str]] = [
    "title",
    "authors",
    "year",
]

METRIC_REQUIRED_COLUMNS: Final[list[str]] = [
    "title",
    "authors",
    "year",
    "citations",
]

INSTITUTION_REQUIRED_COLUMNS: Final[list[str]] = [
    "title",
    "authors",
    "year",
    "affiliations",
]

# ---------------------------------------------------------------------
# Canonical pandas nullable dtypes
# ---------------------------------------------------------------------

DTYPE_MAP: Final[dict[str, str]] = {
    "record_id": "string",
    "source_db": "string",
    "title": "string",
    "authors": "string",
    "year": "Int64",
    "source": "string",
    "doi": "string",
    "affiliations": "string",
    "institution": "string",
    "country": "string",
    "author_keywords": "string",
    "index_keywords": "string",
    "abstract": "string",
    "citations": "Int64",
    "document_type": "string",
    "volume": "string",
    "issue": "string",
    "pages": "string",
    "publisher": "string",
    "issn": "string",
    "isbn": "string",
    "language": "string",
    "open_access": "boolean",
    "url": "string",
    "date_added": "datetime64[ns]",
    "raw_source_id": "string",
}


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------


def is_canonical_column(name: str) -> bool:
    """
    Return True if column name exists in pyxxdi schema.
    """
    return name in CANONICAL_COLUMNS


def get_missing_required_columns(columns: list[str]) -> list[str]:
    """
    Return missing mandatory columns.
    """
    existing = set(columns)
    return [col for col in REQUIRED_COLUMNS if col not in existing]
