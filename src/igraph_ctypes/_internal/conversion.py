"""Conversion functions from Python types to internal igraph types."""

from __future__ import annotations

import numpy as np

from contextlib import contextmanager
from ctypes import addressof, get_errno, memmove, POINTER
from os import strerror
from typing import (
    Any,
    Callable,
    IO,
    Iterable,
    Iterator,
    Mapping,
    Optional,
    Sequence,
    TYPE_CHECKING,
)

from .attributes.utils import python_type_to_igraph_attribute_type
from .enums import AttributeCombinationType, MatrixStorage
from .lib import (
    fdopen,
    fflush,
    igraph_attribute_combination_add,
    igraph_es_all,
    igraph_es_none,
    igraph_es_vector_copy,
    igraph_es_1,
    igraph_matrix_int_init_array,
    igraph_matrix_int_ncol,
    igraph_matrix_int_nrow,
    igraph_matrix_init_array,
    igraph_matrix_ncol,
    igraph_matrix_nrow,
    igraph_vector_bool_get,
    igraph_vector_bool_get_ptr,
    igraph_vector_bool_init_array,
    igraph_vector_bool_push_back,
    igraph_vector_bool_size,
    igraph_vector_bool_view,
    igraph_vector_get,
    igraph_vector_get_ptr,
    igraph_vector_init_array,
    igraph_vector_int_get,
    igraph_vector_int_get_ptr,
    igraph_vector_int_init_array,
    igraph_vector_int_list_get_ptr,
    igraph_vector_int_list_push_back,
    igraph_vector_int_list_size,
    igraph_vector_int_push_back,
    igraph_vector_int_size,
    igraph_vector_int_view,
    igraph_vector_list_get_ptr,
    igraph_vector_list_push_back,
    igraph_vector_list_size,
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
    igraph_int_t,
    igraph_real_t,
    np_type_of_igraph_bool_t,
    np_type_of_igraph_int_t,
    np_type_of_igraph_real_t,
    AttributeCombinationSpecification,
    AttributeCombinationSpecificationEntry,
    BoolArray,
    EdgeLike,
    EdgeSelector,
    FilePtr,
    IntArray,
    MatrixLike,
    MatrixIntLike,
    RealArray,
    VertexLike,
    VertexPair,
    VertexSelector,
)
from .utils import bytes_to_str
from .wrappers import (
    _AttributeCombination,
    _EdgeSelector,
    _Matrix,
    _MatrixInt,
    _Vector,
    _VectorBool,
    _VectorInt,
    _VectorIntList,
    _VectorList,
    _VertexSelector,
)

if TYPE_CHECKING:
    from igraph_ctypes.graph import Graph


__all__ = (
    "any_to_file_ptr",
    "any_to_igraph_bool_t",
    "bytes_to_str",
    "edgelike_to_igraph_int_t",
    "edge_capacities_to_igraph_vector_t",
    "edge_capacities_to_igraph_vector_t_view",
    "edge_colors_to_igraph_vector_t",
    "edge_colors_to_igraph_vector_t_view",
    "edge_lengths_to_igraph_vector_t",
    "edge_lengths_to_igraph_vector_t_view",
    "edge_selector_to_igraph_es_t",
    "edge_weights_to_igraph_vector_t",
    "edge_weights_to_igraph_vector_t_view",
    "igraph_matrix_t_to_numpy_array",
    "igraph_matrix_int_t_to_numpy_array",
    "igraph_vector_t_to_list",
    "igraph_vector_bool_t_to_list",
    "igraph_vector_int_t_to_list",
    "igraph_vector_t_to_numpy_array",
    "igraph_vector_t_to_numpy_array_view",
    "igraph_vector_bool_t_to_numpy_array",
    "igraph_vector_bool_t_to_numpy_array_view",
    "igraph_vector_int_t_to_numpy_array",
    "igraph_vector_int_t_to_numpy_array_view",
    "igraph_vector_int_list_t_to_list_of_numpy_array",
    "igraph_vector_list_t_to_list_of_numpy_array",
    "iterable_edge_indices_to_igraph_vector_int_t",
    "iterable_of_edge_index_iterable_to_igraph_vector_int_list_t",
    "iterable_of_iterable_to_igraph_vector_int_list_t",
    "iterable_of_iterable_to_igraph_vector_list_t",
    "iterable_of_vertex_index_iterable_to_igraph_vector_int_list_t",
    "iterable_to_igraph_vector_bool_t",
    "iterable_to_igraph_vector_bool_t_view",
    "iterable_to_igraph_vector_int_t",
    "iterable_to_igraph_vector_int_t_view",
    "iterable_to_igraph_vector_t",
    "iterable_to_igraph_vector_t_view",
    "iterable_vertex_indices_to_igraph_vector_int_t",
    "mapping_to_attribute_combination_t",
    "python_type_to_igraph_attribute_type",
    "sequence_to_igraph_matrix_int_t",
    "sequence_to_igraph_matrix_int_t_view",
    "sequence_to_igraph_matrix_t",
    "sequence_to_igraph_matrix_t_view",
    "vertexlike_to_igraph_int_t",
    "vertex_pairs_to_igraph_vector_int_t",
    "vertex_selector_to_igraph_vs_t",
    "vertex_colors_to_igraph_vector_int_t",
    "vertex_colors_to_igraph_vector_int_t_view",
    "vertex_qty_to_igraph_vector_t",
    "vertex_qty_to_igraph_vector_t_view",
    "vertex_weights_to_igraph_vector_t",
    "vertex_weights_to_igraph_vector_t_view",
)


