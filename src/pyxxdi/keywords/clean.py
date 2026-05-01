from __future__ import annotations

import re

import pandas as pd


def _split_terms(value: object) -> list[str]:
    if isinstance(value, (list, tuple, set)):
        return [str(x).strip() for x in value if str(x).strip()]

    if pd.isna(value):
        return []

    return [x.strip() for x in re.split(r"[;,|]", str(value)) if x.strip()]


def _normalize_term(term: str) -> str:
    cleaned = str(term).strip().lower().replace("-", " ")
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = re.sub(r"[^\w\s]", "", cleaned).strip()
    return cleaned


def _clean_join(value: object) -> object:
    seen: set[str] = set()
    output: list[str] = []
    for raw in _split_terms(value):
        term = _normalize_term(raw)
        if term and term not in seen:
            seen.add(term)
            output.append(term)
    if not output:
        return pd.NA
    return "; ".join(output)


def clean_keywords(df: pd.DataFrame) -> pd.DataFrame:
    """Clean keyword columns and build keywords_all when possible."""
    out = df.copy()

    for col in ["author_keywords", "index_keywords"]:
        if col in out.columns:
            out[col] = out[col].map(_clean_join).astype("string")

    if "author_keywords" in out.columns and "index_keywords" in out.columns:
        merged = (
            out["author_keywords"].fillna("")
            + "; "
            + out["index_keywords"].fillna("")
        )
        out["keywords_all"] = merged.map(_clean_join).astype("string")

    return out
