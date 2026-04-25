import numpy as np

from pyxxdi.metrics.profile import prepare_citations


def test_prepare_basic():
    arr = prepare_citations([5, 2, 10])
    assert np.array_equal(arr, np.array([10.0, 5.0, 2.0]))


def test_prepare_negative_clipped():
    arr = prepare_citations([5, -2, 1])
    assert np.array_equal(arr, np.array([5.0, 1.0, 0.0]))


def test_prepare_missing_values():
    arr = prepare_citations([5, None, "x", 3])
    assert np.array_equal(arr, np.array([5.0, 3.0, 0.0, 0.0]))


def test_prepare_empty():
    arr = prepare_citations([])
    assert arr.size == 0


def test_prepare_strings():
    arr = prepare_citations(["8", "2", "bad"])
    assert np.array_equal(arr, np.array([8.0, 2.0, 0.0]))
