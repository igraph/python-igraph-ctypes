import numpy as np
import numpy.typing as npt

from ctypes import (
    CFUNCTYPE,
    c_bool,
    c_char_p,
    c_double,
    c_int,
    c_int64,
    c_long,
    c_ulong,
    c_uint8,
    c_uint64,
    c_void_p,
    py_object,
    POINTER,
    Structure,
    Union as CUnion,
)
from io import IOBase
from os import PathLike
from typing import Any, Callable, Iterable, Mapping, Literal, Sequence


def vector_fields(base_type):
    """Function that receives a base type and returns the standard fields used
    in igraph for _vectors_ of the given ctypes base type.
    """
    return [
        ("stor_begin", POINTER(base_type)),
        ("stor_end", POINTER(base_type)),
        ("end", POINTER(base_type)),
    ]


###########################################################################
# Mapping of ctypes types to low-level igraph types

igraph_bool_t = c_bool
igraph_error_t = c_int
igraph_integer_t = (
    c_int64  # TODO(ntamas): this depends on whether igraph is 32-bit or 64-bit
)
igraph_real_t = c_double
igraph_uint_t = (
    c_uint64  # TODO(ntamas): this depends on whether igraph is 32-bit or 64-bit
)

# TODO(ntamas): these depend on whether igraph is 32-bit or 64-bit
np_type_of_igraph_bool_t = np.bool_
np_type_of_igraph_integer_t = np.int64
np_type_of_igraph_real_t = np.float64
np_type_of_igraph_uint_t = np.uint64


class FILE(Structure):
    """ctypes representation of a ``FILE`` object"""

    pass


FilePtr = c_void_p


class igraph_complex_t(Structure):
    """ctypes representation of ``igraph_complex_t``"""

    _fields_ = [("dat", igraph_real_t * 2)]


class igraph_vector_t(Structure):
    """ctypes representation of ``igraph_vector_t``"""

    _fields_ = vector_fields(igraph_real_t)


class igraph_vector_bool_t(Structure):
    """ctypes representation of ``igraph_vector_bool_t``"""

    _fields_ = vector_fields(igraph_bool_t)


class igraph_vector_complex_t(Structure):
    """ctypes representation of ``igraph_vector_complex_t``"""

    _fields_ = vector_fields(igraph_complex_t)


class igraph_vector_int_t(Structure):
    """ctypes representation of ``igraph_vector_int_t``"""

    _fields_ = vector_fields(igraph_integer_t)


class igraph_vector_list_t(Structure):
    """ctypes representation of ``igraph_vector_list_t``"""

    _fields_ = vector_fields(igraph_vector_t)


class igraph_vector_int_list_t(Structure):
    """ctypes representation of ``igraph_vector_int_list_t``"""

    _fields_ = vector_fields(igraph_vector_int_t)


class igraph_vector_ptr_t(Structure):
    """ctypes representation of ``igraph_vector_ptr_t``"""

    _fields_ = vector_fields(c_void_p)


class igraph_matrix_t(Structure):
    """ctypes representation of ``igraph_matrix_t``"""

    _fields_ = [
        ("data", igraph_vector_t),
        ("nrow", c_long),
        ("ncol", c_long),
    ]


class igraph_matrix_int_t(Structure):
    """ctypes representation of ``igraph_matrix_int_t``"""

    _fields_ = [
        ("data", igraph_vector_int_t),
        ("nrow", c_long),
        ("ncol", c_long),
    ]


class igraph_matrix_complex_t(Structure):
    """ctypes representation of ``igraph_matrix_complex_t``"""

    _fields_ = [
        ("data", igraph_vector_complex_t),
        ("nrow", c_long),
        ("ncol", c_long),
    ]


class igraph_matrix_list_t(Structure):
    """ctypes representation of ``igraph_matrix_list_t``"""

    _fields_ = vector_fields(igraph_matrix_t)


class igraph_strvector_t(Structure):
    """ctypes representation of an ``igraph_strvector_t``"""

    _fields_ = vector_fields(c_char_p)


class igraph_sparsemat_t(Structure):
    """ctypes representation of ``igraph_sparsemat_t``"""

    _fields_ = [("cs", c_void_p)]


class igraph_adjlist_t(Structure):
    """ctypes representation of ``igraph_adjlist_t``"""

    _fields_ = [("length", igraph_integer_t), ("adjs", POINTER(igraph_vector_int_t))]


