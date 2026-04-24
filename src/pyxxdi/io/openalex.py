"""
OpenAlex reader for pyxxdi.

Supports:
1. OpenAlex JSONL / JSON exports
2. OpenAlex CSV tabular exports

Maps fields into pyxxdi canonical schema.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from pyxxdi.utils.validation import (
    add_missing_canonical_columns,
    reorder_canonical_columns,
)


class ReaderError(Exception):
    """Raised when OpenAlex file reading fails."""


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------


def _extract_authors(authorships: Any) -> str | pd.NA:
    if not isinstance(authorships, list):
        return pd.NA

    names: list[str] = []

    for item in authorships:
        try:
            name = item["author"]["display_name"]
            if name:
                names.append(name)
        except Exception:
            continue

    return "; ".join(names) if names else pd.NA


def _extract_affiliations(authorships: Any) -> str | pd.NA:
    if not isinstance(authorships, list):
        return pd.NA

    values: list[str] = []

    for item in authorships:
        institutions = item.get("institutions", [])
        for inst in institutions:
            name = inst.get("display_name")
            if name:
                values.append(name)

    uniq = list(dict.fromkeys(values))
    return "; ".join(uniq) if uniq else pd.NA


# ---------------------------------------------------------------------
# JSON reader
# ---------------------------------------------------------------------


def _read_openalex_json(path: Path) -> pd.DataFrame:
    records: list[dict[str, Any]] = []

    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue

            obj = json.loads(line)

            records.append(
                {
                    "raw_source_id": obj.get("id"),
                    "title": obj.get("title"),
                    "year": obj.get("publication_year"),
                    "doi": obj.get("doi"),
                    "citations": obj.get("cited_by_count"),
                    "document_type": obj.get("type"),
                    "source": (
                        obj.get("primary_location", {})
                        .get("source", {})
                        .get("display_name")
                    ),
                    "authors": _extract_authors(obj.get("authorships")),
                    "affiliations": _extract_affiliations(obj.get("authorships")),
                    "abstract": pd.NA,
                }
            )

    return pd.DataFrame(records)


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------


def read_openalex(
    path: str | Path,
    *,
    canonical: bool = True,
    **kwargs: Any,
) -> pd.DataFrame:
    """
    Read OpenAlex export.

    Supports .json, .jsonl, .csv

    Parameters
    ----------
    path:
        Input file path.
    canonical:
        Add missing canonical columns and reorder.
    **kwargs:
        Extra pandas arguments for CSV mode.

    Returns
    -------
    pd.DataFrame
    """
    path = Path(path)

    if not path.exists():
        raise ReaderError(f"File not found: {path}")

    suffix = path.suffix.lower()

    try:
        if suffix in {".json", ".jsonl"}:
            df = _read_openalex_json(path)

        elif suffix == ".csv":
            df = pd.read_csv(path, **kwargs)

        else:
            raise ReaderError("Unsupported OpenAlex format. Use .json, .jsonl, .csv")

    except Exception as exc:
        raise ReaderError(f"Failed to read OpenAlex file: {path}") from exc

    df["source_db"] = "openalex"

    if "record_id" not in df.columns:
        df["record_id"] = [f"px_{i:08d}" for i in range(1, len(df) + 1)]

    if canonical:
        df = add_missing_canonical_columns(df)
        df = reorder_canonical_columns(df)

    return df
