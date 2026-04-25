from __future__ import annotations

from typing import Any

from pyxxdi.metrics.engines import metric


def h_index(*args: Any, **kwargs: Any):
    """
    Compute h-index rankings.
    """
    out = metric(*args, metric="h", **kwargs)

    if "value" in out.columns:
        out = out.rename(columns={"value": "h_index"})

    return out
