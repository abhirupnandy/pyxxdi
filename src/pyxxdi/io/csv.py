"""
CSV readers for pyxxdi.

Generic CSV ingestion with optional canonical schema alignment.
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
    """Raised when file reading fails."""


def read_csv(
    path: str | Path,
    *,
    encoding: str | None = None,
    sep: str = ",",
    canonical: bool = True,
    low_memory: bool = False,
    **kwargs: Any,
) -> pd.DataFrame:
    """
    Read a generic CSV file.

    Parameters
    ----------
    path:
        File path.
    encoding:
        Optional text encoding.
    sep:
        Field separator.
    canonical:
        If True, append missing canonical columns and reorder.
    low_memory:
        Passed to pandas.read_csv.
    **kwargs:
        Extra pandas.read_csv arguments.

    Returns
    -------
    pd.DataFrame
    """
    try:
        df = pd.read_csv(
            path,
            encoding=encoding,
            sep=sep,
            low_memory=low_memory,
            **kwargs,
        )
    except Exception as exc:
        raise ReaderError(f"Failed to read CSV file: {path}") from exc

    if canonical:
        df = add_missing_canonical_columns(df)
        df = reorder_canonical_columns(df)

    return df
