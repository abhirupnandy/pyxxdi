"""Shared helper functions for metrics."""

from __future__ import annotations

import pandas as pd


def apply_filters(
    df: pd.DataFrame,
    *,
    year_from: int | None = None,
    year_to: int | None = None,
    subject: str | list[str] | None = None,
    document_type: str | list[str] | None = None,
) -> pd.DataFrame:
    """
    Apply optional bibliometric filters.

    Filters are only applied if the relevant column exists.
    """
    out = df.copy()

    if year_from is not None and "year" in out.columns:
        out = out[out["year"] >= year_from]

    if year_to is not None and "year" in out.columns:
        out = out[out["year"] <= year_to]

    if subject is not None and "subject" in out.columns:
        values = [subject] if isinstance(subject, str) else list(subject)
        out = out[out["subject"].isin(values)]

    if document_type is not None and "document_type" in out.columns:
        values = (
            [document_type] if isinstance(document_type, str) else list(document_type)
        )
        out = out[out["document_type"].isin(values)]

    return out
