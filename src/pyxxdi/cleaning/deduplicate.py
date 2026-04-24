"""
Deduplication utilities for pyxxdi.

Current strategies:
- DOI exact duplicate removal
- title + year duplicate removal
- combined pipeline

Future-ready for fuzzy matching extensions.
"""

from __future__ import annotations

import re

import pandas as pd

_MULTI_SPACE = re.compile(r"\s+")


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------


def _normalise_title(value: object) -> object:
    """
    Create comparison-safe title key.
    """
    if pd.isna(value):
        return pd.NA

    text = str(value).strip().lower()
    text = _MULTI_SPACE.sub(" ", text)

    if not text:
        return pd.NA

    return text


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------


def drop_duplicate_doi(
    df: pd.DataFrame,
    *,
    keep: str = "first",
) -> pd.DataFrame:
    """
    Remove duplicate rows based on DOI.

    Rows with missing DOI are preserved.
    """
    if "doi" not in df.columns:
        return df.copy()

    out = df.copy()

    has_doi = out["doi"].notna()
    with_doi = out.loc[has_doi]
    no_doi = out.loc[~has_doi]

    with_doi = with_doi.drop_duplicates(
        subset=["doi"],
        keep=keep,
    )

    return pd.concat([with_doi, no_doi], ignore_index=True)


def drop_duplicate_title_year(
    df: pd.DataFrame,
    *,
    keep: str = "first",
) -> pd.DataFrame:
    """
    Remove duplicates using normalised title + year.
    """
    if not {"title", "year"}.issubset(df.columns):
        return df.copy()

    out = df.copy()

    out["_title_key"] = out["title"].map(_normalise_title)

    out = out.drop_duplicates(
        subset=["_title_key", "year"],
        keep=keep,
    )

    return out.drop(columns="_title_key")


def deduplicate(
    df: pd.DataFrame,
    *,
    keep: str = "first",
) -> pd.DataFrame:
    """
    Apply standard pyxxdi deduplication pipeline.

    Order:
    1. DOI duplicates
    2. title + year duplicates
    """
    out = drop_duplicate_doi(df, keep=keep)
    out = drop_duplicate_title_year(out, keep=keep)

    return out.reset_index(drop=True)
