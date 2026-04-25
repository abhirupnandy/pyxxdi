from __future__ import annotations

from pathlib import Path

import pandas as pd

import pyxxdi as px


def test_export_csv(tmp_path: Path) -> None:
    df = pd.DataFrame(
        {
            "title": ["A"],
            "citations": [5],
        }
    )

    file = tmp_path / "report.csv"

    px.export_report(df, file)

    assert file.exists()


def test_export_xlsx(tmp_path: Path) -> None:
    df = pd.DataFrame(
        {
            "title": ["A"],
            "year": [2020],
            "citations": [5],
        }
    )

    file = tmp_path / "report.xlsx"

    px.export_report(df, file)

    assert file.exists()
