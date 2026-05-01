from __future__ import annotations

from collections.abc import Callable

import pandas as pd

from pyxxdi.metrics.core import compute_g, compute_h, compute_x
from pyxxdi.metrics.helpers import apply_filters
from pyxxdi.metrics.profile import prepare_citations
from pyxxdi.metrics.validators import (
    validate_citations_column,
    validate_dataframe,
    validate_metric_name,
)

MetricFunc = Callable[[object], float | int]
_DEFAULT_GLOBAL_UNIT = "all"


def _get_kernel(metric: str) -> MetricFunc:
    kernels: dict[str, MetricFunc] = {
        "h": compute_h,
        "g": compute_g,
        "x": compute_x,
    }
    return kernels[metric]


def _resolve_grouping(
    df: pd.DataFrame,
    unit: str | None,
) -> tuple[pd.DataFrame, str | None]:
    """
    Resolve grouping mode.

    Global mode is used when unit is None or the requested unit column is absent.
    """
    if unit is None or unit not in df.columns:
        work = df.copy()
        work[_DEFAULT_GLOBAL_UNIT] = _DEFAULT_GLOBAL_UNIT
        return work, _DEFAULT_GLOBAL_UNIT

    return df, unit


def metric(
    df: pd.DataFrame,
    *,
    metric: str = "x",
    unit: str | None = "institution",
    citations: str = "citations",
    sort: bool = True,
    top_n: int | None = None,
    min_records: int = 1,
    year_from: int | None = None,
    year_to: int | None = None,
    subject: str | list[str] | None = None,
    document_type: str | list[str] | None = None,
) -> pd.DataFrame:
    """Compute citation metric table in grouped or global mode."""
    validate_dataframe(df)
    validate_metric_name(metric)
    validate_citations_column(df, citations)

    if df.empty:
        return pd.DataFrame(columns=["unit", "records", "value", "rank"])

    filtered = apply_filters(
        df,
        year_from=year_from,
        year_to=year_to,
        subject=subject,
        document_type=document_type,
    )

    if filtered.empty:
        return pd.DataFrame(columns=["unit", "records", "value", "rank"])

    grouped_df, resolved_unit = _resolve_grouping(filtered, unit)
    kernel = _get_kernel(metric)

    rows: list[dict[str, object]] = []

    grouped = grouped_df.groupby(resolved_unit, dropna=True)

    for name, group in grouped:
        records = int(len(group))
        if records < min_records:
            continue

        cites = prepare_citations(group[citations])
        value = kernel(cites)
        rows.append({"unit": name, "records": records, "value": value})

    result = pd.DataFrame(rows)

    if result.empty:
        return pd.DataFrame(columns=["unit", "records", "value", "rank"])

    if sort:
        result = result.sort_values(
            by=["value", "records", "unit"],
            ascending=[False, False, True],
        )

    result["rank"] = result["value"].rank(method="dense", ascending=False).astype(int)
    result = result.reset_index(drop=True)

    if top_n is not None:
        result = result.head(top_n).reset_index(drop=True)

    return result
