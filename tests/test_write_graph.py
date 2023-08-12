from pathlib import Path
from pytest import fixture, raises

from igraph_ctypes.constructors import create_graph_from_edge_list
from igraph_ctypes.io import write_graph_edgelist, write_graph_graphml


@fixture
def simple_graph():
    g = create_graph_from_edge_list([0, 1, 1, 2, 2, 3, 1, 3], directed=False)
    return g


@fixture
def graph_with_attributes():
    g = create_graph_from_edge_list(
        [0, 1, 0, 2, 2, 3, 3, 4, 4, 2, 2, 5, 5, 0, 6, 3, 5, 6], directed=False
    )

    g.attrs["date"] = "2009-01-10"

    g.vattrs.set(
        "name", ["Alice", "Bob", "Claire", "Dennis", "Esther", "Frank", "George"]
    )
    g.vattrs.set("age", [25, 31, 18, 47, 22, 23, 50])
    g.vattrs.set("gender", ["f", "m", "f", "m", "f", "m", "m"])

    g.eattrs.set(
        "is_formal", [False, False, True, True, True, False, True, False, False]
    )

    return g


def test_write_graph_edgelist(simple_graph, tmp_path, datadir):
    path: Path = tmp_path / "edges.txt"
    expected = (datadir / "simple_graph.txt").read_text()
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


def test_write_graph_graphml(simple_graph, tmp_path, datadir):
    path: Path = tmp_path / "edges.graphml"
    expected = (datadir / "simple_graph.graphml").read_text()
    path_str = str(path)

    # Write to a file specified by its filename
    write_graph_graphml(simple_graph, path_str)
    assert path.read_text() == expected
    path.unlink()


def test_write_graph_graphml_attributes(graph_with_attributes, tmp_path, datadir):
    path: Path = tmp_path / "edges.graphml"
    expected = (datadir / "graph_with_attributes.graphml").read_text()
    path_str = str(path)

    # Write to a file specified by its filename
    write_graph_graphml(graph_with_attributes, path_str)
    write_graph_graphml(graph_with_attributes, "/tmp/expected.graphml")
    assert path.read_text() == expected
    path.unlink()
