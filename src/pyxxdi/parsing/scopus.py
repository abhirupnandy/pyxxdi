from __future__ import annotations

import pandas as pd

from pyxxdi.schemas import harmonize_schema


def _split_semicolon(value: object) -> list[str]:
    """
    Convert semicolon-separated strings into clean list.
    """
    if pd.isna(value):
        return []

    parts = [x.strip() for x in str(value).split(";")]
    return [x for x in parts if x]


def _prepare_keywords(df: pd.DataFrame) -> pd.DataFrame:
    if "author_keywords" in df.columns:
        df["author_keywords"] = df["author_keywords"].apply(_split_semicolon)

    if "index_keywords" in df.columns:
        df["index_keywords"] = df["index_keywords"].apply(_split_semicolon)

    return df


def _prepare_affiliations(df: pd.DataFrame) -> pd.DataFrame:
    if "institution" in df.columns:
        df["institutions"] = df["institution"].apply(_split_semicolon)

    return df


def read_scopus(
    path: str,
    *,
    encoding: str = "utf-8",
    low_memory: bool = False,
) -> pd.DataFrame:
    """
    Read Scopus CSV into canonical pyxxdi schema.
    """
    df = pd.read_csv(
        path,
        encoding=encoding,
        low_memory=low_memory,
    )

    df = harmonize_schema(df)
    df = _prepare_keywords(df)
    df = _prepare_affiliations(df)

    # backward compatibility + phase3 naming
    df["source_db"] = "scopus"
    df["data_source"] = "scopus"
    df["raw_source_format"] = "csv"

    return df
