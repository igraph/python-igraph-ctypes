"""Functions related to shortest or widest paths in a graph."""

from typing import Iterable, Optional

from .enums import NeighborMode
from .graph import Graph
from .types import IntArray, VertexLike

from ._internal.functions import (
    get_shortest_path,
    get_shortest_path_bellman_ford,
    get_shortest_path_dijkstra,
)

__all__ = ("shortest_path",)


def shortest_path(
    graph: Graph,
    source: VertexLike,
    target: VertexLike,
    mode: NeighborMode = NeighborMode.OUT,
    weights: Optional[Iterable[float]] = None,
    method: str = "dijkstra",
) -> IntArray:
    # TODO(ntamas): handle epath?
    if weights is None:
        vpath, _ = get_shortest_path(graph, source, target, mode)
    elif method == "dijkstra":
        vpath, _ = get_shortest_path_dijkstra(graph, source, target, weights, mode)
    elif method in ("bellman-ford", "bellman_ford"):
        vpath, _ = get_shortest_path_bellman_ford(graph, source, target, weights, mode)
    else:
        raise ValueError(f"unknown method: {method!r}")
    return vpath
