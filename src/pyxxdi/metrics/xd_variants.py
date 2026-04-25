from __future__ import annotations

import pandas as pd

from pyxxdi.metrics.xd_index import xd_index


def xd_fractional_index(
    df: pd.DataFrame,
    *,
    institutions_col: str = "n_institutions",
    citations: str = "citations",
    **kwargs,
) -> pd.DataFrame:
    """
    Fractional xd-index.

    Citations divided by number of institutions.
    """
    work = df.copy()

    if institutions_col not in work.columns:
        raise ValueError(f"column '{institutions_col}' not found")

    work[citations] = work[citations] / work[institutions_col]

    return xd_index(
        work,
        citations=citations,
        **kwargs,
    )


def xd_field_normalized_index(
    df: pd.DataFrame,
    *,
    expected_col: str = "expected_citations",
    citations: str = "citations",
    **kwargs,
) -> pd.DataFrame:
    """
    Field-normalized xd-index.

    Citations divided by expected field mean.
    """
    work = df.copy()

    if expected_col not in work.columns:
        raise ValueError(f"column '{expected_col}' not found")

    work[citations] = work[citations] / work[expected_col]

    return xd_index(
        work,
        citations=citations,
        **kwargs,
    )


def xd_ivw_index(
    df: pd.DataFrame,
    *,
    variance_col: str = "field_variance",
    citations: str = "citations",
    **kwargs,
) -> pd.DataFrame:
    """
    Inverse-variance weighted xd-index.
    """
    work = df.copy()

    if variance_col not in work.columns:
        raise ValueError(f"column '{variance_col}' not found")

    work[citations] = work[citations] / work[variance_col]

    return xd_index(
        work,
        citations=citations,
        **kwargs,
    )
