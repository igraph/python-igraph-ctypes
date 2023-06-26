from random import randint, seed

from igraph import Graph as LegacyGraph

from igraph_ctypes.constructors import create_square_lattice
from igraph_ctypes.paths import get_shortest_path

seed(42)

n, k = 1000, 100

sources = [randint(0, n - 1) for _ in range(k)]
targets = [randint(0, n - 1) for _ in range(k)]
pairs = list(zip(sources, targets))

old_g = LegacyGraph.Lattice([n, n], directed=False, circular=False)
new_g = create_square_lattice([n, n], directed=False, periodic=False)


def shortest_path_with_old_igraph():
    for u, v in pairs:
        old_g.get_shortest_paths(u, v)


def shortest_path_with_new_igraph():
    for u, v in pairs:
        get_shortest_path(new_g, u, v)


__benchmarks__ = [
    (
        shortest_path_with_old_igraph,
        shortest_path_with_new_igraph,
        "Finding shortest path in grid graph",
    )
]
