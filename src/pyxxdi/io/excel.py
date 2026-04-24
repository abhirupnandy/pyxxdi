"""
Excel readers for pyxxdi.

Production-grade Excel ingestion for bibliometric datasets.

Supported formats
-----------------
.xlsx   -> openpyxl
.xls    -> xlrd (optional legacy support)

The reader defaults to openpyxl for modern Excel files.
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
    """Raised when spreadsheet reading fails."""


def _infer_engine(path: str | Path) -> str:
    """
    Infer pandas Excel engine from file suffix.
    """
    suffix = Path(path).suffix.lower()

    if suffix == ".xlsx":
        return "openpyxl"

    if suffix == ".xls":
        return "xlrd"

    raise ReaderError(f"Unsupported Excel format: {suffix}. Supported: .xlsx, .xls")


def read_excel(
    path: str | Path,
    *,
    sheet_name: str | int = 0,
    canonical: bool = True,
    engine: str | None = None,
    **kwargs: Any,
) -> pd.DataFrame:
    """
    Read an Excel file into DataFrame.

    Parameters
    ----------
    path:
        Path to Excel file.
    sheet_name:
        Sheet index or sheet label.
    canonical:
        If True, add missing pyxxdi canonical columns and reorder.
    engine:
        Explicit pandas engine. If None, inferred from extension.
    **kwargs:
        Additional pandas.read_excel arguments.

    Returns
    -------
    pd.DataFrame

    Raises
    ------
    ReaderError
        If file cannot be read or engine dependency missing.
    """
    path = Path(path)

    if not path.exists():
        raise ReaderError(f"File not found: {path}")

    selected_engine = engine or _infer_engine(path)

    try:
        df = pd.read_excel(
            path,
            sheet_name=sheet_name,
            engine=selected_engine,
            **kwargs,
        )
    except ImportError as exc:
        raise ReaderError(
            f"Missing dependency for Excel engine '{selected_engine}'. "
            f"Install the required package."
        ) from exc
    except Exception as exc:
        raise ReaderError(f"Failed to read Excel file: {path}") from exc

    if canonical:
        df = add_missing_canonical_columns(df)
        df = reorder_canonical_columns(df)

    return df
