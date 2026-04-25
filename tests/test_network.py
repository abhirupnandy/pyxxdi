from __future__ import annotations

import pandas as pd

import pyxxdi as px


def test_collaboration_network_basic() -> None:
    df = pd.DataFrame(
        {
            "authors": [
                "A; B; C",
                "A; C",
            ]
        }
    )

    out = px.collaboration_network(df)

    assert "source" in out.columns
    assert "target" in out.columns
    assert "weight" in out.columns


def test_collaboration_weight() -> None:
    df = pd.DataFrame(
        {
            "authors": [
                "A; C",
                "A; C",
            ]
        }
    )

    out = px.collaboration_network(df)

    row = out[(out["source"] == "A") & (out["target"] == "C")].iloc[0]

    assert row["weight"] == 2


def test_single_author_ignored() -> None:
    df = pd.DataFrame({"authors": ["A"]})

    out = px.collaboration_network(df)

    assert len(out) == 0