class igraph_inclist_t(Structure):
    """ctypes representation of ``igraph_adjlist_t``"""

    _fields_ = [("length", igraph_integer_t), ("incs", POINTER(igraph_vector_int_t))]


class igraph_t(Structure):
    """ctypes representation of ``igraph_t``"""

    _fields_ = [
        ("n", igraph_integer_t),
        ("directed", igraph_bool_t),
        ("from_", igraph_vector_int_t),
        ("to", igraph_vector_int_t),
        ("oi", igraph_vector_int_t),
        ("ii", igraph_vector_int_t),
        ("os", igraph_vector_int_t),
        ("is_", igraph_vector_int_t),
        ("attr", py_object),
        ("cache", c_void_p),
    ]


class igraph_graph_list_t(Structure):
    """ctypes representation of ``igraph_graph_list_t``"""

    _fields_ = vector_fields("igraph_t") + [("directed", igraph_bool_t)]


class _igraph_vs_es_index_mode_t(Structure):
    """ctypes representation of a pair of an index and a neighborhood mode,
    typically used in the .data.adj field in an ``igraph_vs_t``"""

    _fields_ = [("vid", igraph_integer_t), ("mode", c_int)]


class _igraph_vs_es_index_pair_t(Structure):
    """ctypes representation of an index pair, typically used in the
    .data.range field in an ``igraph_vs_t`` or ``igraph_es_t``"""

    _fields_ = [("from", igraph_integer_t), ("to", igraph_integer_t)]


class _igraph_vs_es_index_pair_and_directedness_t(Structure):
    """ctypes representation of an index pair and a directedness indicator,
    typically used in the .data.path field in an ``igraph_es_t``"""

    _fields_ = [
        ("from", igraph_integer_t),
        ("to", igraph_integer_t),
        ("directed", igraph_bool_t),
    ]


class _igraph_es_data_path_t(Structure):
    """ctypes representation of a pair of a vector and a neighborhood mode,
    typically used in the .data.path field in an ``igraph_es_t``"""

    _fields_ = [("ptr", igraph_vector_t), ("mode", c_int)]


class _igraph_vs_t_data(CUnion):
    """ctypes representation of the .data field in an ``igraph_vs_t``"""

    _fields_ = [
        ("vid", igraph_integer_t),
        ("vecptr", POINTER(igraph_vector_int_t)),
        ("adj", _igraph_vs_es_index_mode_t),
        ("range", _igraph_vs_es_index_pair_t),
    ]


class igraph_vs_t(Structure):
    """ctypes representation of ``igraph_vs_t``"""

    _fields_ = [("type", c_int), ("data", _igraph_vs_t_data)]


class _igraph_es_t_data(CUnion):
    """ctypes representation of the .data field in an ``igraph_es_t``"""

    _fields_ = [
        ("vid", igraph_integer_t),
        ("eid", igraph_integer_t),
        ("vecptr", POINTER(igraph_vector_int_t)),
        ("incident", _igraph_vs_es_index_mode_t),
        ("range", _igraph_vs_es_index_pair_t),
        ("path", _igraph_es_data_path_t),
        ("between", _igraph_vs_es_index_pair_and_directedness_t),
    ]


class igraph_es_t(Structure):
    """ctypes representation of ``igraph_es_t``"""

    _fields_ = [("type", c_int), ("data", _igraph_es_t_data)]


class igraph_arpack_options_t(Structure):
    """ctypes representation of an ``igraph_arpack_options_t`` object"""

    # TODO(ntamas)
    pass


class igraph_attribute_combination_t(Structure):
    """ctypes representation of ``igraph_attribute_combination_t``"""

    _fields_ = [("list", igraph_vector_ptr_t)]


class igraph_attribute_combination_record_t(Structure):
    """ctypes representation of ``igraph_attribute_combination_record_t``"""

    _fields_ = [("name", c_char_p), ("type", c_int), ("func", CFUNCTYPE(c_void_p))]


class igraph_bliss_info_t(Structure):
    """ctypes representation of an ``igraph_bliss_info_t`` object"""

    _fields_ = [
        ("nof_nodes", c_ulong),
        ("nof_leaf_nodes", c_ulong),
        ("nof_bad_nodes", c_ulong),
        ("nof_canupdates", c_ulong),
        ("nof_generators", c_ulong),
        ("max_level", c_ulong),
        ("group_size", c_char_p),
    ]


