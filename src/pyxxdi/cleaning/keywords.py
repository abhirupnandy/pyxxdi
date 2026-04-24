"""
Keyword cleaning utilities for pyxxdi.

Starter features:
- lowercase
- trim spaces
- separator normalisation
- duplicate keyword removal
- applies to author_keywords and index_keywords
"""

from __future__ import annotations

import re

import pandas as pd

_MULTI_SPACE = re.compile(r"\s+")
_SEPARATORS = re.compile(r"\s*(;|,|\|)\s*")


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------


def _clean_keyword_text(text: str) -> str:
    text = text.strip().lower()
    text = _MULTI_SPACE.sub(" ", text)
    return text


def _split_keywords(value: object) -> list[str]:
    if pd.isna(value):
        return []

    text = str(value).strip()

    if not text:
        return []

    return [x for x in _SEPARATORS.split(text) if x not in {";", ",", "|"}]


def _clean_keyword_cell(value: object) -> object:
    keywords = _split_keywords(value)

    cleaned: list[str] = []

    for kw in keywords:
        kw2 = _clean_keyword_text(kw)

        if kw2:
            cleaned.append(kw2)

    # preserve order, remove duplicates
    uniq = list(dict.fromkeys(cleaned))

    if not uniq:
        return pd.NA

    return "; ".join(uniq)


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------


def clean_keywords(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Clean keyword columns.

    Applies to:
    - author_keywords
    - index_keywords
    """
    out = df.copy()

    for col in ["author_keywords", "index_keywords"]:
        if col in out.columns:
            out[col] = out[col].map(_clean_keyword_cell).astype("string")

    return out
