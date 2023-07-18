from typing import Iterable, Union

from .graph import Graph
from ._internal.functions import create, empty, famous, grg_game, square_lattice

__all__ = (
    "create_empty_graph",
    "create_famous_graph",
    "create_geometric_random_graph",
    "create_graph_from_edge_list",
    "create_square_lattice",
)


def create_empty_graph(n: int, directed: bool = False) -> Graph:
    """Creates an empty graph with the given number of vertices.

    Parameters:
        n: the number of vertices
        directed: whether the graph is directed
    """
    return empty(n, directed)


def create_famous_graph(name: str) -> Graph:
    """Creates one of the "famous" graphs embedded into igraph by name.

    See the documentation of the ``igraph_famous()`` function in igraph's C core
    for a list of names accepted by this function.

    Parameters:
        name: the name of the graph to construct
    """
    return famous(name)


def create_graph_from_edge_list(
    edges: Iterable[int], n: int = 0, directed: bool = False
) -> Graph:
    """Creates a graph from the given edge list.

    Parameters:
        edges: the list of edges in the graph
        n: the number of vertices in the graph if it cannot be inferred from
            the maximum edge ID in the edge list
    """
    return create(edges, n, directed)


def create_square_lattice(
    dimvector: Iterable[int],
    nei: int = 1,
    directed: bool = False,
    mutual: bool = False,
    periodic: Union[bool, Iterable[bool]] = False,
) -> Graph:
    """Creates a square lattice graph.

    Parameters:
        dimvector: number of vertices along each dimension of the lattice
        directed: whether the generated lattice should be directed
        mutual: whether the vertices should be connected in both directions
            if the lattice is directed
        periodic: whether the lattice should be periodic along each dimension.
            `True` or `False` means a periodic or an aperiodic lattice along
            _all_ dimensions. You may supply an iterable having the same
            length as the number of dimensions to specify periodicity along
            each dimension separately.
    """
    if not hasattr(periodic, "__iter__"):
        num_dims = len(list(dimvector))
        periodic_per_dim = [bool(periodic)] * num_dims
    else:
        periodic_per_dim = list(periodic)  # type: ignore

    return square_lattice(dimvector, nei, directed, mutual, periodic_per_dim)


def create_geometric_random_graph(n: int, radius: float, torus: bool = False):
    """Creates a geometric random graph.

    Parameters:
        n: the number of vertices in the graph
        radius: connection distance; two vertices will be connected if they are
            closer to each other than this threshold
    """
    return grg_game(n, radius, torus)[0]
