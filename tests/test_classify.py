from __future__ import annotations

import pandas as pd

import pyxxdi as px


def test_classify_computer_science() -> None:
    df = pd.DataFrame(
        {
            "title": ["A machine learning model"],
        }
    )

    out = px.classify_subjects(df)

    assert out.loc[0, "subject"] == "Computer Science"


def test_classify_medicine() -> None:
    df = pd.DataFrame(
        {
            "author_keywords": ["covid19; vaccine"],
        }
    )

    out = px.classify_subjects(df)

    assert out.loc[0, "subject"] == "Medicine"


def test_classify_source_rule() -> None:
    df = pd.DataFrame(
        {
            "source": ["IEEE Transactions on AI"],
        }
    )

    out = px.classify_subjects(df)

    assert out.loc[0, "subject"] == "Engineering"
