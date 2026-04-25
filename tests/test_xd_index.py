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
            "category": [
                "CS",
                "Math",
                "Physics",
                "CS",
                "Bio",
                "Chem",
            ],
            "citations": [
                10,
                8,
                3,
                5,
                2,
                1,
            ],
        }
    )


def test_xd_basic():
    out = px.xd_index(sample_df())

    row = out[out["unit"] == "A"].iloc[0]

    assert row["xd_index"] == 3


def test_xd_second():
    out = px.xd_index(sample_df())

    row = out[out["unit"] == "B"].iloc[0]

    assert row["xd_index"] == 1


def test_xd_top_n():
    out = px.xd_index(sample_df(), top_n=1)

    assert len(out) == 1
