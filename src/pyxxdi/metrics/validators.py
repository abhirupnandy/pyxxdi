"""Validation utilities for metrics."""

from __future__ import annotations

import pandas as pd

VALID_METRICS = {"h", "g", "x"}


def validate_dataframe(df: pd.DataFrame) -> None:
    """
    Validate that input is a pandas DataFrame.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")


def validate_citations_column(
    df: pd.DataFrame,
    citations: str,
) -> None:
    """
    Ensure citations column exists.
    """
    if citations not in df.columns:
        raise ValueError(f"citations column '{citations}' not found")


def validate_unit_column(
    df: pd.DataFrame,
    unit: str | None,
) -> None:
    """
    Ensure grouping column exists.
    """
    if unit is not None and unit not in df.columns:
        raise ValueError(f"unit column '{unit}' not found")


def validate_metric_name(metric: str) -> None:
    """
    Ensure metric is supported.
    """
    if metric not in VALID_METRICS:
        allowed = ", ".join(sorted(VALID_METRICS))
        raise ValueError(f"metric must be one of: {allowed}")