@contextmanager
def any_to_file_ptr(obj: Any, mode: str) -> Iterator[Optional[FilePtr]]:
    """Converts an arbitrary Python object to an open file pointer in the C
    layer, using the following rules:

    - ``None`` is returned as is.

    - Integers are treated as file handles and a low-level ``fdopen()`` call
      from the C standard library will be used to convert them into a ``FILE*``
      pointer.

    - File-like objects with a ``fileno()`` method will be converted into a
      file handle and then they will be treated the same way as integers above.

    - Anything else is forwarded to ``open()`` to convert them into a file-like
      object. They will then be treated as any other file-like object. The
      created object will be _closed_ automatically when the context manager
      exits.
    """
    if obj is None:
        yield None
        return

    handle: int
    fp: IO[Any] | None = None
    file_ptr: Optional[FilePtr] = None

    if isinstance(obj, int):
        handle = obj
    elif hasattr(obj, "fileno") and callable(obj.fileno):
        # Flush pending writes first to ensure that they do not get mixed up
        # with the ones performed by igraph's C core
        if hasattr(obj, "flush") and callable(obj.flush):
            obj.flush()
        handle = obj.fileno()
    else:
        fp = open(obj, mode)
        try:
            if hasattr(fp, "fileno") and callable(fp.fileno):
                handle = fp.fileno()
            else:
                raise TypeError("open() returned an object without a file handle")
        except Exception:
            fp.close()
            fp = None
            raise

    try:
        file_ptr = fdopen(
            handle, mode.encode("ascii") if isinstance(mode, str) else mode
        )
        if not file_ptr:
            errno = get_errno()
            raise OSError(errno, strerror(errno))
        yield file_ptr
        fflush(file_ptr)
    finally:
        if fp is not None:
            fp.close()  # takes care of fclose() on file_ptr


def any_to_igraph_bool_t(obj: Any) -> igraph_bool_t:
    """Converts an arbitrary Python object to an igraph boolean by taking its
    truth value.
    """
    return igraph_bool_t(bool(obj))


def edgelike_to_igraph_int_t(edge: EdgeLike) -> igraph_int_t:
    """Converts an edge-like object to an igraph integer."""
    if isinstance(edge, int) and edge >= 0:
        return igraph_int_t(edge)
    else:
        raise ValueError(f"{edge!r} cannot be converted to an igraph edge index")


def edge_selector_to_igraph_es_t(selector: EdgeSelector, graph: Graph) -> _EdgeSelector:
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
        index = edgelike_to_igraph_int_t(selector)  # type: ignore
        return _EdgeSelector.create_with(igraph_es_1, index)


def edge_weights_to_igraph_vector_t(weights: Iterable[float], graph: Graph) -> _Vector:
    """Converts a Python iterable of floating-point numbers to a vector of
    edge weights.
    """
    return iterable_to_igraph_vector_t(weights)


