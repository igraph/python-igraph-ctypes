from numpy import array
from pytest import raises

from igraph_ctypes._internal.enums import NeighborMode
from igraph_ctypes.constructors import create_empty_graph
from igraph_ctypes.errors import IgraphError
from igraph_ctypes.graph import Graph


def create_ring(n: int = 5, directed: bool = False) -> Graph:
    g = create_empty_graph(n, directed=directed)
    pairs = [(i, (i + 1) % n) for i in range(n)]
    g.add_edges(pairs)
    return g


def create_mutual_ring(n: int = 5) -> Graph:
    g = create_empty_graph(n, directed=True)
    pairs = [(i, (i + 1) % n) for i in range(n)]
    pairs += [(v, u) for u, v in pairs]
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


def test_add_edges_from_numpy_array():
    n = 5

    g = create_empty_graph(n)
    assert g.ecount() == 0

    arr = array([[i, (i + 1) % n] for i in range(n)])
    g.add_edges(arr)
    assert g.ecount() == 5


def test_delete_edges_single():
    n = 5
    g = create_empty_graph(n)
    g.add_edges((i, (i + 1) % n) for i in range(n))
    eid = g.get_edge_id(2, 3)

    g.delete_edges(eid)

    assert g.ecount() == 4
    assert g.get_edge_id(2, 3, error=False) == -1


def test_delete_edges_multiple():
    n = 5
    g = create_empty_graph(n)
    g.add_edges((i, (i + 1) % n) for i in range(n))
    assert g.get_edge_id(1, 2, error=False) >= 0
    assert g.get_edge_id(0, 4, error=False) >= 0
    g.delete_edges([1, 4])

    assert g.ecount() == 3
    assert g.get_edge_id(1, 2, error=False) == -1
    assert g.get_edge_id(0, 4, error=False) == -1


def test_delete_vertices_single():
    n = 5
    g = create_empty_graph(n)

    g.delete_vertices(3)

    assert g.vcount() == n - 1


def test_delete_vertices_multiple():
    n = 5
    g = create_empty_graph(n)

    g.delete_vertices([0, 1, 3])

    assert g.vcount() == n - 3


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

        with raises(IgraphError, match="no such edge"):
            assert g.get_edge_id((i + 1) % n, i) == i


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


def test_incident_undirected():
    n = 5
    g = create_ring(n)
    for i in range(n):
        assert sorted(g.incident(i)) == sorted((i, (i - 1) % n))


def test_incident_directed():
    n = 5
    g = create_ring(n, directed=True)
    for i in range(n):
        assert sorted(g.incident(i)) == sorted((i, (i - 1) % n))
        assert g.incident(i, mode=NeighborMode.OUT) == [i]
        assert g.incident(i, mode=NeighborMode.IN) == [(i - 1) % n]

    g = create_mutual_ring(n)
    for i in range(n):
        assert sorted(g.incident(i)) == sorted((i, (i - 1) % n, i + 5, (i - 1) % n + 5))
        assert sorted(g.incident(i, mode=NeighborMode.OUT).tolist()) == sorted(
            [i, (i - 1) % n + 5]
        )
        assert sorted(g.incident(i, mode=NeighborMode.IN).tolist()) == sorted(
            [
                i + 5,
                (i - 1) % n,
            ]
        )
