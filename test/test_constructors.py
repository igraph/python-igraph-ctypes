import pytest

from numpy import array, ndarray
from numpy.testing import assert_array_equal

from igraph_ctypes.constructors import (
    create_famous_graph,
    create_graph_from_edge_list,
    create_square_lattice,
)
from igraph_ctypes._internal.functions import get_edgelist


def test_create_famous_graph():
    g = create_famous_graph("zachary")
    assert not g.is_directed() and g.vcount() == 34 and g.ecount() == 78

    g = create_famous_graph("petersen")
    assert not g.is_directed() and g.vcount() == 10 and g.ecount() == 15


@pytest.mark.parametrize(
    ("edges", "n", "directed"),
    [
        ((), 0, False),
        ((), 5, True),
        ((1, 2, 3, 4), 6, False),
        (array([0, 1, 1, 2, 2, 3, 3, 0], dtype=int), 4, True),
        (array([[0, 1], [1, 2], [2, 3], [3, 0]], dtype=int), 5, True),
    ],
)
def test_create_graph_from_edge_list(edges, n, directed):
    g = create_graph_from_edge_list(edges, n, directed)

    assert g.is_directed() == directed
    assert g.vcount() == n

    if isinstance(edges, ndarray):
        if edges.ndim == 1:
            edges = edges.reshape(-1, 2)
    else:
        edges = [edges[i : i + 2] for i in range(0, len(edges), 2)]

    for i, edge in enumerate(edges):
        assert list(g.edge(i)) == list(edge)


def test_create_square_lattice():
    g = create_square_lattice([4, 3])

    assert not g.is_directed()
    assert g.vcount() == 12 and g.ecount() == 17
    # fmt: off
    assert_array_equal(
        get_edgelist(g._instance),
        array([0, 1, 0, 4, 1, 2, 1, 5, 2, 3, 2, 6, 3, 7,
               4, 5, 4, 8, 5, 6, 5, 9, 6, 7, 6, 10, 7, 11,
               8, 9, 9, 10, 10, 11])
    )
    # fmt: on

    g = create_square_lattice(
        [4, 3], directed=True, mutual=True, periodic=[False, True]
    )

    assert g.is_directed()
    assert g.vcount() == 12 and g.ecount() == 42
