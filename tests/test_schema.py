"""
Tests for pyxxdi schema layer.
"""

from __future__ import annotations

import pandas as pd
import pytest

import pyxxdi as px
from pyxxdi.schemas import SchemaValidationError, validate_schema


def test_canonical_columns_exists() -> None:
    assert isinstance(px.CANONICAL_COLUMNS, list)
    assert len(px.CANONICAL_COLUMNS) > 0


def test_required_columns_present_in_canonical() -> None:
    for col in px.REQUIRED_COLUMNS:
        assert col in px.CANONICAL_COLUMNS


def test_metric_required_columns_present() -> None:
    for col in px.METRIC_REQUIRED_COLUMNS:
        assert col in px.CANONICAL_COLUMNS


def test_dtype_map_contains_core_columns() -> None:
    expected = {
        "title",
        "authors",
        "year",
        "doi",
        "citations",
    }

    for col in expected:
        assert col in px.DTYPE_MAP


def test_title_authors_year_order() -> None:
    idx_title = px.CANONICAL_COLUMNS.index("title")
    idx_authors = px.CANONICAL_COLUMNS.index("authors")
    idx_year = px.CANONICAL_COLUMNS.index("year")

    assert idx_title < idx_authors < idx_year


def test_validate_schema_success() -> None:
    df = pd.DataFrame(
        {
            "record_id": ["1"],
            "title": ["Paper A"],
            "year": [2020],
            "source": ["Journal X"],
            "citations": [12],
        }
    )

    validate_schema(df)


def test_validate_schema_missing_required() -> None:
    df = pd.DataFrame(
        {
            "title": ["Paper A"],
            "year": [2020],
        }
    )

    with pytest.raises(SchemaValidationError):
        validate_schema(df)


def test_validate_schema_negative_citations() -> None:
    df = pd.DataFrame(
        {
            "record_id": ["1"],
            "title": ["Paper A"],
            "year": [2020],
            "source": ["Journal X"],
            "citations": [-5],
        }
    )

    with pytest.raises(SchemaValidationError):
        validate_schema(df)


def test_validate_schema_blank_title() -> None:
    df = pd.DataFrame(
        {
            "record_id": ["1"],
            "title": [""],
            "year": [2020],
            "source": ["Journal X"],
            "citations": [0],
        }
    )

    with pytest.raises(SchemaValidationError):
        validate_schema(df)
