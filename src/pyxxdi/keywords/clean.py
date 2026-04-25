from __future__ import annotations

import re

import pandas as pd


def _split_terms(value: object) -> list[str]:
    """
    Split by ; , |
    """
    if pd.isna(value):
        return []

    text = str(value)

    parts = re.split(r"[;,|]", text)

    return [x.strip() for x in parts if x.strip()]


def _normalize_term(term: str) -> str:
    """
    Light cleaning only.
    No synonym expansion.
    """
    term = str(term).strip().lower()
    term = term.replace("-", " ")
    term = re.sub(r"\s+", " ", term)
    term = re.sub(r"[^\w\s]", "", term).strip()

    return term


def _clean_join(value: object) -> str:
    seen = set()
    out = []

    for raw in _split_terms(value):
        term = _normalize_term(raw)

        if term and term not in seen:
            seen.add(term)
            out.append(term)

    return "; ".join(out)


def clean_keywords(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic keyword cleaning.
    Backward compatible.
    """
    out = df.copy()

    for col in ["author_keywords", "index_keywords"]:
        if col in out.columns:
            out[col] = out[col].apply(_clean_join)

    if "author_keywords" in out.columns and "index_keywords" in out.columns:
        merged = (
            out["author_keywords"].fillna("") + "; " + out["index_keywords"].fillna("")
        )

        out["keywords_all"] = merged.apply(_clean_join)

    return out
