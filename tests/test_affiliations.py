from __future__ import annotations

import pandas as pd

import pyxxdi as px


def test_clean_affiliations_basic() -> None:
    df = pd.DataFrame({"institution": ["IITD; Banaras Hindu Univ."]})

    out = px.clean_affiliations(df)

    val = out.loc[0, "institution"]

    assert "Indian Institute of Technology Delhi" in val
    assert "Banaras Hindu University" in val


def test_clean_affiliations_dedupe() -> None:
    df = pd.DataFrame({"institution": ["IITD; IIT Delhi"]})

    out = px.clean_affiliations(df)

    assert out.loc[0, "institution"] == ("Indian Institute of Technology Delhi")
