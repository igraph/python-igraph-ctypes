"""Conversion functions from Python types to internal igraph types."""

from typing import Iterable

from .lib import igraph_vector_push_back
from .types import igraph_integer_t, igraph_real_t, VertexLike, VertexPair
from .wrappers import _Vector

__all__ = (
    "vertexlike_to_igraph_integer_t",
    "vertexlike_to_igraph_real_t",
    "vertex_pairs_to_igraph_vector_t",
)


def vertexlike_to_igraph_integer_t(vertex: VertexLike) -> igraph_integer_t:
    """Converts a vertex-like object to an igraph integer."""
    return igraph_integer_t(vertex)


def vertexlike_to_igraph_real_t(vertex: VertexLike) -> igraph_real_t:
    """Converts a vertex-like object to an igraph real."""
    return igraph_real_t(int(vertex))


def vertex_pairs_to_igraph_vector_t(pairs: Iterable[VertexPair]) -> _Vector:
    """Converts an iterable containing pairs of vertex-like objects to an
    igraph vector of vertex IDs.
    """
    result = _Vector.create(0)
    for u, v in pairs:
        igraph_vector_push_back(result, vertexlike_to_igraph_real_t(u))
        igraph_vector_push_back(result, vertexlike_to_igraph_real_t(v))
    return result
