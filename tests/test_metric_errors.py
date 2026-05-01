import pandas as pd
import pytest

from pyxxdi.metrics.validators import (
    validate_citations_column,
    validate_dataframe,
    validate_metric_name,
    validate_unit_column,
)


def test_validate_dataframe_type():
    with pytest.raises(TypeError):
        validate_dataframe([1, 2, 3])


def test_validate_dataframe_empty():
    validate_dataframe(pd.DataFrame())


def test_missing_citations():
    df = pd.DataFrame({"x": [1]})

    with pytest.raises(ValueError):
        validate_citations_column(df, "citations")


def test_missing_unit():
    df = pd.DataFrame({"citations": [1]})

    with pytest.raises(ValueError):
        validate_unit_column(df, "institution")


def test_invalid_metric():
    with pytest.raises(ValueError):
        validate_metric_name("bad")


def test_valid_inputs():
    df = pd.DataFrame(
        {
            "institution": ["A"],
            "citations": [5],
        }
    )

    validate_dataframe(df)
    validate_citations_column(df, "citations")
    validate_unit_column(df, "institution")
    validate_metric_name("x")
