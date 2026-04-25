import pandas as pd

import pyxxdi as px


def sample_df():
    return pd.DataFrame(
        {
            "institution": [
                "A",
                "A",
                "A",
                "A",
                "B",
                "B",
            ],
            "keyword": [
                "AI",
                "AI",
                "NLP",
                "ML",
                "Stats",
                "Math",
            ],
            "citations": [
                10,
                5,
                8,
                3,
                2,
                1,
            ],
        }
    )


def test_x_index_basic():
    out = px.x_index(sample_df())

    row = out[out["unit"] == "A"].iloc[0]

    assert row["x_index"] == 3


def test_x_index_second_unit():
    out = px.x_index(sample_df())

    row = out[out["unit"] == "B"].iloc[0]

    assert row["x_index"] == 1


def test_x_top_n():
    out = px.x_index(sample_df(), top_n=1)

    assert len(out) == 1
