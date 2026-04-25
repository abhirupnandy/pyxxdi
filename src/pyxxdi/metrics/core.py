from __future__ import annotations

import numpy as np


def compute_h(cites: np.ndarray) -> int:
    """
    Compute h-index.

    Parameters
    ----------
    cites : np.ndarray
        Descending sorted citation counts.

    Returns
    -------
    int
        h-index.
    """
    if cites.size == 0:
        return 0

    ranks = np.arange(1, cites.size + 1)

    valid = cites >= ranks

    if not np.any(valid):
        return 0

    return int(ranks[valid].max())


def compute_g(cites: np.ndarray) -> int:
    """
    Compute g-index.

    Largest g such that top g papers have at least g² citations.
    """
    if cites.size == 0:
        return 0

    ranks = np.arange(1, cites.size + 1)

    cumulative = np.cumsum(cites)

    valid = cumulative >= (ranks**2)

    if not np.any(valid):
        return 0

    return int(ranks[valid].max())


def compute_x(cites: np.ndarray, decimals: int = 2) -> float:
    """
    Compute x-index.

    x = max(sqrt(k * c_k))
    """
    if cites.size == 0:
        return 0.0

    ranks = np.arange(1, cites.size + 1)

    scores = np.sqrt(ranks * cites)

    value = float(scores.max())

    return round(value, decimals)
