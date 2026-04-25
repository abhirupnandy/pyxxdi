from __future__ import annotations

from datetime import datetime

import pandas as pd

from .columns import ALL_COLUMNS, MANDATORY_COLUMNS

CURRENT_YEAR = datetime.now().year


class SchemaValidationError(ValueError):
    """Raised when dataframe fails hard schema validation."""


def missing_columns(df: pd.DataFrame) -> list[str]:
    """Return missing mandatory columns."""
    return [col for col in MANDATORY_COLUMNS if col not in df.columns]


def validate_required_columns(df: pd.DataFrame) -> None:
    """Raise if mandatory columns missing."""
    missing = missing_columns(df)

    if missing:
        raise SchemaValidationError(f"Missing required columns: {', '.join(missing)}")


def validate_year(df: pd.DataFrame) -> None:
    """Validate publication year values."""
    if "year" not in df.columns:
        return

    invalid = (
        df["year"].dropna().loc[(df["year"] < 1900) | (df["year"] > CURRENT_YEAR + 2)]
    )

    if not invalid.empty:
        raise SchemaValidationError(
            "Invalid values found in 'year'. Allowed range: 1900 to current_year + 2."
        )


def validate_citations(df: pd.DataFrame) -> None:
    """Validate citations are non-negative."""
    if "citations" not in df.columns:
        return

    invalid = df["citations"].dropna().loc[df["citations"] < 0]

    if not invalid.empty:
        raise SchemaValidationError("Negative values found in 'citations'.")


def validate_titles(df: pd.DataFrame) -> None:
    """Ensure title is not empty/null."""
    if "title" not in df.columns:
        return

    invalid = df["title"].isna() | (df["title"].astype(str).str.strip() == "")

    if invalid.any():
        raise SchemaValidationError("Blank or null values found in 'title'.")


def validate_schema(df: pd.DataFrame) -> None:
    """
    Full hard validation for canonical pyxxdi schema.
    Raises SchemaValidationError on failure.
    """
    validate_required_columns(df)
    validate_titles(df)
    validate_year(df)
    validate_citations(df)


def warn_noncanonical(df: pd.DataFrame) -> list[str]:
    """
    Return columns not part of canonical schema.
    Non-blocking informational helper.
    """
    return [col for col in df.columns if col not in ALL_COLUMNS]
