"""
Cleaning utilities for pyxxdi.
"""

from pyxxdi.cleaning.affiliations import clean_affiliations
from pyxxdi.cleaning.deduplicate import (
    deduplicate,
    drop_duplicate_doi,
    drop_duplicate_title_year,
)
from pyxxdi.cleaning.keywords import clean_keywords
from pyxxdi.cleaning.publications import clean_publications

__all__ = [
    "clean_publications",
    "deduplicate",
    "drop_duplicate_doi",
    "drop_duplicate_title_year",
    "clean_affiliations",
    "clean_keywords",
]