def edge_weights_to_igraph_vector_t_view(
    weights: Optional[Iterable[float]], graph: Graph
) -> Optional[_Vector]:
    """Converts a Python iterable of floating-point numbers to a vector of
    edge weights, possibly creating a shallow view if the input is an
    appropriate NumPy array.

    When the input is `None`, the return value will also be `None`, which is
    interpreted by the C core of igraph as all edges having equal weight.
    """
    return iterable_to_igraph_vector_t_view(weights) if weights is not None else None


# Currently we handle lengths the same way as weights; this might change in
# the future
edge_lengths_to_igraph_vector_t = edge_weights_to_igraph_vector_t
edge_lengths_to_igraph_vector_t_view = edge_weights_to_igraph_vector_t_view


# Currently we handle capacities the same way as weights; this might change in
# the future
edge_capacities_to_igraph_vector_t = edge_weights_to_igraph_vector_t
edge_capacities_to_igraph_vector_t_view = edge_weights_to_igraph_vector_t_view


def edge_colors_to_igraph_vector_t(colors: Iterable[int], graph: Graph) -> _VectorInt:
    """Converts a Python iterable of integers to a vector of edge colors."""
    return iterable_to_igraph_vector_int_t(colors)


def edge_colors_to_igraph_vector_t_view(
    colors: Iterable[int], graph: Graph
) -> _VectorInt:
    """Converts a Python iterable of integers to a vector of edge colors,
    possibly creating a shallow view if the input is an appropriate NumPy array.
    """
    return iterable_to_igraph_vector_int_t_view(colors)


def iterable_edge_indices_to_igraph_vector_int_t(
    indices: Iterable[EdgeLike],
) -> _VectorInt:
    """Converts an iterable containing edge-like objects to an igraph vector
    of edge IDs.
    """
    if isinstance(indices, np.ndarray):
        return numpy_array_to_igraph_vector_int_t(indices, flatten=True)

    result = _VectorInt.create(0)
    for index in indices:
        igraph_vector_int_push_back(result, edgelike_to_igraph_int_t(index))
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
    if isinstance(items, np.ndarray):
        return numpy_array_to_igraph_vector_bool_t_view(items)
    else:
        return iterable_to_igraph_vector_bool_t(items)


def iterable_to_igraph_vector_int_t(items: Iterable[int]) -> _VectorInt:
    """Converts an iterable containing Python integers to an igraph vector of
    integers.
    """
    if isinstance(items, np.ndarray):
        return numpy_array_to_igraph_vector_int_t(items, flatten=True)
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
    if isinstance(items, np.ndarray):
        return numpy_array_to_igraph_vector_int_t_view(items, flatten=True)
    else:
        return iterable_to_igraph_vector_int_t(items)


def iterable_to_igraph_vector_t(items: Iterable[float]) -> _Vector:
    """Converts an iterable containing Python integers or floats to an igraph
    vector of floats.
    """
    if isinstance(items, np.ndarray):
        return numpy_array_to_igraph_vector_t(items)
    else:
        result: _Vector = _Vector.create(0)
        for item in items:
            igraph_vector_push_back(result, item)
        return result


def iterable_to_igraph_vector_t_view(items: Iterable[float]) -> _Vector:
    """Converts an iterable containing Python integers or floats to an igraph
    vector of floats, possibly creating a shallow view if the input is an
    appropriate NumPy array.
    """
    if isinstance(items, np.ndarray):
        return numpy_array_to_igraph_vector_t_view(items)
    else:
        return iterable_to_igraph_vector_t(items)


def iterable_vertex_indices_to_igraph_vector_int_t(
    indices: Iterable[VertexLike],
) -> _VectorInt:
    """Converts an iterable containing vertex-like objects to an igraph vector
    of vertex IDs.
    """
    if isinstance(indices, np.ndarray):
        return numpy_array_to_igraph_vector_int_t(indices, flatten=True)

    result: _VectorInt = _VectorInt.create(0)
    for index in indices:
        igraph_vector_int_push_back(result, vertexlike_to_igraph_int_t(index))
    return result


def iterable_of_iterable_to_igraph_vector_int_list_t(
    items: Iterable[Iterable[int]],
) -> _VectorIntList:
    result = _VectorIntList.create(0)

    # TODO:
    #
    # - if items is a sequence (i.e. we know its length), we could optimize the
    #   conversion
    # - we could re-use an already-constructed _VectorInt if we had an alternative
    #   iterable_to_igraph_vector_int_t() that receives a _VectorInt from the
    #   outside

    for item in items:
        vec = iterable_to_igraph_vector_int_t(item)
        igraph_vector_int_list_push_back(result, vec)
        vec.release()

    return result


