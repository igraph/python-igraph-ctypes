from typing import Iterable

from .graph import Graph
from ._internal.functions import create, famous

__all__ = ("create_empty_graph", "create_graph_from_edge_list")


def create_empty_graph(n: int, directed: bool = False) -> Graph:
    """Creates an empty graph with the given number of vertices.

    Parameters:
        n: the number of vertices
        directed: whether the graph is directed
    """
    return Graph(n, directed)


def create_famous_graph(name: str) -> Graph:
    """Creates one of the "famous" graphs embedded into igraph by name.

    See the documentation of the ``igraph_famous()`` function in igraph's C core
    for a list of names accepted by this function.

    Parameters:
        name: the name of the graph to construct
    """
    return Graph(_wrap=famous(name))


def create_graph_from_edge_list(
    edges: Iterable[int], n: int = 0, directed: bool = False
) -> Graph:
    """Creates a graph from the given edge list.

    Parameters:
        edges: the list of edges in the graph
        n: the number of vertices in the graph if it cannot be inferred from
            the maximum edge ID in the edge list
    """
    return Graph(_wrap=create(edges, n, directed))
