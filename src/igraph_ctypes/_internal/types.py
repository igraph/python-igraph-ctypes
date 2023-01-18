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
    c_void_p,
    POINTER,
    Structure,
    Union,
)
from typing import Iterable, Literal, Sequence, Tuple, Union as UnionType


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

# TODO(ntamas): these depend on whether igraph is 32-bit or 64-bit
np_type_of_igraph_bool_t = np.bool_
np_type_of_igraph_integer_t = np.int64
np_type_of_igraph_real_t = np.float64


class FILE(Structure):
    """ctypes representation of a ``FILE`` object"""

    pass


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


class igraph_attribute_combination_t(Structure):
    """ctypes representation of ``igraph_attribute_combination_t``"""

    _fields_ = [("list", igraph_vector_ptr_t)]


class igraph_t(Structure):
    """ctypes representation of ``igraph_t``"""

    _fields_ = [
        ("n", igraph_integer_t),
        ("directed", igraph_bool_t),
        ("from_", igraph_vector_t),
        ("to", igraph_vector_t),
        ("oi", igraph_vector_t),
        ("ii", igraph_vector_t),
        ("os", igraph_vector_t),
        ("is_", igraph_vector_t),
        ("attr", c_void_p),
        ("cache", c_void_p),
    ]


class igraph_graph_list_t(Structure):
    """ctypes representation of ``igraph_graph_list_t``"""

    _fields_ = vector_fields("igraph_t") + [("directed", igraph_bool_t)]


class _igraph_vs_es_index_mode_t(Union):
    """ctypes representation of a pair of an index and a neighborhood mode,
    typically used in the .data.adj field in an ``igraph_vs_t``"""

    _fields_ = [("vid", igraph_integer_t), ("mode", c_int)]


class _igraph_vs_es_index_pair_t(Union):
    """ctypes representation of an index pair, typically used in the
    .data.range field in an ``igraph_vs_t`` or ``igraph_es_t``"""

    _fields_ = [("from", igraph_integer_t), ("to", igraph_integer_t)]


class _igraph_vs_es_index_pair_and_directedness_t(Union):
    """ctypes representation of an index pair and a directedness indicator,
    typically used in the .data.path field in an ``igraph_es_t``"""

    _fields_ = [
        ("from", igraph_integer_t),
        ("to", igraph_integer_t),
        ("directed", igraph_bool_t),
    ]


class _igraph_es_data_path_t(Union):
    """ctypes representation of a pair of a vector and a neighborhood mode,
    typically used in the .data.path field in an ``igraph_es_t``"""

    _fields_ = [("ptr", igraph_vector_t), ("mode", c_int)]


class _igraph_vs_t_data(Union):
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


class _igraph_es_t_data(Union):
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


igraph_isocompat_t = CFUNCTYPE(
    igraph_bool_t,
    POINTER(igraph_t),
    POINTER(igraph_t),
    igraph_integer_t,
    igraph_integer_t,
    c_void_p,
)


###########################################################################
# Type aliases used by the higher level interface

EdgeLike = int
"""Type alias for Python types that can be converted to an igraph edge ID"""

EdgeSelector = Iterable[EdgeLike] | Literal["all"] | EdgeLike | None
"""Type alias for Python types that can be converted to an igraph edge
selector.
"""

MatrixLike = UnionType[Sequence[Sequence[float]], npt.NDArray]
"""Type alias for Python types that can be converted to an igraph matrix."""

MatrixIntLike = UnionType[Sequence[Sequence[int]], npt.NDArray]
"""Type alias for Python types that can be converted to an igraph integer matrix."""

VertexLike = int
"""Type alias for Python types that can be converted to an igraph vertex ID"""

VertexPair = Tuple[VertexLike, VertexLike]
"""A pair of objects that can both be converted into igraph vertex IDs"""

VertexSelector = Iterable[VertexLike] | Literal["all"] | VertexLike | None
"""Type alias for Python types that can be converted to an igraph vertex
selector.
"""
