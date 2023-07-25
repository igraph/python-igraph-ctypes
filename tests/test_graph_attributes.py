from collections.abc import MutableMapping
from igraph_ctypes.constructors import create_empty_graph, create_famous_graph


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

    g2.attrs
