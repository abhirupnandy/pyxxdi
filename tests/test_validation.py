"""
Tests for pyxxdi validation layer.
"""

from __future__ import annotations

import pandas as pd
import pytest

import pyxxdi as px

# ---------------------------------------------------------------------
# validate()
# ---------------------------------------------------------------------


def test_validate_success_minimum_schema() -> None:
    df = pd.DataFrame(
        {
            "title": ["Paper A"],
            "authors": ["Smith J"],
            "year": [2020],
        }
    )

    out = px.validate(df)

    assert isinstance(out, pd.DataFrame)
    assert len(out) == 1


def test_validate_missing_required_columns_raises() -> None:
    df = pd.DataFrame(
        {
            "title": ["Paper A"],
            "year": [2020],
        }
    )

    with pytest.raises(px.ValidationError):
        px.validate(df)


def test_validate_invalid_year_raises() -> None:
    df = pd.DataFrame(
        {
            "title": ["Paper A"],
            "authors": ["Smith J"],
            "year": [1200],
        }
    )

    with pytest.raises(px.ValidationError):
        px.validate(df)


def test_validate_negative_citations_raises() -> None:
    df = pd.DataFrame(
        {
            "title": ["Paper A"],
            "authors": ["Smith J"],
            "year": [2020],
            "citations": [-5],
        }
    )

    with pytest.raises(px.ValidationError):
        px.validate(df)


def test_validate_non_strict_mode_does_not_raise() -> None:
    df = pd.DataFrame(
        {
            "title": ["Paper A"],
            "year": [1200],
        }
    )

    out = px.validate(df, strict=False)

    assert isinstance(out, pd.DataFrame)


# ---------------------------------------------------------------------
# schema_report()
# ---------------------------------------------------------------------


def test_schema_report_detects_duplicates() -> None:
    df = pd.DataFrame(
        {
            "title": ["Paper A", "Paper A"],
            "authors": ["Smith J", "Smith J"],
            "year": [2020, 2020],
        }
    )

    report = px.schema_report(df)

    assert report.rows == 2
    assert report.duplicate_title_year == 2


def test_schema_report_missing_columns() -> None:
    df = pd.DataFrame(
        {
            "title": ["Paper A"],
        }
    )

    report = px.schema_report(df)

    assert "authors" in report.missing_required_columns
    assert "year" in report.missing_required_columns


def test_add_missing_canonical_columns() -> None:
    df = pd.DataFrame(
        {
            "title": ["Paper A"],
            "authors": ["Smith"],
            "year": [2020],
        }
    )

    out = px.add_missing_canonical_columns(df)

    assert "doi" in out.columns
    assert "citations" in out.columns


def test_reorder_canonical_columns() -> None:
    df = pd.DataFrame(
        {
            "year": [2020],
            "authors": ["Smith"],
            "title": ["Paper A"],
        }
    )

    out = px.reorder_canonical_columns(df)

    assert list(out.columns[:3]) == [
        "title",
        "authors",
        "year",
    ]
