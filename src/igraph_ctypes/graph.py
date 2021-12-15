from typing import Iterable, Optional, TypeVar

from igraph_ctypes._internal.types import VertexPair

from ._internal.functions import (
    add_edges,
    add_vertices,
    ecount,
    empty,
    is_directed,
    vcount,
)
from ._internal.wrappers import _Graph


C = TypeVar("C", bound="Graph")


class Graph:
    """A graph object."""

    _instance: _Graph
    """The low-level ctypes wrapper object of the graph."""

    def __init__(self, *args, _wrap: Optional[_Graph] = None, **kwds):
        """Constructor.

        Creates an empty graph. All positional and keyword arguments are
        forwarded to `create_empty_graph()`, except `_wrap`, which may be used
        to let the graph take an ownership of a low-level ctypes wrapper object
        for an igraph graph. Typically you will not need to use the `_wrap
        """
        self._instance = _wrap or empty(*args, **kwds)

    def add_edges(self: C, edges: Iterable[VertexPair]) -> C:
        add_edges(self._instance, edges)
        return self

    def add_vertices(self: C, n: int) -> C:
        add_vertices(self._instance, n)
        return self

    def ecount(self) -> int:
        """Returns the number of edges in the graph."""
        return ecount(self._instance)

    def is_directed(self) -> bool:
        """Returns whether the graph is directed."""
        return is_directed(self._instance)

    def vcount(self) -> int:
        """Returns the number of vertices in the graph."""
        return vcount(self._instance)

    def _as_parameter_(self) -> _Graph:
        """ctypes hook function that extracts the low-level ctypes wrapper object
        from the graph.
        """
        return self._instance
