import gc

from ctypes import c_void_p, sizeof

import numpy as np
import pytest

from igraph_ctypes.graph import Graph
from igraph_ctypes.types import SIRSimulation
from igraph_ctypes._internal.conversion import (
    igraph_strvector_t_to_list,
    iterable_of_graphs_to_igraph_vector_ptr_t,
    iterable_of_strings_to_igraph_strvector_t,
)
from igraph_ctypes._internal.functions import (
    create,
    decompose,
    disjoint_union_many,
    ecount,
    full,
    hsbm_list_game,
    intersection_many,
    layout_merge_dla,
    layout_sugiyama,
    neighborhood_graphs,
    read_graph_dimacs_flow,
    ring,
    sir,
    star,
    subisomorphic_lad,
    union_many,
    vcount,
)
from igraph_ctypes._internal.types import igraph_vector_ptr_t


def test_vector_ptr_struct_matches_c_layout():
    # stor_begin, stor_end, end and item_destructor
    assert sizeof(igraph_vector_ptr_t) == 4 * sizeof(c_void_p)


def test_graph_list_output():
    g = disjoint_union_many([ring(3, False, False, True), ring(4, False, False, True)])
    components = decompose(g)

    assert all(isinstance(c, Graph) for c in components)
    assert [(vcount(c), ecount(c)) for c in components] == [(3, 3), (4, 4)]

    # The graphs must be owned by Python and must survive the destruction of
    # the graph list they came from
    del g
    gc.collect()
    assert [vcount(c) for c in components] == [3, 4]


def test_graph_list_output_neighborhoods():
    graphs = neighborhood_graphs(ring(5, False, False, True), "all", 1)
    assert [vcount(g) for g in graphs] == [3] * 5


def test_graph_ptr_list_input():
    g = disjoint_union_many([ring(3, False, False, True), ring(4, False, False, True)])
    assert (vcount(g), ecount(g)) == (7, 7)

    # Graphs created on the fly by a generator must be kept alive during the
    # call
    g = disjoint_union_many(ring(n, False, False, True) for n in (3, 4, 5))
    assert (vcount(g), ecount(g)) == (12, 12)

    assert vcount(disjoint_union_many([])) == 0


def test_graph_ptr_list_keeps_graphs_alive():
    graphs = iterable_of_graphs_to_igraph_vector_ptr_t(
        ring(n, False, False, True) for n in (3, 4)
    )
    gc.collect()
    assert [vcount(g) for g in graphs._keepalive] == [3, 4]


def test_graph_ptr_list_rejects_non_graphs():
    with pytest.raises(TypeError, match="expected a Graph"):
        disjoint_union_many([ring(3, False, False, True), 42])  # type: ignore


def test_vector_int_list_output():
    triangle = ring(3, False, False, True)
    star3 = star(3, "undirected", 0)

    g, edge_maps = union_many([triangle, star3])
    assert ecount(g) == 3
    assert [m.tolist() for m in edge_maps] == [[2, 0, 1], [2, 1]]

    g, edge_maps = intersection_many([triangle, star3])
    assert ecount(g) == 2
    assert [m.tolist() for m in edge_maps] == [[1, -1, 0], [1, 0]]


def test_vector_int_list_input_and_output():
    # Map a triangle into a complete graph on 4 vertices, with the first
    # pattern vertex restricted to target vertices 0 and 1
    domains = [[0, 1], [0, 1, 2, 3], [0, 1, 2, 3]]
    found, mapping, maps = subisomorphic_lad(
        ring(3, False, False, True), full(4, False, False), False, domains
    )
    assert found
    assert mapping[0] in (0, 1)
    assert len(maps) == 12
    assert all(m[0] in (0, 1) and len(set(m.tolist())) == 3 for m in maps)


def test_vector_list_and_matrix_list_input():
    # Two top-level blocks of 4 vertices, each consisting of two cliques of
    # size 2 without edges between them
    g = hsbm_list_game(
        8,
        [4, 4],
        [[0.5, 0.5], [0.5, 0.5]],
        [np.eye(2), [[1, 0], [0, 1]]],
        0.0,
    )
    assert (vcount(g), ecount(g)) == (8, 4)


def test_graph_ptr_list_and_matrix_list_input():
    layout = layout_merge_dla(
        [ring(3, False, False, True), ring(2, False, False, False)],
        [[[0, 0], [1, 0], [0, 1]], np.array([[0, 0], [1, 1]])],
    )
    assert layout.shape == (5, 2)


def test_matrix_list_output():
    # 0 -> 1 -> 2 and 0 -> 2; the long edge needs a dummy vertex in layer 1
    g = create([0, 1, 1, 2, 0, 2], 3, True)
    layout, routing = layout_sugiyama(g)

    assert layout.shape == (3, 2)
    assert len(routing) == ecount(g)
    assert [r.shape for r in routing] == [(0, 2), (0, 2), (1, 2)]
    assert routing[2][0, 1] == 1


def test_strvector_conversion():
    strings = ["alpha", "", "árvíztűrő tükörfúrógép"]
    converted = iterable_of_strings_to_igraph_strvector_t(strings)
    assert igraph_strvector_t_to_list(converted) == strings

    converted = iterable_of_strings_to_igraph_strvector_t(s for s in "abc")
    assert igraph_strvector_t_to_list(converted) == ["a", "b", "c"]


def test_strvector_rejects_single_string():
    with pytest.raises(TypeError, match="single string"):
        iterable_of_strings_to_igraph_strvector_t("abc")


def test_strvector_output(tmp_path):
    path = tmp_path / "flow.dimacs"
    path.write_text("c test\np max 3 2\nn 1 s\nn 3 t\na 1 2 5\na 2 3 4\n")

    g, problem, labels, source, target, capacity = read_graph_dimacs_flow(str(path))
    assert problem == ["max"]
    assert (vcount(g), ecount(g)) == (3, 2)
    assert (source, target) == (0, 2)
    assert capacity.tolist() == [5, 4]


def test_sir():
    n = 20
    runs = sir(full(n, False, False), 0.5, 0.2, 3)

    assert len(runs) == 3
    for run in runs:
        assert isinstance(run, SIRSimulation)
        assert run.times[0] == 0
        assert (np.diff(run.times) >= 0).all()
        assert len(run.susceptible) == len(run.infected) == len(run.recovered)
        assert len(run.times) == len(run.susceptible)
        assert (run.susceptible + run.infected + run.recovered == n).all()
        assert (run.susceptible[0], run.infected[0]) == (n - 1, 1)
        assert run.infected[-1] == 0

    del runs
    gc.collect()
