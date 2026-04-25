from __future__ import annotations

import pandas as pd

from .dashboard import researcher_dashboard


def compare_researchers(
    profiles: dict[str, pd.DataFrame],
    *,
    sort_by: str = "citations",
    ascending: bool = False,
) -> pd.DataFrame:
    """
    Compare multiple researcher publication datasets.

    Parameters
    ----------
    profiles:
        dict mapping researcher name -> dataframe
    """
    rows = []

    for name, df in profiles.items():
        dash = researcher_dashboard(df)

        rows.append(
            {
                "researcher": name,
                "papers": dash["overview"]["papers"],
                "citations": dash["overview"]["citations"],
                "avg_citations": dash["overview"]["avg_citations"],
                "h_index": dash["metrics"]["h_index"],
                "g_index": dash["metrics"]["g_index"],
                "x_index": dash["metrics"]["x_index"],
                "xd_index": dash["metrics"]["xd_index"],
            }
        )

    out = pd.DataFrame(rows)

    if sort_by in out.columns:
        out = out.sort_values(
            by=sort_by,
            ascending=ascending,
        )

    return out.reset_index(drop=True)
