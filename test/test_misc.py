from igraph_ctypes._internal.functions import strerror, version


def test_strerror():
    assert strerror(0) == "No error"
    assert strerror(1) == "Failed"
    assert strerror(9) == "Invalid mode"


def test_version():
    version_str, major, minor, patch = version()
    assert major >= 0 and major <= 255
    assert minor >= (10 if major == 0 else 0) and minor <= 255
    assert patch >= 0 and patch <= 255
    assert version_str.startswith(f"{major}.{minor}.{patch}")
