"""
Scopus reader for pyxxdi.

Reads Scopus CSV exports and maps source columns into the pyxxdi
canonical bibliometric schema.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from pyxxdi.utils.validation import (
    add_missing_canonical_columns,
    reorder_canonical_columns,
)


class ReaderError(Exception):
    """Raised when Scopus file reading fails."""


# ---------------------------------------------------------------------
# Scopus column mapping
# ---------------------------------------------------------------------

SCOPUS_COLUMN_MAP: dict[str, str] = {
    "Title": "title",
    "Authors": "authors",
    "Year": "year",
    "Source title": "source",
    "DOI": "doi",
    "Affiliations": "affiliations",
    "Author Keywords": "author_keywords",
    "Index Keywords": "index_keywords",
    "Cited by": "citations",
    "Document Type": "document_type",
    "Publisher": "publisher",
    "ISSN": "issn",
    "Language of Original Document": "language",
    "Abstract": "abstract",
    "Volume": "volume",
    "Issue": "issue",
    "Page start": "pages",
    "EID": "raw_source_id",
}


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------


def read_scopus(
    path: str | Path,
    *,
    encoding: str | None = "utf-8",
    low_memory: bool = False,
    canonical: bool = True,
    **kwargs: Any,
) -> pd.DataFrame:
    """
    Read Scopus CSV export.

    Parameters
    ----------
    path:
        CSV export path.
    encoding:
        Text encoding.
    low_memory:
        Passed to pandas.read_csv.
    canonical:
        If True, add missing canonical columns and reorder.
    **kwargs:
        Additional pandas.read_csv args.

    Returns
    -------
    pd.DataFrame
    """
    path = Path(path)

    if not path.exists():
        raise ReaderError(f"File not found: {path}")

    try:
        df = pd.read_csv(
            path,
            encoding=encoding,
            low_memory=low_memory,
            **kwargs,
        )
    except Exception as exc:
        raise ReaderError(f"Failed to read Scopus file: {path}") from exc

    # Rename known columns
    rename_map = {
        col: SCOPUS_COLUMN_MAP[col] for col in df.columns if col in SCOPUS_COLUMN_MAP
    }

    df = df.rename(columns=rename_map)

    # Provenance
    df["source_db"] = "scopus"

    # Stable internal ids
    if "record_id" not in df.columns:
        df["record_id"] = [f"px_{i:08d}" for i in range(1, len(df) + 1)]

    if canonical:
        df = add_missing_canonical_columns(df)
        df = reorder_canonical_columns(df)

    return df
