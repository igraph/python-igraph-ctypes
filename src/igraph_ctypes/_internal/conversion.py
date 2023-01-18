"""Conversion functions from Python types to internal igraph types."""

import numpy as np
import numpy.typing as npt

from ctypes import memmove, POINTER
from typing import Any, Iterable, List, Sequence

from .enums import MatrixStorage
from .lib import (
    igraph_es_all,
    igraph_es_none,
    igraph_es_vector_copy,
    igraph_es_1,
    igraph_matrix_int_init_array,
    igraph_matrix_int_ncol,
    igraph_matrix_int_nrow,
    igraph_matrix_int_e_ptr,
    igraph_matrix_init_array,
    igraph_matrix_ncol,
    igraph_matrix_nrow,
    igraph_matrix_e_ptr,
    igraph_vector_bool_e,
    igraph_vector_bool_e_ptr,
    igraph_vector_bool_init_array,
    igraph_vector_bool_push_back,
    igraph_vector_bool_size,
    igraph_vector_bool_view,
    igraph_vector_int_e,
    igraph_vector_int_e_ptr,
    igraph_vector_int_init_array,
    igraph_vector_int_push_back,
    igraph_vector_int_size,
    igraph_vector_int_view,
    igraph_vector_e,
    igraph_vector_e_ptr,
    igraph_vector_init_array,
    igraph_vector_push_back,
    igraph_vector_size,
    igraph_vector_view,
    igraph_vs_all,
    igraph_vs_none,
    igraph_vs_vector_copy,
    igraph_vs_1,
)
from .types import (
    igraph_bool_t,
    igraph_integer_t,
    igraph_real_t,
    np_type_of_igraph_bool_t,
    np_type_of_igraph_integer_t,
    np_type_of_igraph_real_t,
    EdgeLike,
    EdgeSelector,
    MatrixLike,
    MatrixIntLike,
    VertexLike,
    VertexPair,
    VertexSelector,
)
from .wrappers import (
    _EdgeSelector,
    _Graph,
    _Matrix,
    _MatrixInt,
    _Vector,
    _VectorBool,
    _VectorInt,
    _VertexSelector,
)

