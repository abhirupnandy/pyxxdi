"""
Publication-level cleaning utilities for pyxxdi.

Includes:
- title cleanup
- DOI normalisation
- year coercion
- missing value standardisation
- whitespace cleanup
"""

from __future__ import annotations

import re
from datetime import datetime

import pandas as pd

# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

_DOI_PREFIX = re.compile(r"^(https?://(dx\.)?doi\.org/)", re.I)
_MULTI_SPACE = re.compile(r"\s+")


def _clean_text(value: object) -> object:
    """
    Generic text normalisation.
    """
    if pd.isna(value):
        return pd.NA

    text = str(value).strip()

    if not text:
        return pd.NA

    text = _MULTI_SPACE.sub(" ", text)

    return text


def _clean_title(value: object) -> object:
    """
    Clean publication title.
    """
    text = _clean_text(value)

    if pd.isna(text):
        return pd.NA

    return str(text)


def _clean_doi(value: object) -> object:
    """
    Standardise DOI.

    Examples
    --------
    https://doi.org/10.xxxx/abc -> 10.xxxx/abc
    DOI:10.xxxx/abc -> 10.xxxx/abc
    """
    if pd.isna(value):
        return pd.NA

    doi = str(value).strip().lower()

    if not doi:
        return pd.NA

    doi = doi.replace("doi:", "").strip()
    doi = _DOI_PREFIX.sub("", doi)
    doi = doi.strip("/ ")

    return doi if doi else pd.NA


def _clean_year(value: object) -> object:
    """
    Coerce year safely.
    """
    if pd.isna(value):
        return pd.NA

    try:
        year = int(float(value))
    except Exception:
        return pd.NA

    current_year = datetime.now().year + 1

    if 1500 <= year <= current_year:
        return year

    return pd.NA


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------


def clean_publications(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Clean publication metadata columns.

    Parameters
    ----------
    df:
        Input dataframe.

    Returns
    -------
    pd.DataFrame
    """
    out = df.copy()

    if "title" in out.columns:
        out["title"] = out["title"].map(_clean_title).astype("string")

    if "doi" in out.columns:
        out["doi"] = out["doi"].map(_clean_doi).astype("string")

    if "year" in out.columns:
        out["year"] = out["year"].map(_clean_year).astype("Int64")

    if "source" in out.columns:
        out["source"] = out["source"].map(_clean_text).astype("string")

    if "document_type" in out.columns:
        out["document_type"] = (
            out["document_type"].map(_clean_text).astype("string").str.lower()
        )

    if "citations" in out.columns:
        out["citations"] = (
            pd.to_numeric(
                out["citations"],
                errors="coerce",
            )
            .clip(lower=0)
            .astype("Int64")
        )

    return out
