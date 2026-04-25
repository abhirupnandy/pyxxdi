from __future__ import annotations

import pandas as pd


def compare_institutions(
    profiles: dict[str, pd.DataFrame],
    *,
    sort_by: str = "citations",
    ascending: bool = False,
) -> pd.DataFrame:
    """
    Compare multiple institutional publication datasets.
    """
    rows = []

    for name, df in profiles.items():
        temp = df.copy()

        if "citations" not in temp.columns:
            temp["citations"] = 0

        papers = len(temp)
        citations = int(temp["citations"].sum())

        avg = (
            round(
                citations / papers,
                2,
            )
            if papers > 0
            else 0.0
        )

        top = int(temp["citations"].max()) if papers > 0 else 0

        rows.append(
            {
                "institution": name,
                "papers": papers,
                "citations": citations,
                "avg_citations": avg,
                "top_paper": top,
            }
        )

    out = pd.DataFrame(rows)

    if sort_by in out.columns:
        out = out.sort_values(
            by=sort_by,
            ascending=ascending,
        )

    return out.reset_index(drop=True)