def iterable_of_iterable_to_igraph_vector_list_t(
    items: Iterable[Iterable[float]],
) -> _VectorList:
    result = _VectorList.create(0)

    # TODO:
    #
    # - if items is a sequence (i.e. we know its length), we could optimize the
    #   conversion
    # - we could re-use an already-constructed _VectorInt if we had an alternative
    #   iterable_to_igraph_vector_t() that receives a _VectorInt from the
    #   outside

    for item in items:
        vec = iterable_to_igraph_vector_t(item)
        igraph_vector_list_push_back(result, vec)
        vec.release()

    return result


def iterable_of_edge_index_iterable_to_igraph_vector_int_list_t(
    items: Iterable[Iterable[VertexLike]],
) -> _VectorIntList:
    return iterable_of_iterable_to_igraph_vector_int_list_t(items)


def iterable_of_vertex_index_iterable_to_igraph_vector_int_list_t(
    items: Iterable[Iterable[VertexLike]],
) -> _VectorIntList:
    return iterable_of_iterable_to_igraph_vector_int_list_t(items)


def _any_to_attribute_combination_type_and_func(
    value: AttributeCombinationSpecificationEntry,
) -> tuple[AttributeCombinationType, Callable | None]:
    if callable(value):
        # TODO(ntamas): need a Python-to-C wrapper around value!
        return AttributeCombinationType.FUNCTION, value
    else:
        return AttributeCombinationType.from_(value), None


def mapping_to_attribute_combination_t(
    mapping: Optional[AttributeCombinationSpecification],
) -> _AttributeCombination:
    """Converts a Python mapping from attribute names to attribute combination
    handlers to a low-level igraph attribute combination object.
    """
    if mapping is None:
        # Default behaviour: keep the first attribute from every collapsed group
        mapping = "first"

    if not isinstance(mapping, Mapping):
        # Single attribute combination entry, to be applied for all attributes
        return mapping_to_attribute_combination_t({None: mapping})  # type: ignore

    result = _AttributeCombination.create()

    for key, value in (mapping or {}).items():
        combination_type, func = _any_to_attribute_combination_type_and_func(value)
        igraph_attribute_combination_add(
            result, key.encode("utf-8") if key else None, combination_type.value, func
        )

    return result


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
            np.array(items, dtype=np_type_of_igraph_int_t)
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
    """Ensures that the given NumPy array is one-dimensional and matches the
    given NumPy type, avoiding copies during the conversion if possible.
    """
    if len(arr.shape) != 1:
        if flatten:
            arr = arr.reshape(-1)
        else:
            raise TypeError("NumPy array must be one-dimensional")
    return np.ravel(arr.astype(np_type, order="C", casting="safe", copy=False))


def _force_into_2d_numpy_array(arr: np.ndarray, np_type) -> np.ndarray:
    """Ensures that the given NumPy array is two-dimensional and matches the
    given NumPy type, avoiding copies during the conversion if possible.
    """
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
    arr = _force_into_2d_numpy_array(arr, np_type_of_igraph_int_t)
    return _MatrixInt.create_with(
        igraph_matrix_int_init_array,
        arr.ctypes.data_as(POINTER(igraph_int_t)),
        arr.shape[0],
        arr.shape[1],
        MatrixStorage.COLUMN_MAJOR,
    )


def numpy_array_to_igraph_vector_bool_t(
    arr: np.ndarray, flatten: bool = False
) -> _VectorBool:
    """Converts a one-dimensional NumPy array to an igraph vector of booleans."""
    arr = _force_into_1d_numpy_array(arr, np_type_of_igraph_bool_t, flatten=flatten)
    return _VectorBool.create_with(
        igraph_vector_bool_init_array,
        arr.ctypes.data_as(POINTER(igraph_bool_t)),
        arr.shape[0],
    )