__all__ = (
    "any_to_igraph_bool_t",
    "edgelike_to_igraph_integer_t",
    "edge_selector_to_igraph_es_t",
    "igraph_matrix_t_to_numpy_array",
    "igraph_matrix_int_t_to_numpy_array",
    "igraph_vector_t_to_list",
    "igraph_vector_bool_t_to_list",
    "igraph_vector_int_t_to_list",
    "igraph_vector_t_to_numpy_array",
    "igraph_vector_bool_t_to_numpy_array",
    "igraph_vector_int_t_to_numpy_array",
    "iterable_edge_indices_to_igraph_vector_int_t",
    "iterable_to_igraph_vector_bool_t",
    "iterable_to_igraph_vector_bool_t_view",
    "iterable_to_igraph_vector_int_t",
    "iterable_to_igraph_vector_int_t_view",
    "iterable_to_igraph_vector_t",
    "iterable_to_igraph_vector_t_view",
    "sequence_to_igraph_matrix_int_t",
    "sequence_to_igraph_matrix_int_t_view",
    "sequence_to_igraph_matrix_t",
    "sequence_to_igraph_matrix_t_view",
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
    if isinstance(edge, int) and edge >= 0:
        return igraph_integer_t(edge)
    else:
        raise ValueError(f"{edge!r} cannot be converted to an igraph edge index")


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
    elif isinstance(selector, str):
        # TODO(ntamas): implement name lookup?
        raise TypeError("edge selector cannot be a string")
    elif hasattr(selector, "__iter__"):
        indices = iterable_edge_indices_to_igraph_vector_int_t(selector)  # type: ignore
        return _EdgeSelector.create_with(igraph_es_vector_copy, indices)
    else:
        index = edgelike_to_igraph_integer_t(selector)  # type: ignore
        return _EdgeSelector.create_with(igraph_es_1, index)


def iterable_edge_indices_to_igraph_vector_int_t(
    indices: Iterable[EdgeLike],
) -> _VectorInt:
    """Converts an iterable containing edge-like objects to an igraph vector
    of edge IDs.
    """
    if isinstance(indices, np.ndarray):
        return numpy_array_to_igraph_vector_int_t(indices)

    result: _VectorInt = _VectorInt.create(0)
    for index in indices:
        igraph_vector_int_push_back(result, edgelike_to_igraph_integer_t(index))
    return result


def iterable_to_igraph_vector_bool_t(items: Iterable[Any]) -> _VectorBool:
    """Converts an iterable containing Python objects to an igraph vector of
    booleans based on their truth values.
    """
    if isinstance(items, np.ndarray):
        return numpy_array_to_igraph_vector_bool_t(items)
    else:
        result: _VectorBool = _VectorBool.create(0)
        for item in items:
            igraph_vector_bool_push_back(result, bool(item))
        return result


def iterable_to_igraph_vector_bool_t_view(items: Iterable[Any]) -> _VectorBool:
    """Converts an iterable containing Python objects to an igraph vector of
    booleans based on their truth values, possibly creating a shallow view if
    the input is an appropriate NumPy array.
    """
    # TODO(ntamas)
    return iterable_to_igraph_vector_bool_t(items)


def iterable_to_igraph_vector_int_t(items: Iterable[int]) -> _VectorInt:
    """Converts an iterable containing Python integers to an igraph vector of
    integers.
    """
    if isinstance(items, np.ndarray):
        return numpy_array_to_igraph_vector_int_t(items)
    else:
        result = _VectorInt.create(0)
        for item in items:
            igraph_vector_int_push_back(result, item)
        return result


def iterable_to_igraph_vector_int_t_view(items: Iterable[Any]) -> _VectorInt:
    """Converts an iterable containing Python objects to an igraph vector of
    integers, possibly creating a shallow view if the input is an appropriate
    NumPy array.
    """
    # TODO(ntamas)
    return iterable_to_igraph_vector_int_t(items)


def iterable_to_igraph_vector_t(items: Iterable[float]) -> _Vector:
    """Converts an iterable containing Python integers or floats to an igraph
    vector of floats.
    """
    result: _Vector = _Vector.create(0)
    for item in items:
        igraph_vector_push_back(result, item)
    return result


def iterable_to_igraph_vector_t_view(items: Iterable[float]) -> _Vector:
    """Converts an iterable containing Python integers or floats to an igraph
    vector of floats, possibly creating a shallow view if the input is an
    appropriate NumPy array.
    """
    # TODO(ntamas)
    return iterable_to_igraph_vector_t(items)


def sequence_to_igraph_matrix_int_t(items: MatrixIntLike) -> _MatrixInt:
    """Converts a sequence of sequences of Python integers to an igraph matrix
    of integers. Each sequence in the top-level sequence must have the same
    length.
    """
    if isinstance(items, np.ndarray):
        return numpy_array_to_igraph_matrix_int_t(items)
    else:
        _ensure_matrix(items)
        return numpy_array_to_igraph_matrix_int_t(
            np.array(items, dtype=np_type_of_igraph_integer_t)
        )


def sequence_to_igraph_matrix_int_t_view(items: MatrixIntLike) -> _MatrixInt:
    """Converts a sequence of sequences of Python integers to an igraph matrix
    of integers, possibly creating a shallow view if the input is an
    appropriate NumPy matrix. Each sequence in the top-level sequence must have
    the same length.
    """
    # TODO(ntamas)
    return sequence_to_igraph_matrix_int_t(items)


def sequence_to_igraph_matrix_t(items: MatrixLike) -> _Matrix:
    """Converts a sequence of sequences of Python integers or floats to an
    igraph matrix of floats. Each sequence in the top-level sequence must have
    the same length.
    """
    if isinstance(items, np.ndarray):
        return numpy_array_to_igraph_matrix_t(items)
    else:
        _ensure_matrix(items)
        return numpy_array_to_igraph_matrix_t(
            np.array(items, dtype=np_type_of_igraph_real_t)
        )


def sequence_to_igraph_matrix_t_view(items: MatrixLike) -> _Matrix:
    """Converts a sequence of sequences of Python integers or floats to an
    igraph matrix of floats, possibly creating a shallow view if the input is an
    appropriate NumPy matrix. Each sequence in the top-level sequence must have
    the same length.
    """
    # TODO(ntamas)
    return sequence_to_igraph_matrix_t(items)


def _ensure_matrix(items: Sequence[Sequence[Any]]) -> None:
    """Ensures that the given Python sequence of sequences is a valid matrix,
    i.e. all of its items have the same length.

    Raises:
        ValueError: if the input is not a matrix
    """
    nrow = len(items)
    if nrow:
        ncol = len(items[0])
        if not any(len(row) == ncol for row in items):
            raise ValueError("rows of a matrix must have the same length")


def _force_into_1d_numpy_array(arr: np.ndarray, np_type, flatten: bool) -> np.ndarray:
    if len(arr.shape) != 1:
        if flatten:
            arr = arr.reshape((-1,))
        else:
            raise TypeError("NumPy array must be one-dimensional")
    return np.ravel(arr.astype(np_type, order="C", casting="safe", copy=False))


def _force_into_2d_numpy_array(arr: np.ndarray, np_type) -> np.ndarray:
    if len(arr.shape) != 2:
        raise TypeError("NumPy array must be two-dimensional")
    return arr.astype(np_type, order="C", casting="safe", copy=False)


def numpy_array_to_igraph_matrix_t(arr: np.ndarray) -> _Matrix:
    """Converts a two-dimensional NumPy array to an igraph matrix of reals."""
    arr = _force_into_2d_numpy_array(arr, np_type_of_igraph_real_t)
    return _Matrix.create_with(
        igraph_matrix_init_array,
        arr.ctypes.data_as(POINTER(igraph_real_t)),
        arr.shape[0],
        arr.shape[1],
        MatrixStorage.COLUMN_MAJOR,
    )


def numpy_array_to_igraph_matrix_int_t(arr: np.ndarray) -> _MatrixInt:
    """Converts a two-dimensional NumPy array to an igraph matrix of integers."""
    arr = _force_into_2d_numpy_array(arr, np_type_of_igraph_integer_t)
    return _MatrixInt.create_with(
        igraph_matrix_int_init_array,
        arr.ctypes.data_as(POINTER(igraph_integer_t)),
        arr.shape[0],
        arr.shape[1],
        MatrixStorage.COLUMN_MAJOR,
    )


def numpy_array_to_igraph_vector_bool_t(
    arr: np.ndarray, flatten: bool = False
) -> _VectorBool:
    """Converts a one-dimensional NumPy array to an igraph vector of booleans."""
    arr = _force_into_1d_numpy_array(arr, np_type_of_igraph_bool_t, flatten=flatten)
    arr = np.ravel(
        arr.astype(np_type_of_igraph_bool_t, order="C", casting="safe", copy=False)
    )
    return _VectorBool.create_with(
        igraph_vector_bool_init_array,
        arr.ctypes.data_as(POINTER(igraph_bool_t)),
        arr.shape[0],
    )


def numpy_array_to_igraph_vector_int_t(
    arr: np.ndarray, flatten: bool = False
) -> _VectorInt:
    """Converts a one-dimensional NumPy array to an igraph vector of integers."""
    arr = _force_into_1d_numpy_array(arr, np_type_of_igraph_integer_t, flatten=flatten)
    arr = np.ravel(
        arr.astype(np_type_of_igraph_integer_t, order="C", casting="safe", copy=False)
    )
    return _VectorInt.create_with(
        igraph_vector_int_init_array,
        arr.ctypes.data_as(POINTER(igraph_integer_t)),
        arr.shape[0],
    )


def numpy_array_to_igraph_vector_t(arr: np.ndarray, flatten: bool = False) -> _Vector:
    """Converts a one-dimensional NumPy array to an igraph vector of reals."""
    arr = _force_into_1d_numpy_array(arr, np_type_of_igraph_real_t, flatten=flatten)
    return _Vector.create_with(
        igraph_vector_init_array,
        arr.ctypes.data_as(POINTER(igraph_real_t)),
        arr.shape[0],
    )


def vertexlike_to_igraph_integer_t(vertex: VertexLike) -> igraph_integer_t:
    """Converts a vertex-like object to an igraph integer."""
    if isinstance(vertex, int) and vertex >= 0:
        return igraph_integer_t(vertex)
    else:
        raise ValueError(f"{vertex!r} cannot be converted to an igraph vertex index")


def vertex_indices_to_igraph_vector_int_t(indices: Iterable[VertexLike]) -> _VectorInt:
    """Converts an iterable containing vertex-like objects to an igraph vector
    of vertex IDs.
    """
    if isinstance(indices, np.ndarray):
        return numpy_array_to_igraph_vector_int_t(indices)

    result: _VectorInt = _VectorInt.create(0)
    for index in indices:
        igraph_vector_int_push_back(result, vertexlike_to_igraph_integer_t(index))
    return result


def vertex_pairs_to_igraph_vector_int_t(pairs: Iterable[VertexPair]) -> _VectorInt:
    """Converts an iterable containing pairs of vertex-like objects to an
    igraph vector of vertex IDs.
    """
    if isinstance(pairs, np.ndarray):
        return numpy_array_to_igraph_vector_int_t(pairs, flatten=True)

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
    elif isinstance(selector, str):
        # TODO(ntamas): implement name lookup?
        raise TypeError("vertex selector cannot be a string")
    elif hasattr(selector, "__iter__"):
        indices = vertex_indices_to_igraph_vector_int_t(selector)  # type: ignore
        return _VertexSelector.create_with(igraph_vs_vector_copy, indices)
    else:
        index = vertexlike_to_igraph_integer_t(selector)  # type: ignore
        return _VertexSelector.create_with(igraph_vs_1, index)


################################################################################
# Conversion from igraph data types to Python                                  #
################################################################################


def igraph_vector_t_to_list(vector: _Vector) -> List[float]:
    n = igraph_vector_size(vector)
    return [float(igraph_vector_e(vector, i)) for i in range(n)]


def igraph_vector_bool_t_to_list(vector: _VectorBool) -> List[bool]:
    n = igraph_vector_bool_size(vector)
    return [bool(igraph_vector_bool_e(vector, i)) for i in range(n)]


def igraph_vector_int_t_to_list(vector: _VectorInt) -> List[int]:
    n = igraph_vector_int_size(vector)
    return [int(igraph_vector_int_e(vector, i)) for i in range(n)]


def igraph_matrix_t_to_numpy_array(
    matrix: _Matrix,
) -> npt.NDArray[np_type_of_igraph_real_t]:
    shape = igraph_matrix_nrow(matrix), igraph_matrix_ncol(matrix)
    result = np.zeros(shape, dtype=np_type_of_igraph_real_t)
    if result.size > 0:
        memmove(result.ctypes.data, igraph_matrix_e_ptr(matrix, 0, 0), result.nbytes)
    return result


def igraph_matrix_int_t_to_numpy_array(
    matrix: _MatrixInt,
) -> npt.NDArray[np_type_of_igraph_integer_t]:
    shape = igraph_matrix_int_nrow(matrix), igraph_matrix_int_ncol(matrix)
    result = np.zeros(shape, dtype=np_type_of_igraph_integer_t)
    if result.size > 0:
        memmove(
            result.ctypes.data, igraph_matrix_int_e_ptr(matrix, 0, 0), result.nbytes
        )
    return result


def igraph_vector_t_to_numpy_array(
    vector: _Vector,
) -> npt.NDArray[np_type_of_igraph_real_t]:
    n = igraph_vector_size(vector)
    result = np.zeros(n, dtype=np_type_of_igraph_real_t)
    if n > 0:
        memmove(result.ctypes.data, igraph_vector_e_ptr(vector, 0), result.nbytes)
    return result


def igraph_vector_bool_t_to_numpy_array(
    vector: _VectorBool,
) -> npt.NDArray[np_type_of_igraph_bool_t]:
    n = igraph_vector_bool_size(vector)
    result = np.zeros(n, dtype=np_type_of_igraph_bool_t)
    if n > 0:
        memmove(result.ctypes.data, igraph_vector_bool_e_ptr(vector, 0), result.nbytes)
    return result


def igraph_vector_int_t_to_numpy_array(
    vector: _VectorInt,
) -> npt.NDArray[np_type_of_igraph_integer_t]:
    n = igraph_vector_int_size(vector)
    result = np.zeros(n, dtype=np_type_of_igraph_integer_t)
    if n > 0:
        memmove(result.ctypes.data, igraph_vector_int_e_ptr(vector, 0), result.nbytes)
    return result
