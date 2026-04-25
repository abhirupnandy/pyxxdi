from __future__ import annotations

import pandas as pd


def institution_profile(
    df: pd.DataFrame,
    *,
    sort_by: str = "papers",
    ascending: bool = False,
) -> pd.DataFrame:
    """
    Aggregate publication analytics by institution.
    """
    if "institution" not in df.columns:
        raise ValueError("Column 'institution' not found.")

    out = df.copy()

    if "citations" not in out.columns:
        out["citations"] = 0

    grouped = (
        out.groupby("institution", dropna=False)
        .agg(
            papers=("institution", "size"),
            citations=("citations", "sum"),
            avg_citations=("citations", "mean"),
            max_citations=("citations", "max"),
        )
        .reset_index()
    )

    grouped["avg_citations"] = grouped["avg_citations"].round(2)

    if sort_by in grouped.columns:
        grouped = grouped.sort_values(
            by=sort_by,
            ascending=ascending,
        )

    grouped = grouped.reset_index(drop=True)

    return grouped
