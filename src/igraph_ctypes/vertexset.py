from __future__ import annotations

from typing import TYPE_CHECKING

from .types import IntArray

if TYPE_CHECKING:
    from .graph import Graph


class VertexSet:
    """Object representing the entire vertex set or a subset of the vertex
    set of a graph.
    """

    _graph: Graph
    """The graph that the vertex set belongs to."""

    _indices: IntArray | None
    """The indices in the set; ``None`` if this object represents the entire
    vertex set of the graph.
    """

    def __init__(self, graph: Graph, indices: IntArray | None = None):
        """Constructor."""
        # TODO(ntamas): be more lenient with indices; accept sequences of ints
        self._graph = graph
        self._indices = indices
