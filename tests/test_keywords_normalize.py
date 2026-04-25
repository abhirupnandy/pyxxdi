from __future__ import annotations

import pandas as pd

import pyxxdi as px


def test_normalize_keywords_basic() -> None:
    df = pd.DataFrame({"author_keywords": ["ai; ml; nlp; covid19"]})

    out = px.normalize_keywords(df)

    vals = out.loc[0, "author_keywords"]

    assert "artificial intelligence" in vals
    assert "machine learning" in vals
    assert "natural language processing" in vals
    assert "covid-19" in vals


def test_normalize_keywords_dedupe() -> None:
    df = pd.DataFrame({"author_keywords": ["ai; artificial intelligence"]})

    out = px.normalize_keywords(df)

    assert out.loc[0, "author_keywords"] == ("artificial intelligence")