class igraph_hrg_t(Structure):
    """ctypes representation of an ``igraph_hrg_t`` object"""

    _fields_ = [
        ("left", igraph_vector_int_t),
        ("right", igraph_vector_int_t),
        ("prob", igraph_vector_t),
        ("vertices", igraph_vector_int_t),
        ("edges", igraph_vector_int_t),
    ]


class igraph_layout_drl_options_t(Structure):
    """ctypes representation of an ``igraph_drl_options_t`` object"""

    _fields_ = [
        ("edge_cut", igraph_real_t),
        ("init_iterations", igraph_integer_t),
        ("init_temperature", igraph_real_t),
        ("init_attraction", igraph_real_t),
        ("init_damping_mult", igraph_real_t),
        ("liquid_iterations", igraph_integer_t),
        ("liquid_temperature", igraph_real_t),
        ("liquid_attraction", igraph_real_t),
        ("liquid_damping_mult", igraph_real_t),
        ("expansion_iterations", igraph_integer_t),
        ("expansion_temperature", igraph_real_t),
        ("expansion_attraction", igraph_real_t),
        ("expansion_damping_mult", igraph_real_t),
        ("cooldown_iterations", igraph_integer_t),
        ("cooldown_temperature", igraph_real_t),
        ("cooldown_attraction", igraph_real_t),
        ("cooldown_damping_mult", igraph_real_t),
        ("crunch_iterations", igraph_integer_t),
        ("crunch_temperature", igraph_real_t),
        ("crunch_attraction", igraph_real_t),
        ("crunch_damping_mult", igraph_real_t),
        ("simmer_iterations", igraph_integer_t),
        ("simmer_temperature", igraph_real_t),
        ("simmer_attraction", igraph_real_t),
        ("simmer_damping_mult", igraph_real_t),
    ]


class igraph_maxflow_stats_t(Structure):
    """ctypes representation of an ``igraph_maxflow_stats_t`` object"""

    _fields_ = [
        ("nopush", igraph_integer_t),
        ("norelabel", igraph_integer_t),
        ("nogap", igraph_integer_t),
        ("nogapnodes", igraph_integer_t),
        ("nobfs", igraph_integer_t),
    ]


class igraph_plfit_result_t(Structure):
    """ctypes representation of an ``igraph_plfit_result_t`` object"""

    _fields_ = [
        ("continuous", igraph_bool_t),
        ("alpha", igraph_real_t),
        ("xmin", igraph_real_t),
        ("L", igraph_real_t),
        ("D", igraph_real_t),
        ("data", POINTER(igraph_vector_t)),
    ]


igraph_rng_state_t = c_void_p


class igraph_rng_type_t(Structure):
    """ctypes representation of an ``igraph_rng_type_t`` object"""

    TYPES = {
        "init": CFUNCTYPE(igraph_error_t, POINTER(igraph_rng_state_t)),
        "destroy": CFUNCTYPE(None, igraph_rng_state_t),
        "seed": CFUNCTYPE(igraph_error_t, igraph_rng_state_t, igraph_uint_t),
        "get": CFUNCTYPE(igraph_uint_t, igraph_rng_state_t),
        "get_int": CFUNCTYPE(
            igraph_integer_t, igraph_rng_state_t, igraph_integer_t, igraph_integer_t
        ),
        "get_real": CFUNCTYPE(igraph_real_t, igraph_rng_state_t),
        "get_norm": CFUNCTYPE(igraph_real_t, igraph_rng_state_t),
        "get_geom": CFUNCTYPE(igraph_real_t, igraph_rng_state_t, igraph_real_t),
        "get_binom": CFUNCTYPE(
            igraph_real_t, igraph_rng_state_t, igraph_integer_t, igraph_real_t
        ),
        "get_exp": CFUNCTYPE(igraph_real_t, igraph_rng_state_t, igraph_real_t),
        "get_gamma": CFUNCTYPE(
            igraph_real_t, igraph_rng_state_t, igraph_real_t, igraph_real_t
        ),
        "get_pois": CFUNCTYPE(igraph_real_t, igraph_rng_state_t, igraph_real_t),
    }

    _fields_ = [
        ("name", c_char_p),
        ("bits", c_uint8),
        ("init", TYPES["init"]),
        ("destroy", TYPES["destroy"]),
        ("seed", TYPES["seed"]),
        ("get", TYPES["get"]),
        ("get_int", TYPES["get_int"]),
        ("get_real", TYPES["get_real"]),
        ("get_norm", TYPES["get_norm"]),
        ("get_geom", TYPES["get_geom"]),
        ("get_binom", TYPES["get_binom"]),
        ("get_exp", TYPES["get_exp"]),
        ("get_gamma", TYPES["get_gamma"]),
        ("get_pois", TYPES["get_pois"]),
    ]


