"""Backward-compatible affiliation cleaning entrypoints."""

from __future__ import annotations

from pyxxdi.affiliations.clean import ALIASES as DEFAULT_AFFILIATION_ALIASES
from pyxxdi.affiliations.clean import clean_affiliations

__all__ = ["clean_affiliations", "DEFAULT_AFFILIATION_ALIASES"]
