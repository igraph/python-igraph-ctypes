from typing import Iterable, Optional, TypeVar

from .enums import NeighborMode
from .types import (
    EdgeSelector,
    IntArray,
    VertexLike,
    VertexPair,
    VertexSelector,
)

from ._internal.functions import (
    add_edges,
    add_vertices,
    delete_edges,
    delete_vertices,
    ecount,
    edge,
    empty,
    get_eid,
    incident,
    is_directed,
    neighbors,
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
        to let the graph take the ownership of a low-level ctypes wrapper object
        for an igraph graph. Typically you will not need to use `_wrap`.
        """
        self._instance = _wrap or empty(*args, **kwds)._instance

    def add_edges(self: C, edges: Iterable[VertexPair]) -> C:
        add_edges(self, edges)
        return self

    def add_vertices(self: C, n: int) -> C:
        add_vertices(self, n)
        return self

    def delete_edges(self: C, edges: EdgeSelector) -> C:
        delete_edges(self, edges)
        return self

    def delete_vertices(self: C, vertices: VertexSelector) -> C:
        delete_vertices(self, vertices)
        return self

    def ecount(self) -> int:
        """Returns the number of edges in the graph."""
        return ecount(self)

    def edge(self, eid: int) -> VertexPair:
        """Returns the endpoints of the edge with the given index from the
        graph.
        """
        return edge(self, eid)

    def get_edge_id(
        self,
        from_: VertexLike,
        to: VertexLike,
        *,
        directed: bool = True,
        error: bool = True
    ) -> int:
        """Returns the ID of an arbitrary edge between the given source and
        target vertices.
        """
        return get_eid(self, from_, to, directed, error)

    def incident(
        self, vid: VertexLike, mode: NeighborMode = NeighborMode.ALL
    ) -> IntArray:
        return incident(self, vid, mode)

    def is_directed(self) -> bool:
        """Returns whether the graph is directed."""
        return is_directed(self)

    def neighbors(
        self, vid: VertexLike, mode: NeighborMode = NeighborMode.ALL
    ) -> IntArray:
        """Returns the list of neighbors of a vertex."""
        return neighbors(self, vid, mode)

    def vcount(self) -> int:
        """Returns the number of vertices in the graph."""
        return vcount(self)

    @property
    def _as_parameter_(self) -> _Graph:
        """ctypes hook function that extracts the low-level ctypes wrapper
        object from the graph.
        """
        return self._instance
