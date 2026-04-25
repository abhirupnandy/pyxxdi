"""Citation profile utilities."""

from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pandas as pd


def prepare_citations(values: Iterable[object]) -> np.ndarray:
    """
    Prepare a ranked citation profile.

    Parameters
    ----------
    values :
        Iterable of citation values.

    Returns
    -------
    numpy.ndarray
        1D float array sorted descending.

    Notes
    -----
    Rules:
    - non-numeric values become 0
    - missing values become 0
    - negative values clipped to 0
    - sorted descending
    """
    series = pd.Series(values, copy=False)

    numeric = pd.to_numeric(series, errors="coerce").fillna(0)

    arr = numeric.to_numpy(dtype=float)

    arr = np.clip(arr, a_min=0, a_max=None)

    if arr.size == 0:
        return np.array([], dtype=float)

    arr.sort()
    arr = arr[::-1]

    return arr
