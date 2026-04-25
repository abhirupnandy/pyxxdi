from __future__ import annotations

import pandas as pd

import pyxxdi as px


def test_compare_researchers_basic() -> None:
    a = pd.DataFrame({"citations": [10, 5]})
    b = pd.DataFrame({"citations": [20]})

    out = px.compare_researchers(
        {
            "Alice": a,
            "Bob": b,
        }
    )

    assert "researcher" in out.columns
    assert len(out) == 2


def test_compare_researchers_sort() -> None:
    a = pd.DataFrame({"citations": [1]})
    b = pd.DataFrame({"citations": [10]})

    out = px.compare_researchers(
        {
            "A": a,
            "B": b,
        }
    )

    assert out.loc[0, "researcher"] == "B"
