"""Conversion functions from Python types to internal igraph types."""

import numpy as np
import numpy.typing as npt

from ctypes import memmove
from typing import Any, Iterable, List

from .lib import (
    igraph_es_all,
    igraph_es_none,
    igraph_es_vector,
    igraph_es_1,
    igraph_vector_bool_e,
    igraph_vector_bool_e_ptr,
    igraph_vector_bool_push_back,
    igraph_vector_bool_size,
    igraph_vector_int_e,
    igraph_vector_int_e_ptr,
    igraph_vector_int_push_back,
    igraph_vector_int_size,
    igraph_vector_e,
    igraph_vector_e_ptr,
    igraph_vector_push_back,
    igraph_vector_size,
    igraph_vs_all,
    igraph_vs_none,
    igraph_vs_vector,
    igraph_vs_1,
)
from .types import (
    igraph_bool_t,
    igraph_integer_t,
    EdgeLike,
    EdgeSelector,
    VertexLike,
    VertexPair,
    VertexSelector,
)
from .wrappers import (
    _EdgeSelector,
    _Graph,
    _Vector,
    _VectorBool,
    _VectorInt,
    _VertexSelector,
)

__all__ = (
    "any_to_igraph_bool_t",
    "edgelike_to_igraph_integer_t",
    "edge_indices_to_igraph_vector_int_t",
    "edge_selector_to_igraph_es_t",
    "igraph_vector_t_to_list",
    "igraph_vector_bool_t_to_list",
    "igraph_vector_int_t_to_list",
    "igraph_vector_t_to_numpy_array",
    "igraph_vector_bool_t_to_numpy_array",
    "igraph_vector_int_t_to_numpy_array",
    "iterable_to_igraph_vector_bool_t",
    "iterable_to_igraph_vector_int_t",
    "iterable_to_igraph_vector_t",
    "vertexlike_to_igraph_integer_t",
    "vertex_indices_to_igraph_vector_int_t",
    "vertex_pairs_to_igraph_vector_int_t",
    "vertex_selector_to_igraph_vs_t",
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


def edge_selector_to_igraph_es_t(
    selector: EdgeSelector, graph: _Graph
) -> _EdgeSelector:
    """Converts a Python object representing a selection of edges to an
    igraph_es_t object.
    """
    if selector is None:
        return _EdgeSelector.create_with(igraph_es_none)
    elif selector == "all":
        return _EdgeSelector.create_with(igraph_es_all)
    elif hasattr(selector, "__iter__"):
        indices = edge_indices_to_igraph_vector_int_t(selector)
        return _EdgeSelector.create_with(igraph_es_vector, indices)
    else:
        return _EdgeSelector.create_with(igraph_es_1, selector)


def iterable_to_igraph_vector_bool_t(items: Iterable[Any]) -> _VectorBool:
    """Converts an iterable containing Python objects to an igraph vector of
    booleans based on their truth values.
    """
    # TODO(ntamas): more efficient copy for NumPy arrays or cases where we could
    # get around with an igraph_vector_bool_view()
    result: _VectorBool = _VectorBool.create(0)
    for item in items:
        igraph_vector_bool_push_back(result, bool(item))
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


def iterable_to_igraph_vector_t(items: Iterable[float]) -> _Vector:
    """Converts an iterable containing Python integers or floats to an igraph
    vector of floats.
    """
    # TODO(ntamas): more efficient copy for NumPy arrays or cases where we could
    # get around with an igraph_vector_int_view()
    result: _Vector = _Vector.create(0)
    for item in items:
        igraph_vector_push_back(result, item)
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


def vertex_selector_to_igraph_vs_t(
    selector: VertexSelector, graph: _Graph
) -> _VertexSelector:
    """Converts a Python object representing a selection of vertices to an
    igraph_vs_t object.
    """
    if selector is None:
        return _VertexSelector.create_with(igraph_vs_none)
    elif selector == "all":
        return _VertexSelector.create_with(igraph_vs_all)
    elif hasattr(selector, "__iter__"):
        indices = vertex_indices_to_igraph_vector_int_t(selector)
        return _VertexSelector.create_with(igraph_vs_vector, indices)
    else:
        return _VertexSelector.create_with(igraph_vs_1, selector)


################################################################################
# Conversion from igraph data types to Python                                  #
################################################################################


def igraph_vector_t_to_list(vector: _Vector) -> List[float]:
    n = igraph_vector_size(vector)
    return [float(igraph_vector_e(vector, i)) for i in range(n)]


def igraph_vector_bool_t_to_list(vector: _VectorInt) -> List[bool]:
    n = igraph_vector_bool_size(vector)
    return [bool(igraph_vector_bool_e(vector, i)) for i in range(n)]


def igraph_vector_int_t_to_list(vector: _VectorInt) -> List[int]:
    n = igraph_vector_int_size(vector)
    return [int(igraph_vector_int_e(vector, i)) for i in range(n)]


def igraph_vector_t_to_numpy_array(vector: _Vector) -> npt.NDArray[np.float64]:
    n = igraph_vector_size(vector)
    result = np.zeros(n, dtype=np.float64)
    if n > 0:
        memmove(result.ctypes.data, igraph_vector_e_ptr(vector, 0), result.nbytes)
    return result


def igraph_vector_bool_t_to_numpy_array(vector: _VectorBool) -> npt.NDArray[np.bool_]:
    n = igraph_vector_bool_size(vector)
    result = np.zeros(n, dtype=np.bool_)
    if n > 0:
        memmove(result.ctypes.data, igraph_vector_bool_e_ptr(vector, 0), result.nbytes)
    return result


def igraph_vector_int_t_to_numpy_array(vector: _VectorInt) -> npt.NDArray[np.int64]:
    n = igraph_vector_int_size(vector)
    result = np.zeros(n, dtype=np.int64)
    if n > 0:
        memmove(result.ctypes.data, igraph_vector_int_e_ptr(vector, 0), result.nbytes)
    return result
