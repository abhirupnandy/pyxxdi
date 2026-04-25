from __future__ import annotations

import pandas as pd

from .columns import ALIASES


def _rename_alias_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rename known legacy/source columns into canonical names.
    """
    rename_map: dict[str, str] = {}

    for col in df.columns:
        if col in ALIASES:
            rename_map[col] = ALIASES[col]

    if rename_map:
        df = df.rename(columns=rename_map)

    return df


def _ensure_core_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Guarantee minimum canonical columns exist.
    """
    defaults = {
        "record_id": None,
        "title": None,
        "authors": None,
        "year": pd.NA,
        "source": None,
        "citations": 0,
        "doi": None,
    }

    for col, val in defaults.items():
        if col not in df.columns:
            df[col] = val

    return df


def _cast_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Safe dtype coercion.
    """
    if "year" in df.columns:
        df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")

    if "citations" in df.columns:
        df["citations"] = (
            pd.to_numeric(df["citations"], errors="coerce").fillna(0).astype("Int64")
        )

    text_cols = [
        "record_id",
        "title",
        "authors",
        "source",
        "doi",
        "institution",
        "country",
    ]

    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype("string")

    return df


def _generate_record_id(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fill missing record_id values.
    """
    if "record_id" not in df.columns:
        df["record_id"] = range(1, len(df) + 1)

    missing = df["record_id"].isna() | (df["record_id"].astype(str).str.strip() == "")

    if missing.any():
        df.loc[missing, "record_id"] = [
            f"px_{i}" for i in range(1, int(missing.sum()) + 1)
        ]

    df["record_id"] = df["record_id"].astype("string")

    return df


def harmonize_schema(df: pd.DataFrame) -> pd.DataFrame:
    """
    Main public harmonisation pipeline.
    """
    out = df.copy()

    out = _rename_alias_columns(out)
    out = _ensure_core_columns(out)
    out = _generate_record_id(out)
    out = _cast_types(out)

    return out
