from __future__ import annotations

import pandas as pd

import pyxxdi as px


def test_read_scopus(tmp_path) -> None:
    data = pd.DataFrame(
        {
            "Title": ["Paper A"],
            "Authors": ["A; B"],
            "Year": [2020],
            "Source title": ["Nature"],
            "Cited by": [15],
            "Author Keywords": ["AI; ML"],
            "Affiliations": ["IIT Delhi; BHU"],
        }
    )

    file = tmp_path / "scopus.csv"
    data.to_csv(file, index=False)

    df = px.read_scopus(file)

    assert "title" in df.columns
    assert "citations" in df.columns
    assert df.loc[0, "citations"] == 15
    assert isinstance(df.loc[0, "author_keywords"], list)
