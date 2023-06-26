from igraph_ctypes._internal.functions import get_edgelist

from .graph import Graph
from .types import IntArray

__all__ = ("get_edge_list",)


def get_edge_list(graph: Graph) -> IntArray:
    return get_edgelist(graph).reshape((-1, 2))
