from __future__ import annotations

import pandas as pd

import pyxxdi as px


def test_institution_profile_basic() -> None:
    df = pd.DataFrame(
        {
            "institution": [
                "IIT Delhi",
                "IIT Delhi",
                "BHU",
            ],
            "citations": [10, 20, 5],
        }
    )

    out = px.institution_profile(df)

    assert "papers" in out.columns
    assert "citations" in out.columns
    assert len(out) == 2


def test_institution_profile_counts() -> None:
    df = pd.DataFrame(
        {
            "institution": [
                "A",
                "A",
                "B",
            ],
            "citations": [1, 2, 3],
        }
    )

    out = px.institution_profile(df)

    row = out[out["institution"] == "A"].iloc[0]

    assert row["papers"] == 2
    assert row["citations"] == 3
