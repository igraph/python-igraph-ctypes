from igraph_ctypes.constructors import create_empty_graph


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
