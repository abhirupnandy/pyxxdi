from __future__ import annotations

import pandas as pd

from pyxxdi.metrics.helpers import apply_filters
from pyxxdi.metrics.validators import (
    validate_citations_column,
    validate_dataframe,
    validate_unit_column,
)


def _compute_xd_from_totals(values: pd.Series) -> int:
    """
    Compute xd-index using CRR >= 1.
    """
    totals = values.sort_values(ascending=False).reset_index(drop=True)

    ranks = pd.Series(
        range(1, len(totals) + 1),
        dtype=float,
    )

    crr = totals.astype(float) / ranks

    valid = crr >= 1

    if not valid.any():
        return 0

    return int(valid[valid].index.max() + 1)


def xd_index(
    df: pd.DataFrame,
    *,
    unit: str = "institution",
    category: str = "category",
    citations: str = "citations",
    top_n: int | None = None,
    min_records: int = 1,
    sort: bool = True,
    year_from: int | None = None,
    year_to: int | None = None,
    subject: str | list[str] | None = None,
    document_type: str | list[str] | None = None,
) -> pd.DataFrame:
    """
    Compute xd-index (expertise diversity index).

    Returns
    -------
    DataFrame
        unit, records, xd_index, rank
    """
    validate_dataframe(df)
    validate_unit_column(df, unit)
    validate_citations_column(df, citations)

    if category not in df.columns:
        raise ValueError(f"category column '{category}' not found")

    df = apply_filters(
        df,
        year_from=year_from,
        year_to=year_to,
        subject=subject,
        document_type=document_type,
    )

    if df.empty:
        return pd.DataFrame()

    rows: list[dict[str, object]] = []

    grouped = df.groupby(unit, dropna=True)

    for name, group in grouped:
        records = int(len(group))

        if records < min_records:
            continue

        agg = group.groupby(category)[citations].sum().sort_values(ascending=False)

        value = _compute_xd_from_totals(agg)

        rows.append(
            {
                "unit": name,
                "records": records,
                "xd_index": value,
            }
        )

    result = pd.DataFrame(rows)

    if result.empty:
        return result

    if sort:
        result = result.sort_values(
            by=["xd_index", "records", "unit"],
            ascending=[False, False, True],
        )

    result["rank"] = (
        result["xd_index"].rank(method="dense", ascending=False).astype(int)
    )

    result = result.reset_index(drop=True)

    if top_n is not None:
        result = result.head(top_n).reset_index(drop=True)

    return result
