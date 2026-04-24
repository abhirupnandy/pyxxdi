"""
Affiliation cleaning utilities for pyxxdi.

Includes:
- whitespace cleanup
- case normalisation
- separator cleanup
- alias mapping
- institution extraction helpers
"""

from __future__ import annotations

import re
from collections.abc import Mapping

import pandas as pd

_MULTI_SPACE = re.compile(r"\s+")
_MULTI_SEP = re.compile(r"\s*;\s*")


# ---------------------------------------------------------------------
# Default alias map
# Extend over time
# ---------------------------------------------------------------------

DEFAULT_AFFILIATION_ALIASES: dict[str, str] = {
    "iit delhi": "Indian Institute of Technology Delhi",
    "iit bombay": "Indian Institute of Technology Bombay",
    "iit kharagpur": "Indian Institute of Technology Kharagpur",
    "bhu": "Banaras Hindu University",
    "banaras hindu univ": "Banaras Hindu University",
    "jnu": "Jawaharlal Nehru University",
}


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------


def _clean_text(value: object) -> object:
    if pd.isna(value):
        return pd.NA

    text = str(value).strip()

    if not text:
        return pd.NA

    text = _MULTI_SPACE.sub(" ", text)
    return text


def _normalise_affiliation_name(
    name: str,
    alias_map: Mapping[str, str],
) -> str:
    key = name.strip().lower()
    key = _MULTI_SPACE.sub(" ", key)

    return alias_map.get(key, name.strip())


def _split_affiliations(value: object) -> list[str]:
    if pd.isna(value):
        return []

    text = str(value).strip()

    if not text:
        return []

    return [x.strip() for x in _MULTI_SEP.split(text) if x.strip()]


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------


def clean_affiliations(
    df: pd.DataFrame,
    *,
    alias_map: Mapping[str, str] | None = None,
) -> pd.DataFrame:
    """
    Clean affiliations column.

    Parameters
    ----------
    df:
        Input dataframe.
    alias_map:
        Optional custom alias mapping.

    Returns
    -------
    pd.DataFrame
    """
    if "affiliations" not in df.columns:
        return df.copy()

    aliases = dict(DEFAULT_AFFILIATION_ALIASES)

    if alias_map:
        aliases.update(alias_map)

    out = df.copy()

    cleaned_values: list[object] = []
    institutions: list[object] = []

    for raw in out["affiliations"]:
        parts = _split_affiliations(raw)

        cleaned_parts = [
            _normalise_affiliation_name(
                _clean_text(p),
                aliases,
            )
            for p in parts
            if not pd.isna(_clean_text(p))
        ]

        # preserve order + remove duplicates
        uniq = list(dict.fromkeys(cleaned_parts))

        if uniq:
            cleaned_values.append("; ".join(uniq))
            institutions.append(uniq[0])
        else:
            cleaned_values.append(pd.NA)
            institutions.append(pd.NA)

    out["affiliations"] = pd.Series(
        cleaned_values,
        dtype="string",
    )

    out["institution"] = pd.Series(
        institutions,
        dtype="string",
    )

    return out
