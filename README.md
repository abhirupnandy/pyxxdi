# pyxxdi

[![PyPI version](https://img.shields.io/pypi/v/pyxxdi.svg)](https://pypi.org/project/pyxxdi/)

`pyxxdi` is a Python package for bibliometric analytics, scientometric metrics, and research intelligence workflows.

## Install

```bash
pip install pyxxdi
```

## Quickstart

```python
import pandas as pd
import pyxxdi as px

# Global metric mode (unit omitted / missing)
df = pd.DataFrame({"citations": [10, 8, 5, 4, 3]})
px.h_index(df)

# Grouped metric mode
df2 = pd.DataFrame({
    "institution": ["A", "A", "B"],
    "citations": [5, 3, 7],
})
px.h_index(df2, unit="institution")
```

## Main capabilities

- Metrics: `h_index`, `g_index`, `x_index`, `xd_index`, `xc_index`, `xx_index`, `xxd_index`
- Cleaning: keyword normalization, affiliation normalization, publication deduplication
- Parsing: Scopus, OpenAlex, CSV, Excel
- Analytics: author/institution profiles, collaboration network, temporal trends, dashboard summary
- Export: CSV/Excel analytics report output

## Typical workflow

```python
import pyxxdi as px

raw = px.read_scopus("scopus_export.csv")
clean = px.clean_keywords(px.clean_affiliations(raw))
rank = px.xd_index(clean, unit="institution", category="subject")
dash = px.researcher_dashboard(clean)
px.institution_keyword_network(clean, keyword_col="author_keywords")
px.export_report(clean, "report.xlsx")
```

## Citation

If you use `pyxxdi` in research outputs, please cite the software release and associated methodological references.

## License

MIT
