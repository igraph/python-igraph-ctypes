from collections.abc import MutableMapping

from pytest import raises

from igraph_ctypes.constructors import create_empty_graph, create_famous_graph


def test_new_graph_has_no_vertex_attributes():
    g = create_empty_graph(5)
    assert isinstance(g.vattrs, MutableMapping)
    assert len(g.vattrs) == 0


def test_create_vertex_attribute():
    g = create_empty_graph(5)

    g.vattrs.set("name", "test")
    assert list(g.vattrs["name"]) == ["test"] * 5

    g.vattrs.set("age", (5, 10, 15, 20, 25))
    assert list(g.vattrs["age"]) == [5, 10, 15, 20, 25]

    g.vattrs.set("cost", 1)
    assert list(g.vattrs["cost"]) == [1] * 5

    with raises(RuntimeError, match="length must be"):
        g.vattrs.set("city", ("London", "Stockholm"))


def test_copying_graph_copies_vertex_attributes():
    g = create_famous_graph("zachary")
    n = g.vcount()

    g.vattrs.set("age", list(range(n)))
    g.vattrs.set("name", [f"V{i}" for i in range(n)])

    g2 = g.copy()
    assert sorted(g2.vattrs.keys()) == ["age", "name"]
    assert list(g2.vattrs["age"]) == list(range(n))
    assert list(g2.vattrs["name"]) == [f"V{i}" for i in range(n)]

    del g2.vattrs["age"]
    assert "age" not in g2.vattrs
    assert list(g.vattrs["age"]) == list(range(n))


def test_adding_vertices_extends_vertex_attribute_vectors():
    g = create_empty_graph(5)

    g.vattrs.set("name", "test")
    g.vattrs.set("age", (5, 10, 15, 20, 25))

    g.add_vertices(3)
    assert list(g.vattrs["name"]) == ["test"] * 5 + [""] * 3
    assert list(g.vattrs["age"]) == [5, 10, 15, 20, 25] + [0] * 3


def test_assigning_vertex_attributes_between_graphs():
    g = create_empty_graph(5)
    g.vattrs.set("age", (5, 10, 15, 20, 25))

    g2 = create_empty_graph(5)
    g2.vattrs["age"] = g.vattrs["age"]

    assert g2.vattrs["age"] == g.vattrs["age"]
    assert g2.vattrs["age"] is not g.vattrs["age"]

    g2 = create_empty_graph(8)
    with raises(RuntimeError, match="length must be"):
        g2.vattrs["age"] = g.vattrs["age"]


def test_shallow_copy():
    g = create_empty_graph(5)
    g.vattrs.set("name", "test")
    g.vattrs.set("age", (5, 10, 15, 20, 25))

    map = g.vattrs.copy()
    assert map["name"] == g.vattrs["name"] and map["name"] is not g.vattrs["name"]
    assert map["age"] == g.vattrs["age"] and map["age"] is not g.vattrs["age"]
