"""Compatibility wrapper for Scopus parsing."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from pyxxdi.io.scopus import read_scopus as _read_scopus


def _split_semicolon(value: object) -> list[str]:
    if pd.isna(value):
        return []
    return [x.strip() for x in str(value).split(";") if x.strip()]


def read_scopus(
    path: str | Path,
    *,
    encoding: str = "utf-8",
    low_memory: bool = False,
    canonical: bool = True,
    **kwargs: Any,
) -> pd.DataFrame:
    """Read Scopus files via the canonical IO implementation."""
    df = _read_scopus(
        path,
        encoding=encoding,
        low_memory=low_memory,
        canonical=canonical,
        **kwargs,
    )

    for col in ("author_keywords", "index_keywords"):
        if col in df.columns:
            df[col] = df[col].map(_split_semicolon)

    if "institution" in df.columns:
        df["institutions"] = df["institution"].map(_split_semicolon)

    df["data_source"] = "scopus"
    df["raw_source_format"] = "csv"

    return df
