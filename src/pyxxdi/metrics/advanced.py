from __future__ import annotations

import pandas as pd

from pyxxdi.metrics.core import compute_h
from pyxxdi.metrics.x_index import x_index
from pyxxdi.metrics.xd_index import xd_index


def xc_index(
    df: pd.DataFrame,
    *,
    unit: str | None = "institution",
    category: str = "category",
    keyword: str = "keyword",
    citations: str = "citations",
) -> pd.DataFrame:
    """
    Category-adjusted x-index.
    """
    work = df.copy()

    if category not in work.columns:
        raise ValueError(f"category column '{category}' not found")

    if keyword not in work.columns:
        raise ValueError(f"keyword column '{keyword}' not found")

    work["_xc_token"] = work[category].astype(str) + " | " + work[keyword].astype(str)

    return x_index(
        work,
        unit=unit,
        keyword="_xc_token",
        citations=citations,
    )


def xo_index(
    df: pd.DataFrame,
    *,
    unit: str | None = "institution",
    category: str = "category",
    keyword: str = "keyword",
    citations: str = "citations",
) -> pd.DataFrame:
    """
    Overall expertise index.
    """
    rows = []

    grouped = (
        df.groupby(unit)
        if unit is not None and unit in df.columns
        else [("all", df)]
    )

    for name, group in grouped:
        scores = []

        for _, sub in group.groupby(category):
            out = x_index(
                sub,
                unit=unit,
                keyword=keyword,
                citations=citations,
            )

            if not out.empty:
                scores.append(float(out.iloc[0]["x_index"]))

        value = compute_h(pd.Series(scores).to_numpy())

        rows.append(
            {
                "unit": name,
                "xo_index": int(value),
                "records": len(group),
            }
        )

    result = pd.DataFrame(rows)

    result["rank"] = (
        result["xo_index"].rank(method="dense", ascending=False).astype(int)
    )

    return result.sort_values(
        by=["xo_index", "records", "unit"],
        ascending=[False, False, True],
    ).reset_index(drop=True)


def xx_index(
    df: pd.DataFrame,
    *,
    region: str = "country",
    institution: str = "institution",
    keyword: str = "keyword",
    citations: str = "citations",
) -> pd.DataFrame:
    """
    Nested x-index over institutions.
    """
    base = x_index(
        df,
        unit=institution,
        keyword=keyword,
        citations=citations,
    )

    merged = df[[region, institution]].drop_duplicates()

    base = base.merge(
        merged,
        left_on="unit",
        right_on=institution,
        how="left",
    )

    rows = []

    for name, group in base.groupby(region):
        value = compute_h(group["x_index"].to_numpy())

        rows.append(
            {
                "unit": name,
                "xx_index": int(value),
                "records": len(group),
            }
        )

    result = pd.DataFrame(rows)

    result["rank"] = (
        result["xx_index"].rank(method="dense", ascending=False).astype(int)
    )

    return result


def xxd_index(
    df: pd.DataFrame,
    *,
    region: str = "country",
    institution: str = "institution",
    category: str = "category",
    citations: str = "citations",
) -> pd.DataFrame:
    """
    Nested xd-index over institutions.
    """
    base = xd_index(
        df,
        unit=institution,
        category=category,
        citations=citations,
    )

    merged = df[[region, institution]].drop_duplicates()

    base = base.merge(
        merged,
        left_on="unit",
        right_on=institution,
        how="left",
    )

    rows = []

    for name, group in base.groupby(region):
        value = compute_h(group["xd_index"].to_numpy())

        rows.append(
            {
                "unit": name,
                "xxd_index": int(value),
                "records": len(group),
            }
        )

    result = pd.DataFrame(rows)

    result["rank"] = (
        result["xxd_index"].rank(method="dense", ascending=False).astype(int)
    )

    return result
