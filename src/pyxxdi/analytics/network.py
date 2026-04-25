from __future__ import annotations

from itertools import combinations

import pandas as pd


def _split_authors(value: object) -> list[str]:
    if pd.isna(value):
        return []

    parts = str(value).split(";")

    authors = [x.strip() for x in parts if x.strip()]

    # preserve order, remove duplicates
    seen = set()
    out = []

    for a in authors:
        if a not in seen:
            seen.add(a)
            out.append(a)

    return out


def collaboration_network(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build co-author weighted edge list.
    """
    if "authors" not in df.columns:
        raise ValueError("Column 'authors' not found.")

    edges: dict[tuple[str, str], int] = {}

    for _, row in df.iterrows():
        authors = _split_authors(row["authors"])

        if len(authors) < 2:
            continue

        for a, b in combinations(sorted(authors), 2):
            key = (a, b)
            edges[key] = edges.get(key, 0) + 1

    out = pd.DataFrame(
        [
            {
                "source": a,
                "target": b,
                "weight": w,
            }
            for (a, b), w in edges.items()
        ]
    )

    if out.empty:
        return pd.DataFrame(columns=["source", "target", "weight"])

    out = out.sort_values(
        by=["weight", "source", "target"],
        ascending=[False, True, True],
    )

    return out.reset_index(drop=True)
