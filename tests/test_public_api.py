import pandas as pd

import pyxxdi as px


def sample_df():
    return pd.DataFrame(
        {
            "institution": [
                "A",
                "A",
                "A",
                "B",
                "B",
                "C",
            ],
            "citations": [
                10,
                8,
                5,
                4,
                3,
                1,
            ],
        }
    )


def test_h_wrapper():
    out = px.h_index(sample_df())
    assert "h_index" in out.columns


def test_g_wrapper():
    out = px.g_index(sample_df())
    assert "g_index" in out.columns


def test_x_wrapper():
    out = px.x_index(sample_df())
    assert "x_index" in out.columns


def test_top_n():
    out = px.x_index(sample_df(), top_n=2)
    assert len(out) == 2


def test_min_records():
    out = px.x_index(sample_df(), min_records=2)
    assert "C" not in set(out["unit"])
