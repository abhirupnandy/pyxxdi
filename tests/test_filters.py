import pandas as pd

import pyxxdi as px


def sample_df():
    return pd.DataFrame(
        {
            "institution": ["A", "A", "B", "B"],
            "citations": [10, 5, 8, 3],
            "year": [2020, 2023, 2021, 2024],
            "subject": [
                "CS",
                "Physics",
                "CS",
                "Math",
            ],
            "document_type": [
                "Article",
                "Review",
                "Article",
                "Conference",
            ],
        }
    )


def test_year_filter():
    out = px.x_index(sample_df(), year_from=2023)
    assert set(out["unit"]) == {"A", "B"}


def test_subject_filter():
    out = px.h_index(sample_df(), subject="CS")
    assert set(out["unit"]) == {"A", "B"}


def test_doc_type_filter():
    out = px.g_index(
        sample_df(),
        document_type="Review",
    )
    assert set(out["unit"]) == {"A"}


def test_year_range():
    out = px.x_index(
        sample_df(),
        year_from=2021,
        year_to=2023,
    )
    assert set(out["unit"]) == {"A", "B"}
