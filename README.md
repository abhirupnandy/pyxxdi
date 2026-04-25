# pyxxdi

Modern Python package for bibliometric analytics, research evaluation, and expertise intelligence.

`pyxxdi` is the Python successor to the earlier R package **xxdi**, designed for scalable, transparent, and reproducible scientometric workflows.

---

## Overview

`pyxxdi` provides production-grade tools for evaluating research strength, thematic expertise, institutional diversity, and scholarly performance using modern Python workflows.

The package is built for:

- researchers
- universities
- policy analysts
- ranking teams
- scientometricians
- research intelligence units

---

## Core Focus Areas

- x-index
- xc-index
- xd-index
- xo-index
- xx-index
- xxd-index
- h-index
- g-index
- expertise diversity analytics
- institutional benchmarking
- ranking workflows
- portfolio intelligence
- reproducible research evaluation

---

## Why pyxxdi?

Modern research analytics requires tools that are:

- transparent
- programmable
- scalable
- auditable
- publication-ready
- open-source

`pyxxdi` aims to provide:

- clean pandas-first APIs
- robust metric implementations
- reproducible workflows
- extensible package architecture
- research-grade outputs
- modern Python tooling

---

## Installation

### Basic

```bash
pip install pyxxdi
````

### Development

```bash
uv sync --extra dev --extra docs --extra viz --extra network
```

---

## Quick Start

```python
import pyxxdi as px
import pandas as pd

df = pd.read_csv("data.csv")

px.h_index(df, unit="institution")
px.g_index(df, unit="institution")

px.x_index(df)
px.xd_index(df)
px.xo_index(df)
```

---

## Example Outputs

```python
px.xd_index(df, top_n=10)
```

| unit   | records | xd_index | rank |
| ------ | ------- | -------- | ---- |
| Inst A | 240     | 18       | 1    |
| Inst B | 221     | 16       | 2    |

---

## Available Metrics

### Traditional Citation Metrics

* `h_index()`
* `g_index()`

### Expertise Metrics

* `x_index()`
* `xc_index()`
* `xd_index()`
* `xo_index()`

### Nested / Policy Metrics

* `xx_index()`
* `xxd_index()`

### xd-index Variants

* `xd_fractional_index()`
* `xd_field_normalized_index()`
* `xd_ivw_index()`

---

## Important Methodological Note

Fractional, field-normalized, and inverse-variance-weighted variants are recommended for **xd-index**, not **x-index**.

Reason:

* `x-index` operates on fine-grained keywords
* keywords often lack stable field-wide baselines
* broad categories are more suitable for normalization

---

## Planned Modules

* `pyxxdi.io`
* `pyxxdi.cleaning`
* `pyxxdi.classify`
* `pyxxdi.metrics`
* `pyxxdi.ranking`
* `pyxxdi.trends`
* `pyxxdi.portfolio`
* `pyxxdi.network`
* `pyxxdi.viz`
* `pyxxdi.report`
* `pyxxdi.utils`

---

## Development Status

### Current Release

`v0.2.x beta`

### Status

* Core metrics implemented
* Tests passing
* Ongoing optimization
* Documentation expansion in progress

---

## Roadmap

### Phase 1

Foundation package architecture

### Phase 2

Metric engine and expertise indices

### Phase 3

Data ingestion, cleaning, classification

### Phase 4

Network analytics and collaboration intelligence

### Phase 5

Visual dashboards and reporting

### Phase 6

Research paper + software citation release

---

## Reproducibility

`pyxxdi` is built with reproducible research principles:

* versioned outputs
* deterministic calculations
* transparent formulas
* test coverage
* open-source workflows

---

## Contributing

Contributions, bug reports, feature requests, and academic collaborations are welcome.

---

## Citation

A formal `CITATION.cff` file will be included in the repository.

If using `pyxxdi` in academic work, please cite the software and related methodological publications.

---

## License

MIT License

---

## Author

**Abhirup Nandy**

---