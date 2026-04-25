from __future__ import annotations

from typing import Any

from pyxxdi.metrics.engines import metric


def g_index(*args: Any, **kwargs: Any):
    """
    Compute g-index rankings.
    """
    out = metric(*args, metric="g", **kwargs)

    if "value" in out.columns:
        out = out.rename(columns={"value": "g_index"})

    return out
