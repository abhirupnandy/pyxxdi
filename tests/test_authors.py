from __future__ import annotations

import pandas as pd

import pyxxdi as px


def test_author_profile_basic() -> None:
    df = pd.DataFrame(
        {
            "authors": [
                "A; B",
                "A",
            ],
            "citations": [10, 5],
        }
    )

    out = px.author_profile(df)

    assert "author" in out.columns
    assert len(out) == 2


def test_author_profile_counts() -> None:
    df = pd.DataFrame(
        {
            "authors": [
                "A; B",
                "A",
            ],
            "citations": [10, 5],
        }
    )

    out = px.author_profile(df)

    row = out[out["author"] == "A"].iloc[0]

    assert row["papers"] == 2
    assert row["citations"] == 15


def test_author_profile_fractional() -> None:
    df = pd.DataFrame(
        {
            "authors": ["A; B"],
            "citations": [10],
        }
    )

    out = px.author_profile(df, fractional=True)

    row = out[out["author"] == "A"].iloc[0]

    assert row["papers"] == 0.5