class igraph_rng_t(Structure):
    """ctypes representation of an ``igraph_rng_t`` object"""

    _fields_ = [
        ("type", POINTER(igraph_rng_type_t)),
        ("state", igraph_rng_state_t),
        ("is_seeded", igraph_bool_t),
    ]


igraph_function_pointer_t = CFUNCTYPE(None)
igraph_error_handler_t = CFUNCTYPE(None, c_char_p, c_char_p, c_int, igraph_error_t)
igraph_fatal_handler_t = CFUNCTYPE(None, c_char_p, c_char_p, c_int)
igraph_interruption_handler_t = CFUNCTYPE(igraph_bool_t)
igraph_isocompat_t = CFUNCTYPE(
    igraph_bool_t,
    POINTER(igraph_t),
    POINTER(igraph_t),
    igraph_integer_t,
    igraph_integer_t,
    c_void_p,
)
igraph_warning_handler_t = CFUNCTYPE(None, c_char_p, c_char_p, c_int)


p_attribute_combination_t = POINTER(igraph_attribute_combination_t)
p_igraph_t = POINTER(igraph_t)
p_strvector_t = POINTER(igraph_strvector_t)
p_vector_t = POINTER(igraph_vector_t)
p_vector_bool_t = POINTER(igraph_vector_bool_t)
p_vector_int_t = POINTER(igraph_vector_int_t)
p_vector_int_list_t = POINTER(igraph_vector_int_list_t)
p_vector_ptr_t = POINTER(igraph_vector_ptr_t)


class igraph_attribute_table_t(Structure):
    """ctypes representation of ``igraph_attribute_table_t``"""

    TYPES = {
        "init": CFUNCTYPE(igraph_error_t, p_igraph_t, p_vector_ptr_t),
        "destroy": CFUNCTYPE(None, p_igraph_t),
        "copy": CFUNCTYPE(
            igraph_error_t,
            p_igraph_t,
            p_igraph_t,
            igraph_bool_t,
            igraph_bool_t,
            igraph_bool_t,
        ),
        "add_vertices": CFUNCTYPE(
            igraph_error_t, p_igraph_t, igraph_integer_t, p_vector_ptr_t
        ),
        "permute_vertices": CFUNCTYPE(
            igraph_error_t, p_igraph_t, p_igraph_t, p_vector_int_t
        ),
        "combine_vertices": CFUNCTYPE(
            igraph_error_t,
            p_igraph_t,
            p_igraph_t,
            p_vector_int_list_t,
            p_attribute_combination_t,
        ),
        "add_edges": CFUNCTYPE(
            igraph_error_t, p_igraph_t, p_vector_int_t, p_vector_ptr_t
        ),
        "permute_edges": CFUNCTYPE(
            igraph_error_t, p_igraph_t, p_igraph_t, p_vector_int_t
        ),
        "combine_edges": CFUNCTYPE(
            igraph_error_t,
            p_igraph_t,
            p_igraph_t,
            p_vector_int_list_t,
            p_attribute_combination_t,
        ),
        "get_info": CFUNCTYPE(
            igraph_error_t,
            p_igraph_t,
            p_strvector_t,
            p_vector_int_t,
            p_strvector_t,
            p_vector_int_t,
            p_strvector_t,
            p_vector_int_t,
        ),
        "has_attr": CFUNCTYPE(igraph_bool_t, p_igraph_t, c_int, c_char_p),
        "get_type": CFUNCTYPE(
            igraph_error_t, p_igraph_t, POINTER(c_int), c_int, c_char_p
        ),
        "get_numeric_graph_attr": CFUNCTYPE(
            igraph_error_t, p_igraph_t, c_char_p, p_vector_t
        ),
        "get_string_graph_attr": CFUNCTYPE(
            igraph_error_t, p_igraph_t, c_char_p, p_strvector_t
        ),
        "get_bool_graph_attr": CFUNCTYPE(
            igraph_error_t, p_igraph_t, c_char_p, p_vector_bool_t
        ),
        "get_numeric_vertex_attr": CFUNCTYPE(
            igraph_error_t, p_igraph_t, c_char_p, igraph_vs_t, p_vector_t
        ),
        "get_string_vertex_attr": CFUNCTYPE(
            igraph_error_t, p_igraph_t, c_char_p, igraph_vs_t, p_strvector_t
        ),
        "get_bool_vertex_attr": CFUNCTYPE(
            igraph_error_t, p_igraph_t, c_char_p, igraph_vs_t, p_vector_bool_t
        ),
        "get_numeric_edge_attr": CFUNCTYPE(
            igraph_error_t, p_igraph_t, c_char_p, igraph_es_t, p_vector_t
        ),
        "get_string_edge_attr": CFUNCTYPE(
            igraph_error_t, p_igraph_t, c_char_p, igraph_es_t, p_strvector_t
        ),
        "get_bool_edge_attr": CFUNCTYPE(
            igraph_error_t, p_igraph_t, c_char_p, igraph_es_t, p_vector_bool_t
        ),
    }

    _fields_ = [
        ("init", TYPES["init"]),
        ("destroy", TYPES["destroy"]),
        ("copy", TYPES["copy"]),
        ("add_vertices", TYPES["add_vertices"]),
        ("permute_vertices", TYPES["permute_vertices"]),
        ("combine_vertices", TYPES["combine_vertices"]),
        ("add_edges", TYPES["add_edges"]),
        ("permute_edges", TYPES["permute_edges"]),
        ("combine_edges", TYPES["combine_edges"]),
        ("get_info", TYPES["get_info"]),
        ("has_attr", TYPES["has_attr"]),
        ("get_type", TYPES["get_type"]),
        ("get_numeric_graph_attr", TYPES["get_numeric_graph_attr"]),
        ("get_string_graph_attr", TYPES["get_string_graph_attr"]),
        ("get_bool_graph_attr", TYPES["get_bool_graph_attr"]),
        ("get_numeric_vertex_attr", TYPES["get_numeric_vertex_attr"]),
        ("get_string_vertex_attr", TYPES["get_string_vertex_attr"]),
        ("get_bool_vertex_attr", TYPES["get_bool_vertex_attr"]),
        ("get_numeric_edge_attr", TYPES["get_numeric_edge_attr"]),
        ("get_string_edge_attr", TYPES["get_string_edge_attr"]),
        ("get_bool_edge_attr", TYPES["get_bool_edge_attr"]),
    ]


