"""
Tests for pyxxdi IO layer.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

import pyxxdi as px

# ---------------------------------------------------------------------
# Generic CSV
# ---------------------------------------------------------------------


def test_read_csv(tmp_path: Path) -> None:
    file = tmp_path / "sample.csv"

    pd.DataFrame(
        {
            "title": ["Paper A"],
            "authors": ["Smith"],
            "year": [2020],
        }
    ).to_csv(file, index=False)

    df = px.read_csv(file)

    assert len(df) == 1
    assert "title" in df.columns
    assert "doi" in df.columns  # canonical appended


# ---------------------------------------------------------------------
# Excel
# ---------------------------------------------------------------------


def test_read_excel(tmp_path: Path) -> None:
    file = tmp_path / "sample.xlsx"

    pd.DataFrame(
        {
            "title": ["Paper A"],
            "authors": ["Smith"],
            "year": [2020],
        }
    ).to_excel(file, index=False)

    df = px.read_excel(file)

    assert len(df) == 1
    assert "title" in df.columns


# ---------------------------------------------------------------------
# Scopus
# ---------------------------------------------------------------------


def test_read_scopus(tmp_path: Path) -> None:
    file = tmp_path / "scopus.csv"

    pd.DataFrame(
        {
            "Title": ["Paper A"],
            "Authors": ["Smith"],
            "Year": [2020],
            "DOI": ["10.1/a"],
            "Cited by": [5],
        }
    ).to_csv(file, index=False)

    df = px.read_scopus(file)

    assert "title" in df.columns
    assert "authors" in df.columns
    assert "doi" in df.columns
    assert df.loc[0, "source_db"] == "scopus"


# ---------------------------------------------------------------------
# WoS
# ---------------------------------------------------------------------


def test_read_wos(tmp_path: Path) -> None:
    file = tmp_path / "wos.txt"

    pd.DataFrame(
        {
            "TI": ["Paper A"],
            "AU": ["Smith"],
            "PY": [2020],
            "DI": ["10.1/a"],
            "TC": [7],
        }
    ).to_csv(file, sep="\t", index=False)

    df = px.read_wos(file)

    assert "title" in df.columns
    assert "authors" in df.columns
    assert df.loc[0, "source_db"] == "wos"


# ---------------------------------------------------------------------
# OpenAlex CSV
# ---------------------------------------------------------------------


def test_read_openalex_csv(tmp_path: Path) -> None:
    file = tmp_path / "openalex.csv"

    pd.DataFrame(
        {
            "title": ["Paper A"],
            "year": [2020],
        }
    ).to_csv(file, index=False)

    df = px.read_openalex(file)

    assert len(df) == 1
    assert df.loc[0, "source_db"] == "openalex"
