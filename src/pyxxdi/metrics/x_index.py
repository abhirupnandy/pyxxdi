from __future__ import annotations

import pandas as pd

from pyxxdi.metrics.engines import metric as generic_metric
from pyxxdi.metrics.helpers import apply_filters
from pyxxdi.metrics.validators import (
    validate_citations_column,
    validate_dataframe,
)


def _compute_x_from_totals(values: pd.Series) -> int:
    totals = values.sort_values(ascending=False).reset_index(drop=True)
    ranks = pd.Series(range(1, len(totals) + 1), dtype=float)
    crr = totals.astype(float) / ranks
    valid = crr >= 1
    if not valid.any():
        return 0
    return int(valid[valid].index.max() + 1)


def _thematic_x_index(
    df: pd.DataFrame,
    *,
    unit: str | None,
    keyword: str,
    citations: str,
    top_n: int | None,
    min_records: int,
    sort: bool,
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []

    if unit is not None and unit in df.columns:
        grouped = df.groupby(unit, dropna=True)
    else:
        grouped = [("all", df)]

    for name, group in grouped:
        records = int(len(group))
        if records < min_records:
            continue

        agg = group.groupby(keyword)[citations].sum().sort_values(ascending=False)
        value = _compute_x_from_totals(agg)
        rows.append({"unit": name, "records": records, "x_index": value})

    result = pd.DataFrame(rows)

    if result.empty:
        return pd.DataFrame(columns=["unit", "records", "x_index", "rank"])

    if sort:
        result = result.sort_values(
            by=["x_index", "records", "unit"],
            ascending=[False, False, True],
        )

    result["rank"] = result["x_index"].rank(method="dense", ascending=False).astype(int)
    result = result.reset_index(drop=True)

    if top_n is not None:
        result = result.head(top_n).reset_index(drop=True)

    return result


def x_index(
    df: pd.DataFrame,
    *,
    unit: str | None = "institution",
    keyword: str = "keyword",
    citations: str = "citations",
    top_n: int | None = None,
    min_records: int = 1,
    sort: bool = True,
    year_from: int | None = None,
    year_to: int | None = None,
    subject: str | list[str] | None = None,
    document_type: str | list[str] | None = None,
) -> pd.DataFrame:
    """Compute x-index in thematic mode or citation-profile fallback mode."""
    validate_dataframe(df)
    validate_citations_column(df, citations)

    filtered = apply_filters(
        df,
        year_from=year_from,
        year_to=year_to,
        subject=subject,
        document_type=document_type,
    )

    if filtered.empty:
        return pd.DataFrame(columns=["unit", "records", "x_index", "rank"])

    if keyword in filtered.columns:
        return _thematic_x_index(
            filtered,
            unit=unit,
            keyword=keyword,
            citations=citations,
            top_n=top_n,
            min_records=min_records,
            sort=sort,
        )

    out = generic_metric(
        filtered,
        metric="x",
        unit=unit,
        citations=citations,
        top_n=top_n,
        min_records=min_records,
        sort=sort,
    )
    if "value" in out.columns:
        out = out.rename(columns={"value": "x_index"})
    return out
