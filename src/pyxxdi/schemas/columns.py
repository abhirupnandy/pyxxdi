from __future__ import annotations

# ==========================================================
# Core canonical schema for pyxxdi
# ==========================================================

MANDATORY_COLUMNS: list[str] = [
    "record_id",
    "title",
    "year",
    "source",
    "citations",
]

RECOMMENDED_COLUMNS: list[str] = [
    "authors",
    "author_count",
    "doi",
    "institution",
    "country",
    "author_keywords",
    "index_keywords",
    "subject",
    "document_type",
]

OPTIONAL_COLUMNS: list[str] = [
    "institutions",
    "countries",
    "city",
    "keywords_all",
    "subjects",
    "asjc_code",
    "isbn",
    "issn",
    "eid",
    "wos_id",
    "openalex_id",
    "citations_per_year",
    "age_years",
    "is_recent",
    "is_open_access",
    "data_source",
    "raw_source_format",
    "imported_at",
    "raw_row_hash",
]

ALL_COLUMNS: list[str] = MANDATORY_COLUMNS + RECOMMENDED_COLUMNS + OPTIONAL_COLUMNS

# ==========================================================
# Common legacy aliases for backward compatibility
# ==========================================================

ALIASES: dict[str, str] = {
    "Title": "title",
    "TITLE": "title",
    "Publication Year": "year",
    "Year": "year",
    "PY": "year",
    "Source title": "source",
    "Journal": "source",
    "SO": "source",
    "Cited by": "citations",
    "Citations": "citations",
    "TC": "citations",
    "Authors": "authors",
    "AU": "authors",
    "DOI": "doi",
    "Affiliations": "institution",
    "Author Keywords": "author_keywords",
    "Index Keywords": "index_keywords",
    "Document Type": "document_type",
}
