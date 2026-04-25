import pandas as pd

from pyxxdi.metrics.engines import metric


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


def test_metric_x():
    df = sample_df()

    out = metric(df, metric="x", unit="institution")

    assert list(out["unit"]) == ["A", "B", "C"]
    assert "rank" in out.columns


def test_metric_h():
    df = sample_df()

    out = metric(df, metric="h", unit="institution")

    assert out.iloc[0]["unit"] == "A"


def test_metric_g():
    df = sample_df()

    out = metric(df, metric="g", unit="institution")

    assert len(out) == 3


def test_metric_no_sort():
    df = sample_df()

    out = metric(
        df,
        metric="x",
        unit="institution",
        sort=False,
    )

    assert len(out) == 3
