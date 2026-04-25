import pandas as pd

import pyxxdi as px


def sample():
    return pd.DataFrame(
        {
            "country": ["IN", "IN", "US"],
            "institution": ["A", "A", "B"],
            "category": ["CS", "Math", "Bio"],
            "keyword": ["AI", "Stats", "Gene"],
            "citations": [10, 8, 7],
        }
    )


def test_xc():
    assert not px.xc_index(sample()).empty


def test_xo():
    assert not px.xo_index(sample()).empty


def test_xx():
    assert not px.xx_index(sample()).empty


def test_xxd():
    assert not px.xxd_index(sample()).empty
