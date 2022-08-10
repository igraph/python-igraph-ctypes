from pytest import raises

from igraph_ctypes._internal.enums import NeighborMode
from igraph_ctypes.constructors import create_empty_graph
from igraph_ctypes.graph import Graph


def create_ring(n: int = 5, directed: bool = False) -> Graph:
    g = create_empty_graph(n, directed=directed)
    pairs = [(i, (i + 1) % n) for i in range(n)]
    g.add_edges(pairs)
    return g


def test_create_empty_graph():
    g = create_empty_graph(10)
    assert g.vcount() == 10
    assert g.ecount() == 0
    assert not g.is_directed()


def test_add_vertices():
    g = create_empty_graph(10)
    assert g.vcount() == 10

    g.add_vertices(5)
    assert g.vcount() == 15


def test_add_edges():
    n = 5

    g = create_empty_graph(n)
    assert g.ecount() == 0

    g.add_edges((i, (i + 1) % n) for i in range(n))
    assert g.ecount() == 5


def test_edge():
    n = 5

    g = create_empty_graph(n)
    pairs = [(i, (i + 1) % n) for i in range(n)]
    g.add_edges(pairs)

    for index, pair in enumerate(pairs):
        assert sorted(pair) == sorted(g.edge(index))


def test_edge_directed():
    n = 5

    g = create_empty_graph(n, directed=True)
    pairs = [(i, (i + 1) % n) for i in range(n)]
    g.add_edges(pairs)

    for index, pair in enumerate(pairs):
        assert pair == g.edge(index)


def test_get_eid_directed():
    n = 5
    g = create_ring(n, directed=True)
    for i in range(5):
        assert g.get_edge_id(i, (i + 1) % n) == i
        assert g.get_edge_id((i + 1) % n, i, error=False) == -1
        assert g.get_edge_id((i + 1) % n, i, directed=False) == i

        # TODO(ntamas): does not work yet, error handler must be implemented
        """
        with raises(match="no such edge"):
            assert g.get_edge_id((i + 1) % n, i) == i
        """


def test_get_eid_undirected():
    n = 5
    g = create_ring(n)
    for i in range(5):
        assert g.get_edge_id(i, (i + 1) % n) == i
        assert g.get_edge_id((i + 1) % n, i) == i


def test_neighbors_undirected():
    n = 5
    g = create_ring(n)
    for i in range(n):
        assert sorted(g.neighbors(i)) == sorted(((i - 1) % n, (i + 1) % n))


def test_neighbors_directed():
    n = 5
    g = create_ring(n, directed=True)
    for i in range(n):
        assert sorted(g.neighbors(i)) == sorted(((i - 1) % n, (i + 1) % n))
        assert g.neighbors(i, mode=NeighborMode.OUT) == [(i + 1) % n]
        assert g.neighbors(i, mode=NeighborMode.IN) == [(i - 1) % n]
