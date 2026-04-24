"""
Tests for pyxxdi cleaning layer.
"""

from __future__ import annotations

import pandas as pd

import pyxxdi as px

# ---------------------------------------------------------------------
# clean_publications()
# ---------------------------------------------------------------------


def test_clean_publications_doi_normalisation() -> None:
    df = pd.DataFrame(
        {
            "title": ["Paper A"],
            "authors": ["Smith"],
            "year": [2020],
            "doi": ["https://doi.org/10.1000/ABC123"],
        }
    )

    out = px.clean_publications(df)

    assert out.loc[0, "doi"] == "10.1000/abc123"


def test_clean_publications_invalid_year_to_na() -> None:
    df = pd.DataFrame(
        {
            "title": ["Paper A"],
            "authors": ["Smith"],
            "year": [1400],
        }
    )

    out = px.clean_publications(df)

    assert pd.isna(out.loc[0, "year"])


def test_clean_publications_negative_citations_to_zero() -> None:
    df = pd.DataFrame(
        {
            "title": ["Paper A"],
            "authors": ["Smith"],
            "year": [2020],
            "citations": [-10],
        }
    )

    out = px.clean_publications(df)

    assert out.loc[0, "citations"] == 0


# ---------------------------------------------------------------------
# clean_keywords()
# ---------------------------------------------------------------------


def test_clean_keywords_lowercase_and_dedupe() -> None:
    df = pd.DataFrame({"author_keywords": ["AI; Machine Learning; ai ; Deep Learning"]})

    out = px.clean_keywords(df)

    assert out.loc[0, "author_keywords"] == ("ai; machine learning; deep learning")


def test_clean_keywords_multiple_separators() -> None:
    df = pd.DataFrame({"index_keywords": ["data mining, AI | analytics"]})

    out = px.clean_keywords(df)

    assert out.loc[0, "index_keywords"] == ("data mining; ai; analytics")


# ---------------------------------------------------------------------
# clean_affiliations()
# ---------------------------------------------------------------------


def test_clean_affiliations_alias_mapping() -> None:
    df = pd.DataFrame({"affiliations": ["IIT Delhi; BHU"]})

    out = px.clean_affiliations(df)

    assert "Indian Institute of Technology Delhi" in out.loc[0, "affiliations"]
    assert out.loc[0, "institution"] == ("Indian Institute of Technology Delhi")


# ---------------------------------------------------------------------
# deduplicate()
# ---------------------------------------------------------------------


def test_drop_duplicate_doi() -> None:
    df = pd.DataFrame(
        {
            "doi": ["10.1/a", "10.1/a", "10.1/b"],
            "title": ["A", "A2", "B"],
        }
    )

    out = px.drop_duplicate_doi(df)

    assert len(out) == 2


def test_drop_duplicate_title_year() -> None:
    df = pd.DataFrame(
        {
            "title": ["Paper A", "paper a", "Paper B"],
            "year": [2020, 2020, 2021],
        }
    )

    out = px.drop_duplicate_title_year(df)

    assert len(out) == 2


def test_deduplicate_pipeline() -> None:
    df = pd.DataFrame(
        {
            "title": ["Paper A", "paper a", "Paper B"],
            "year": [2020, 2020, 2021],
            "doi": [pd.NA, pd.NA, "10.1/b"],
        }
    )

    out = px.deduplicate(df)

    assert len(out) == 2
