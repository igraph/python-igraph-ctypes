from collections.abc import MutableMapping

from pytest import raises

from igraph_ctypes.constructors import (
    create_graph_from_edge_list,
    create_full_graph,
    create_famous_graph,
)
from igraph_ctypes.types import AttributeCombinationSpecification


def test_new_graph_has_no_edge_attributes():
    g = create_full_graph(4)
    assert isinstance(g.eattrs, MutableMapping)
    assert len(g.eattrs) == 0


def test_create_edge_attribute():
    g = create_full_graph(4)

    g.eattrs.set("name", "test")
    assert list(g.eattrs["name"]) == ["test"] * 6

    g.eattrs.set("weight", (5, 10, 15, 20, 25, 30))
    assert list(g.eattrs["weight"]) == [5, 10, 15, 20, 25, 30]

    g.eattrs.set("cost", 1)
    assert list(g.eattrs["cost"]) == [1] * 6

    with raises(RuntimeError, match="length must be"):
        g.eattrs.set("city", ("London", "Stockholm"))


def test_copying_graph_copies_edge_attributes():
    g = create_famous_graph("zachary")
    n = g.ecount()

    g.eattrs.set("index", list(range(n)))
    g.eattrs.set("name", [f"E{i}" for i in range(n)])

    g2 = g.copy()
    assert sorted(g2.eattrs.keys()) == ["index", "name"]
    assert list(g2.eattrs["index"]) == list(range(n))
    assert list(g2.eattrs["name"]) == [f"E{i}" for i in range(n)]

    del g2.eattrs["index"]
    assert "index" not in g2.eattrs
    assert list(g.eattrs["index"]) == list(range(n))


def test_adding_edges_extends_edge_attribute_vectors():
    g = create_full_graph(4)

    g.eattrs.set("name", "test")
    g.eattrs.set("age", (5, 10, 15, 20, 25, 30))

    g.add_vertices(1)
    g.add_edges([(0, 4), (2, 4), (3, 4)])
    assert list(g.eattrs["name"]) == ["test"] * 6 + [""] * 3
    assert list(g.eattrs["age"]) == [5, 10, 15, 20, 25, 30] + [0] * 3


def test_assigning_edge_attributes_between_graphs():
    g = create_full_graph(4)
    g.eattrs.set("age", (5, 10, 15, 20, 25, 30))

    g2 = create_full_graph(4)
    g2.eattrs["age"] = g.eattrs["age"]

    assert g2.eattrs["age"] == g.eattrs["age"]
    assert g2.eattrs["age"] is not g.eattrs["age"]

    g2 = create_full_graph(8)
    with raises(RuntimeError, match="length must be"):
        g2.eattrs["age"] = g.eattrs["age"]


def test_shallow_copy():
    g = create_full_graph(4)

    g.eattrs.set("name", "test")
    g.eattrs.set("age", (5, 10, 15, 20, 25, 30))

    map = g.eattrs.copy()
    assert map["name"] == g.eattrs["name"] and map["name"] is not g.eattrs["name"]
    assert map["age"] == g.eattrs["age"] and map["age"] is not g.eattrs["age"]


def test_attempt_to_change_attribute_type():
    g = create_full_graph(4)
    g.eattrs.set("age", (5, 10, 15, 20, 25, 30))

    with raises(ValueError, match="could not convert"):
        g.eattrs["age"][2] = "test"


def test_edge_attribute_combination():
    g = create_graph_from_edge_list([0, 1, 1, 2, 2, 3, 0, 1, 0, 1, 3, 2], directed=True)
    g.eattrs.set("weight", [1, 2, 3, 4, 5, 6])
    g.eattrs.set("name", [f"E{i}" for i in range(1, g.ecount() + 1)])
    g.eattrs.set("capacity", [1, 2, 3, 4, 5, 6])
    g.eattrs.set("to_remove", [6, 5, 4, 3, 2, 1])
    g.eattrs.set("should_keep", [True, True, False, True, False, False])

    combinations: AttributeCombinationSpecification = {
        "weight": "sum",
        "name": "concat",
        "capacity": "min",
        "to_remove": "ignore",
        None: "first",
    }

    g.convert_to_undirected("collapse", combinations)

    assert list(g.eattrs["should_keep"]) == [True, True, False]  # 1, 2 and 3
    assert list(g.eattrs["weight"]) == [1 + 4 + 5, 2, 3 + 6]
    assert list(g.eattrs["name"]) == ["E1E4E5", "E2", "E3E6"]
    assert list(g.eattrs["capacity"]) == [1, 2, 3]

    # TODO(ntamas): test custom function!
