# tests/test_all_round_metrics.py

from __future__ import annotations

import pandas as pd

import pyxxdi as px


def sample_df() -> pd.DataFrame:
    """
    Comprehensive synthetic dataset covering:

    - institutions
    - countries
    - categories
    - keywords
    - citations
    - years
    - document types
    - variant columns
    """
    return pd.DataFrame(
        {
            "country": [
                "IN",
                "IN",
                "IN",
                "US",
                "US",
                "UK",
                "UK",
                "UK",
            ],
            "institution": [
                "IIT Delhi",
                "IIT Delhi",
                "DU",
                "MIT",
                "MIT",
                "Oxford",
                "Oxford",
                "Cambridge",
            ],
            "category": [
                "CS",
                "Math",
                "Economics",
                "CS",
                "Physics",
                "Medicine",
                "CS",
                "Biology",
            ],
            "keyword": [
                "AI",
                "Optimization",
                "Finance",
                "ML",
                "Quantum",
                "Cancer",
                "Vision",
                "Genomics",
            ],
            "citations": [
                30,
                12,
                8,
                40,
                18,
                25,
                10,
                15,
            ],
            "year": [
                2022,
                2023,
                2021,
                2022,
                2024,
                2020,
                2023,
                2024,
            ],
            "subject": [
                "Engineering",
                "Mathematics",
                "Economics",
                "Engineering",
                "Physics",
                "Medicine",
                "Engineering",
                "Biology",
            ],
            "document_type": [
                "Article",
                "Article",
                "Review",
                "Article",
                "Conference",
                "Article",
                "Review",
                "Article",
            ],
            "n_institutions": [
                3,
                2,
                1,
                4,
                2,
                3,
                2,
                1,
            ],
            "expected_citations": [
                10,
                6,
                4,
                12,
                8,
                10,
                5,
                7,
            ],
            "field_variance": [
                4,
                3,
                2,
                5,
                4,
                3,
                2,
                2,
            ],
        }
    )


# -------------------------------------------------------------------
# Traditional Metrics
# -------------------------------------------------------------------


def test_h_index():
    df = sample_df()
    out = px.h_index(df, unit="institution")

    assert not out.empty
    assert "h_index" in out.columns
    assert "rank" in out.columns


def test_g_index():
    df = sample_df()
    out = px.g_index(df, unit="institution")

    assert not out.empty
    assert "g_index" in out.columns


# -------------------------------------------------------------------
# Expertise Metrics
# -------------------------------------------------------------------


def test_x_index():
    df = sample_df()
    out = px.x_index(df)

    assert not out.empty
    assert "x_index" in out.columns


def test_xc_index():
    df = sample_df()
    out = px.xc_index(df)

    assert not out.empty
    assert "x_index" in out.columns


def test_xd_index():
    df = sample_df()
    out = px.xd_index(df)

    assert not out.empty
    assert "xd_index" in out.columns



# -------------------------------------------------------------------
# Nested Metrics
# -------------------------------------------------------------------


def test_xx_index():
    df = sample_df()
    out = px.xx_index(df)

    assert not out.empty
    assert "xx_index" in out.columns


def test_xxd_index():
    df = sample_df()
    out = px.xxd_index(df)

    assert not out.empty
    assert "xxd_index" in out.columns


# -------------------------------------------------------------------
# xd Variants
# -------------------------------------------------------------------


def test_xd_fractional_index():
    df = sample_df()
    out = px.xd_fractional_index(df)

    assert not out.empty
    assert "xd_index" in out.columns


def test_xd_field_normalized_index():
    df = sample_df()
    out = px.xd_field_normalized_index(df)

    assert not out.empty
    assert "xd_index" in out.columns


def test_xd_ivw_index():
    df = sample_df()
    out = px.xd_ivw_index(df)

    assert not out.empty
    assert "xd_index" in out.columns


# -------------------------------------------------------------------
# Filters
# -------------------------------------------------------------------


def test_year_filter():
    df = sample_df()
    out = px.xd_index(df, year_from=2023)

    assert not out.empty


def test_subject_filter():
    df = sample_df()
    out = px.xd_index(df, subject="Engineering")

    assert not out.empty


def test_document_type_filter():
    df = sample_df()
    out = px.xd_index(df, document_type="Review")

    assert not out.empty


# -------------------------------------------------------------------
# Ranking Options
# -------------------------------------------------------------------


def test_top_n():
    df = sample_df()
    out = px.xd_index(df, top_n=2)

    assert len(out) == 2


def test_min_records():
    df = sample_df()
    out = px.xd_index(df, min_records=2)

    assert not out.empty


# -------------------------------------------------------------------
# Root Namespace Exposure
# -------------------------------------------------------------------


def test_root_namespace():
    assert callable(px.h_index)
    assert callable(px.g_index)
    assert callable(px.x_index)
    assert callable(px.xd_index)
    assert callable(px.xx_index)
    assert callable(px.xxd_index)


# -------------------------------------------------------------------
# Output Structure
# -------------------------------------------------------------------


def test_common_columns():
    df = sample_df()
    out = px.xd_index(df)

    assert "unit" in out.columns
    assert "records" in out.columns
    assert "rank" in out.columns
