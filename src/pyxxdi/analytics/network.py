from __future__ import annotations

from itertools import combinations

import pandas as pd

# ---------------------------------------------------------------------
# Author collaboration network
# ---------------------------------------------------------------------


def _split_authors(value: object) -> list[str]:
    if pd.isna(value):
        return []

    parts = str(value).split(";")
    authors = [x.strip() for x in parts if x.strip()]

    seen: set[str] = set()
    output: list[str] = []
    for author in authors:
        if author not in seen:
            seen.add(author)
            output.append(author)

    return output


def collaboration_network(df: pd.DataFrame) -> pd.DataFrame:
    """Build co-author weighted edge list from semicolon-separated `authors`."""
    if "authors" not in df.columns:
        raise ValueError("Column 'authors' not found.")

    edges: dict[tuple[str, str], int] = {}

    for authors in df["authors"]:
        names = _split_authors(authors)

        if len(names) < 2:
            continue

        for source, target in combinations(sorted(names), 2):
            key = (source, target)
            edges[key] = edges.get(key, 0) + 1

    if not edges:
        return pd.DataFrame(columns=["source", "target", "weight"])

    out = pd.DataFrame(
        [{"source": a, "target": b, "weight": w} for (a, b), w in edges.items()]
    )

    return out.sort_values(
        by=["weight", "source", "target"],
        ascending=[False, True, True],
    ).reset_index(drop=True)


# ---------------------------------------------------------------------
# Institution-keyword bipartite network
# ---------------------------------------------------------------------


def _split_terms(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]

    if pd.isna(value):
        return []

    text = str(value)
    separators = [";", "|", ","]
    for sep in separators[1:]:
        text = text.replace(sep, separators[0])

    return [x.strip() for x in text.split(separators[0]) if x.strip()]


def institution_keyword_network(
    df: pd.DataFrame,
    *,
    institution_col: str = "institution",
    keyword_col: str = "author_keywords",
    weight_col: str = "citations",
) -> pd.DataFrame:
    """Build institution-keyword weighted links using vectorized pandas operations.

    Weight defaults to citations but can be any numeric column (e.g., altmetrics).
    """
    missing = [
        col
        for col in (institution_col, keyword_col)
        if col not in df.columns
    ]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    work = df[[institution_col, keyword_col]].copy()

    if weight_col in df.columns:
        work["edge_weight"] = pd.to_numeric(df[weight_col], errors="coerce").fillna(0.0)
    else:
        work["edge_weight"] = 1.0

    work = work.rename(
        columns={institution_col: "source", keyword_col: "keyword_value"}
    )

    work = work.assign(target=work["keyword_value"].map(_split_terms)).explode("target")

    work["source"] = work["source"].astype("string").str.strip()
    work["target"] = work["target"].astype("string").str.strip().str.lower()

    work = work.drop(columns=["keyword_value"])
    work = work.dropna(subset=["source", "target"])
    work = work[(work["source"] != "") & (work["target"] != "")]

    if work.empty:
        return pd.DataFrame(columns=["source", "target", "weight"])

    out = (
        work.groupby(["source", "target"], as_index=False, dropna=False)["edge_weight"]
        .sum()
        .rename(columns={"edge_weight": "weight"})
        .sort_values(by=["weight", "source", "target"], ascending=[False, True, True])
        .reset_index(drop=True)
    )

    return out
