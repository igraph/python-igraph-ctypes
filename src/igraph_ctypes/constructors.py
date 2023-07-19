from typing import Iterable, Union

from .graph import Graph
from ._internal.functions import (
    create as create_graph_from_edge_list,
    empty as create_empty_graph,
    famous as create_famous_graph,
    grg_game,
    square_lattice,
)

__all__ = (
    "create_empty_graph",
    "create_famous_graph",
    "create_geometric_random_graph",
    "create_graph_from_edge_list",
    "create_square_lattice",
)


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
