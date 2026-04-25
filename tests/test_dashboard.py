from __future__ import annotations

import pandas as pd

import pyxxdi as px


def test_dashboard_basic() -> None:
    df = pd.DataFrame(
        {
            "title": ["A", "B"],
            "year": [2020, 2021],
            "citations": [10, 5],
        }
    )

    out = px.researcher_dashboard(df)

    assert "overview" in out
    assert "metrics" in out
    assert "top_papers" in out
    assert "yearly_trends" in out


def test_dashboard_counts() -> None:
    df = pd.DataFrame(
        {
            "title": ["A", "B"],
            "citations": [2, 3],
        }
    )

    out = px.researcher_dashboard(df)

    assert out["overview"]["papers"] == 2
    assert out["overview"]["citations"] == 5
