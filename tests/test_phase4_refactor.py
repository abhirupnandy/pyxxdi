from __future__ import annotations

import pandas as pd
import pytest

import pyxxdi as px


def test_metric_global_mode_without_unit_column() -> None:
    df = pd.DataFrame({"citations": [10, 8, 5, 4, 3]})
    out = px.h_index(df)
    assert len(out) == 1
    assert out.loc[0, "unit"] == "all"
    assert out.loc[0, "h_index"] == 4


def test_metric_grouped_mode_with_unit() -> None:
    df = pd.DataFrame(
        {
            "institution": ["A", "A", "B"],
            "citations": [5, 3, 7],
        }
    )
    out = px.h_index(df, unit="institution")
    assert set(out["unit"]) == {"A", "B"}


def test_metric_empty_dataframe_behaviour() -> None:
    df = pd.DataFrame(columns=["citations"])
    out = px.h_index(df)
    assert out.empty
    assert list(out.columns) == ["unit", "records", "h_index", "rank"]


def test_metric_missing_citations_column_error() -> None:
    with pytest.raises(ValueError, match="citations column"):
        px.h_index(pd.DataFrame({"institution": ["A"]}))


def test_metric_handles_nan_citations() -> None:
    df = pd.DataFrame({"citations": [10, None, 5]})
    out = px.h_index(df)
    assert out.loc[0, "h_index"] == 2


def test_keyword_cleaning_edge_cases() -> None:
    df = pd.DataFrame(
        {
            "author_keywords": [" AI ; ML|ai, Deep-Learning ", None],
            "index_keywords": ["NLP; ML", ""],
        }
    )
    out = px.clean_keywords(df)
    assert out.loc[0, "author_keywords"] == "ai; ml; deep learning"
    assert out.loc[0, "keywords_all"] == "ai; ml; deep learning; nlp"


def test_affiliation_normalization() -> None:
    df = pd.DataFrame({"institution": ["IITD; banaras hindu univ"]})
    out = px.clean_affiliations(df)
    assert out.loc[0, "institution"] == (
        "Indian Institute of Technology Delhi; Banaras Hindu University"
    )


def test_parser_smoke_csv(tmp_path) -> None:
    path = tmp_path / "sample.csv"
    pd.DataFrame({"citations": [1, 2]}).to_csv(path, index=False)
    out = px.read_csv(path)
    assert len(out) == 2
    assert "citations" in out.columns


def test_end_to_end_smoke_workflow(tmp_path) -> None:
    path = tmp_path / "raw.csv"
    export_path = tmp_path / "report.csv"

    pd.DataFrame(
        {
            "Title": ["Paper 1", "Paper 2"],
            "Year": [2024, 2025],
            "Cited by": [10, 5],
            "Affiliations": ["IITD; BHU", "IIT Delhi"],
            "Author Keywords": ["AI; ML", "NLP"],
            "Index Keywords": ["DL", "AI"],
            "Document Type": ["Article", "Article"],
        }
    ).to_csv(path, index=False)

    read_df = px.read_scopus(path)
    clean_df = px.clean_keywords(px.clean_affiliations(read_df))
    metric_df = px.h_index(clean_df)
    dashboard = px.researcher_dashboard(clean_df)
    output = px.export_report(clean_df, str(export_path))

    assert not metric_df.empty
    assert "overview" in dashboard
    assert output.endswith("report.csv")
