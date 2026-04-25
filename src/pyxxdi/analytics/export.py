from __future__ import annotations

from pathlib import Path

import pandas as pd

from .dashboard import researcher_dashboard


def export_report(
    df: pd.DataFrame,
    path: str,
) -> str:
    """
    Export analytics report to CSV or Excel.

    Parameters
    ----------
    df:
        publication dataframe
    path:
        output path (.csv or .xlsx)
    """
    target = Path(path)

    dash = researcher_dashboard(df)

    overview = pd.DataFrame([dash["overview"]])

    top_papers = dash["top_papers"]
    trends = dash["yearly_trends"]

    suffix = target.suffix.lower()

    if suffix == ".csv":
        top_papers.to_csv(target, index=False)
        return str(target)

    if suffix == ".xlsx":
        with pd.ExcelWriter(target) as writer:
            overview.to_excel(
                writer,
                sheet_name="overview",
                index=False,
            )

            top_papers.to_excel(
                writer,
                sheet_name="top_papers",
                index=False,
            )

            trends.to_excel(
                writer,
                sheet_name="yearly_trends",
                index=False,
            )

        return str(target)

    raise ValueError("Only .csv or .xlsx supported.")
