"""
Web of Science reader for pyxxdi.

Reads Web of Science exports and maps standard WoS tagged columns
into the pyxxdi canonical schema.
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
    """Raised when Web of Science file reading fails."""


# ---------------------------------------------------------------------
# WoS field tag mapping
# ---------------------------------------------------------------------

WOS_COLUMN_MAP: dict[str, str] = {
    "TI": "title",  # Title
    "AU": "authors",  # Authors
    "PY": "year",  # Publication year
    "SO": "source",  # Source title
    "DI": "doi",  # DOI
    "C1": "affiliations",  # Addresses / affiliations
    "DE": "author_keywords",  # Author keywords
    "ID": "index_keywords",  # Keywords Plus
    "TC": "citations",  # Times cited
    "DT": "document_type",  # Document type
    "AB": "abstract",  # Abstract
    "VL": "volume",
    "IS": "issue",
    "BP": "pages",
    "PU": "publisher",
    "SN": "issn",
    "LA": "language",
    "UT": "raw_source_id",  # Unique accession number
}


def read_wos(
    path: str | Path,
    *,
    sep: str = "\t",
    encoding: str | None = "utf-8",
    canonical: bool = True,
    low_memory: bool = False,
    **kwargs: Any,
) -> pd.DataFrame:
    """
    Read Web of Science export file.

    Parameters
    ----------
    path:
        Export file path.
    sep:
        Default tab-delimited for WoS plain text exports.
    encoding:
        Text encoding.
    canonical:
        Add missing canonical columns and reorder.
    low_memory:
        Passed to pandas.read_csv.
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
            sep=sep,
            encoding=encoding,
            low_memory=low_memory,
            **kwargs,
        )
    except Exception as exc:
        raise ReaderError(f"Failed to read Web of Science file: {path}") from exc

    rename_map = {
        col: WOS_COLUMN_MAP[col] for col in df.columns if col in WOS_COLUMN_MAP
    }

    df = df.rename(columns=rename_map)

    df["source_db"] = "wos"

    if "record_id" not in df.columns:
        df["record_id"] = [f"px_{i:08d}" for i in range(1, len(df) + 1)]

    if canonical:
        df = add_missing_canonical_columns(df)
        df = reorder_canonical_columns(df)

    return df
