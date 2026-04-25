from __future__ import annotations

import pandas as pd


def _split_authors(value: object) -> list[str]:
    if pd.isna(value):
        return []

    parts = str(value).split(";")

    return [x.strip() for x in parts if x.strip()]


def author_profile(
    df: pd.DataFrame,
    *,
    fractional: bool = False,
    sort_by: str = "papers",
    ascending: bool = False,
) -> pd.DataFrame:
    """
    Aggregate publication metrics by author.

    fractional=True:
        each paper contributes 1/n authors.
    """
    if "authors" not in df.columns:
        raise ValueError("Column 'authors' not found.")

    rows = []

    for _, row in df.iterrows():
        authors = _split_authors(row["authors"])

        if not authors:
            continue

        n = len(authors)
        weight = 1 / n if fractional else 1

        cites = row["citations"] if "citations" in row else 0

        for author in authors:
            rows.append(
                {
                    "author": author,
                    "papers": weight,
                    "citations": cites * weight,
                    "raw_papers": 1,
                    "raw_citations": cites,
                }
            )

    out = pd.DataFrame(rows)

    if out.empty:
        return pd.DataFrame(
            columns=[
                "author",
                "papers",
                "citations",
                "avg_citations",
                "max_citations",
            ]
        )

    grouped = (
        out.groupby("author")
        .agg(
            papers=("papers", "sum"),
            citations=("citations", "sum"),
            avg_citations=("raw_citations", "mean"),
            max_citations=("raw_citations", "max"),
        )
        .reset_index()
    )

    grouped["papers"] = grouped["papers"].round(3)
    grouped["citations"] = grouped["citations"].round(3)
    grouped["avg_citations"] = grouped["avg_citations"].round(2)

    if sort_by in grouped.columns:
        grouped = grouped.sort_values(
            by=sort_by,
            ascending=ascending,
        )

    return grouped.reset_index(drop=True)
