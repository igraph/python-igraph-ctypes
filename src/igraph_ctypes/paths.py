"""Functions related to shortest or widest paths in a graph."""

from typing import Iterable, Literal, Optional

from .enums import Connectedness, NeighborMode
from .graph import Graph
from .types import IntArray, VertexLike

from ._internal.functions import (
    connected_components,
    get_shortest_path,
    get_shortest_path_bellman_ford,
    get_shortest_path_dijkstra,
)

__all__ = ("components", "shortest_path")


def components(graph: Graph, mode: Connectedness = Connectedness.WEAK) -> IntArray:
    """Finds the weakly or strongly connected components of a graph.

    Args:
        graph: the graph
        mode: whether the function should return weakly or strongly connected
            components
    """
    membership, _, _ = connected_components(graph, mode)
    return membership


def shortest_path(
    graph: Graph,
    source: VertexLike,
    target: VertexLike,
    mode: NeighborMode = NeighborMode.OUT,
    weights: Optional[Iterable[float]] = None,
    method: Literal["auto", "dijkstra", "bellman_ford"] = "dijkstra",
) -> IntArray:
    """Finds a single shortest path between two vertices in a graph.

    Args:
        graph: the graph
        source: the source vertex
        target: the target vertex
        mode: TODO
        weights: list of weights for each edge in the graph, or ``None`` to treat
            the edges as unweighted
        method: the method to use for finding shortest paths when the graph is
            weighted. May be one of `"auto"` (pick the best method), `"dijkstra"`
            (Dijkstra's algorithm) or `"bellman_ford"` (Bellman-Ford algorithm).

    Returns:
        the IDs of the vertices along the shortest path
    """
    # TODO(ntamas): handle epath?
    if method == "auto":
        vpath, _ = get_shortest_path(graph, source, target, weights, mode)
    elif method == "dijkstra":
        vpath, _ = get_shortest_path_dijkstra(graph, source, target, weights, mode)
    elif method in ("bellman-ford", "bellman_ford"):
        vpath, _ = get_shortest_path_bellman_ford(graph, source, target, weights, mode)
    else:
        raise ValueError(f"unknown method: {method!r}")
    return vpath
