"""Conversion functions from Python types to internal igraph types."""

from typing import Any, Iterable

from .lib import igraph_vector_int_push_back
from .types import (
    igraph_bool_t,
    igraph_integer_t,
    igraph_real_t,
    VertexLike,
    VertexPair,
)
from .wrappers import _VectorInt

__all__ = (
    "any_to_igraph_bool_t",
    "vertexlike_to_igraph_integer_t",
    "vertexlike_to_igraph_real_t",
    "vertex_pairs_to_igraph_vector_int_t",
)


def any_to_igraph_bool_t(obj: Any) -> igraph_bool_t:
    """Converts an arbitrary Python object to an igraph boolean by taking its
    truth value.
    """
    return igraph_bool_t(bool(obj))


def vertexlike_to_igraph_integer_t(vertex: VertexLike) -> igraph_integer_t:
    """Converts a vertex-like object to an igraph integer."""
    return igraph_integer_t(vertex)


def vertexlike_to_igraph_real_t(vertex: VertexLike) -> igraph_real_t:
    """Converts a vertex-like object to an igraph real."""
    return igraph_real_t(int(vertex))


def vertex_pairs_to_igraph_vector_int_t(pairs: Iterable[VertexPair]) -> _VectorInt:
    """Converts an iterable containing pairs of vertex-like objects to an
    igraph vector of vertex IDs.
    """
    result = _VectorInt.create(0)
    for u, v in pairs:
        igraph_vector_int_push_back(result, vertexlike_to_igraph_integer_t(u))
        igraph_vector_int_push_back(result, vertexlike_to_igraph_integer_t(v))
    return result
