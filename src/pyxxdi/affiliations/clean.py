from __future__ import annotations

import re

import pandas as pd

ALIASES = {
    "iitd": "Indian Institute of Technology Delhi",
    "iit delhi": "Indian Institute of Technology Delhi",
    "banaras hindu univ": "Banaras Hindu University",
    "banaras hindu university": "Banaras Hindu University",
    "bhu": "Banaras Hindu University",
    "univ of delhi": "University of Delhi",
    "university of delhi": "University of Delhi",
}


def _split_terms(value: object) -> list[str]:
    if isinstance(value, (list, tuple, set)):
        return [str(x).strip() for x in value if str(x).strip()]

    if pd.isna(value):
        return []

    parts = re.split(r"[;|]", str(value))
    return [x.strip() for x in parts if x.strip()]


def _normalize(term: str) -> str:
    term = str(term).strip().lower()
    term = re.sub(r"[.,]", " ", term)
    term = re.sub(r"\s+", " ", term).strip()

    if term in ALIASES:
        return ALIASES[term]

    return term.title()


def _clean_list(value: object) -> list[str]:
    seen = set()
    out = []

    for raw in _split_terms(value):
        val = _normalize(raw)

        if val and val not in seen:
            seen.add(val)
            out.append(val)

    return out


def _clean_join(value: object) -> str:
    return "; ".join(_clean_list(value))


def clean_affiliations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean affiliation strings.
    Backward compatible:
    affiliations -> institution
    """
    out = df.copy()

    for col in ["affiliations", "institution", "institutions"]:
        if col in out.columns:
            out[col] = out[col].apply(_clean_join)

    # legacy behaviour:
    # if affiliations exists, also create institution
    if "affiliations" in out.columns:
        first_vals = out["affiliations"].apply(
            lambda x: str(x).split(";")[0].strip() if str(x).strip() else ""
        )
        out["institution"] = first_vals

    return out
