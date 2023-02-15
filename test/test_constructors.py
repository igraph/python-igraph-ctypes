import pytest

from numpy import array, ndarray

from igraph_ctypes.constructors import create_famous_graph, create_graph_from_edge_list


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
