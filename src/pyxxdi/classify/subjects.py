from __future__ import annotations

import pandas as pd

RULES = {
    "Computer Science": [
        "machine learning",
        "artificial intelligence",
        "deep learning",
        "data mining",
        "neural network",
        "computer vision",
        "nlp",
        "natural language processing",
        "software",
        "algorithm",
    ],
    "Medicine": [
        "covid",
        "cancer",
        "clinical",
        "patient",
        "hospital",
        "drug",
        "health",
        "medical",
    ],
    "Physics": [
        "quantum",
        "particle",
        "relativity",
        "optics",
        "photon",
        "plasma",
    ],
    "Engineering": [
        "sensor",
        "manufacturing",
        "civil",
        "electrical",
        "mechanical",
        "robotics",
    ],
    "Social Sciences": [
        "policy",
        "education",
        "economics",
        "sociology",
        "psychology",
    ],
}


SOURCE_RULES = {
    "nature": "Multidisciplinary",
    "science": "Multidisciplinary",
    "ieee": "Engineering",
    "acm": "Computer Science",
    "lancet": "Medicine",
}


def _text_blob(row: pd.Series) -> str:
    vals = []

    for col in ["title", "author_keywords", "index_keywords", "keywords_all", "source"]:
        if col in row.index and pd.notna(row[col]):
            vals.append(str(row[col]).lower())

    return " ".join(vals)


def _classify_text(text: str) -> str:
    for field, keywords in RULES.items():
        for kw in keywords:
            if kw in text:
                return field

    for token, field in SOURCE_RULES.items():
        if token in text:
            return field

    return "Unknown"


def classify_subjects(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rule-based subject classification.
    """
    out = df.copy()

    out["subject"] = out.apply(
        lambda row: _classify_text(_text_blob(row)),
        axis=1,
    )

    return out
