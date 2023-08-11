from pathlib import Path
from pytest import fixture, raises

from igraph_ctypes.constructors import create_graph_from_edge_list
from igraph_ctypes.io import write_graph_edgelist


@fixture
def simple_graph():
    g = create_graph_from_edge_list([0, 1, 1, 2, 2, 3, 1, 3], directed=False)
    return g


def test_write_graph_edgelist(simple_graph, tmp_path):
    path: Path = tmp_path / "edges.txt"
    expected = "0 1\n1 2\n1 3\n2 3\n"
    path_str = str(path)

    # Write to a file specified by its filename
    write_graph_edgelist(simple_graph, path_str)
    assert path.read_text() == expected
    path.unlink()

    # Write to a Path object
    path: Path = tmp_path / "edges.txt"
    write_graph_edgelist(simple_graph, path)
    assert path.read_text() == expected
    path.unlink()

    # Write to an already-open file-like object
    path: Path = tmp_path / "edges.txt"
    with path.open("w") as fp:
        write_graph_edgelist(simple_graph, fp)
    assert path.read_text() == expected
    path.unlink()

    # Write to an already-open file-like object specified with its file handle
    path: Path = tmp_path / "edges.txt"
    with path.open("w") as fp:
        fd = fp.fileno()
        write_graph_edgelist(simple_graph, fd)
    assert path.read_text() == expected
    path.unlink()

    # Write to a file-like object that is open for writing, not reading
    path: Path = tmp_path / "edges.txt"
    path.write_text("dummy")
    with raises(OSError):
        with path.open("r") as fp:
            write_graph_edgelist(simple_graph, fp)
