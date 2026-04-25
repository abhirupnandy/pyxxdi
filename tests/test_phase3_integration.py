from __future__ import annotations

import pandas as pd

import pyxxdi as px


def test_phase3_pipeline() -> None:
    df = pd.DataFrame(
        {
            "title": ["AI Paper", "ML Paper"],
            "authors": ["A; B", "A"],
            "year": [2020, 2021],
            "citations": [10, 5],
            "institution": ["IITD", "BHU"],
            "author_keywords": ["AI", "ML"],
        }
    )

    df = px.clean_keywords(df)
    df = px.clean_affiliations(df)
    df = px.normalize_keywords(df)
    df = px.classify_subjects(df)

    assert len(df) == 2

    dash = px.researcher_dashboard(df)

    assert "overview" in dash