def numpy_array_to_igraph_vector_bool_t_view(
    arr: np.ndarray, flatten: bool = False
) -> _VectorBool:
    """Provides a view into an existing one-dimensional NumPy array with an
    igraph boolean vector view if the data type and the layout of the NumPy
    array is suitable. If the NumPy array is not suitable, it will be copied
    into the appropriate layout and data type first and then a view will be
    provided into the copy.
    """
    arr = _force_into_1d_numpy_array(arr, np_type_of_igraph_bool_t, flatten=flatten)
    arr_ptr = arr.ctypes.data_as(POINTER(igraph_bool_t))

    result = _VectorBool(igraph_vector_bool_view(arr_ptr, arr.shape[0]))

    # Destructor must not be called so we never mark result as initialized;
    result.release()

    return result


def numpy_array_to_igraph_vector_int_t(
    arr: np.ndarray, flatten: bool = False
) -> _VectorInt:
    """Converts a one-dimensional NumPy array to an igraph vector of integers."""
    arr = _force_into_1d_numpy_array(arr, np_type_of_igraph_int_t, flatten=flatten)
    return _VectorInt.create_with(
        igraph_vector_int_init_array,
        arr.ctypes.data_as(POINTER(igraph_int_t)),
        arr.shape[0],
    )


def numpy_array_to_igraph_vector_int_t_view(
    arr: np.ndarray, flatten: bool = False
) -> _VectorInt:
    """Provides a view into an existing one-dimensional NumPy array with an
    igraph integer vector view if the data type and the layout of the NumPy
    array is suitable. If the NumPy array is not suitable, it will be copied
    into the appropriate layout and data type first and then a view will be
    provided into the copy.
    """
    arr = _force_into_1d_numpy_array(arr, np_type_of_igraph_int_t, flatten=flatten)
    arr_ptr = arr.ctypes.data_as(POINTER(igraph_int_t))

    result = _VectorInt(igraph_vector_int_view(arr_ptr, arr.shape[0]))

    # Destructor must not be called so we need to call .release()
    result.release()

    return result


def numpy_array_to_igraph_vector_t(arr: np.ndarray, flatten: bool = False) -> _Vector:
    """Converts a one-dimensional NumPy array to an igraph vector of reals."""
    arr = _force_into_1d_numpy_array(arr, np_type_of_igraph_real_t, flatten=flatten)
    return _Vector.create_with(
        igraph_vector_init_array,
        arr.ctypes.data_as(POINTER(igraph_real_t)),
        arr.shape[0],
    )


def numpy_array_to_igraph_vector_t_view(
    arr: np.ndarray, flatten: bool = False
) -> _Vector:
    """Provides a view into an existing one-dimensional NumPy array with an
    igraph floating-point vector view if the data type and the layout of the NumPy
    array is suitable. If the NumPy array is not suitable, it will be copied
    into the appropriate layout and data type first and then a view will be
    provided into the copy.
    """
    arr = _force_into_1d_numpy_array(arr, np_type_of_igraph_real_t, flatten=flatten)
    arr_ptr = arr.ctypes.data_as(POINTER(igraph_real_t))

    result = _Vector(igraph_vector_view(arr_ptr, arr.shape[0]))

    # Destructor must not be called so we need to call .release()
    result.release()

    return result


def vertexlike_to_igraph_int_t(vertex: VertexLike) -> igraph_int_t:
    """Converts a vertex-like object to an igraph integer."""
    if isinstance(vertex, int) and vertex >= 0:
        return igraph_int_t(vertex)
    else:
        raise ValueError(f"{vertex!r} cannot be converted to an igraph vertex index")


def vertex_pairs_to_igraph_vector_int_t(pairs: Iterable[VertexPair]) -> _VectorInt:
    """Converts an iterable containing pairs of vertex-like objects to an
    igraph vector of vertex IDs.
    """
    if isinstance(pairs, np.ndarray):
        return numpy_array_to_igraph_vector_int_t(pairs, flatten=True)

    result: _VectorInt = _VectorInt.create(0)
    for u, v in pairs:
        igraph_vector_int_push_back(result, vertexlike_to_igraph_int_t(u))
        igraph_vector_int_push_back(result, vertexlike_to_igraph_int_t(v))
    return result


