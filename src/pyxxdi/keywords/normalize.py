from __future__ import annotations

import re

import pandas as pd

VOCAB = {
    "ai": "artificial intelligence",
    "ml": "machine learning",
    "dl": "deep learning",
    "nlp": "natural language processing",
    "covid19": "covid-19",
    "covid 19": "covid-19",
    "deep-learning": "deep learning",
}


def _split_terms(value: object) -> list[str]:
    if pd.isna(value):
        return []

    text = str(value)

    return [x.strip() for x in text.split(";") if x.strip()]


def _normalize_term(term: str) -> str:
    term = str(term).strip().lower()
    term = re.sub(r"\s+", " ", term)

    return VOCAB.get(term, term)


def _normalize_join(value: object) -> str:
    seen = set()
    out = []

    for raw in _split_terms(value):
        term = _normalize_term(raw)

        if term and term not in seen:
            seen.add(term)
            out.append(term)

    return "; ".join(out)


def normalize_keywords(df: pd.DataFrame) -> pd.DataFrame:
    """
    Semantic keyword normalization.
    """
    out = df.copy()

    for col in ["author_keywords", "index_keywords", "keywords_all"]:
        if col in out.columns:
            out[col] = out[col].apply(_normalize_join)

    return out
