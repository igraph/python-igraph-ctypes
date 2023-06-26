from itertools import combinations
from random import seed

from igraph import Graph as LegacyGraph

from igraph_ctypes.constructors import (
    create_graph_from_edge_list,
    create_geometric_random_graph,
)
from igraph_ctypes.conversion import get_edge_list
from igraph_ctypes.paths import components
from igraph_ctypes._internal.functions import maximal_cliques

seed(42)

n, r, k = 1600, 0.0625, 4

new_g = create_geometric_random_graph(n, r)
old_g = LegacyGraph(get_edge_list(new_g).tolist())


def _gen_pairs(sets, threshold: int):
    return (
        (u, v)
        for u, v in combinations(range(len(sets)), 2)
        if u != v and len(sets[u] & sets[v]) >= threshold
    )


def _find_edgelist_pairs(sets, threshold: int):
    return list(_gen_pairs(sets, threshold))


def _find_edgelist(sets, threshold: int):
    result = []
    for pair in _gen_pairs(sets, threshold):
        result.extend(pair)
    return result


def clique_percolation_with_old_igraph():
    cliques = [set(cl) for cl in old_g.maximal_cliques(min=k)]
    el = _find_edgelist_pairs(cliques, k - 1)
    clique_g = LegacyGraph(el, directed=False)
    clique_g.components()


def clique_percolation_with_new_igraph():
    cliques = [set(cl) for cl in maximal_cliques(new_g, min_size=4)]
    el = _find_edgelist(cliques, k - 1)
    clique_g = create_graph_from_edge_list(el, directed=False)
    components(clique_g)


__benchmarks__ = [
    (
        clique_percolation_with_old_igraph,
        clique_percolation_with_new_igraph,
        "Clique percolation method",
    )
]
