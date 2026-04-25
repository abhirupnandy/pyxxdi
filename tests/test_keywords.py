from __future__ import annotations

import pandas as pd

import pyxxdi as px


def test_clean_keywords_basic() -> None:
    df = pd.DataFrame({"author_keywords": ["AI; ML; ai; Deep-Learning; covid19"]})

    out = px.clean_keywords(df)

    assert out.loc[0, "author_keywords"] == ("ai; ml; deep learning; covid19")


def test_keywords_all_created() -> None:
    df = pd.DataFrame(
        {
            "author_keywords": ["AI"],
            "index_keywords": ["ML"],
        }
    )

    out = px.clean_keywords(df)

    assert "keywords_all" in out.columns
