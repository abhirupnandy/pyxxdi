from pyxxdi.metrics.core import compute_g, compute_h, compute_x
from pyxxdi.metrics.profile import prepare_citations


def test_h_index():
    cites = prepare_citations([10, 8, 5, 4, 3])
    assert compute_h(cites) == 4


def test_h_empty():
    cites = prepare_citations([])
    assert compute_h(cites) == 0


def test_g_index():
    cites = prepare_citations([10, 8, 5, 4, 3])
    assert compute_g(cites) == 5


def test_g_empty():
    cites = prepare_citations([])
    assert compute_g(cites) == 0


def test_x_index():
    cites = prepare_citations([10, 8, 5, 4, 3])
    assert compute_x(cites) == 4.0


def test_x_empty():
    cites = prepare_citations([])
    assert compute_x(cites) == 0.0


def test_low_values():
    cites = prepare_citations([1, 0, 0])
    assert compute_h(cites) == 1
    assert compute_g(cites) == 1
