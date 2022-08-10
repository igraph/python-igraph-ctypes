"""Conversion functions from Python types to internal igraph types."""

from typing import Any, Iterable, List

from .lib import (
    igraph_vector_int_e,
    igraph_vector_int_push_back,
    igraph_vector_int_size,
    igraph_vector_e,
    igraph_vector_push_back,
    igraph_vector_size,
)
from .types import (
    igraph_bool_t,
    igraph_integer_t,
    EdgeLike,
    VertexLike,
    VertexPair,
)
from .wrappers import _Vector, _VectorInt

__all__ = (
    "any_to_igraph_bool_t",
    "edgelike_to_igraph_integer_t",
    "edge_indices_to_igraph_vector_int_t",
    "igraph_vector_t_to_list",
    "igraph_vector_int_t_to_list",
    "iterable_to_igraph_vector_int_t",
    "vertexlike_to_igraph_integer_t",
    "vertex_indices_to_igraph_vector_int_t",
    "vertex_pairs_to_igraph_vector_int_t",
)


################################################################################
#  Conversion from Python data types to igraph                                 #
################################################################################


def any_to_igraph_bool_t(obj: Any) -> igraph_bool_t:
    """Converts an arbitrary Python object to an igraph boolean by taking its
    truth value.
    """
    return igraph_bool_t(bool(obj))


def edgelike_to_igraph_integer_t(edge: EdgeLike) -> igraph_integer_t:
    """Converts an edge-like object to an igraph integer."""
    return igraph_integer_t(edge)


def edge_indices_to_igraph_vector_int_t(indices: Iterable[EdgeLike]) -> _VectorInt:
    """Converts an iterable containing edge-like objects to an igraph vector
    of edge IDs.
    """
    result: _VectorInt = _VectorInt.create(0)
    for index in indices:
        igraph_vector_int_push_back(result, edgelike_to_igraph_integer_t(index))
    return result


def iterable_to_igraph_vector_int_t(items: Iterable[int]) -> _VectorInt:
    """Converts an iterable containing Python integers to an igraph vector of
    integers.
    """
    # TODO(ntamas): more efficient copy for NumPy arrays or cases where we could
    # get around with an igraph_vector_int_view()
    result: _VectorInt = _VectorInt.create(0)
    for item in items:
        igraph_vector_int_push_back(result, item)
    return result


def vertexlike_to_igraph_integer_t(vertex: VertexLike) -> igraph_integer_t:
    """Converts a vertex-like object to an igraph integer."""
    return igraph_integer_t(vertex)


def vertex_indices_to_igraph_vector_int_t(indices: Iterable[VertexLike]) -> _VectorInt:
    """Converts an iterable containing vertex-like objects to an igraph vector
    of vertex IDs.
    """
    result: _VectorInt = _VectorInt.create(0)
    for index in indices:
        igraph_vector_int_push_back(result, vertexlike_to_igraph_integer_t(index))
    return result


def vertex_pairs_to_igraph_vector_int_t(pairs: Iterable[VertexPair]) -> _VectorInt:
    """Converts an iterable containing pairs of vertex-like objects to an
    igraph vector of vertex IDs.
    """
    result: _VectorInt = _VectorInt.create(0)
    for u, v in pairs:
        igraph_vector_int_push_back(result, vertexlike_to_igraph_integer_t(u))
        igraph_vector_int_push_back(result, vertexlike_to_igraph_integer_t(v))
    return result


################################################################################
# Conversion from igraph data types to Python                                  #
################################################################################


def igraph_vector_t_to_list(vector: _Vector) -> List[int]:
    n = igraph_vector_size(vector)
    return [int(igraph_vector_e(vector, i)) for i in range(n)]


def igraph_vector_int_t_to_list(vector: _VectorInt) -> List[int]:
    n = igraph_vector_int_size(vector)
    return [int(igraph_vector_int_e(vector, i)) for i in range(n)]
