import pandas as pd

import pyxxdi as px


def sample_df():
    return pd.DataFrame(
        {
            "institution": ["A", "A", "B"],
            "category": ["CS", "Math", "Bio"],
            "citations": [10, 8, 6],
            "n_institutions": [2, 1, 3],
            "expected_citations": [5, 4, 3],
            "field_variance": [2, 2, 1],
        }
    )


def test_fractional():
    out = px.xd_fractional_index(sample_df())
    assert "xd_index" in out.columns


def test_fn():
    out = px.xd_field_normalized_index(sample_df())
    assert "xd_index" in out.columns


def test_ivw():
    out = px.xd_ivw_index(sample_df())
    assert "xd_index" in out.columns
