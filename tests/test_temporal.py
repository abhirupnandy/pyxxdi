from __future__ import annotations

import pandas as pd

import pyxxdi as px


def test_temporal_trends_basic() -> None:
    df = pd.DataFrame(
        {
            "year": [2020, 2020, 2021],
            "citations": [5, 10, 20],
        }
    )

    out = px.temporal_trends(df)

    assert "papers" in out.columns
    assert len(out) == 2


def test_temporal_counts() -> None:
    df = pd.DataFrame(
        {
            "year": [2020, 2020],
            "citations": [2, 3],
        }
    )

    out = px.temporal_trends(df)

    row = out[out["year"] == 2020].iloc[0]

    assert row["papers"] == 2
    assert row["citations"] == 5


def test_temporal_cumulative() -> None:
    df = pd.DataFrame(
        {
            "year": [2020, 2021],
            "citations": [1, 2],
        }
    )

    out = px.temporal_trends(df, cumulative=True)

    assert "cum_papers" in out.columns
    assert out.loc[1, "cum_papers"] == 2
