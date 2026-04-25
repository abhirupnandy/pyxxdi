from __future__ import annotations

import pandas as pd


def temporal_trends(
    df: pd.DataFrame,
    *,
    cumulative: bool = False,
) -> pd.DataFrame:
    """
    Aggregate annual publication trends.
    """
    if "year" not in df.columns:
        raise ValueError("Column 'year' not found.")

    out = df.copy()

    if "citations" not in out.columns:
        out["citations"] = 0

    grouped = (
        out.groupby("year")
        .agg(
            papers=("year", "size"),
            citations=("citations", "sum"),
            avg_citations=("citations", "mean"),
        )
        .reset_index()
        .sort_values("year")
        .reset_index(drop=True)
    )

    grouped["avg_citations"] = grouped["avg_citations"].round(2)

    if cumulative:
        grouped["cum_papers"] = grouped["papers"].cumsum()
        grouped["cum_citations"] = grouped["citations"].cumsum()

    return grouped
