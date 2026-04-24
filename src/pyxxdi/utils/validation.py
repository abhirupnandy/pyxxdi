"""
Validation utilities for pyxxdi.

Provides schema checks, datatype coercion, duplicate detection,
range validation, and publication metadata quality checks.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

import pandas as pd

from pyxxdi.utils.schema import (
    CANONICAL_COLUMNS,
    DTYPE_MAP,
    get_missing_required_columns,
)

# ---------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------


class ValidationError(Exception):
    """Raised when dataframe validation fails."""


# ---------------------------------------------------------------------
# Report object
# ---------------------------------------------------------------------


@dataclass(slots=True)
class ValidationReport:
    rows: int
    columns: int
    missing_required_columns: list[str]
    duplicate_rows: int
    duplicate_title_year: int
    invalid_year_rows: int
    negative_citation_rows: int
    null_title_rows: int
    null_author_rows: int
    passed: bool


# ---------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------


def _coerce_known_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply canonical pandas nullable dtypes where possible.
    """
    out = df.copy()

    for col, dtype in DTYPE_MAP.items():
        if col not in out.columns:
            continue

        try:
            if dtype == "datetime64[ns]":
                out[col] = pd.to_datetime(out[col], errors="coerce")
            else:
                out[col] = out[col].astype(dtype)
        except Exception:
            # fail soft: preserve raw values for later diagnosis
            continue

    return out


def _invalid_year_mask(series: pd.Series) -> pd.Series:
    """
    Detect impossible publication years.
    """
    current_year = datetime.now().year + 1
    years = pd.to_numeric(series, errors="coerce")

    return years.notna() & ((years < 1500) | (years > current_year))


def _negative_numeric_mask(series: pd.Series) -> pd.Series:
    vals = pd.to_numeric(series, errors="coerce")
    return vals.notna() & (vals < 0)


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------


def schema_report(df: pd.DataFrame) -> ValidationReport:
    """
    Generate validation diagnostics without raising exceptions.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    rows = len(df)
    cols = len(df.columns)

    missing_required = get_missing_required_columns(df.columns.tolist())

    duplicate_rows = int(df.duplicated().sum())

    duplicate_title_year = 0
    if {"title", "year"}.issubset(df.columns):
        duplicate_title_year = int(
            df.duplicated(subset=["title", "year"], keep=False).sum()
        )

    invalid_year_rows = 0
    if "year" in df.columns:
        invalid_year_rows = int(_invalid_year_mask(df["year"]).sum())

    negative_citation_rows = 0
    if "citations" in df.columns:
        negative_citation_rows = int(_negative_numeric_mask(df["citations"]).sum())

    null_title_rows = 0
    if "title" in df.columns:
        null_title_rows = int(df["title"].astype("string").str.strip().isna().sum())

    null_author_rows = 0
    if "authors" in df.columns:
        null_author_rows = int(df["authors"].astype("string").str.strip().isna().sum())

    passed = (
        len(missing_required) == 0
        and invalid_year_rows == 0
        and negative_citation_rows == 0
    )

    return ValidationReport(
        rows=rows,
        columns=cols,
        missing_required_columns=missing_required,
        duplicate_rows=duplicate_rows,
        duplicate_title_year=duplicate_title_year,
        invalid_year_rows=invalid_year_rows,
        negative_citation_rows=negative_citation_rows,
        null_title_rows=null_title_rows,
        null_author_rows=null_author_rows,
        passed=passed,
    )


def validate(
    df: pd.DataFrame,
    *,
    coerce_dtypes: bool = True,
    strict: bool = True,
) -> pd.DataFrame:
    """
    Validate bibliometric dataframe.

    Parameters
    ----------
    df:
        Input dataframe.
    coerce_dtypes:
        Apply canonical dtype coercion.
    strict:
        If True, raise ValidationError when required checks fail.

    Returns
    -------
    pd.DataFrame
        Validated dataframe.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    out = df.copy()

    if coerce_dtypes:
        out = _coerce_known_dtypes(out)

    report = schema_report(out)

    if strict and not report.passed:
        msgs: list[str] = []

        if report.missing_required_columns:
            msgs.append(f"Missing required columns: {report.missing_required_columns}")

        if report.invalid_year_rows:
            msgs.append(f"Invalid year rows: {report.invalid_year_rows}")

        if report.negative_citation_rows:
            msgs.append(f"Negative citation rows: {report.negative_citation_rows}")

        raise ValidationError(" | ".join(msgs))

    return out


def add_missing_canonical_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add absent canonical columns with pd.NA values.
    """
    out = df.copy()

    for col in CANONICAL_COLUMNS:
        if col not in out.columns:
            out[col] = pd.NA

    return out


def reorder_canonical_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reorder dataframe to canonical-first layout.
    """
    ordered = [c for c in CANONICAL_COLUMNS if c in df.columns]
    remaining = [c for c in df.columns if c not in ordered]
    return df[ordered + remaining]
