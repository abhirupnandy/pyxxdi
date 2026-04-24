import pyxxdi


def test_import():
    assert pyxxdi is not None


def test_version_exists():
    assert hasattr(pyxxdi, "__version__")


def test_version_is_string():
    assert isinstance(pyxxdi.__version__, str)