def vertex_selector_to_igraph_vs_t(
    selector: VertexSelector, graph: Graph
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
        indices = iterable_vertex_indices_to_igraph_vector_int_t(
            selector  # type: ignore
        )
        return _VertexSelector.create_with(igraph_vs_vector_copy, indices)
    else:
        index = vertexlike_to_igraph_int_t(selector)  # type: ignore
        return _VertexSelector.create_with(igraph_vs_1, index)


def vertex_colors_to_igraph_vector_int_t(
    colors: Iterable[int], graph: Graph
) -> _VectorInt:
    """Converts a Python iterable of integers to a vector of vertex colors."""
    return iterable_to_igraph_vector_int_t(colors)


def vertex_colors_to_igraph_vector_int_t_view(
    colors: Iterable[int], graph: Graph
) -> _VectorInt:
    """Converts a Python iterable of integers to a vector of vertex colors,
    possibly creating a shallow view if the input is an appropriate NumPy array.
    """
    return iterable_to_igraph_vector_int_t_view(colors)


def vertex_qty_to_igraph_vector_t(weights: Iterable[float], graph: Graph) -> _Vector:
    """Converts a Python iterable of floating-point numbers to a vector of
    vertex-related quantities.
    """
    return iterable_to_igraph_vector_t(weights)


def vertex_qty_to_igraph_vector_t_view(
    weights: Optional[Iterable[float]], graph: Graph
) -> Optional[_Vector]:
    """Converts a Python iterable of floating-point numbers to a vector of
    vertex-related quantities, possibly creating a shallow view if the input is
    an appropriate NumPy array.

    When the input is `None`, the return value will also be `None`, which is
    interpreted by the C core of igraph as all edges having equal weight.
    """
    return iterable_to_igraph_vector_t_view(weights) if weights else None


def vertex_weights_to_igraph_vector_t(
    weights: Iterable[float], graph: Graph
) -> _Vector:
    """Converts a Python iterable of floating-point numbers to a vector of
    vertex weights.
    """
    return iterable_to_igraph_vector_t(weights)


def vertex_weights_to_igraph_vector_t_view(
    weights: Optional[Iterable[float]], graph: Graph
) -> Optional[_Vector]:
    """Converts a Python iterable of floating-point numbers to a vector of
    vertex weights, possibly creating a shallow view if the input is an
    appropriate NumPy array.

    When the input is `None`, the return value will also be `None`, which is
    interpreted by the C core of igraph as all vertices having equal weight.
    """
    return iterable_to_igraph_vector_t_view(weights) if weights is not None else None


################################################################################
# Conversion from igraph data types to Python                                  #
################################################################################


def igraph_vector_t_to_list(vector: _Vector) -> list[float]:
    n = igraph_vector_size(vector)
    return [float(igraph_vector_get(vector, i)) for i in range(n)]


def igraph_vector_bool_t_to_list(vector: _VectorBool) -> list[bool]:
    n = igraph_vector_bool_size(vector)
    return [bool(igraph_vector_bool_get(vector, i)) for i in range(n)]


def igraph_vector_int_t_to_list(vector: _VectorInt) -> list[int]:
    n = igraph_vector_int_size(vector)
    return [int(igraph_vector_int_get(vector, i)) for i in range(n)]


def igraph_matrix_t_to_numpy_array(matrix: _Matrix) -> RealArray:
    shape = igraph_matrix_nrow(matrix), igraph_matrix_ncol(matrix)
    result = np.zeros(shape, dtype=np_type_of_igraph_real_t)
    if result.size > 0:
        memmove(result.ctypes.data, matrix.unwrap().data.stor_begin, result.nbytes)
    return result


def igraph_matrix_int_t_to_numpy_array(matrix: _MatrixInt) -> IntArray:
    shape = igraph_matrix_int_nrow(matrix), igraph_matrix_int_ncol(matrix)
    result = np.zeros(shape, dtype=np_type_of_igraph_int_t)
    if result.size > 0:
        memmove(result.ctypes.data, matrix.unwrap().data.stor_begin, result.nbytes)
    return result


def igraph_vector_t_to_numpy_array(vector: _Vector) -> RealArray:
    n = igraph_vector_size(vector)
    result = np.zeros(n, dtype=np_type_of_igraph_real_t)
    if n > 0:
        memmove(result.ctypes.data, igraph_vector_get_ptr(vector, 0), result.nbytes)
    return result


def igraph_vector_t_to_numpy_array_view(vector: _Vector) -> RealArray:
    n = igraph_vector_size(vector)
    addr = addressof(igraph_vector_get_ptr(vector, 0).contents)
    buf_type = igraph_real_t * n
    buf = buf_type.from_address(addr)
    return np.frombuffer(buf, dtype=np_type_of_igraph_real_t)


def igraph_vector_bool_t_to_numpy_array(vector: _VectorBool) -> BoolArray:
    n = igraph_vector_bool_size(vector)
    result = np.zeros(n, dtype=np_type_of_igraph_bool_t)
    if n > 0:
        memmove(
            result.ctypes.data, igraph_vector_bool_get_ptr(vector, 0), result.nbytes
        )
    return result


def igraph_vector_bool_t_to_numpy_array_view(vector: _VectorBool) -> BoolArray:
    n = igraph_vector_bool_size(vector)
    addr = addressof(igraph_vector_bool_get_ptr(vector, 0).contents)
    buf_type = igraph_bool_t * n
    buf = buf_type.from_address(addr)
    return np.frombuffer(buf, dtype=np_type_of_igraph_bool_t)


def igraph_vector_int_t_to_numpy_array(vector: _VectorInt) -> IntArray:
    n = igraph_vector_int_size(vector)
    result = np.zeros(n, dtype=np_type_of_igraph_int_t)
    if n > 0:
        memmove(result.ctypes.data, igraph_vector_int_get_ptr(vector, 0), result.nbytes)
    return result


def igraph_vector_int_t_to_numpy_array_view(vector: _VectorInt) -> IntArray:
    n = igraph_vector_int_size(vector)
    addr = addressof(igraph_vector_int_get_ptr(vector, 0).contents)
    buf_type = igraph_int_t * n
    buf = buf_type.from_address(addr)
    return np.frombuffer(buf, dtype=np_type_of_igraph_int_t)


def igraph_vector_list_t_to_list_of_numpy_array(
    vector_list: _VectorList,
) -> list[RealArray]:
    n = igraph_vector_list_size(vector_list)
    vec = _Vector()
    result = []

    for i in range(n):
        # We are re-using the same _Vector instance to wrap different
        # low-level igraph_vector_t instances because it's only temporary
        # until we convert it to a NumPy array
        ptr = igraph_vector_list_get_ptr(vector_list, i)
        vec._set_wrapped_instance(ptr.contents)
        result.append(igraph_vector_t_to_numpy_array(vec))

    return result


def igraph_vector_list_t_to_list_of_numpy_array_view(
    vector_list: _VectorList,
) -> list[RealArray]:
    n = igraph_vector_list_size(vector_list)
    vec = _Vector()
    result = []

    for i in range(n):
        # We are re-using the same _Vector instance to wrap different
        # low-level igraph_vector_t instances because it's only temporary
        # until we convert it to a NumPy array
        ptr = igraph_vector_list_get_ptr(vector_list, i)
        vec._set_wrapped_instance(ptr.contents)
        result.append(igraph_vector_t_to_numpy_array_view(vec))

    return result


def igraph_vector_int_list_t_to_list_of_numpy_array(
    vector_list: _VectorIntList,
) -> list[IntArray]:
    n = igraph_vector_int_list_size(vector_list)
    vec = _VectorInt()
    result = []

    for i in range(n):
        # We are re-using the same _VectorInt instance to wrap different
        # low-level igraph_vector_int_t instances because it's only temporary
        # until we convert it to a NumPy array
        ptr = igraph_vector_int_list_get_ptr(vector_list, i)
        vec._set_wrapped_instance(ptr.contents)
        result.append(igraph_vector_int_t_to_numpy_array(vec))

    return result


def igraph_vector_int_list_t_to_list_of_numpy_array_view(
    vector_list: _VectorIntList,
) -> list[IntArray]:
    n = igraph_vector_int_list_size(vector_list)
    vec = _VectorInt()
    result = []

    for i in range(n):
        # We are re-using the same _VectorInt instance to wrap different
        # low-level igraph_vector_int_t instances because it's only temporary
        # until we convert it to a NumPy array
        ptr = igraph_vector_int_list_get_ptr(vector_list, i)
        vec._set_wrapped_instance(ptr.contents)
        result.append(igraph_vector_int_t_to_numpy_array_view(vec))

    return result