###########################################################################
# Type aliases used by the higher level interface

BoolArray = npt.NDArray[np_type_of_igraph_bool_t]
"""Type alias for NumPy arrays containing igraph booleans"""

IntArray = npt.NDArray[np_type_of_igraph_integer_t]
"""Type alias for NumPy arrays containing igraph integers"""

RealArray = npt.NDArray[np_type_of_igraph_real_t]
"""Type alias for NumPy arrays containing igraph reals"""

MatrixLike = Sequence[Sequence[float]] | npt.NDArray
"""Type alias for Python types that can be converted to an igraph matrix."""

MatrixIntLike = Sequence[Sequence[int]] | npt.NDArray
"""Type alias for Python types that can be converted to an igraph integer matrix."""

VertexLike = int
"""Type alias for Python types that can be converted to an igraph vertex ID"""

VertexPair = tuple[VertexLike, VertexLike]
"""A pair of objects that can both be converted into igraph vertex IDs"""

VertexSelector = Iterable[VertexLike] | Literal["all"] | VertexLike | None
"""Type alias for Python types that can be converted to an igraph vertex
selector.
"""

EdgeLike = int
"""Type alias for Python types that can be converted to an igraph edge ID"""

EdgeSelector = Iterable[EdgeLike] | Literal["all"] | EdgeLike | None
"""Type alias for Python types that can be converted to an igraph edge
selector.
"""

FileLike = int | bytes | str | PathLike[bytes] | PathLike[str] | IOBase
"""Type alias for Python types that can be used in places where the C core
expects a FILE* pointer.
"""

AttributeCombinationSpecificationEntry = (
    Literal[
        "default",
        "ignore",
        "sum",
        "prod",
        "min",
        "max",
        "random",
        "first",
        "last",
        "mean",
        "median",
        "concat",
    ]
    | Callable[[Sequence[Any]], Any]
)
"""Type alias for values that can be accepted in an AttributeCombinationSpecification_
mapping.
"""

AttributeCombinationSpecification = Mapping[str, AttributeCombinationSpecificationEntry]
"""Type alias for mappings that specify how to merge vertex or edge attributes
during an operation that contracts multiple vertices or edge into a single one.
"""
