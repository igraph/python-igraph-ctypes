from collections.abc import MutableMapping
from igraph_ctypes.constructors import (
    create_empty_graph,
    create_famous_graph,
    create_full_graph,
)


def test_attribute_mapping_basic_operations():
    g = create_empty_graph(5)
    assert isinstance(g.attrs, MutableMapping)
    assert len(g.attrs) == 0

    g.attrs["name"] = "Empty graph with 5 vertices"
    g.attrs["age"] = 42

    assert sorted(g.attrs.keys()) == ["age", "name"]
    assert g.attrs["age"] == 42
    assert g.attrs["name"] == "Empty graph with 5 vertices"

    g.attrs["age"] = 21
    assert g.attrs["age"] + 21 == 42

    del g.attrs["name"]
    assert "name" not in g.attrs

    assert list(g.attrs.items()) == [("age", 21)]


def test_copying_graph_copies_attributes():
    g = create_famous_graph("zachary")
    g.attrs["name"] = "Zachary karate club graph"
    g.attrs["age"] = 42

    g2 = g.copy()

    assert sorted(g2.attrs.keys()) == ["age", "name"]
    assert g2.attrs["age"] == 42
    assert g2.attrs["name"] == "Zachary karate club graph"

    del g2.attrs["age"]
    assert "age" not in g2.attrs
    assert g.attrs["age"] == 42


def test_deleting_edges_updates_edge_attributes():
    g = create_full_graph(6)
    weights = [i + 10 for i in range(g.ecount())]
    g.eattrs.set("weight", weights)

    assert list(g.eattrs["weight"]) == weights
    g.delete_edges([6, 4, 11])
    assert list(g.eattrs["weight"]) == [10, 11, 12, 13, 15, 17, 18, 19, 20, 22, 23, 24]


def test_deleting_vertices_updates_vertex_and_edge_attributes():
    g = create_full_graph(5)
    g.vattrs.set("name", list("ABCDE"))
    weights = [i + 10 for i in range(g.ecount())]
    g.eattrs.set("weight", weights)

    assert list(g.vattrs["name"]) == ["A", "B", "C", "D", "E"]
    g.delete_vertices([0, 3])
    assert list(g.eattrs["weight"]) == [14, 16, 18]
