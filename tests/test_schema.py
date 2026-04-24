"""
Tests for pyxxdi schema layer.
"""

from __future__ import annotations

import pyxxdi as px


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
