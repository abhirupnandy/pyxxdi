from __future__ import annotations

import pandas as pd

from pyxxdi.metrics import (
    g_index,
    h_index,
    x_index,
    xd_index,
)

from .temporal import temporal_trends


def _safe_metric(func, df: pd.DataFrame):
    """
    Run existing metric engine with temporary unit column.
    """
    temp = df.copy()

    if "institution" not in temp.columns:
        temp["institution"] = "all"

    try:
        result = func(temp)

        # if scalar already
        if isinstance(result, (int, float)):
            return result

        # if dataframe/series output
        if hasattr(result, "iloc"):
            val = result.iloc[0]

            if hasattr(val, "item"):
                try:
                    return val.item()
                except Exception:
                    return val

            return val

        return result

    except Exception:
        return None


def researcher_dashboard(df: pd.DataFrame) -> dict:
    """
    One-call researcher analytics summary.
    """
    out = df.copy()

    if "citations" not in out.columns:
        out["citations"] = 0

    papers = len(out)
    total_citations = int(out["citations"].sum())

    avg_citations = round(total_citations / papers, 2) if papers > 0 else 0.0

    metrics = {
        "h_index": _safe_metric(h_index, out),
        "g_index": _safe_metric(g_index, out),
        "x_index": _safe_metric(x_index, out),
        "xd_index": _safe_metric(xd_index, out),
    }

    result = {
        "overview": {
            "papers": papers,
            "citations": total_citations,
            "avg_citations": avg_citations,
        },
        "metrics": metrics,
        "top_papers": out.sort_values(
            by="citations",
            ascending=False,
        ).head(10),
        "yearly_trends": temporal_trends(out)
        if "year" in out.columns
        else pd.DataFrame(),
    }

    return result
