# pyxxdi

Modern Python package for bibliometric analytics, research evaluation, and expertise intelligence.

`pyxxdi` is the Python successor to the earlier R package `xxdi`, designed for scalable and reproducible scientometric workflows.

## Core Focus Areas

- x-index
- xd-index
- variants of x-index / xd-index
- institutional expertise analytics
- portfolio intelligence
- benchmarking
- ranking workflows
- research performance evaluation

## Why pyxxdi?

Modern research analytics needs transparent, reproducible, programmable tools.

`pyxxdi` aims to provide:

- production-grade Python APIs
- clean dataframe-based workflows
- robust metric implementations
- extensible architecture
- publication-ready outputs
- open-source reproducibility

## Installation

### Basic

```bash
pip install pyxxdi
```

## Development
```bash
uv sync --extra dev --extra docs --extra viz --extra network
```

### Quick Start
```python
import pyxxdi
```

### Future examples:
```python

from pyxxdi.metrics import x_index, xd_index
from pyxxdi.ranking import rank_entities
```

### Planned Modules

- pyxxdi.io
- pyxxdi.cleaning
- pyxxdi.classify
- pyxxdi.metrics
- pyxxdi.ranking
- pyxxdi.trends
- pyxxdi.portfolio
- pyxxdi.network
- pyxxdi.viz
- pyxxdi.report
- pyxxdi.utils

### Development Status

#### Current stage: Phase 0 — Foundation Setup

Initial public release target: 0.x alpha

### Roadmap
- Foundation package architecture
- Core metric engine
- Ranking and benchmarking toolkit
- Expertise portfolio analytics
- Visualisation layer
- Documentation site
- PyPI release
- Research paper / software citation release
- Contributing

#### Contributions, issue reports, and academic collaborations are welcome.

### Citation

A formal citation file (CITATION.cff) will be included.

### License

MIT License

### Author

Abhirup Nandy