# fmt: off

from ctypes import cdll, c_char_p, c_double, c_int, c_size_t, c_void_p, CDLL, POINTER
from ctypes.util import find_library
from platform import system
from typing import Any

from .errors import handle_igraph_error_t
from .types import (
    FILE,
    igraph_attribute_combination_t,
    igraph_attribute_record_t,
    igraph_attribute_record_list_t,
    igraph_attribute_table_t,
    igraph_bool_t,
    igraph_integer_t,
    igraph_real_t,
    igraph_error_t,
    igraph_t,
    igraph_graph_list_t,
    igraph_matrix_t,
    igraph_matrix_int_t,
    igraph_matrix_list_t,
    igraph_sparsemat_t,
    igraph_strvector_t,
    igraph_vector_t,
    igraph_vector_bool_t,
    igraph_vector_int_t,
    igraph_vector_int_list_t,
    igraph_vector_list_t,
    igraph_vector_ptr_t,
    igraph_vs_t,
    igraph_es_t,
    igraph_adjlist_t,
    igraph_arpack_options_t,
    igraph_bliss_info_t,
    igraph_cycle_handler_t,
    igraph_error_handler_t,
    igraph_fatal_handler_t,
    igraph_hrg_t,
    igraph_layout_drl_options_t,
    igraph_maxflow_stats_t,
    igraph_interruption_handler_t,
    igraph_isocompat_t,
    igraph_isohandler_t,
    igraph_plfit_result_t,
    igraph_rng_t,
    igraph_rng_type_t,
    igraph_warning_handler_t,
)


def _load_igraph_c_library():
    """Imports the low-level igraph C library using `ctypes`."""
    candidates = ("igraph", "libigraph")
    for candidate in candidates:
        path = find_library(candidate)
        if path is not None:
            break
    else:
        # Hardcoded path for testing purposes
        path = "/Users/tamas/dev/igraph/igraph/build/src/libigraph.3.dylib"

    lib = cdll.LoadLibrary(path)
    return lib


def _load_libc():
    """Imports the C standard library using `ctypes`."""
    if system() == "Windows":
        return CDLL("msvcrt.dll", use_errno=True)
    elif system() == "Darwin":
        return CDLL("libc.dylib", use_errno=True)
    elif system() == "Linux":
        return CDLL("libc.so.6", use_errno=True)
    else:
        raise RuntimeError("Cannot import C standard library on this platform")


_libc: Any = _load_libc()
_lib: Any = _load_igraph_c_library()

# Standard libc functions

fclose = _libc.fclose
fclose.restype = int
fclose.argtypes = [POINTER(FILE)]

fflush = _libc.fflush
fflush.restype = int
fflush.argtypes = [POINTER(FILE)]

fdopen = _libc.fdopen
fdopen.restype = POINTER(FILE)
fdopen.argtypes = [c_int, c_char_p]

# Vector type

igraph_vector_init = _lib.igraph_vector_init
igraph_vector_init.restype = handle_igraph_error_t
igraph_vector_init.argtypes = [POINTER(igraph_vector_t), igraph_integer_t]

igraph_vector_destroy = _lib.igraph_vector_destroy
igraph_vector_destroy.restype = None
igraph_vector_destroy.argtypes = [c_void_p]

igraph_vector_init_array = _lib.igraph_vector_init_array
igraph_vector_init_array.restype = handle_igraph_error_t
igraph_vector_init_array.argtypes = [POINTER(igraph_vector_t), POINTER(igraph_real_t), igraph_integer_t]

igraph_vector_view = _lib.igraph_vector_view
igraph_vector_view.restype = POINTER(igraph_vector_t)
igraph_vector_view.argtypes = [POINTER(igraph_vector_t), POINTER(igraph_real_t), igraph_integer_t]

igraph_vector_clear = _lib.igraph_vector_clear
igraph_vector_clear.restype = None
igraph_vector_clear.argtypes = [POINTER(igraph_vector_t)]

igraph_vector_get = _lib.igraph_vector_get
igraph_vector_get.restype = igraph_real_t
igraph_vector_get.argtypes = [POINTER(igraph_vector_t), igraph_integer_t]

igraph_vector_get_ptr = _lib.igraph_vector_get_ptr
igraph_vector_get_ptr.restype = POINTER(igraph_real_t)
igraph_vector_get_ptr.argtypes = [POINTER(igraph_vector_t), igraph_integer_t]

igraph_vector_push_back = _lib.igraph_vector_push_back
igraph_vector_push_back.restype = handle_igraph_error_t
igraph_vector_push_back.argtypes = [POINTER(igraph_vector_t), igraph_real_t]

igraph_vector_resize = _lib.igraph_vector_resize
igraph_vector_resize.restype = handle_igraph_error_t
igraph_vector_resize.argtypes = [POINTER(igraph_vector_t), igraph_integer_t]

igraph_vector_set = _lib.igraph_vector_set
igraph_vector_set.restype = None
igraph_vector_set.argtypes = [POINTER(igraph_vector_t), igraph_integer_t, igraph_real_t]

igraph_vector_size = _lib.igraph_vector_size
igraph_vector_size.restype = igraph_integer_t
igraph_vector_size.argtypes = [POINTER(igraph_vector_t)]

igraph_vector_update = _lib.igraph_vector_update
igraph_vector_update.restype = handle_igraph_error_t
igraph_vector_update.argtypes = [POINTER(igraph_vector_t), POINTER(igraph_vector_t)]

# Integer vector type

igraph_vector_int_init = _lib.igraph_vector_int_init
igraph_vector_int_init.restype = handle_igraph_error_t
igraph_vector_int_init.argtypes = [POINTER(igraph_vector_int_t), igraph_integer_t]

igraph_vector_int_destroy = _lib.igraph_vector_int_destroy
igraph_vector_int_destroy.restype = None
igraph_vector_int_destroy.argtypes = [c_void_p]

igraph_vector_int_init_array = _lib.igraph_vector_int_init_array
igraph_vector_int_init_array.restype = handle_igraph_error_t
igraph_vector_int_init_array.argtypes = [POINTER(igraph_vector_int_t), POINTER(igraph_integer_t), igraph_integer_t]

igraph_vector_int_view = _lib.igraph_vector_int_view
igraph_vector_int_view.restype = POINTER(igraph_vector_int_t)
igraph_vector_int_view.argtypes = [POINTER(igraph_vector_int_t), POINTER(igraph_integer_t), igraph_integer_t]

igraph_vector_int_clear = _lib.igraph_vector_int_clear
igraph_vector_int_clear.restype = None
igraph_vector_int_clear.argtypes = [POINTER(igraph_vector_int_t)]

igraph_vector_int_get = _lib.igraph_vector_int_get
igraph_vector_int_get.restype = igraph_integer_t
igraph_vector_int_get.argtypes = [POINTER(igraph_vector_int_t), igraph_integer_t]

igraph_vector_int_get_ptr = _lib.igraph_vector_int_get_ptr
igraph_vector_int_get_ptr.restype = POINTER(igraph_integer_t)
igraph_vector_int_get_ptr.argtypes = [POINTER(igraph_vector_int_t), igraph_integer_t]

igraph_vector_int_push_back = _lib.igraph_vector_int_push_back
igraph_vector_int_push_back.restype = handle_igraph_error_t
igraph_vector_int_push_back.argtypes = [POINTER(igraph_vector_int_t), igraph_integer_t]

igraph_vector_int_resize = _lib.igraph_vector_int_resize
igraph_vector_int_resize.restype = handle_igraph_error_t
igraph_vector_int_resize.argtypes = [POINTER(igraph_vector_int_t), igraph_integer_t]

igraph_vector_int_set = _lib.igraph_vector_int_set
igraph_vector_int_set.restype = None
igraph_vector_int_set.argtypes = [POINTER(igraph_vector_int_t), igraph_integer_t, igraph_integer_t]

igraph_vector_int_size = _lib.igraph_vector_int_size
igraph_vector_int_size.restype = igraph_integer_t
igraph_vector_int_size.argtypes = [POINTER(igraph_vector_int_t)]

igraph_vector_int_update = _lib.igraph_vector_int_update
igraph_vector_int_update.restype = handle_igraph_error_t
igraph_vector_int_update.argtypes = [POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t)]

# Boolean vector type

igraph_vector_bool_init = _lib.igraph_vector_bool_init
igraph_vector_bool_init.restype = handle_igraph_error_t
igraph_vector_bool_init.argtypes = [POINTER(igraph_vector_bool_t), igraph_integer_t]

igraph_vector_bool_destroy = _lib.igraph_vector_bool_destroy
igraph_vector_bool_destroy.restype = None
igraph_vector_bool_destroy.argtypes = [c_void_p]

igraph_vector_bool_init_array = _lib.igraph_vector_bool_init_array
igraph_vector_bool_init_array.restype = handle_igraph_error_t
igraph_vector_bool_init_array.argtypes = [POINTER(igraph_vector_bool_t), POINTER(igraph_bool_t), igraph_integer_t]

igraph_vector_bool_view = _lib.igraph_vector_bool_view
igraph_vector_bool_view.restype = POINTER(igraph_vector_bool_t)
igraph_vector_bool_view.argtypes = [POINTER(igraph_vector_bool_t), POINTER(igraph_bool_t), igraph_integer_t]

igraph_vector_bool_clear = _lib.igraph_vector_bool_clear
igraph_vector_bool_clear.restype = None
igraph_vector_bool_clear.argtypes = [POINTER(igraph_vector_bool_t)]

igraph_vector_bool_get = _lib.igraph_vector_bool_get
igraph_vector_bool_get.restype = igraph_bool_t
igraph_vector_bool_get.argtypes = [POINTER(igraph_vector_bool_t), igraph_integer_t]

igraph_vector_bool_get_ptr = _lib.igraph_vector_bool_get_ptr
igraph_vector_bool_get_ptr.restype = POINTER(igraph_bool_t)
igraph_vector_bool_get_ptr.argtypes = [POINTER(igraph_vector_bool_t), igraph_integer_t]

igraph_vector_bool_push_back = _lib.igraph_vector_bool_push_back
igraph_vector_bool_push_back.restype = handle_igraph_error_t
igraph_vector_bool_push_back.argtypes = [POINTER(igraph_vector_bool_t), igraph_bool_t]

igraph_vector_bool_resize = _lib.igraph_vector_bool_resize
igraph_vector_bool_resize.restype = handle_igraph_error_t
igraph_vector_bool_resize.argtypes = [POINTER(igraph_vector_bool_t), igraph_integer_t]

igraph_vector_bool_set = _lib.igraph_vector_bool_set
igraph_vector_bool_set.restype = None
igraph_vector_bool_set.argtypes = [POINTER(igraph_vector_bool_t), igraph_integer_t, igraph_bool_t]

igraph_vector_bool_size = _lib.igraph_vector_bool_size
igraph_vector_bool_size.restype = igraph_integer_t
igraph_vector_bool_size.argtypes = [POINTER(igraph_vector_bool_t)]

igraph_vector_bool_update = _lib.igraph_vector_bool_update
igraph_vector_bool_update.restype = handle_igraph_error_t
igraph_vector_bool_update.argtypes = [POINTER(igraph_vector_bool_t), POINTER(igraph_vector_bool_t)]

# Pointer vector type

igraph_vector_ptr_init = _lib.igraph_vector_ptr_init
igraph_vector_ptr_init.restype = handle_igraph_error_t
igraph_vector_ptr_init.argtypes = [POINTER(igraph_vector_ptr_t), igraph_integer_t]

igraph_vector_ptr_destroy = _lib.igraph_vector_ptr_destroy
igraph_vector_ptr_destroy.restype = None
igraph_vector_ptr_destroy.argtypes = [c_void_p]

igraph_vector_ptr_clear = _lib.igraph_vector_ptr_clear
igraph_vector_ptr_clear.restype = None
igraph_vector_ptr_clear.argtypes = [POINTER(igraph_vector_ptr_t)]

igraph_vector_ptr_get = _lib.igraph_vector_ptr_get
igraph_vector_ptr_get.restype = c_void_p
igraph_vector_ptr_get.argtypes = [POINTER(igraph_vector_ptr_t), igraph_integer_t]

igraph_vector_ptr_resize = _lib.igraph_vector_ptr_resize
igraph_vector_ptr_resize.restype = handle_igraph_error_t
igraph_vector_ptr_resize.argtypes = [POINTER(igraph_vector_ptr_t), igraph_integer_t]

igraph_vector_ptr_size = _lib.igraph_vector_ptr_size
igraph_vector_ptr_size.restype = igraph_integer_t
igraph_vector_ptr_size.argtypes = [POINTER(igraph_vector_ptr_t)]

# String vector type

igraph_strvector_clear = _lib.igraph_strvector_clear
igraph_strvector_clear.restype = None
igraph_strvector_clear.argtypes = [POINTER(igraph_strvector_t)]

igraph_strvector_push_back = _lib.igraph_strvector_push_back
igraph_strvector_push_back.restype = handle_igraph_error_t
igraph_strvector_push_back.argtypes = [POINTER(igraph_strvector_t), c_char_p]

igraph_strvector_resize = _lib.igraph_strvector_resize
igraph_strvector_resize.restype = handle_igraph_error_t
igraph_strvector_resize.argtypes = [POINTER(igraph_strvector_t), igraph_integer_t]

igraph_strvector_set = _lib.igraph_strvector_set
igraph_strvector_set.restype = handle_igraph_error_t
igraph_strvector_set.argtypes = [POINTER(igraph_strvector_t), igraph_integer_t, c_char_p]

igraph_strvector_set_len = _lib.igraph_strvector_set_len
igraph_strvector_set_len.restype = handle_igraph_error_t
igraph_strvector_set_len.argtypes = [POINTER(igraph_strvector_t), igraph_integer_t, c_char_p, c_size_t]

igraph_strvector_size = _lib.igraph_strvector_size
igraph_strvector_size.restype = igraph_integer_t
igraph_strvector_size.argtypes = [POINTER(igraph_strvector_t)]

# Matrix type

igraph_matrix_init = _lib.igraph_matrix_init
igraph_matrix_init.restype = handle_igraph_error_t
igraph_matrix_init.argtypes = [
    POINTER(igraph_matrix_t),
    igraph_integer_t,
    igraph_integer_t,
]

igraph_matrix_destroy = _lib.igraph_matrix_destroy
igraph_matrix_destroy.restype = None
igraph_matrix_destroy.argtypes = [c_void_p]

igraph_matrix_init_array = _lib.igraph_matrix_init_array
igraph_matrix_init_array.restype = handle_igraph_error_t
igraph_matrix_init_array.argtypes = [
    POINTER(igraph_matrix_t),
    POINTER(igraph_real_t),
    igraph_integer_t,
    igraph_integer_t,
    c_int,
]

igraph_matrix_view = _lib.igraph_matrix_view
igraph_matrix_view.restype = POINTER(igraph_matrix_t)
igraph_matrix_view.argtypes = [
    POINTER(igraph_matrix_t),
    POINTER(igraph_real_t),
    igraph_integer_t,
    igraph_integer_t,
]

igraph_matrix_ncol = _lib.igraph_matrix_ncol
igraph_matrix_ncol.restype = igraph_integer_t
igraph_matrix_ncol.argtypes = [POINTER(igraph_matrix_t)]

igraph_matrix_nrow = _lib.igraph_matrix_nrow
igraph_matrix_nrow.restype = igraph_integer_t
igraph_matrix_nrow.argtypes = [POINTER(igraph_matrix_t)]

# Integer matrix type

igraph_matrix_int_init = _lib.igraph_matrix_int_init
igraph_matrix_int_init.restype = handle_igraph_error_t
igraph_matrix_int_init.argtypes = [
    POINTER(igraph_matrix_int_t),
    igraph_integer_t,
    igraph_integer_t,
]

igraph_matrix_int_destroy = _lib.igraph_matrix_int_destroy
igraph_matrix_int_destroy.restype = None
igraph_matrix_int_destroy.argtypes = [c_void_p]

igraph_matrix_int_init_array = _lib.igraph_matrix_int_init_array
igraph_matrix_int_init_array.restype = handle_igraph_error_t
igraph_matrix_int_init_array.argtypes = [
    POINTER(igraph_matrix_int_t),
    POINTER(igraph_integer_t),
    igraph_integer_t,
    igraph_integer_t,
    c_int,
]

igraph_matrix_int_view = _lib.igraph_matrix_int_view
igraph_matrix_int_view.restype = POINTER(igraph_matrix_int_t)
igraph_matrix_int_view.argtypes = [
    POINTER(igraph_matrix_int_t),
    POINTER(igraph_integer_t),
    igraph_integer_t,
    igraph_integer_t,
]

igraph_matrix_int_ncol = _lib.igraph_matrix_int_ncol
igraph_matrix_int_ncol.restype = igraph_integer_t
igraph_matrix_int_ncol.argtypes = [POINTER(igraph_matrix_int_t)]

igraph_matrix_int_nrow = _lib.igraph_matrix_int_nrow
igraph_matrix_int_nrow.restype = igraph_integer_t
igraph_matrix_int_nrow.argtypes = [POINTER(igraph_matrix_int_t)]

# List of vectors type

igraph_vector_list_init = _lib.igraph_vector_list_init
igraph_vector_list_init.restype = handle_igraph_error_t
igraph_vector_list_init.argtypes = [POINTER(igraph_vector_list_t), igraph_integer_t]

igraph_vector_list_destroy = _lib.igraph_vector_list_destroy
igraph_vector_list_destroy.restype = None
igraph_vector_list_destroy.argtypes = [c_void_p]

igraph_vector_list_get_ptr = _lib.igraph_vector_list_get_ptr
igraph_vector_list_get_ptr.restype = POINTER(igraph_vector_t)
igraph_vector_list_get_ptr.argtypes = [POINTER(igraph_vector_list_t), igraph_integer_t]

igraph_vector_list_push_back = _lib.igraph_vector_list_push_back
igraph_vector_list_push_back.restype = handle_igraph_error_t
igraph_vector_list_push_back.argtypes = [POINTER(igraph_vector_list_t), POINTER(igraph_vector_t)]

igraph_vector_list_size = _lib.igraph_vector_list_size
igraph_vector_list_size.restype = igraph_integer_t
igraph_vector_list_size.argtypes = [POINTER(igraph_vector_list_t)]

# List of integer vectors type

igraph_vector_int_list_init = _lib.igraph_vector_int_list_init
igraph_vector_int_list_init.restype = handle_igraph_error_t
igraph_vector_int_list_init.argtypes = [POINTER(igraph_vector_int_list_t), igraph_integer_t]

igraph_vector_int_list_destroy = _lib.igraph_vector_int_list_destroy
igraph_vector_int_list_destroy.restype = None
igraph_vector_int_list_destroy.argtypes = [c_void_p]

igraph_vector_int_list_get_ptr = _lib.igraph_vector_int_list_get_ptr
igraph_vector_int_list_get_ptr.restype = POINTER(igraph_vector_int_t)
igraph_vector_int_list_get_ptr.argtypes = [POINTER(igraph_vector_int_list_t), igraph_integer_t]

igraph_vector_int_list_push_back = _lib.igraph_vector_int_list_push_back
igraph_vector_int_list_push_back.restype = handle_igraph_error_t
igraph_vector_int_list_push_back.argtypes = [POINTER(igraph_vector_int_list_t), POINTER(igraph_vector_int_t)]

igraph_vector_int_list_size = _lib.igraph_vector_int_list_size
igraph_vector_int_list_size.restype = igraph_integer_t
igraph_vector_int_list_size.argtypes = [POINTER(igraph_vector_int_list_t)]

# Vertex selector type

igraph_vs_none = _lib.igraph_vs_none
igraph_vs_none.restype = handle_igraph_error_t
igraph_vs_none.argtypes = [POINTER(igraph_vs_t)]

igraph_vs_1 = _lib.igraph_vs_1
igraph_vs_1.restype = handle_igraph_error_t
igraph_vs_1.argtypes = [POINTER(igraph_vs_t), igraph_integer_t]

igraph_vs_all = _lib.igraph_vs_all
igraph_vs_all.restype = handle_igraph_error_t
igraph_vs_all.argtypes = [POINTER(igraph_vs_t)]

igraph_vs_as_vector = _lib.igraph_vs_as_vector
igraph_vs_as_vector.restype = handle_igraph_error_t
igraph_vs_as_vector.argtypes = [POINTER(igraph_t), igraph_vs_t, POINTER(igraph_vector_int_t)]

igraph_vs_type = _lib.igraph_vs_type
igraph_vs_type.restype = c_int
igraph_vs_type.argtypes = [POINTER(igraph_vs_t)]

igraph_vs_vector = _lib.igraph_vs_vector
igraph_vs_vector.restype = handle_igraph_error_t
igraph_vs_vector.argtypes = [POINTER(igraph_vs_t), POINTER(igraph_vector_int_t)]

igraph_vs_vector_copy = _lib.igraph_vs_vector_copy
igraph_vs_vector_copy.restype = handle_igraph_error_t
igraph_vs_vector_copy.argtypes = [POINTER(igraph_vs_t), POINTER(igraph_vector_int_t)]

igraph_vs_destroy = _lib.igraph_vs_destroy
igraph_vs_destroy.restype = None
igraph_vs_destroy.argtypes = [c_void_p]

# Edge selector type

igraph_es_none = _lib.igraph_es_none
igraph_es_none.restype = handle_igraph_error_t
igraph_es_none.argtypes = [POINTER(igraph_es_t)]

igraph_es_1 = _lib.igraph_es_1
igraph_es_1.restype = handle_igraph_error_t
igraph_es_1.argtypes = [POINTER(igraph_es_t), igraph_integer_t]

igraph_es_all = _lib.igraph_es_all
igraph_es_all.restype = handle_igraph_error_t
igraph_es_all.argtypes = [POINTER(igraph_es_t)]

igraph_es_as_vector = _lib.igraph_es_as_vector
igraph_es_as_vector.restype = handle_igraph_error_t
igraph_es_as_vector.argtypes = [POINTER(igraph_t), igraph_es_t, POINTER(igraph_vector_int_t)]

igraph_es_type = _lib.igraph_es_type
igraph_es_type.restype = c_int
igraph_es_type.argtypes = [POINTER(igraph_es_t)]

igraph_es_vector = _lib.igraph_es_vector
igraph_es_vector.restype = handle_igraph_error_t
igraph_es_vector.argtypes = [POINTER(igraph_es_t), POINTER(igraph_vector_int_t)]

igraph_es_vector_copy = _lib.igraph_es_vector_copy
igraph_es_vector_copy.restype = handle_igraph_error_t
igraph_es_vector_copy.argtypes = [POINTER(igraph_es_t), POINTER(igraph_vector_int_t)]

igraph_es_destroy = _lib.igraph_es_destroy
igraph_es_destroy.restype = None
igraph_es_destroy.argtypes = [c_void_p]

# Random number generators

igraph_rng_init = _lib.igraph_rng_init
igraph_rng_init.restype = handle_igraph_error_t
igraph_rng_init.argtypes = [POINTER(igraph_rng_t), POINTER(igraph_rng_type_t)]

igraph_rng_destroy = _lib.igraph_rng_destroy
igraph_rng_destroy.restype = None
igraph_rng_destroy.argtypes = [c_void_p]

igraph_rng_default = _lib.igraph_rng_default
igraph_rng_default.restype = POINTER(igraph_rng_t)

igraph_rng_set_default = _lib.igraph_rng_set_default
igraph_rng_set_default.restype = POINTER(igraph_rng_t)
igraph_rng_set_default.argtypes = [POINTER(igraph_rng_t)]

# Graph type

igraph_destroy = _lib.igraph_destroy
igraph_destroy.restype = None
igraph_destroy.argtypes = [POINTER(igraph_t)]

# Attributes

igraph_has_attribute_table = _lib.igraph_has_attribute_table
igraph_has_attribute_table.restype = igraph_bool_t
igraph_has_attribute_table.argtypes = []

igraph_set_attribute_table = _lib.igraph_set_attribute_table
igraph_set_attribute_table.restype = POINTER(igraph_attribute_table_t)
igraph_set_attribute_table.argtypes = [POINTER(igraph_attribute_table_t)]

igraph_attribute_combination_init = _lib.igraph_attribute_combination_init
igraph_attribute_combination_init.restype = handle_igraph_error_t
igraph_attribute_combination_init.argtypes = [POINTER(igraph_attribute_combination_t)]

igraph_attribute_combination_destroy = _lib.igraph_attribute_combination_destroy
igraph_attribute_combination_destroy.restype = None
igraph_attribute_combination_destroy.argtypes = [POINTER(igraph_attribute_combination_t)]

igraph_attribute_combination_add = _lib.igraph_attribute_combination_add
igraph_attribute_combination_add.restype = handle_igraph_error_t
igraph_attribute_combination_add.argtypes = [POINTER(igraph_attribute_combination_t), c_char_p, c_int, c_void_p]

igraph_attribute_combination_query = _lib.igraph_attribute_combination_query
igraph_attribute_combination_query.restype = handle_igraph_error_t
igraph_attribute_combination_query.argtypes = [POINTER(igraph_attribute_combination_t), c_char_p, POINTER(c_int), POINTER(c_void_p)]

igraph_attribute_record_list_get_ptr = _lib.igraph_attribute_record_list_get_ptr
igraph_attribute_record_list_get_ptr.restype = POINTER(igraph_attribute_record_t)
igraph_attribute_record_list_get_ptr.argtypes = [POINTER(igraph_attribute_record_list_t), igraph_integer_t]

igraph_attribute_record_list_size = _lib.igraph_attribute_record_list_size
igraph_attribute_record_list_size.restype = igraph_integer_t
igraph_attribute_record_list_size.argtypes = [POINTER(igraph_attribute_record_list_t)]

# Error handling and interruptions

igraph_error = _lib.igraph_error
igraph_error.restype = igraph_error_t   # this is OK; it will be called from attribute handlers in Python
igraph_error.argtypes = [c_char_p, c_char_p, c_int, igraph_error_t]

IGRAPH_FINALLY_FREE = _lib.IGRAPH_FINALLY_FREE
IGRAPH_FINALLY_FREE.restype = None
IGRAPH_FINALLY_FREE.argtypes = []

igraph_set_error_handler = _lib.igraph_set_error_handler
igraph_set_error_handler.restype = igraph_error_handler_t
igraph_set_error_handler.argtypes = [igraph_error_handler_t]

igraph_set_fatal_handler = _lib.igraph_set_fatal_handler
igraph_set_fatal_handler.restype = igraph_fatal_handler_t
igraph_set_fatal_handler.argtypes = [igraph_fatal_handler_t]

igraph_set_interruption_handler = _lib.igraph_set_interruption_handler
igraph_set_interruption_handler.restype = igraph_interruption_handler_t
igraph_set_interruption_handler.argtypes = [igraph_interruption_handler_t]

igraph_set_warning_handler = _lib.igraph_set_warning_handler
igraph_set_warning_handler.restype = igraph_warning_handler_t
igraph_set_warning_handler.argtypes = [igraph_warning_handler_t]

# The rest of this file is generated by Stimulus
# Set up aliases for all enum types

igraph_add_weights_t = c_int
igraph_adjacency_t = c_int
igraph_barabasi_algorithm_t = c_int
igraph_bliss_sh_t = c_int
igraph_chung_lu_t = c_int
igraph_coloring_greedy_t = c_int
igraph_community_comparison_t = c_int
igraph_connectedness_t = c_int
igraph_degseq_t = c_int
igraph_eigen_which_position_t = c_int
igraph_fas_algorithm_t = c_int
igraph_floyd_warshall_algorithm_t = c_int
igraph_fvs_algorithm_t = c_int
igraph_get_adjacency_t = c_int
igraph_laplacian_normalization_t = c_int
igraph_laplacian_spectral_embedding_type_t = c_int
igraph_layout_grid_t = c_int
igraph_loops_t = c_int
igraph_lpa_variant_t = c_int
igraph_mst_algorithm_t = c_int
igraph_neimode_t = c_int
igraph_pagerank_algo_t = c_int
igraph_product_t = c_int
igraph_random_tree_t = c_int
igraph_random_walk_stuck_t = c_int
igraph_realize_degseq_t = c_int
igraph_reciprocity_t = c_int
igraph_rewiring_t = c_int
igraph_root_choice_t = c_int
igraph_spincomm_update_t = c_int
igraph_spinglass_implementation_t = c_int
igraph_star_mode_t = c_int
igraph_subgraph_implementation_t = c_int
igraph_to_directed_t = c_int
igraph_to_undirected_t = c_int
igraph_transitivity_mode_t = c_int
igraph_tree_mode_t = c_int
igraph_vconn_nei_t = c_int
igraph_voronoi_tiebreaker_t = c_int
igraph_wheel_mode_t = c_int

# Set up aliases for all bitfield types

igraph_edge_type_sw_t = c_int
igraph_write_gml_sw_t = c_int

# Add argument and return types for functions imported from igraph

igraph_empty = _lib.igraph_empty
igraph_empty.restype = handle_igraph_error_t
igraph_empty.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_bool_t]

igraph_add_edges = _lib.igraph_add_edges
igraph_add_edges.restype = handle_igraph_error_t
igraph_add_edges.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_attribute_record_list_t)]

igraph_add_vertices = _lib.igraph_add_vertices
igraph_add_vertices.restype = handle_igraph_error_t
igraph_add_vertices.argtypes = [POINTER(igraph_t), igraph_integer_t, POINTER(igraph_attribute_record_list_t)]

igraph_copy = _lib.igraph_copy
igraph_copy.restype = handle_igraph_error_t
igraph_copy.argtypes = [POINTER(igraph_t), POINTER(igraph_t)]

igraph_delete_edges = _lib.igraph_delete_edges
igraph_delete_edges.restype = handle_igraph_error_t
igraph_delete_edges.argtypes = [POINTER(igraph_t), igraph_es_t]

igraph_delete_vertices = _lib.igraph_delete_vertices
igraph_delete_vertices.restype = handle_igraph_error_t
igraph_delete_vertices.argtypes = [POINTER(igraph_t), igraph_vs_t]

igraph_delete_vertices_map = _lib.igraph_delete_vertices_map
igraph_delete_vertices_map.restype = handle_igraph_error_t
igraph_delete_vertices_map.argtypes = [POINTER(igraph_t), igraph_vs_t, POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t)]

igraph_vcount = _lib.igraph_vcount
igraph_vcount.restype = igraph_integer_t
igraph_vcount.argtypes = [POINTER(igraph_t)]

igraph_ecount = _lib.igraph_ecount
igraph_ecount.restype = igraph_integer_t
igraph_ecount.argtypes = [POINTER(igraph_t)]

igraph_neighbors = _lib.igraph_neighbors
igraph_neighbors.restype = handle_igraph_error_t
igraph_neighbors.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), igraph_integer_t, igraph_neimode_t, igraph_loops_t, igraph_bool_t]

igraph_is_directed = _lib.igraph_is_directed
igraph_is_directed.restype = igraph_bool_t
igraph_is_directed.argtypes = [POINTER(igraph_t)]

igraph_degree = _lib.igraph_degree
igraph_degree.restype = handle_igraph_error_t
igraph_degree.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), igraph_vs_t, igraph_neimode_t, igraph_bool_t]

igraph_edge = _lib.igraph_edge
igraph_edge.restype = handle_igraph_error_t
igraph_edge.argtypes = [POINTER(igraph_t), igraph_integer_t, POINTER(igraph_integer_t), POINTER(igraph_integer_t)]

igraph_edges = _lib.igraph_edges
igraph_edges.restype = handle_igraph_error_t
igraph_edges.argtypes = [POINTER(igraph_t), igraph_es_t, POINTER(igraph_vector_int_t), igraph_bool_t]

igraph_get_eid = _lib.igraph_get_eid
igraph_get_eid.restype = handle_igraph_error_t
igraph_get_eid.argtypes = [POINTER(igraph_t), POINTER(igraph_integer_t), igraph_integer_t, igraph_integer_t, igraph_bool_t, igraph_bool_t]

igraph_get_eids = _lib.igraph_get_eids
igraph_get_eids.restype = handle_igraph_error_t
igraph_get_eids.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), igraph_bool_t, igraph_bool_t]

igraph_get_all_eids_between = _lib.igraph_get_all_eids_between
igraph_get_all_eids_between.restype = handle_igraph_error_t
igraph_get_all_eids_between.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), igraph_integer_t, igraph_integer_t, igraph_bool_t]

igraph_incident = _lib.igraph_incident
igraph_incident.restype = handle_igraph_error_t
igraph_incident.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), igraph_integer_t, igraph_neimode_t, igraph_loops_t]

igraph_is_same_graph = _lib.igraph_is_same_graph
igraph_is_same_graph.restype = handle_igraph_error_t
igraph_is_same_graph.argtypes = [POINTER(igraph_t), POINTER(igraph_t), POINTER(igraph_bool_t)]

igraph_create = _lib.igraph_create
igraph_create.restype = handle_igraph_error_t
igraph_create.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), igraph_integer_t, igraph_bool_t]

igraph_adjacency = _lib.igraph_adjacency
igraph_adjacency.restype = handle_igraph_error_t
igraph_adjacency.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_adjacency_t, igraph_loops_t]

igraph_sparse_adjacency = _lib.igraph_sparse_adjacency
igraph_sparse_adjacency.restype = handle_igraph_error_t
igraph_sparse_adjacency.argtypes = [POINTER(igraph_t), POINTER(igraph_sparsemat_t), igraph_adjacency_t, igraph_loops_t]

igraph_sparse_weighted_adjacency = _lib.igraph_sparse_weighted_adjacency
igraph_sparse_weighted_adjacency.restype = handle_igraph_error_t
igraph_sparse_weighted_adjacency.argtypes = [POINTER(igraph_t), POINTER(igraph_sparsemat_t), igraph_adjacency_t, POINTER(igraph_vector_t), igraph_loops_t]

igraph_weighted_adjacency = _lib.igraph_weighted_adjacency
igraph_weighted_adjacency.restype = handle_igraph_error_t
igraph_weighted_adjacency.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_adjacency_t, POINTER(igraph_vector_t), igraph_loops_t]

igraph_star = _lib.igraph_star
igraph_star.restype = handle_igraph_error_t
igraph_star.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_star_mode_t, igraph_integer_t]

igraph_wheel = _lib.igraph_wheel
igraph_wheel.restype = handle_igraph_error_t
igraph_wheel.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_wheel_mode_t, igraph_integer_t]

igraph_hypercube = _lib.igraph_hypercube
igraph_hypercube.restype = handle_igraph_error_t
igraph_hypercube.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_bool_t]

igraph_square_lattice = _lib.igraph_square_lattice
igraph_square_lattice.restype = handle_igraph_error_t
igraph_square_lattice.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), igraph_integer_t, igraph_bool_t, igraph_bool_t, POINTER(igraph_vector_bool_t)]

igraph_triangular_lattice = _lib.igraph_triangular_lattice
igraph_triangular_lattice.restype = handle_igraph_error_t
igraph_triangular_lattice.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), igraph_bool_t, igraph_bool_t]

igraph_ring = _lib.igraph_ring
igraph_ring.restype = handle_igraph_error_t
igraph_ring.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_bool_t, igraph_bool_t, igraph_bool_t]

igraph_kary_tree = _lib.igraph_kary_tree
igraph_kary_tree.restype = handle_igraph_error_t
igraph_kary_tree.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_integer_t, igraph_tree_mode_t]

igraph_symmetric_tree = _lib.igraph_symmetric_tree
igraph_symmetric_tree.restype = handle_igraph_error_t
igraph_symmetric_tree.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), igraph_tree_mode_t]

igraph_regular_tree = _lib.igraph_regular_tree
igraph_regular_tree.restype = handle_igraph_error_t
igraph_regular_tree.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_integer_t, igraph_tree_mode_t]

igraph_full = _lib.igraph_full
igraph_full.restype = handle_igraph_error_t
igraph_full.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_bool_t, igraph_bool_t]

igraph_full_citation = _lib.igraph_full_citation
igraph_full_citation.restype = handle_igraph_error_t
igraph_full_citation.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_bool_t]

igraph_atlas = _lib.igraph_atlas
igraph_atlas.restype = handle_igraph_error_t
igraph_atlas.argtypes = [POINTER(igraph_t), igraph_integer_t]

igraph_extended_chordal_ring = _lib.igraph_extended_chordal_ring
igraph_extended_chordal_ring.restype = handle_igraph_error_t
igraph_extended_chordal_ring.argtypes = [POINTER(igraph_t), igraph_integer_t, POINTER(igraph_matrix_int_t), igraph_bool_t]

igraph_connect_neighborhood = _lib.igraph_connect_neighborhood
igraph_connect_neighborhood.restype = handle_igraph_error_t
igraph_connect_neighborhood.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_neimode_t]

igraph_graph_power = _lib.igraph_graph_power
igraph_graph_power.restype = handle_igraph_error_t
igraph_graph_power.argtypes = [POINTER(igraph_t), POINTER(igraph_t), igraph_integer_t, igraph_bool_t]

igraph_linegraph = _lib.igraph_linegraph
igraph_linegraph.restype = handle_igraph_error_t
igraph_linegraph.argtypes = [POINTER(igraph_t), POINTER(igraph_t)]

igraph_de_bruijn = _lib.igraph_de_bruijn
igraph_de_bruijn.restype = handle_igraph_error_t
igraph_de_bruijn.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_integer_t]

igraph_kautz = _lib.igraph_kautz
igraph_kautz.restype = handle_igraph_error_t
igraph_kautz.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_integer_t]

igraph_famous = _lib.igraph_famous
igraph_famous.restype = handle_igraph_error_t
igraph_famous.argtypes = [POINTER(igraph_t), c_char_p]

igraph_lcf = _lib.igraph_lcf
igraph_lcf.restype = handle_igraph_error_t
igraph_lcf.argtypes = [POINTER(igraph_t), igraph_integer_t, POINTER(igraph_vector_int_t), igraph_integer_t]

igraph_adjlist = _lib.igraph_adjlist
igraph_adjlist.restype = handle_igraph_error_t
igraph_adjlist.argtypes = [POINTER(igraph_t), POINTER(igraph_adjlist_t), igraph_neimode_t, igraph_bool_t]

igraph_full_bipartite = _lib.igraph_full_bipartite
igraph_full_bipartite.restype = handle_igraph_error_t
igraph_full_bipartite.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_bool_t), igraph_integer_t, igraph_integer_t, igraph_bool_t, igraph_neimode_t]

igraph_full_multipartite = _lib.igraph_full_multipartite
igraph_full_multipartite.restype = handle_igraph_error_t
igraph_full_multipartite.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), igraph_bool_t, igraph_neimode_t]

igraph_realize_degree_sequence = _lib.igraph_realize_degree_sequence
igraph_realize_degree_sequence.restype = handle_igraph_error_t
igraph_realize_degree_sequence.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), igraph_edge_type_sw_t, igraph_realize_degseq_t]

igraph_realize_bipartite_degree_sequence = _lib.igraph_realize_bipartite_degree_sequence
igraph_realize_bipartite_degree_sequence.restype = handle_igraph_error_t
igraph_realize_bipartite_degree_sequence.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), igraph_edge_type_sw_t, igraph_realize_degseq_t]

igraph_circulant = _lib.igraph_circulant
igraph_circulant.restype = handle_igraph_error_t
igraph_circulant.argtypes = [POINTER(igraph_t), igraph_integer_t, POINTER(igraph_vector_int_t), igraph_bool_t]

igraph_generalized_petersen = _lib.igraph_generalized_petersen
igraph_generalized_petersen.restype = handle_igraph_error_t
igraph_generalized_petersen.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_integer_t]

igraph_turan = _lib.igraph_turan
igraph_turan.restype = handle_igraph_error_t
igraph_turan.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), igraph_integer_t, igraph_integer_t]

igraph_weighted_sparsemat = _lib.igraph_weighted_sparsemat
igraph_weighted_sparsemat.restype = handle_igraph_error_t
igraph_weighted_sparsemat.argtypes = [POINTER(igraph_t), POINTER(igraph_sparsemat_t), igraph_bool_t, c_char_p, igraph_bool_t]

igraph_barabasi_game = _lib.igraph_barabasi_game
igraph_barabasi_game.restype = handle_igraph_error_t
igraph_barabasi_game.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_real_t, igraph_integer_t, POINTER(igraph_vector_int_t), igraph_bool_t, igraph_real_t, igraph_bool_t, igraph_barabasi_algorithm_t, POINTER(igraph_t)]

igraph_erdos_renyi_game_gnp = _lib.igraph_erdos_renyi_game_gnp
igraph_erdos_renyi_game_gnp.restype = handle_igraph_error_t
igraph_erdos_renyi_game_gnp.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_real_t, igraph_bool_t, igraph_bool_t]

igraph_erdos_renyi_game_gnm = _lib.igraph_erdos_renyi_game_gnm
igraph_erdos_renyi_game_gnm.restype = handle_igraph_error_t
igraph_erdos_renyi_game_gnm.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_integer_t, igraph_bool_t, igraph_bool_t, igraph_bool_t]

igraph_iea_game = _lib.igraph_iea_game
igraph_iea_game.restype = handle_igraph_error_t
igraph_iea_game.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_integer_t, igraph_bool_t, igraph_bool_t]

igraph_degree_sequence_game = _lib.igraph_degree_sequence_game
igraph_degree_sequence_game.restype = handle_igraph_error_t
igraph_degree_sequence_game.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), igraph_degseq_t]

igraph_growing_random_game = _lib.igraph_growing_random_game
igraph_growing_random_game.restype = handle_igraph_error_t
igraph_growing_random_game.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_integer_t, igraph_bool_t, igraph_bool_t]

igraph_barabasi_aging_game = _lib.igraph_barabasi_aging_game
igraph_barabasi_aging_game.restype = handle_igraph_error_t
igraph_barabasi_aging_game.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_integer_t, POINTER(igraph_vector_int_t), igraph_bool_t, igraph_real_t, igraph_real_t, igraph_integer_t, igraph_real_t, igraph_real_t, igraph_real_t, igraph_real_t, igraph_bool_t]

igraph_recent_degree_game = _lib.igraph_recent_degree_game
igraph_recent_degree_game.restype = handle_igraph_error_t
igraph_recent_degree_game.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_real_t, igraph_integer_t, igraph_integer_t, POINTER(igraph_vector_int_t), igraph_bool_t, igraph_real_t, igraph_bool_t]

igraph_recent_degree_aging_game = _lib.igraph_recent_degree_aging_game
igraph_recent_degree_aging_game.restype = handle_igraph_error_t
igraph_recent_degree_aging_game.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_integer_t, POINTER(igraph_vector_int_t), igraph_bool_t, igraph_real_t, igraph_real_t, igraph_integer_t, igraph_integer_t, igraph_real_t, igraph_bool_t]

igraph_callaway_traits_game = _lib.igraph_callaway_traits_game
igraph_callaway_traits_game.restype = handle_igraph_error_t
igraph_callaway_traits_game.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_integer_t, igraph_integer_t, POINTER(igraph_vector_t), POINTER(igraph_matrix_t), igraph_bool_t, POINTER(igraph_vector_int_t)]

igraph_establishment_game = _lib.igraph_establishment_game
igraph_establishment_game.restype = handle_igraph_error_t
igraph_establishment_game.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_integer_t, igraph_integer_t, POINTER(igraph_vector_t), POINTER(igraph_matrix_t), igraph_bool_t, POINTER(igraph_vector_int_t)]

igraph_grg_game = _lib.igraph_grg_game
igraph_grg_game.restype = handle_igraph_error_t
igraph_grg_game.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_real_t, igraph_bool_t, POINTER(igraph_vector_t), POINTER(igraph_vector_t)]

igraph_preference_game = _lib.igraph_preference_game
igraph_preference_game.restype = handle_igraph_error_t
igraph_preference_game.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_integer_t, POINTER(igraph_vector_t), igraph_bool_t, POINTER(igraph_matrix_t), POINTER(igraph_vector_int_t), igraph_bool_t, igraph_bool_t]

igraph_asymmetric_preference_game = _lib.igraph_asymmetric_preference_game
igraph_asymmetric_preference_game.restype = handle_igraph_error_t
igraph_asymmetric_preference_game.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_integer_t, igraph_integer_t, POINTER(igraph_matrix_t), POINTER(igraph_matrix_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), igraph_bool_t]

igraph_rewire_edges = _lib.igraph_rewire_edges
igraph_rewire_edges.restype = handle_igraph_error_t
igraph_rewire_edges.argtypes = [POINTER(igraph_t), igraph_real_t, igraph_bool_t, igraph_bool_t]

igraph_rewire_directed_edges = _lib.igraph_rewire_directed_edges
igraph_rewire_directed_edges.restype = handle_igraph_error_t
igraph_rewire_directed_edges.argtypes = [POINTER(igraph_t), igraph_real_t, igraph_bool_t, igraph_neimode_t]

igraph_watts_strogatz_game = _lib.igraph_watts_strogatz_game
igraph_watts_strogatz_game.restype = handle_igraph_error_t
igraph_watts_strogatz_game.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_integer_t, igraph_integer_t, igraph_real_t, igraph_bool_t, igraph_bool_t]

igraph_lastcit_game = _lib.igraph_lastcit_game
igraph_lastcit_game.restype = handle_igraph_error_t
igraph_lastcit_game.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_integer_t, igraph_integer_t, POINTER(igraph_vector_t), igraph_bool_t]

igraph_cited_type_game = _lib.igraph_cited_type_game
igraph_cited_type_game.restype = handle_igraph_error_t
igraph_cited_type_game.argtypes = [POINTER(igraph_t), igraph_integer_t, POINTER(igraph_vector_int_t), POINTER(igraph_vector_t), igraph_integer_t, igraph_bool_t]

igraph_citing_cited_type_game = _lib.igraph_citing_cited_type_game
igraph_citing_cited_type_game.restype = handle_igraph_error_t
igraph_citing_cited_type_game.argtypes = [POINTER(igraph_t), igraph_integer_t, POINTER(igraph_vector_int_t), POINTER(igraph_matrix_t), igraph_integer_t, igraph_bool_t]

igraph_forest_fire_game = _lib.igraph_forest_fire_game
igraph_forest_fire_game.restype = handle_igraph_error_t
igraph_forest_fire_game.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_real_t, igraph_real_t, igraph_integer_t, igraph_bool_t]

igraph_simple_interconnected_islands_game = _lib.igraph_simple_interconnected_islands_game
igraph_simple_interconnected_islands_game.restype = handle_igraph_error_t
igraph_simple_interconnected_islands_game.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_integer_t, igraph_real_t, igraph_integer_t]

igraph_chung_lu_game = _lib.igraph_chung_lu_game
igraph_chung_lu_game.restype = handle_igraph_error_t
igraph_chung_lu_game.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t), igraph_bool_t, igraph_chung_lu_t]

igraph_static_fitness_game = _lib.igraph_static_fitness_game
igraph_static_fitness_game.restype = handle_igraph_error_t
igraph_static_fitness_game.argtypes = [POINTER(igraph_t), igraph_integer_t, POINTER(igraph_vector_t), POINTER(igraph_vector_t), igraph_bool_t, igraph_bool_t]

igraph_static_power_law_game = _lib.igraph_static_power_law_game
igraph_static_power_law_game.restype = handle_igraph_error_t
igraph_static_power_law_game.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_integer_t, igraph_real_t, igraph_real_t, igraph_bool_t, igraph_bool_t, igraph_bool_t]

igraph_k_regular_game = _lib.igraph_k_regular_game
igraph_k_regular_game.restype = handle_igraph_error_t
igraph_k_regular_game.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_integer_t, igraph_bool_t, igraph_bool_t]

igraph_sbm_game = _lib.igraph_sbm_game
igraph_sbm_game.restype = handle_igraph_error_t
igraph_sbm_game.argtypes = [POINTER(igraph_t), igraph_integer_t, POINTER(igraph_matrix_t), POINTER(igraph_vector_int_t), igraph_bool_t, igraph_bool_t]

igraph_hsbm_game = _lib.igraph_hsbm_game
igraph_hsbm_game.restype = handle_igraph_error_t
igraph_hsbm_game.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_integer_t, POINTER(igraph_vector_t), POINTER(igraph_matrix_t), igraph_real_t]

igraph_hsbm_list_game = _lib.igraph_hsbm_list_game
igraph_hsbm_list_game.restype = handle_igraph_error_t
igraph_hsbm_list_game.argtypes = [POINTER(igraph_t), igraph_integer_t, POINTER(igraph_vector_int_t), POINTER(igraph_vector_list_t), POINTER(igraph_matrix_list_t), igraph_real_t]

igraph_correlated_game = _lib.igraph_correlated_game
igraph_correlated_game.restype = handle_igraph_error_t
igraph_correlated_game.argtypes = [POINTER(igraph_t), POINTER(igraph_t), igraph_real_t, igraph_real_t, POINTER(igraph_vector_int_t)]

igraph_correlated_pair_game = _lib.igraph_correlated_pair_game
igraph_correlated_pair_game.restype = handle_igraph_error_t
igraph_correlated_pair_game.argtypes = [POINTER(igraph_t), POINTER(igraph_t), igraph_integer_t, igraph_real_t, igraph_real_t, igraph_bool_t, POINTER(igraph_vector_int_t)]

igraph_dot_product_game = _lib.igraph_dot_product_game
igraph_dot_product_game.restype = handle_igraph_error_t
igraph_dot_product_game.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_bool_t]

igraph_sample_sphere_surface = _lib.igraph_sample_sphere_surface
igraph_sample_sphere_surface.restype = handle_igraph_error_t
igraph_sample_sphere_surface.argtypes = [igraph_integer_t, igraph_integer_t, igraph_real_t, igraph_bool_t, POINTER(igraph_matrix_t)]

igraph_sample_sphere_volume = _lib.igraph_sample_sphere_volume
igraph_sample_sphere_volume.restype = handle_igraph_error_t
igraph_sample_sphere_volume.argtypes = [igraph_integer_t, igraph_integer_t, igraph_real_t, igraph_bool_t, POINTER(igraph_matrix_t)]

igraph_sample_dirichlet = _lib.igraph_sample_dirichlet
igraph_sample_dirichlet.restype = handle_igraph_error_t
igraph_sample_dirichlet.argtypes = [igraph_integer_t, POINTER(igraph_vector_t), POINTER(igraph_matrix_t)]

igraph_are_adjacent = _lib.igraph_are_adjacent
igraph_are_adjacent.restype = handle_igraph_error_t
igraph_are_adjacent.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_integer_t, POINTER(igraph_bool_t)]

igraph_diameter = _lib.igraph_diameter
igraph_diameter.restype = handle_igraph_error_t
igraph_diameter.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_real_t), POINTER(igraph_integer_t), POINTER(igraph_integer_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), igraph_bool_t, igraph_bool_t]

igraph_closeness = _lib.igraph_closeness
igraph_closeness.restype = handle_igraph_error_t
igraph_closeness.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_vector_int_t), POINTER(igraph_bool_t), igraph_vs_t, igraph_neimode_t, POINTER(igraph_vector_t), igraph_bool_t]

igraph_closeness_cutoff = _lib.igraph_closeness_cutoff
igraph_closeness_cutoff.restype = handle_igraph_error_t
igraph_closeness_cutoff.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_vector_int_t), POINTER(igraph_bool_t), igraph_vs_t, igraph_neimode_t, POINTER(igraph_vector_t), igraph_bool_t, igraph_real_t]

igraph_distances = _lib.igraph_distances
igraph_distances.restype = handle_igraph_error_t
igraph_distances.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_vs_t, igraph_vs_t, igraph_neimode_t]

igraph_distances_cutoff = _lib.igraph_distances_cutoff
igraph_distances_cutoff.restype = handle_igraph_error_t
igraph_distances_cutoff.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_vs_t, igraph_vs_t, igraph_neimode_t, igraph_real_t]

igraph_get_shortest_path = _lib.igraph_get_shortest_path
igraph_get_shortest_path.restype = handle_igraph_error_t
igraph_get_shortest_path.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), igraph_integer_t, igraph_integer_t, igraph_neimode_t]

igraph_get_shortest_path_bellman_ford = _lib.igraph_get_shortest_path_bellman_ford
igraph_get_shortest_path_bellman_ford.restype = handle_igraph_error_t
igraph_get_shortest_path_bellman_ford.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), igraph_integer_t, igraph_integer_t, POINTER(igraph_vector_t), igraph_neimode_t]

igraph_get_shortest_path_dijkstra = _lib.igraph_get_shortest_path_dijkstra
igraph_get_shortest_path_dijkstra.restype = handle_igraph_error_t
igraph_get_shortest_path_dijkstra.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), igraph_integer_t, igraph_integer_t, POINTER(igraph_vector_t), igraph_neimode_t]

igraph_get_shortest_paths = _lib.igraph_get_shortest_paths
igraph_get_shortest_paths.restype = handle_igraph_error_t
igraph_get_shortest_paths.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_list_t), POINTER(igraph_vector_int_list_t), igraph_integer_t, igraph_vs_t, igraph_neimode_t, POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t)]

igraph_get_all_shortest_paths = _lib.igraph_get_all_shortest_paths
igraph_get_all_shortest_paths.restype = handle_igraph_error_t
igraph_get_all_shortest_paths.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_list_t), POINTER(igraph_vector_int_list_t), POINTER(igraph_vector_int_t), igraph_integer_t, igraph_vs_t, igraph_neimode_t]

igraph_distances_dijkstra = _lib.igraph_distances_dijkstra
igraph_distances_dijkstra.restype = handle_igraph_error_t
igraph_distances_dijkstra.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_vs_t, igraph_vs_t, POINTER(igraph_vector_t), igraph_neimode_t]

igraph_distances_dijkstra_cutoff = _lib.igraph_distances_dijkstra_cutoff
igraph_distances_dijkstra_cutoff.restype = handle_igraph_error_t
igraph_distances_dijkstra_cutoff.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_vs_t, igraph_vs_t, POINTER(igraph_vector_t), igraph_neimode_t, igraph_real_t]

igraph_get_shortest_paths_dijkstra = _lib.igraph_get_shortest_paths_dijkstra
igraph_get_shortest_paths_dijkstra.restype = handle_igraph_error_t
igraph_get_shortest_paths_dijkstra.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_list_t), POINTER(igraph_vector_int_list_t), igraph_integer_t, igraph_vs_t, POINTER(igraph_vector_t), igraph_neimode_t, POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t)]

igraph_get_shortest_paths_bellman_ford = _lib.igraph_get_shortest_paths_bellman_ford
igraph_get_shortest_paths_bellman_ford.restype = handle_igraph_error_t
igraph_get_shortest_paths_bellman_ford.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_list_t), POINTER(igraph_vector_int_list_t), igraph_integer_t, igraph_vs_t, POINTER(igraph_vector_t), igraph_neimode_t, POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t)]

igraph_get_all_shortest_paths_dijkstra = _lib.igraph_get_all_shortest_paths_dijkstra
igraph_get_all_shortest_paths_dijkstra.restype = handle_igraph_error_t
igraph_get_all_shortest_paths_dijkstra.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_list_t), POINTER(igraph_vector_int_list_t), POINTER(igraph_vector_int_t), igraph_integer_t, igraph_vs_t, POINTER(igraph_vector_t), igraph_neimode_t]

igraph_distances_bellman_ford = _lib.igraph_distances_bellman_ford
igraph_distances_bellman_ford.restype = handle_igraph_error_t
igraph_distances_bellman_ford.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_vs_t, igraph_vs_t, POINTER(igraph_vector_t), igraph_neimode_t]

igraph_distances_johnson = _lib.igraph_distances_johnson
igraph_distances_johnson.restype = handle_igraph_error_t
igraph_distances_johnson.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_vs_t, igraph_vs_t, POINTER(igraph_vector_t), igraph_neimode_t]

igraph_distances_floyd_warshall = _lib.igraph_distances_floyd_warshall
igraph_distances_floyd_warshall.restype = handle_igraph_error_t
igraph_distances_floyd_warshall.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_vs_t, igraph_vs_t, POINTER(igraph_vector_t), igraph_neimode_t, igraph_floyd_warshall_algorithm_t]

igraph_voronoi = _lib.igraph_voronoi
igraph_voronoi.restype = handle_igraph_error_t
igraph_voronoi.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_t), igraph_neimode_t, igraph_voronoi_tiebreaker_t]

igraph_get_all_simple_paths = _lib.igraph_get_all_simple_paths
igraph_get_all_simple_paths.restype = handle_igraph_error_t
igraph_get_all_simple_paths.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_list_t), igraph_integer_t, igraph_vs_t, igraph_integer_t, igraph_integer_t, igraph_neimode_t]

igraph_get_k_shortest_paths = _lib.igraph_get_k_shortest_paths
igraph_get_k_shortest_paths.restype = handle_igraph_error_t
igraph_get_k_shortest_paths.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_vector_int_list_t), POINTER(igraph_vector_int_list_t), igraph_integer_t, igraph_integer_t, igraph_integer_t, igraph_neimode_t]

igraph_get_widest_path = _lib.igraph_get_widest_path
igraph_get_widest_path.restype = handle_igraph_error_t
igraph_get_widest_path.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), igraph_integer_t, igraph_integer_t, POINTER(igraph_vector_t), igraph_neimode_t]

igraph_get_widest_paths = _lib.igraph_get_widest_paths
igraph_get_widest_paths.restype = handle_igraph_error_t
igraph_get_widest_paths.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_list_t), POINTER(igraph_vector_int_list_t), igraph_integer_t, igraph_vs_t, POINTER(igraph_vector_t), igraph_neimode_t, POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t)]

igraph_widest_path_widths_dijkstra = _lib.igraph_widest_path_widths_dijkstra
igraph_widest_path_widths_dijkstra.restype = handle_igraph_error_t
igraph_widest_path_widths_dijkstra.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_vs_t, igraph_vs_t, POINTER(igraph_vector_t), igraph_neimode_t]

igraph_widest_path_widths_floyd_warshall = _lib.igraph_widest_path_widths_floyd_warshall
igraph_widest_path_widths_floyd_warshall.restype = handle_igraph_error_t
igraph_widest_path_widths_floyd_warshall.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_vs_t, igraph_vs_t, POINTER(igraph_vector_t), igraph_neimode_t]

igraph_spanner = _lib.igraph_spanner
igraph_spanner.restype = handle_igraph_error_t
igraph_spanner.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), igraph_real_t, POINTER(igraph_vector_t)]

igraph_subcomponent = _lib.igraph_subcomponent
igraph_subcomponent.restype = handle_igraph_error_t
igraph_subcomponent.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), igraph_integer_t, igraph_neimode_t]

igraph_betweenness = _lib.igraph_betweenness
igraph_betweenness.restype = handle_igraph_error_t
igraph_betweenness.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), igraph_vs_t, igraph_bool_t, POINTER(igraph_vector_t)]

igraph_betweenness_cutoff = _lib.igraph_betweenness_cutoff
igraph_betweenness_cutoff.restype = handle_igraph_error_t
igraph_betweenness_cutoff.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), igraph_vs_t, igraph_bool_t, POINTER(igraph_vector_t), igraph_real_t]

igraph_betweenness_subset = _lib.igraph_betweenness_subset
igraph_betweenness_subset.restype = handle_igraph_error_t
igraph_betweenness_subset.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), igraph_vs_t, igraph_bool_t, igraph_vs_t, igraph_vs_t, POINTER(igraph_vector_t)]

igraph_edge_betweenness = _lib.igraph_edge_betweenness
igraph_edge_betweenness.restype = handle_igraph_error_t
igraph_edge_betweenness.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), igraph_bool_t, POINTER(igraph_vector_t)]

igraph_edge_betweenness_cutoff = _lib.igraph_edge_betweenness_cutoff
igraph_edge_betweenness_cutoff.restype = handle_igraph_error_t
igraph_edge_betweenness_cutoff.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), igraph_bool_t, POINTER(igraph_vector_t), igraph_real_t]

igraph_edge_betweenness_subset = _lib.igraph_edge_betweenness_subset
igraph_edge_betweenness_subset.restype = handle_igraph_error_t
igraph_edge_betweenness_subset.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), igraph_es_t, igraph_bool_t, igraph_vs_t, igraph_vs_t, POINTER(igraph_vector_t)]

igraph_harmonic_centrality = _lib.igraph_harmonic_centrality
igraph_harmonic_centrality.restype = handle_igraph_error_t
igraph_harmonic_centrality.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), igraph_vs_t, igraph_neimode_t, POINTER(igraph_vector_t), igraph_bool_t]

igraph_harmonic_centrality_cutoff = _lib.igraph_harmonic_centrality_cutoff
igraph_harmonic_centrality_cutoff.restype = handle_igraph_error_t
igraph_harmonic_centrality_cutoff.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), igraph_vs_t, igraph_neimode_t, POINTER(igraph_vector_t), igraph_bool_t, igraph_real_t]

igraph_pagerank = _lib.igraph_pagerank
igraph_pagerank.restype = handle_igraph_error_t
igraph_pagerank.argtypes = [POINTER(igraph_t), igraph_pagerank_algo_t, POINTER(igraph_vector_t), POINTER(igraph_real_t), igraph_vs_t, igraph_bool_t, igraph_real_t, POINTER(igraph_vector_t), POINTER(igraph_arpack_options_t)]

igraph_personalized_pagerank = _lib.igraph_personalized_pagerank
igraph_personalized_pagerank.restype = handle_igraph_error_t
igraph_personalized_pagerank.argtypes = [POINTER(igraph_t), igraph_pagerank_algo_t, POINTER(igraph_vector_t), POINTER(igraph_real_t), igraph_vs_t, igraph_bool_t, igraph_real_t, POINTER(igraph_vector_t), POINTER(igraph_vector_t), POINTER(igraph_arpack_options_t)]

igraph_personalized_pagerank_vs = _lib.igraph_personalized_pagerank_vs
igraph_personalized_pagerank_vs.restype = handle_igraph_error_t
igraph_personalized_pagerank_vs.argtypes = [POINTER(igraph_t), igraph_pagerank_algo_t, POINTER(igraph_vector_t), POINTER(igraph_real_t), igraph_vs_t, igraph_bool_t, igraph_real_t, igraph_vs_t, POINTER(igraph_vector_t), POINTER(igraph_arpack_options_t)]

igraph_rewire = _lib.igraph_rewire
igraph_rewire.restype = handle_igraph_error_t
igraph_rewire.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_rewiring_t]

igraph_induced_subgraph = _lib.igraph_induced_subgraph
igraph_induced_subgraph.restype = handle_igraph_error_t
igraph_induced_subgraph.argtypes = [POINTER(igraph_t), POINTER(igraph_t), igraph_vs_t, igraph_subgraph_implementation_t]

igraph_subgraph_from_edges = _lib.igraph_subgraph_from_edges
igraph_subgraph_from_edges.restype = handle_igraph_error_t
igraph_subgraph_from_edges.argtypes = [POINTER(igraph_t), POINTER(igraph_t), igraph_es_t, igraph_bool_t]

igraph_reverse_edges = _lib.igraph_reverse_edges
igraph_reverse_edges.restype = handle_igraph_error_t
igraph_reverse_edges.argtypes = [POINTER(igraph_t), igraph_es_t]

igraph_average_path_length = _lib.igraph_average_path_length
igraph_average_path_length.restype = handle_igraph_error_t
igraph_average_path_length.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_real_t), POINTER(igraph_real_t), igraph_bool_t, igraph_bool_t]

igraph_path_length_hist = _lib.igraph_path_length_hist
igraph_path_length_hist.restype = handle_igraph_error_t
igraph_path_length_hist.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_real_t), igraph_bool_t]

igraph_simplify = _lib.igraph_simplify
igraph_simplify.restype = handle_igraph_error_t
igraph_simplify.argtypes = [POINTER(igraph_t), igraph_bool_t, igraph_bool_t, POINTER(igraph_attribute_combination_t)]

igraph_transitivity_undirected = _lib.igraph_transitivity_undirected
igraph_transitivity_undirected.restype = handle_igraph_error_t
igraph_transitivity_undirected.argtypes = [POINTER(igraph_t), POINTER(igraph_real_t), igraph_transitivity_mode_t]

igraph_transitivity_local_undirected = _lib.igraph_transitivity_local_undirected
igraph_transitivity_local_undirected.restype = handle_igraph_error_t
igraph_transitivity_local_undirected.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), igraph_vs_t, igraph_transitivity_mode_t]

igraph_transitivity_avglocal_undirected = _lib.igraph_transitivity_avglocal_undirected
igraph_transitivity_avglocal_undirected.restype = handle_igraph_error_t
igraph_transitivity_avglocal_undirected.argtypes = [POINTER(igraph_t), POINTER(igraph_real_t), igraph_transitivity_mode_t]

igraph_transitivity_barrat = _lib.igraph_transitivity_barrat
igraph_transitivity_barrat.restype = handle_igraph_error_t
igraph_transitivity_barrat.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), igraph_vs_t, POINTER(igraph_vector_t), igraph_transitivity_mode_t]

igraph_ecc = _lib.igraph_ecc
igraph_ecc.restype = handle_igraph_error_t
igraph_ecc.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), igraph_es_t, igraph_integer_t, igraph_bool_t, igraph_bool_t]

igraph_reciprocity = _lib.igraph_reciprocity
igraph_reciprocity.restype = handle_igraph_error_t
igraph_reciprocity.argtypes = [POINTER(igraph_t), POINTER(igraph_real_t), igraph_bool_t, igraph_reciprocity_t]

igraph_constraint = _lib.igraph_constraint
igraph_constraint.restype = handle_igraph_error_t
igraph_constraint.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), igraph_vs_t, POINTER(igraph_vector_t)]

igraph_maxdegree = _lib.igraph_maxdegree
igraph_maxdegree.restype = handle_igraph_error_t
igraph_maxdegree.argtypes = [POINTER(igraph_t), POINTER(igraph_integer_t), igraph_vs_t, igraph_neimode_t, igraph_bool_t]

igraph_density = _lib.igraph_density
igraph_density.restype = handle_igraph_error_t
igraph_density.argtypes = [POINTER(igraph_t), POINTER(igraph_real_t), igraph_bool_t]

igraph_mean_degree = _lib.igraph_mean_degree
igraph_mean_degree.restype = handle_igraph_error_t
igraph_mean_degree.argtypes = [POINTER(igraph_t), POINTER(igraph_real_t), igraph_bool_t]

igraph_neighborhood_size = _lib.igraph_neighborhood_size
igraph_neighborhood_size.restype = handle_igraph_error_t
igraph_neighborhood_size.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), igraph_vs_t, igraph_integer_t, igraph_neimode_t, igraph_integer_t]

igraph_neighborhood = _lib.igraph_neighborhood
igraph_neighborhood.restype = handle_igraph_error_t
igraph_neighborhood.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_list_t), igraph_vs_t, igraph_integer_t, igraph_neimode_t, igraph_integer_t]

igraph_neighborhood_graphs = _lib.igraph_neighborhood_graphs
igraph_neighborhood_graphs.restype = handle_igraph_error_t
igraph_neighborhood_graphs.argtypes = [POINTER(igraph_t), POINTER(igraph_graph_list_t), igraph_vs_t, igraph_integer_t, igraph_neimode_t, igraph_integer_t]

igraph_topological_sorting = _lib.igraph_topological_sorting
igraph_topological_sorting.restype = handle_igraph_error_t
igraph_topological_sorting.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), igraph_neimode_t]

igraph_feedback_arc_set = _lib.igraph_feedback_arc_set
igraph_feedback_arc_set.restype = handle_igraph_error_t
igraph_feedback_arc_set.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_t), igraph_fas_algorithm_t]

igraph_feedback_vertex_set = _lib.igraph_feedback_vertex_set
igraph_feedback_vertex_set.restype = handle_igraph_error_t
igraph_feedback_vertex_set.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_t), igraph_fvs_algorithm_t]

igraph_is_loop = _lib.igraph_is_loop
igraph_is_loop.restype = handle_igraph_error_t
igraph_is_loop.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_bool_t), igraph_es_t]

igraph_is_dag = _lib.igraph_is_dag
igraph_is_dag.restype = handle_igraph_error_t
igraph_is_dag.argtypes = [POINTER(igraph_t), POINTER(igraph_bool_t)]

igraph_is_acyclic = _lib.igraph_is_acyclic
igraph_is_acyclic.restype = handle_igraph_error_t
igraph_is_acyclic.argtypes = [POINTER(igraph_t), POINTER(igraph_bool_t)]

igraph_is_simple = _lib.igraph_is_simple
igraph_is_simple.restype = handle_igraph_error_t
igraph_is_simple.argtypes = [POINTER(igraph_t), POINTER(igraph_bool_t)]

igraph_is_multiple = _lib.igraph_is_multiple
igraph_is_multiple.restype = handle_igraph_error_t
igraph_is_multiple.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_bool_t), igraph_es_t]

igraph_has_loop = _lib.igraph_has_loop
igraph_has_loop.restype = handle_igraph_error_t
igraph_has_loop.argtypes = [POINTER(igraph_t), POINTER(igraph_bool_t)]

igraph_has_multiple = _lib.igraph_has_multiple
igraph_has_multiple.restype = handle_igraph_error_t
igraph_has_multiple.argtypes = [POINTER(igraph_t), POINTER(igraph_bool_t)]

igraph_count_loops = _lib.igraph_count_loops
igraph_count_loops.restype = handle_igraph_error_t
igraph_count_loops.argtypes = [POINTER(igraph_t), POINTER(igraph_integer_t)]

igraph_count_multiple = _lib.igraph_count_multiple
igraph_count_multiple.restype = handle_igraph_error_t
igraph_count_multiple.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), igraph_es_t]

igraph_girth = _lib.igraph_girth
igraph_girth.restype = handle_igraph_error_t
igraph_girth.argtypes = [POINTER(igraph_t), POINTER(igraph_real_t), POINTER(igraph_vector_int_t)]

igraph_is_perfect = _lib.igraph_is_perfect
igraph_is_perfect.restype = handle_igraph_error_t
igraph_is_perfect.argtypes = [POINTER(igraph_t), POINTER(igraph_bool_t)]

igraph_add_edge = _lib.igraph_add_edge
igraph_add_edge.restype = handle_igraph_error_t
igraph_add_edge.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_integer_t]

igraph_eigenvector_centrality = _lib.igraph_eigenvector_centrality
igraph_eigenvector_centrality.restype = handle_igraph_error_t
igraph_eigenvector_centrality.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_real_t), igraph_neimode_t, POINTER(igraph_vector_t), POINTER(igraph_arpack_options_t)]

igraph_hub_and_authority_scores = _lib.igraph_hub_and_authority_scores
igraph_hub_and_authority_scores.restype = handle_igraph_error_t
igraph_hub_and_authority_scores.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t), POINTER(igraph_real_t), POINTER(igraph_vector_t), POINTER(igraph_arpack_options_t)]

igraph_unfold_tree = _lib.igraph_unfold_tree
igraph_unfold_tree.restype = handle_igraph_error_t
igraph_unfold_tree.argtypes = [POINTER(igraph_t), POINTER(igraph_t), igraph_neimode_t, POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t)]

igraph_is_mutual = _lib.igraph_is_mutual
igraph_is_mutual.restype = handle_igraph_error_t
igraph_is_mutual.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_bool_t), igraph_es_t, igraph_bool_t]

igraph_has_mutual = _lib.igraph_has_mutual
igraph_has_mutual.restype = handle_igraph_error_t
igraph_has_mutual.argtypes = [POINTER(igraph_t), POINTER(igraph_bool_t), igraph_bool_t]

igraph_maximum_cardinality_search = _lib.igraph_maximum_cardinality_search
igraph_maximum_cardinality_search.restype = handle_igraph_error_t
igraph_maximum_cardinality_search.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t)]

igraph_is_chordal = _lib.igraph_is_chordal
igraph_is_chordal.restype = handle_igraph_error_t
igraph_is_chordal.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_bool_t), POINTER(igraph_vector_int_t), POINTER(igraph_t)]

igraph_avg_nearest_neighbor_degree = _lib.igraph_avg_nearest_neighbor_degree
igraph_avg_nearest_neighbor_degree.restype = handle_igraph_error_t
igraph_avg_nearest_neighbor_degree.argtypes = [POINTER(igraph_t), igraph_vs_t, igraph_neimode_t, igraph_neimode_t, POINTER(igraph_vector_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t)]

igraph_degree_correlation_vector = _lib.igraph_degree_correlation_vector
igraph_degree_correlation_vector.restype = handle_igraph_error_t
igraph_degree_correlation_vector.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t), igraph_neimode_t, igraph_neimode_t, igraph_bool_t]

igraph_strength = _lib.igraph_strength
igraph_strength.restype = handle_igraph_error_t
igraph_strength.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), igraph_vs_t, igraph_neimode_t, igraph_bool_t, POINTER(igraph_vector_t)]

igraph_centralization = _lib.igraph_centralization
igraph_centralization.restype = igraph_real_t
igraph_centralization.argtypes = [POINTER(igraph_vector_t), igraph_real_t, igraph_bool_t]

igraph_centralization_degree = _lib.igraph_centralization_degree
igraph_centralization_degree.restype = handle_igraph_error_t
igraph_centralization_degree.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), igraph_neimode_t, igraph_bool_t, POINTER(igraph_real_t), POINTER(igraph_real_t), igraph_bool_t]

igraph_centralization_degree_tmax = _lib.igraph_centralization_degree_tmax
igraph_centralization_degree_tmax.restype = handle_igraph_error_t
igraph_centralization_degree_tmax.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_neimode_t, igraph_bool_t, POINTER(igraph_real_t)]

igraph_centralization_betweenness = _lib.igraph_centralization_betweenness
igraph_centralization_betweenness.restype = handle_igraph_error_t
igraph_centralization_betweenness.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), igraph_bool_t, POINTER(igraph_real_t), POINTER(igraph_real_t), igraph_bool_t]

igraph_centralization_betweenness_tmax = _lib.igraph_centralization_betweenness_tmax
igraph_centralization_betweenness_tmax.restype = handle_igraph_error_t
igraph_centralization_betweenness_tmax.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_bool_t, POINTER(igraph_real_t)]

igraph_centralization_closeness = _lib.igraph_centralization_closeness
igraph_centralization_closeness.restype = handle_igraph_error_t
igraph_centralization_closeness.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), igraph_neimode_t, POINTER(igraph_real_t), POINTER(igraph_real_t), igraph_bool_t]

igraph_centralization_closeness_tmax = _lib.igraph_centralization_closeness_tmax
igraph_centralization_closeness_tmax.restype = handle_igraph_error_t
igraph_centralization_closeness_tmax.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_neimode_t, POINTER(igraph_real_t)]

igraph_centralization_eigenvector_centrality = _lib.igraph_centralization_eigenvector_centrality
igraph_centralization_eigenvector_centrality.restype = handle_igraph_error_t
igraph_centralization_eigenvector_centrality.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_real_t), igraph_neimode_t, POINTER(igraph_arpack_options_t), POINTER(igraph_real_t), POINTER(igraph_real_t), igraph_bool_t]

igraph_centralization_eigenvector_centrality_tmax = _lib.igraph_centralization_eigenvector_centrality_tmax
igraph_centralization_eigenvector_centrality_tmax.restype = handle_igraph_error_t
igraph_centralization_eigenvector_centrality_tmax.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_neimode_t, POINTER(igraph_real_t)]

igraph_assortativity_nominal = _lib.igraph_assortativity_nominal
igraph_assortativity_nominal.restype = handle_igraph_error_t
igraph_assortativity_nominal.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_real_t), igraph_bool_t, igraph_bool_t]

igraph_assortativity = _lib.igraph_assortativity
igraph_assortativity.restype = handle_igraph_error_t
igraph_assortativity.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t), POINTER(igraph_real_t), igraph_bool_t, igraph_bool_t]

igraph_assortativity_degree = _lib.igraph_assortativity_degree
igraph_assortativity_degree.restype = handle_igraph_error_t
igraph_assortativity_degree.argtypes = [POINTER(igraph_t), POINTER(igraph_real_t), igraph_bool_t]

igraph_joint_degree_matrix = _lib.igraph_joint_degree_matrix
igraph_joint_degree_matrix.restype = handle_igraph_error_t
igraph_joint_degree_matrix.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_matrix_t), igraph_integer_t, igraph_integer_t]

igraph_joint_degree_distribution = _lib.igraph_joint_degree_distribution
igraph_joint_degree_distribution.restype = handle_igraph_error_t
igraph_joint_degree_distribution.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_matrix_t), igraph_neimode_t, igraph_neimode_t, igraph_bool_t, igraph_bool_t, igraph_integer_t, igraph_integer_t]

igraph_joint_type_distribution = _lib.igraph_joint_type_distribution
igraph_joint_type_distribution.restype = handle_igraph_error_t
igraph_joint_type_distribution.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_matrix_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), igraph_bool_t, igraph_bool_t]

igraph_contract_vertices = _lib.igraph_contract_vertices
igraph_contract_vertices.restype = handle_igraph_error_t
igraph_contract_vertices.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_attribute_combination_t)]

igraph_eccentricity = _lib.igraph_eccentricity
igraph_eccentricity.restype = handle_igraph_error_t
igraph_eccentricity.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t), igraph_vs_t, igraph_neimode_t]

igraph_graph_center = _lib.igraph_graph_center
igraph_graph_center.restype = handle_igraph_error_t
igraph_graph_center.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_vector_int_t), igraph_neimode_t]

igraph_radius = _lib.igraph_radius
igraph_radius.restype = handle_igraph_error_t
igraph_radius.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_real_t), igraph_neimode_t]

igraph_pseudo_diameter = _lib.igraph_pseudo_diameter
igraph_pseudo_diameter.restype = handle_igraph_error_t
igraph_pseudo_diameter.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_real_t), igraph_integer_t, POINTER(igraph_integer_t), POINTER(igraph_integer_t), igraph_bool_t, igraph_bool_t]

igraph_diversity = _lib.igraph_diversity
igraph_diversity.restype = handle_igraph_error_t
igraph_diversity.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t), igraph_vs_t]

igraph_random_walk = _lib.igraph_random_walk
igraph_random_walk.restype = handle_igraph_error_t
igraph_random_walk.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), igraph_integer_t, igraph_neimode_t, igraph_integer_t, igraph_random_walk_stuck_t]

igraph_global_efficiency = _lib.igraph_global_efficiency
igraph_global_efficiency.restype = handle_igraph_error_t
igraph_global_efficiency.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_real_t), igraph_bool_t]

igraph_local_efficiency = _lib.igraph_local_efficiency
igraph_local_efficiency.restype = handle_igraph_error_t
igraph_local_efficiency.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t), igraph_vs_t, igraph_bool_t, igraph_neimode_t]

igraph_average_local_efficiency = _lib.igraph_average_local_efficiency
igraph_average_local_efficiency.restype = handle_igraph_error_t
igraph_average_local_efficiency.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_real_t), igraph_bool_t, igraph_neimode_t]

igraph_transitive_closure = _lib.igraph_transitive_closure
igraph_transitive_closure.restype = handle_igraph_error_t
igraph_transitive_closure.argtypes = [POINTER(igraph_t), POINTER(igraph_t)]

igraph_trussness = _lib.igraph_trussness
igraph_trussness.restype = handle_igraph_error_t
igraph_trussness.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t)]

igraph_is_bigraphical = _lib.igraph_is_bigraphical
igraph_is_bigraphical.restype = handle_igraph_error_t
igraph_is_bigraphical.argtypes = [POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), igraph_edge_type_sw_t, POINTER(igraph_bool_t)]

igraph_is_graphical = _lib.igraph_is_graphical
igraph_is_graphical.restype = handle_igraph_error_t
igraph_is_graphical.argtypes = [POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), igraph_edge_type_sw_t, POINTER(igraph_bool_t)]

igraph_bfs_simple = _lib.igraph_bfs_simple
igraph_bfs_simple.restype = handle_igraph_error_t
igraph_bfs_simple.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_neimode_t, POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t)]

igraph_bipartite_projection_size = _lib.igraph_bipartite_projection_size
igraph_bipartite_projection_size.restype = handle_igraph_error_t
igraph_bipartite_projection_size.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_bool_t), POINTER(igraph_integer_t), POINTER(igraph_integer_t), POINTER(igraph_integer_t), POINTER(igraph_integer_t)]

igraph_bipartite_projection = _lib.igraph_bipartite_projection
igraph_bipartite_projection.restype = handle_igraph_error_t
igraph_bipartite_projection.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_bool_t), POINTER(igraph_t), POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), igraph_integer_t]

igraph_create_bipartite = _lib.igraph_create_bipartite
igraph_create_bipartite.restype = handle_igraph_error_t
igraph_create_bipartite.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_bool_t), POINTER(igraph_vector_int_t), igraph_bool_t]

igraph_biadjacency = _lib.igraph_biadjacency
igraph_biadjacency.restype = handle_igraph_error_t
igraph_biadjacency.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_bool_t), POINTER(igraph_matrix_t), igraph_bool_t, igraph_neimode_t, igraph_bool_t]

igraph_weighted_biadjacency = _lib.igraph_weighted_biadjacency
igraph_weighted_biadjacency.restype = handle_igraph_error_t
igraph_weighted_biadjacency.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_bool_t), POINTER(igraph_vector_t), POINTER(igraph_matrix_t), igraph_bool_t, igraph_neimode_t]

igraph_get_biadjacency = _lib.igraph_get_biadjacency
igraph_get_biadjacency.restype = handle_igraph_error_t
igraph_get_biadjacency.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_bool_t), POINTER(igraph_vector_t), POINTER(igraph_matrix_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t)]

igraph_is_bipartite = _lib.igraph_is_bipartite
igraph_is_bipartite.restype = handle_igraph_error_t
igraph_is_bipartite.argtypes = [POINTER(igraph_t), POINTER(igraph_bool_t), POINTER(igraph_vector_bool_t)]

igraph_bipartite_game_gnp = _lib.igraph_bipartite_game_gnp
igraph_bipartite_game_gnp.restype = handle_igraph_error_t
igraph_bipartite_game_gnp.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_bool_t), igraph_integer_t, igraph_integer_t, igraph_real_t, igraph_bool_t, igraph_neimode_t]

igraph_bipartite_game_gnm = _lib.igraph_bipartite_game_gnm
igraph_bipartite_game_gnm.restype = handle_igraph_error_t
igraph_bipartite_game_gnm.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_bool_t), igraph_integer_t, igraph_integer_t, igraph_integer_t, igraph_bool_t, igraph_neimode_t, igraph_bool_t]

igraph_bipartite_iea_game = _lib.igraph_bipartite_iea_game
igraph_bipartite_iea_game.restype = handle_igraph_error_t
igraph_bipartite_iea_game.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_bool_t), igraph_integer_t, igraph_integer_t, igraph_integer_t, igraph_bool_t, igraph_neimode_t]

igraph_get_laplacian = _lib.igraph_get_laplacian
igraph_get_laplacian.restype = handle_igraph_error_t
igraph_get_laplacian.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_neimode_t, igraph_laplacian_normalization_t, POINTER(igraph_vector_t)]

igraph_get_laplacian_sparse = _lib.igraph_get_laplacian_sparse
igraph_get_laplacian_sparse.restype = handle_igraph_error_t
igraph_get_laplacian_sparse.argtypes = [POINTER(igraph_t), POINTER(igraph_sparsemat_t), igraph_neimode_t, igraph_laplacian_normalization_t, POINTER(igraph_vector_t)]

igraph_connected_components = _lib.igraph_connected_components
igraph_connected_components.restype = handle_igraph_error_t
igraph_connected_components.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_integer_t), igraph_connectedness_t]

igraph_is_connected = _lib.igraph_is_connected
igraph_is_connected.restype = handle_igraph_error_t
igraph_is_connected.argtypes = [POINTER(igraph_t), POINTER(igraph_bool_t), igraph_connectedness_t]

igraph_decompose = _lib.igraph_decompose
igraph_decompose.restype = handle_igraph_error_t
igraph_decompose.argtypes = [POINTER(igraph_t), POINTER(igraph_graph_list_t), igraph_connectedness_t, igraph_integer_t, igraph_integer_t]

igraph_articulation_points = _lib.igraph_articulation_points
igraph_articulation_points.restype = handle_igraph_error_t
igraph_articulation_points.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t)]

igraph_biconnected_components = _lib.igraph_biconnected_components
igraph_biconnected_components.restype = handle_igraph_error_t
igraph_biconnected_components.argtypes = [POINTER(igraph_t), POINTER(igraph_integer_t), POINTER(igraph_vector_int_list_t), POINTER(igraph_vector_int_list_t), POINTER(igraph_vector_int_list_t), POINTER(igraph_vector_int_t)]

igraph_bridges = _lib.igraph_bridges
igraph_bridges.restype = handle_igraph_error_t
igraph_bridges.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t)]

igraph_is_biconnected = _lib.igraph_is_biconnected
igraph_is_biconnected.restype = handle_igraph_error_t
igraph_is_biconnected.argtypes = [POINTER(igraph_t), POINTER(igraph_bool_t)]

igraph_count_reachable = _lib.igraph_count_reachable
igraph_count_reachable.restype = handle_igraph_error_t
igraph_count_reachable.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), igraph_neimode_t]

igraph_is_clique = _lib.igraph_is_clique
igraph_is_clique.restype = handle_igraph_error_t
igraph_is_clique.argtypes = [POINTER(igraph_t), igraph_vs_t, igraph_bool_t, POINTER(igraph_bool_t)]

igraph_cliques = _lib.igraph_cliques
igraph_cliques.restype = handle_igraph_error_t
igraph_cliques.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_list_t), igraph_integer_t, igraph_integer_t]

igraph_clique_size_hist = _lib.igraph_clique_size_hist
igraph_clique_size_hist.restype = handle_igraph_error_t
igraph_clique_size_hist.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), igraph_integer_t, igraph_integer_t]

igraph_largest_cliques = _lib.igraph_largest_cliques
igraph_largest_cliques.restype = handle_igraph_error_t
igraph_largest_cliques.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_list_t)]

igraph_maximal_cliques = _lib.igraph_maximal_cliques
igraph_maximal_cliques.restype = handle_igraph_error_t
igraph_maximal_cliques.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_list_t), igraph_integer_t, igraph_integer_t]

igraph_maximal_cliques_subset = _lib.igraph_maximal_cliques_subset
igraph_maximal_cliques_subset.restype = handle_igraph_error_t
igraph_maximal_cliques_subset.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_list_t), POINTER(igraph_integer_t), POINTER(FILE), igraph_integer_t, igraph_integer_t]

igraph_maximal_cliques_count = _lib.igraph_maximal_cliques_count
igraph_maximal_cliques_count.restype = handle_igraph_error_t
igraph_maximal_cliques_count.argtypes = [POINTER(igraph_t), POINTER(igraph_integer_t), igraph_integer_t, igraph_integer_t]

igraph_maximal_cliques_file = _lib.igraph_maximal_cliques_file
igraph_maximal_cliques_file.restype = handle_igraph_error_t
igraph_maximal_cliques_file.argtypes = [POINTER(igraph_t), POINTER(FILE), igraph_integer_t, igraph_integer_t]

igraph_maximal_cliques_hist = _lib.igraph_maximal_cliques_hist
igraph_maximal_cliques_hist.restype = handle_igraph_error_t
igraph_maximal_cliques_hist.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), igraph_integer_t, igraph_integer_t]

igraph_clique_number = _lib.igraph_clique_number
igraph_clique_number.restype = handle_igraph_error_t
igraph_clique_number.argtypes = [POINTER(igraph_t), POINTER(igraph_integer_t)]

igraph_weighted_cliques = _lib.igraph_weighted_cliques
igraph_weighted_cliques.restype = handle_igraph_error_t
igraph_weighted_cliques.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_vector_int_list_t), igraph_real_t, igraph_real_t, igraph_bool_t]

igraph_largest_weighted_cliques = _lib.igraph_largest_weighted_cliques
igraph_largest_weighted_cliques.restype = handle_igraph_error_t
igraph_largest_weighted_cliques.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_vector_int_list_t)]

igraph_weighted_clique_number = _lib.igraph_weighted_clique_number
igraph_weighted_clique_number.restype = handle_igraph_error_t
igraph_weighted_clique_number.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_real_t)]

igraph_is_independent_vertex_set = _lib.igraph_is_independent_vertex_set
igraph_is_independent_vertex_set.restype = handle_igraph_error_t
igraph_is_independent_vertex_set.argtypes = [POINTER(igraph_t), igraph_vs_t, POINTER(igraph_bool_t)]

igraph_independent_vertex_sets = _lib.igraph_independent_vertex_sets
igraph_independent_vertex_sets.restype = handle_igraph_error_t
igraph_independent_vertex_sets.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_list_t), igraph_integer_t, igraph_integer_t]

igraph_largest_independent_vertex_sets = _lib.igraph_largest_independent_vertex_sets
igraph_largest_independent_vertex_sets.restype = handle_igraph_error_t
igraph_largest_independent_vertex_sets.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_list_t)]

igraph_maximal_independent_vertex_sets = _lib.igraph_maximal_independent_vertex_sets
igraph_maximal_independent_vertex_sets.restype = handle_igraph_error_t
igraph_maximal_independent_vertex_sets.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_list_t)]

igraph_independence_number = _lib.igraph_independence_number
igraph_independence_number.restype = handle_igraph_error_t
igraph_independence_number.argtypes = [POINTER(igraph_t), POINTER(igraph_integer_t)]

igraph_layout_random = _lib.igraph_layout_random
igraph_layout_random.restype = handle_igraph_error_t
igraph_layout_random.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t)]

igraph_layout_circle = _lib.igraph_layout_circle
igraph_layout_circle.restype = handle_igraph_error_t
igraph_layout_circle.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_vs_t]

igraph_layout_star = _lib.igraph_layout_star
igraph_layout_star.restype = handle_igraph_error_t
igraph_layout_star.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_integer_t, POINTER(igraph_vector_int_t)]

igraph_layout_grid = _lib.igraph_layout_grid
igraph_layout_grid.restype = handle_igraph_error_t
igraph_layout_grid.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_integer_t]

igraph_layout_grid_3d = _lib.igraph_layout_grid_3d
igraph_layout_grid_3d.restype = handle_igraph_error_t
igraph_layout_grid_3d.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_integer_t, igraph_integer_t]

igraph_layout_fruchterman_reingold = _lib.igraph_layout_fruchterman_reingold
igraph_layout_fruchterman_reingold.restype = handle_igraph_error_t
igraph_layout_fruchterman_reingold.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_bool_t, igraph_integer_t, igraph_real_t, igraph_layout_grid_t, POINTER(igraph_vector_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t)]

igraph_layout_kamada_kawai = _lib.igraph_layout_kamada_kawai
igraph_layout_kamada_kawai.restype = handle_igraph_error_t
igraph_layout_kamada_kawai.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_bool_t, igraph_integer_t, igraph_real_t, igraph_real_t, POINTER(igraph_vector_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t)]

igraph_layout_lgl = _lib.igraph_layout_lgl
igraph_layout_lgl.restype = handle_igraph_error_t
igraph_layout_lgl.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_integer_t, igraph_real_t, igraph_real_t, igraph_real_t, igraph_real_t, igraph_real_t, igraph_integer_t]

igraph_layout_reingold_tilford = _lib.igraph_layout_reingold_tilford
igraph_layout_reingold_tilford.restype = handle_igraph_error_t
igraph_layout_reingold_tilford.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_neimode_t, POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t)]

igraph_layout_reingold_tilford_circular = _lib.igraph_layout_reingold_tilford_circular
igraph_layout_reingold_tilford_circular.restype = handle_igraph_error_t
igraph_layout_reingold_tilford_circular.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_neimode_t, POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t)]

igraph_roots_for_tree_layout = _lib.igraph_roots_for_tree_layout
igraph_roots_for_tree_layout.restype = handle_igraph_error_t
igraph_roots_for_tree_layout.argtypes = [POINTER(igraph_t), igraph_neimode_t, POINTER(igraph_vector_int_t), igraph_root_choice_t]

igraph_layout_random_3d = _lib.igraph_layout_random_3d
igraph_layout_random_3d.restype = handle_igraph_error_t
igraph_layout_random_3d.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t)]

igraph_layout_sphere = _lib.igraph_layout_sphere
igraph_layout_sphere.restype = handle_igraph_error_t
igraph_layout_sphere.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t)]

igraph_layout_fruchterman_reingold_3d = _lib.igraph_layout_fruchterman_reingold_3d
igraph_layout_fruchterman_reingold_3d.restype = handle_igraph_error_t
igraph_layout_fruchterman_reingold_3d.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_bool_t, igraph_integer_t, igraph_real_t, POINTER(igraph_vector_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t)]

igraph_layout_kamada_kawai_3d = _lib.igraph_layout_kamada_kawai_3d
igraph_layout_kamada_kawai_3d.restype = handle_igraph_error_t
igraph_layout_kamada_kawai_3d.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_bool_t, igraph_integer_t, igraph_real_t, igraph_real_t, POINTER(igraph_vector_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t)]

igraph_layout_graphopt = _lib.igraph_layout_graphopt
igraph_layout_graphopt.restype = handle_igraph_error_t
igraph_layout_graphopt.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_integer_t, igraph_real_t, igraph_real_t, igraph_real_t, igraph_real_t, igraph_real_t, igraph_bool_t]

igraph_layout_drl = _lib.igraph_layout_drl
igraph_layout_drl.restype = handle_igraph_error_t
igraph_layout_drl.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_bool_t, POINTER(igraph_layout_drl_options_t), POINTER(igraph_vector_t)]

igraph_layout_drl_3d = _lib.igraph_layout_drl_3d
igraph_layout_drl_3d.restype = handle_igraph_error_t
igraph_layout_drl_3d.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_bool_t, POINTER(igraph_layout_drl_options_t), POINTER(igraph_vector_t)]

igraph_layout_merge_dla = _lib.igraph_layout_merge_dla
igraph_layout_merge_dla.restype = handle_igraph_error_t
igraph_layout_merge_dla.argtypes = [POINTER(igraph_vector_ptr_t), POINTER(igraph_matrix_list_t), POINTER(igraph_matrix_t)]

igraph_layout_sugiyama = _lib.igraph_layout_sugiyama
igraph_layout_sugiyama.restype = handle_igraph_error_t
igraph_layout_sugiyama.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), igraph_real_t, igraph_real_t, igraph_integer_t, POINTER(igraph_vector_t)]

igraph_layout_mds = _lib.igraph_layout_mds
igraph_layout_mds.restype = handle_igraph_error_t
igraph_layout_mds.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), POINTER(igraph_matrix_t), igraph_integer_t]

igraph_layout_bipartite = _lib.igraph_layout_bipartite
igraph_layout_bipartite.restype = handle_igraph_error_t
igraph_layout_bipartite.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_bool_t), POINTER(igraph_matrix_t), igraph_real_t, igraph_real_t, igraph_integer_t]

igraph_layout_gem = _lib.igraph_layout_gem
igraph_layout_gem.restype = handle_igraph_error_t
igraph_layout_gem.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_bool_t, igraph_integer_t, igraph_real_t, igraph_real_t, igraph_real_t]

igraph_layout_davidson_harel = _lib.igraph_layout_davidson_harel
igraph_layout_davidson_harel.restype = handle_igraph_error_t
igraph_layout_davidson_harel.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_bool_t, igraph_integer_t, igraph_integer_t, igraph_real_t, igraph_real_t, igraph_real_t, igraph_real_t, igraph_real_t, igraph_real_t]

igraph_layout_umap = _lib.igraph_layout_umap
igraph_layout_umap.restype = handle_igraph_error_t
igraph_layout_umap.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_bool_t, POINTER(igraph_vector_t), igraph_real_t, igraph_integer_t, igraph_bool_t]

igraph_layout_umap_3d = _lib.igraph_layout_umap_3d
igraph_layout_umap_3d.restype = handle_igraph_error_t
igraph_layout_umap_3d.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_bool_t, POINTER(igraph_vector_t), igraph_real_t, igraph_integer_t, igraph_bool_t]

igraph_layout_umap_compute_weights = _lib.igraph_layout_umap_compute_weights
igraph_layout_umap_compute_weights.restype = handle_igraph_error_t
igraph_layout_umap_compute_weights.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t)]

igraph_cocitation = _lib.igraph_cocitation
igraph_cocitation.restype = handle_igraph_error_t
igraph_cocitation.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_vs_t]

igraph_bibcoupling = _lib.igraph_bibcoupling
igraph_bibcoupling.restype = handle_igraph_error_t
igraph_bibcoupling.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_vs_t]

igraph_similarity_dice = _lib.igraph_similarity_dice
igraph_similarity_dice.restype = handle_igraph_error_t
igraph_similarity_dice.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_vs_t, igraph_vs_t, igraph_neimode_t, igraph_bool_t]

igraph_similarity_dice_es = _lib.igraph_similarity_dice_es
igraph_similarity_dice_es.restype = handle_igraph_error_t
igraph_similarity_dice_es.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), igraph_es_t, igraph_neimode_t, igraph_bool_t]

igraph_similarity_dice_pairs = _lib.igraph_similarity_dice_pairs
igraph_similarity_dice_pairs.restype = handle_igraph_error_t
igraph_similarity_dice_pairs.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_vector_int_t), igraph_neimode_t, igraph_bool_t]

igraph_similarity_inverse_log_weighted = _lib.igraph_similarity_inverse_log_weighted
igraph_similarity_inverse_log_weighted.restype = handle_igraph_error_t
igraph_similarity_inverse_log_weighted.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_vs_t, igraph_neimode_t]

igraph_similarity_jaccard = _lib.igraph_similarity_jaccard
igraph_similarity_jaccard.restype = handle_igraph_error_t
igraph_similarity_jaccard.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_vs_t, igraph_vs_t, igraph_neimode_t, igraph_bool_t]

igraph_similarity_jaccard_es = _lib.igraph_similarity_jaccard_es
igraph_similarity_jaccard_es.restype = handle_igraph_error_t
igraph_similarity_jaccard_es.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), igraph_es_t, igraph_neimode_t, igraph_bool_t]

igraph_similarity_jaccard_pairs = _lib.igraph_similarity_jaccard_pairs
igraph_similarity_jaccard_pairs.restype = handle_igraph_error_t
igraph_similarity_jaccard_pairs.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_vector_int_t), igraph_neimode_t, igraph_bool_t]

igraph_compare_communities = _lib.igraph_compare_communities
igraph_compare_communities.restype = handle_igraph_error_t
igraph_compare_communities.argtypes = [POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_real_t), igraph_community_comparison_t]

igraph_community_spinglass = _lib.igraph_community_spinglass
igraph_community_spinglass.restype = handle_igraph_error_t
igraph_community_spinglass.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_real_t), POINTER(igraph_real_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), igraph_integer_t, igraph_bool_t, igraph_real_t, igraph_real_t, igraph_real_t, igraph_spincomm_update_t, igraph_real_t, igraph_spinglass_implementation_t, igraph_real_t]

igraph_community_spinglass_single = _lib.igraph_community_spinglass_single
igraph_community_spinglass_single.restype = handle_igraph_error_t
igraph_community_spinglass_single.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), igraph_integer_t, POINTER(igraph_vector_int_t), POINTER(igraph_real_t), POINTER(igraph_real_t), POINTER(igraph_real_t), POINTER(igraph_real_t), igraph_integer_t, igraph_spincomm_update_t, igraph_real_t]

igraph_community_walktrap = _lib.igraph_community_walktrap
igraph_community_walktrap.restype = handle_igraph_error_t
igraph_community_walktrap.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), igraph_integer_t, POINTER(igraph_matrix_int_t), POINTER(igraph_vector_t), POINTER(igraph_vector_int_t)]

igraph_community_edge_betweenness = _lib.igraph_community_edge_betweenness
igraph_community_edge_betweenness.restype = handle_igraph_error_t
igraph_community_edge_betweenness.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_t), POINTER(igraph_matrix_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_t), POINTER(igraph_vector_int_t), igraph_bool_t, POINTER(igraph_vector_t), POINTER(igraph_vector_t)]

igraph_community_eb_get_merges = _lib.igraph_community_eb_get_merges
igraph_community_eb_get_merges.restype = handle_igraph_error_t
igraph_community_eb_get_merges.argtypes = [POINTER(igraph_t), igraph_bool_t, POINTER(igraph_vector_int_t), POINTER(igraph_vector_t), POINTER(igraph_matrix_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_t), POINTER(igraph_vector_int_t)]

igraph_community_fastgreedy = _lib.igraph_community_fastgreedy
igraph_community_fastgreedy.restype = handle_igraph_error_t
igraph_community_fastgreedy.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_matrix_int_t), POINTER(igraph_vector_t), POINTER(igraph_vector_int_t)]

igraph_community_to_membership = _lib.igraph_community_to_membership
igraph_community_to_membership.restype = handle_igraph_error_t
igraph_community_to_membership.argtypes = [POINTER(igraph_matrix_int_t), igraph_integer_t, igraph_integer_t, POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t)]

igraph_le_community_to_membership = _lib.igraph_le_community_to_membership
igraph_le_community_to_membership.restype = handle_igraph_error_t
igraph_le_community_to_membership.argtypes = [POINTER(igraph_matrix_int_t), igraph_integer_t, POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t)]

igraph_modularity = _lib.igraph_modularity
igraph_modularity.restype = handle_igraph_error_t
igraph_modularity.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_t), igraph_real_t, igraph_bool_t, POINTER(igraph_real_t)]

igraph_modularity_matrix = _lib.igraph_modularity_matrix
igraph_modularity_matrix.restype = handle_igraph_error_t
igraph_modularity_matrix.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), igraph_real_t, POINTER(igraph_matrix_t), igraph_bool_t]

igraph_reindex_membership = _lib.igraph_reindex_membership
igraph_reindex_membership.restype = handle_igraph_error_t
igraph_reindex_membership.argtypes = [POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_integer_t)]

igraph_community_fluid_communities = _lib.igraph_community_fluid_communities
igraph_community_fluid_communities.restype = handle_igraph_error_t
igraph_community_fluid_communities.argtypes = [POINTER(igraph_t), igraph_integer_t, POINTER(igraph_vector_int_t)]

igraph_community_label_propagation = _lib.igraph_community_label_propagation
igraph_community_label_propagation.restype = handle_igraph_error_t
igraph_community_label_propagation.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), igraph_neimode_t, POINTER(igraph_vector_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_bool_t), igraph_lpa_variant_t]

igraph_community_multilevel = _lib.igraph_community_multilevel
igraph_community_multilevel.restype = handle_igraph_error_t
igraph_community_multilevel.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), igraph_real_t, POINTER(igraph_vector_int_t), POINTER(igraph_matrix_int_t), POINTER(igraph_vector_t)]

igraph_community_optimal_modularity = _lib.igraph_community_optimal_modularity
igraph_community_optimal_modularity.restype = handle_igraph_error_t
igraph_community_optimal_modularity.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), igraph_real_t, POINTER(igraph_real_t), POINTER(igraph_vector_int_t)]

igraph_community_leiden = _lib.igraph_community_leiden
igraph_community_leiden.restype = handle_igraph_error_t
igraph_community_leiden.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t), igraph_real_t, igraph_real_t, igraph_bool_t, igraph_integer_t, POINTER(igraph_vector_int_t), POINTER(igraph_integer_t), POINTER(igraph_real_t)]

igraph_split_join_distance = _lib.igraph_split_join_distance
igraph_split_join_distance.restype = handle_igraph_error_t
igraph_split_join_distance.argtypes = [POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_integer_t), POINTER(igraph_integer_t)]

igraph_community_infomap = _lib.igraph_community_infomap
igraph_community_infomap.restype = handle_igraph_error_t
igraph_community_infomap.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t), igraph_integer_t, POINTER(igraph_vector_int_t), POINTER(igraph_real_t)]

igraph_community_voronoi = _lib.igraph_community_voronoi
igraph_community_voronoi.restype = handle_igraph_error_t
igraph_community_voronoi.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_real_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t), igraph_neimode_t, igraph_real_t]

igraph_graphlets = _lib.igraph_graphlets
igraph_graphlets.restype = handle_igraph_error_t
igraph_graphlets.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_vector_int_list_t), POINTER(igraph_vector_t), igraph_integer_t]

igraph_graphlets_candidate_basis = _lib.igraph_graphlets_candidate_basis
igraph_graphlets_candidate_basis.restype = handle_igraph_error_t
igraph_graphlets_candidate_basis.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_vector_int_list_t), POINTER(igraph_vector_t)]

igraph_graphlets_project = _lib.igraph_graphlets_project
igraph_graphlets_project.restype = handle_igraph_error_t
igraph_graphlets_project.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_vector_int_list_t), POINTER(igraph_vector_t), igraph_bool_t, igraph_integer_t]

igraph_hrg_fit = _lib.igraph_hrg_fit
igraph_hrg_fit.restype = handle_igraph_error_t
igraph_hrg_fit.argtypes = [POINTER(igraph_t), POINTER(igraph_hrg_t), igraph_bool_t, igraph_integer_t]

igraph_hrg_sample = _lib.igraph_hrg_sample
igraph_hrg_sample.restype = handle_igraph_error_t
igraph_hrg_sample.argtypes = [POINTER(igraph_hrg_t), POINTER(igraph_t)]

igraph_hrg_sample_many = _lib.igraph_hrg_sample_many
igraph_hrg_sample_many.restype = handle_igraph_error_t
igraph_hrg_sample_many.argtypes = [POINTER(igraph_hrg_t), POINTER(igraph_graph_list_t), igraph_integer_t]

igraph_hrg_game = _lib.igraph_hrg_game
igraph_hrg_game.restype = handle_igraph_error_t
igraph_hrg_game.argtypes = [POINTER(igraph_t), POINTER(igraph_hrg_t)]

igraph_hrg_consensus = _lib.igraph_hrg_consensus
igraph_hrg_consensus.restype = handle_igraph_error_t
igraph_hrg_consensus.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_t), POINTER(igraph_hrg_t), igraph_bool_t, igraph_integer_t]

igraph_hrg_predict = _lib.igraph_hrg_predict
igraph_hrg_predict.restype = handle_igraph_error_t
igraph_hrg_predict.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_t), POINTER(igraph_hrg_t), igraph_bool_t, igraph_integer_t, igraph_integer_t]

igraph_hrg_create = _lib.igraph_hrg_create
igraph_hrg_create.restype = handle_igraph_error_t
igraph_hrg_create.argtypes = [POINTER(igraph_hrg_t), POINTER(igraph_t), POINTER(igraph_vector_t)]

igraph_hrg_resize = _lib.igraph_hrg_resize
igraph_hrg_resize.restype = handle_igraph_error_t
igraph_hrg_resize.argtypes = [POINTER(igraph_hrg_t), igraph_integer_t]

igraph_hrg_size = _lib.igraph_hrg_size
igraph_hrg_size.restype = igraph_integer_t
igraph_hrg_size.argtypes = [POINTER(igraph_hrg_t)]

igraph_from_hrg_dendrogram = _lib.igraph_from_hrg_dendrogram
igraph_from_hrg_dendrogram.restype = handle_igraph_error_t
igraph_from_hrg_dendrogram.argtypes = [POINTER(igraph_t), POINTER(igraph_hrg_t), POINTER(igraph_vector_t)]

igraph_get_adjacency = _lib.igraph_get_adjacency
igraph_get_adjacency.restype = handle_igraph_error_t
igraph_get_adjacency.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_get_adjacency_t, POINTER(igraph_vector_t), igraph_loops_t]

igraph_get_adjacency_sparse = _lib.igraph_get_adjacency_sparse
igraph_get_adjacency_sparse.restype = handle_igraph_error_t
igraph_get_adjacency_sparse.argtypes = [POINTER(igraph_t), POINTER(igraph_sparsemat_t), igraph_get_adjacency_t, POINTER(igraph_vector_t), igraph_loops_t]

igraph_get_edgelist = _lib.igraph_get_edgelist
igraph_get_edgelist.restype = handle_igraph_error_t
igraph_get_edgelist.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), igraph_bool_t]

igraph_get_stochastic = _lib.igraph_get_stochastic
igraph_get_stochastic.restype = handle_igraph_error_t
igraph_get_stochastic.argtypes = [POINTER(igraph_t), POINTER(igraph_matrix_t), igraph_bool_t, POINTER(igraph_vector_t)]

igraph_get_stochastic_sparse = _lib.igraph_get_stochastic_sparse
igraph_get_stochastic_sparse.restype = handle_igraph_error_t
igraph_get_stochastic_sparse.argtypes = [POINTER(igraph_t), POINTER(igraph_sparsemat_t), igraph_bool_t, POINTER(igraph_vector_t)]

igraph_to_directed = _lib.igraph_to_directed
igraph_to_directed.restype = handle_igraph_error_t
igraph_to_directed.argtypes = [POINTER(igraph_t), igraph_to_directed_t]

igraph_to_undirected = _lib.igraph_to_undirected
igraph_to_undirected.restype = handle_igraph_error_t
igraph_to_undirected.argtypes = [POINTER(igraph_t), igraph_to_undirected_t, POINTER(igraph_attribute_combination_t)]

igraph_read_graph_edgelist = _lib.igraph_read_graph_edgelist
igraph_read_graph_edgelist.restype = handle_igraph_error_t
igraph_read_graph_edgelist.argtypes = [POINTER(igraph_t), POINTER(FILE), igraph_integer_t, igraph_bool_t]

igraph_read_graph_ncol = _lib.igraph_read_graph_ncol
igraph_read_graph_ncol.restype = handle_igraph_error_t
igraph_read_graph_ncol.argtypes = [POINTER(igraph_t), POINTER(FILE), POINTER(igraph_strvector_t), igraph_bool_t, igraph_add_weights_t, igraph_bool_t]

igraph_read_graph_lgl = _lib.igraph_read_graph_lgl
igraph_read_graph_lgl.restype = handle_igraph_error_t
igraph_read_graph_lgl.argtypes = [POINTER(igraph_t), POINTER(FILE), igraph_bool_t, igraph_add_weights_t, igraph_bool_t]

igraph_read_graph_pajek = _lib.igraph_read_graph_pajek
igraph_read_graph_pajek.restype = handle_igraph_error_t
igraph_read_graph_pajek.argtypes = [POINTER(igraph_t), POINTER(FILE)]

igraph_read_graph_graphml = _lib.igraph_read_graph_graphml
igraph_read_graph_graphml.restype = handle_igraph_error_t
igraph_read_graph_graphml.argtypes = [POINTER(igraph_t), POINTER(FILE), igraph_integer_t]

igraph_read_graph_dimacs_flow = _lib.igraph_read_graph_dimacs_flow
igraph_read_graph_dimacs_flow.restype = handle_igraph_error_t
igraph_read_graph_dimacs_flow.argtypes = [POINTER(igraph_t), POINTER(FILE), POINTER(igraph_strvector_t), POINTER(igraph_vector_int_t), POINTER(igraph_integer_t), POINTER(igraph_integer_t), POINTER(igraph_vector_t), igraph_bool_t]

igraph_read_graph_graphdb = _lib.igraph_read_graph_graphdb
igraph_read_graph_graphdb.restype = handle_igraph_error_t
igraph_read_graph_graphdb.argtypes = [POINTER(igraph_t), POINTER(FILE), igraph_bool_t]

igraph_read_graph_gml = _lib.igraph_read_graph_gml
igraph_read_graph_gml.restype = handle_igraph_error_t
igraph_read_graph_gml.argtypes = [POINTER(igraph_t), POINTER(FILE)]

igraph_read_graph_dl = _lib.igraph_read_graph_dl
igraph_read_graph_dl.restype = handle_igraph_error_t
igraph_read_graph_dl.argtypes = [POINTER(igraph_t), POINTER(FILE), igraph_bool_t]

igraph_write_graph_edgelist = _lib.igraph_write_graph_edgelist
igraph_write_graph_edgelist.restype = handle_igraph_error_t
igraph_write_graph_edgelist.argtypes = [POINTER(igraph_t), POINTER(FILE)]

igraph_write_graph_ncol = _lib.igraph_write_graph_ncol
igraph_write_graph_ncol.restype = handle_igraph_error_t
igraph_write_graph_ncol.argtypes = [POINTER(igraph_t), POINTER(FILE), c_char_p, c_char_p]

igraph_write_graph_lgl = _lib.igraph_write_graph_lgl
igraph_write_graph_lgl.restype = handle_igraph_error_t
igraph_write_graph_lgl.argtypes = [POINTER(igraph_t), POINTER(FILE), c_char_p, c_char_p, igraph_bool_t]

igraph_write_graph_leda = _lib.igraph_write_graph_leda
igraph_write_graph_leda.restype = handle_igraph_error_t
igraph_write_graph_leda.argtypes = [POINTER(igraph_t), POINTER(FILE), c_char_p, c_char_p]

igraph_write_graph_graphml = _lib.igraph_write_graph_graphml
igraph_write_graph_graphml.restype = handle_igraph_error_t
igraph_write_graph_graphml.argtypes = [POINTER(igraph_t), POINTER(FILE), igraph_bool_t]

igraph_write_graph_pajek = _lib.igraph_write_graph_pajek
igraph_write_graph_pajek.restype = handle_igraph_error_t
igraph_write_graph_pajek.argtypes = [POINTER(igraph_t), POINTER(FILE)]

igraph_write_graph_dimacs_flow = _lib.igraph_write_graph_dimacs_flow
igraph_write_graph_dimacs_flow.restype = handle_igraph_error_t
igraph_write_graph_dimacs_flow.argtypes = [POINTER(igraph_t), POINTER(FILE), igraph_integer_t, igraph_integer_t, POINTER(igraph_vector_t)]

igraph_write_graph_gml = _lib.igraph_write_graph_gml
igraph_write_graph_gml.restype = handle_igraph_error_t
igraph_write_graph_gml.argtypes = [POINTER(igraph_t), POINTER(FILE), igraph_write_gml_sw_t, POINTER(igraph_vector_t), c_char_p]

igraph_write_graph_dot = _lib.igraph_write_graph_dot
igraph_write_graph_dot.restype = handle_igraph_error_t
igraph_write_graph_dot.argtypes = [POINTER(igraph_t), POINTER(FILE)]

igraph_motifs_randesu = _lib.igraph_motifs_randesu
igraph_motifs_randesu.restype = handle_igraph_error_t
igraph_motifs_randesu.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), igraph_integer_t, POINTER(igraph_vector_t)]

igraph_motifs_randesu_estimate = _lib.igraph_motifs_randesu_estimate
igraph_motifs_randesu_estimate.restype = handle_igraph_error_t
igraph_motifs_randesu_estimate.argtypes = [POINTER(igraph_t), POINTER(igraph_real_t), igraph_integer_t, POINTER(igraph_vector_t), igraph_integer_t, POINTER(igraph_vector_int_t)]

igraph_motifs_randesu_no = _lib.igraph_motifs_randesu_no
igraph_motifs_randesu_no.restype = handle_igraph_error_t
igraph_motifs_randesu_no.argtypes = [POINTER(igraph_t), POINTER(igraph_real_t), igraph_integer_t, POINTER(igraph_vector_t)]

igraph_dyad_census = _lib.igraph_dyad_census
igraph_dyad_census.restype = handle_igraph_error_t
igraph_dyad_census.argtypes = [POINTER(igraph_t), POINTER(igraph_real_t), POINTER(igraph_real_t), POINTER(igraph_real_t)]

igraph_triad_census = _lib.igraph_triad_census
igraph_triad_census.restype = handle_igraph_error_t
igraph_triad_census.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t)]

igraph_count_adjacent_triangles = _lib.igraph_count_adjacent_triangles
igraph_count_adjacent_triangles.restype = handle_igraph_error_t
igraph_count_adjacent_triangles.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), igraph_vs_t]

igraph_count_triangles = _lib.igraph_count_triangles
igraph_count_triangles.restype = handle_igraph_error_t
igraph_count_triangles.argtypes = [POINTER(igraph_t), POINTER(igraph_real_t)]

igraph_local_scan_0 = _lib.igraph_local_scan_0
igraph_local_scan_0.restype = handle_igraph_error_t
igraph_local_scan_0.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t), igraph_neimode_t]

igraph_local_scan_0_them = _lib.igraph_local_scan_0_them
igraph_local_scan_0_them.restype = handle_igraph_error_t
igraph_local_scan_0_them.argtypes = [POINTER(igraph_t), POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t), igraph_neimode_t]

igraph_local_scan_1_ecount = _lib.igraph_local_scan_1_ecount
igraph_local_scan_1_ecount.restype = handle_igraph_error_t
igraph_local_scan_1_ecount.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t), igraph_neimode_t]

igraph_local_scan_1_ecount_them = _lib.igraph_local_scan_1_ecount_them
igraph_local_scan_1_ecount_them.restype = handle_igraph_error_t
igraph_local_scan_1_ecount_them.argtypes = [POINTER(igraph_t), POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t), igraph_neimode_t]

igraph_local_scan_k_ecount = _lib.igraph_local_scan_k_ecount
igraph_local_scan_k_ecount.restype = handle_igraph_error_t
igraph_local_scan_k_ecount.argtypes = [POINTER(igraph_t), igraph_integer_t, POINTER(igraph_vector_t), POINTER(igraph_vector_t), igraph_neimode_t]

igraph_local_scan_k_ecount_them = _lib.igraph_local_scan_k_ecount_them
igraph_local_scan_k_ecount_them.restype = handle_igraph_error_t
igraph_local_scan_k_ecount_them.argtypes = [POINTER(igraph_t), POINTER(igraph_t), igraph_integer_t, POINTER(igraph_vector_t), POINTER(igraph_vector_t), igraph_neimode_t]

igraph_local_scan_neighborhood_ecount = _lib.igraph_local_scan_neighborhood_ecount
igraph_local_scan_neighborhood_ecount.restype = handle_igraph_error_t
igraph_local_scan_neighborhood_ecount.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t), POINTER(igraph_vector_int_list_t)]

igraph_local_scan_subset_ecount = _lib.igraph_local_scan_subset_ecount
igraph_local_scan_subset_ecount.restype = handle_igraph_error_t
igraph_local_scan_subset_ecount.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t), POINTER(igraph_vector_int_list_t)]

igraph_list_triangles = _lib.igraph_list_triangles
igraph_list_triangles.restype = handle_igraph_error_t
igraph_list_triangles.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t)]

igraph_disjoint_union = _lib.igraph_disjoint_union
igraph_disjoint_union.restype = handle_igraph_error_t
igraph_disjoint_union.argtypes = [POINTER(igraph_t), POINTER(igraph_t), POINTER(igraph_t)]

igraph_disjoint_union_many = _lib.igraph_disjoint_union_many
igraph_disjoint_union_many.restype = handle_igraph_error_t
igraph_disjoint_union_many.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_ptr_t)]

igraph_join = _lib.igraph_join
igraph_join.restype = handle_igraph_error_t
igraph_join.argtypes = [POINTER(igraph_t), POINTER(igraph_t), POINTER(igraph_t)]

igraph_union = _lib.igraph_union
igraph_union.restype = handle_igraph_error_t
igraph_union.argtypes = [POINTER(igraph_t), POINTER(igraph_t), POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t)]

igraph_union_many = _lib.igraph_union_many
igraph_union_many.restype = handle_igraph_error_t
igraph_union_many.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_ptr_t), POINTER(igraph_vector_int_list_t)]

igraph_intersection = _lib.igraph_intersection
igraph_intersection.restype = handle_igraph_error_t
igraph_intersection.argtypes = [POINTER(igraph_t), POINTER(igraph_t), POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t)]

igraph_intersection_many = _lib.igraph_intersection_many
igraph_intersection_many.restype = handle_igraph_error_t
igraph_intersection_many.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_ptr_t), POINTER(igraph_vector_int_list_t)]

igraph_difference = _lib.igraph_difference
igraph_difference.restype = handle_igraph_error_t
igraph_difference.argtypes = [POINTER(igraph_t), POINTER(igraph_t), POINTER(igraph_t)]

igraph_complementer = _lib.igraph_complementer
igraph_complementer.restype = handle_igraph_error_t
igraph_complementer.argtypes = [POINTER(igraph_t), POINTER(igraph_t), igraph_bool_t]

igraph_compose = _lib.igraph_compose
igraph_compose.restype = handle_igraph_error_t
igraph_compose.argtypes = [POINTER(igraph_t), POINTER(igraph_t), POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t)]

igraph_induced_subgraph_map = _lib.igraph_induced_subgraph_map
igraph_induced_subgraph_map.restype = handle_igraph_error_t
igraph_induced_subgraph_map.argtypes = [POINTER(igraph_t), POINTER(igraph_t), igraph_vs_t, igraph_subgraph_implementation_t, POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t)]

igraph_product = _lib.igraph_product
igraph_product.restype = handle_igraph_error_t
igraph_product.argtypes = [POINTER(igraph_t), POINTER(igraph_t), POINTER(igraph_t), igraph_product_t]

igraph_gomory_hu_tree = _lib.igraph_gomory_hu_tree
igraph_gomory_hu_tree.restype = handle_igraph_error_t
igraph_gomory_hu_tree.argtypes = [POINTER(igraph_t), POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t)]

igraph_maxflow = _lib.igraph_maxflow
igraph_maxflow.restype = handle_igraph_error_t
igraph_maxflow.argtypes = [POINTER(igraph_t), POINTER(igraph_real_t), POINTER(igraph_vector_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), igraph_integer_t, igraph_integer_t, POINTER(igraph_vector_t), POINTER(igraph_maxflow_stats_t)]

igraph_maxflow_value = _lib.igraph_maxflow_value
igraph_maxflow_value.restype = handle_igraph_error_t
igraph_maxflow_value.argtypes = [POINTER(igraph_t), POINTER(igraph_real_t), igraph_integer_t, igraph_integer_t, POINTER(igraph_vector_t), POINTER(igraph_maxflow_stats_t)]

igraph_mincut = _lib.igraph_mincut
igraph_mincut.restype = handle_igraph_error_t
igraph_mincut.argtypes = [POINTER(igraph_t), POINTER(igraph_real_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_t)]

igraph_mincut_value = _lib.igraph_mincut_value
igraph_mincut_value.restype = handle_igraph_error_t
igraph_mincut_value.argtypes = [POINTER(igraph_t), POINTER(igraph_real_t), POINTER(igraph_vector_t)]

igraph_residual_graph = _lib.igraph_residual_graph
igraph_residual_graph.restype = handle_igraph_error_t
igraph_residual_graph.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t)]

igraph_reverse_residual_graph = _lib.igraph_reverse_residual_graph
igraph_reverse_residual_graph.restype = handle_igraph_error_t
igraph_reverse_residual_graph.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_t), POINTER(igraph_vector_t)]

igraph_st_mincut = _lib.igraph_st_mincut
igraph_st_mincut.restype = handle_igraph_error_t
igraph_st_mincut.argtypes = [POINTER(igraph_t), POINTER(igraph_real_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), igraph_integer_t, igraph_integer_t, POINTER(igraph_vector_t)]

igraph_st_mincut_value = _lib.igraph_st_mincut_value
igraph_st_mincut_value.restype = handle_igraph_error_t
igraph_st_mincut_value.argtypes = [POINTER(igraph_t), POINTER(igraph_real_t), igraph_integer_t, igraph_integer_t, POINTER(igraph_vector_t)]

igraph_st_vertex_connectivity = _lib.igraph_st_vertex_connectivity
igraph_st_vertex_connectivity.restype = handle_igraph_error_t
igraph_st_vertex_connectivity.argtypes = [POINTER(igraph_t), POINTER(igraph_integer_t), igraph_integer_t, igraph_integer_t, igraph_vconn_nei_t]

igraph_vertex_connectivity = _lib.igraph_vertex_connectivity
igraph_vertex_connectivity.restype = handle_igraph_error_t
igraph_vertex_connectivity.argtypes = [POINTER(igraph_t), POINTER(igraph_integer_t), igraph_bool_t]

igraph_st_edge_connectivity = _lib.igraph_st_edge_connectivity
igraph_st_edge_connectivity.restype = handle_igraph_error_t
igraph_st_edge_connectivity.argtypes = [POINTER(igraph_t), POINTER(igraph_integer_t), igraph_integer_t, igraph_integer_t]

igraph_edge_connectivity = _lib.igraph_edge_connectivity
igraph_edge_connectivity.restype = handle_igraph_error_t
igraph_edge_connectivity.argtypes = [POINTER(igraph_t), POINTER(igraph_integer_t), igraph_bool_t]

igraph_edge_disjoint_paths = _lib.igraph_edge_disjoint_paths
igraph_edge_disjoint_paths.restype = handle_igraph_error_t
igraph_edge_disjoint_paths.argtypes = [POINTER(igraph_t), POINTER(igraph_integer_t), igraph_integer_t, igraph_integer_t]

igraph_vertex_disjoint_paths = _lib.igraph_vertex_disjoint_paths
igraph_vertex_disjoint_paths.restype = handle_igraph_error_t
igraph_vertex_disjoint_paths.argtypes = [POINTER(igraph_t), POINTER(igraph_integer_t), igraph_integer_t, igraph_integer_t]

igraph_adhesion = _lib.igraph_adhesion
igraph_adhesion.restype = handle_igraph_error_t
igraph_adhesion.argtypes = [POINTER(igraph_t), POINTER(igraph_integer_t), igraph_bool_t]

igraph_cohesion = _lib.igraph_cohesion
igraph_cohesion.restype = handle_igraph_error_t
igraph_cohesion.argtypes = [POINTER(igraph_t), POINTER(igraph_integer_t), igraph_bool_t]

igraph_dominator_tree = _lib.igraph_dominator_tree
igraph_dominator_tree.restype = handle_igraph_error_t
igraph_dominator_tree.argtypes = [POINTER(igraph_t), igraph_integer_t, POINTER(igraph_vector_int_t), POINTER(igraph_t), POINTER(igraph_vector_int_t), igraph_neimode_t]

igraph_all_st_cuts = _lib.igraph_all_st_cuts
igraph_all_st_cuts.restype = handle_igraph_error_t
igraph_all_st_cuts.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_list_t), POINTER(igraph_vector_int_list_t), igraph_integer_t, igraph_integer_t]

igraph_all_st_mincuts = _lib.igraph_all_st_mincuts
igraph_all_st_mincuts.restype = handle_igraph_error_t
igraph_all_st_mincuts.argtypes = [POINTER(igraph_t), POINTER(igraph_real_t), POINTER(igraph_vector_int_list_t), POINTER(igraph_vector_int_list_t), igraph_integer_t, igraph_integer_t, POINTER(igraph_vector_t)]

igraph_even_tarjan_reduction = _lib.igraph_even_tarjan_reduction
igraph_even_tarjan_reduction.restype = handle_igraph_error_t
igraph_even_tarjan_reduction.argtypes = [POINTER(igraph_t), POINTER(igraph_t), POINTER(igraph_vector_t)]

igraph_is_separator = _lib.igraph_is_separator
igraph_is_separator.restype = handle_igraph_error_t
igraph_is_separator.argtypes = [POINTER(igraph_t), igraph_vs_t, POINTER(igraph_bool_t)]

igraph_is_minimal_separator = _lib.igraph_is_minimal_separator
igraph_is_minimal_separator.restype = handle_igraph_error_t
igraph_is_minimal_separator.argtypes = [POINTER(igraph_t), igraph_vs_t, POINTER(igraph_bool_t)]

igraph_all_minimal_st_separators = _lib.igraph_all_minimal_st_separators
igraph_all_minimal_st_separators.restype = handle_igraph_error_t
igraph_all_minimal_st_separators.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_list_t)]

igraph_minimum_size_separators = _lib.igraph_minimum_size_separators
igraph_minimum_size_separators.restype = handle_igraph_error_t
igraph_minimum_size_separators.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_list_t)]

igraph_cohesive_blocks = _lib.igraph_cohesive_blocks
igraph_cohesive_blocks.restype = handle_igraph_error_t
igraph_cohesive_blocks.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_list_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_t)]

igraph_coreness = _lib.igraph_coreness
igraph_coreness.restype = handle_igraph_error_t
igraph_coreness.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), igraph_neimode_t]

igraph_isoclass = _lib.igraph_isoclass
igraph_isoclass.restype = handle_igraph_error_t
igraph_isoclass.argtypes = [POINTER(igraph_t), POINTER(igraph_integer_t)]

igraph_isomorphic = _lib.igraph_isomorphic
igraph_isomorphic.restype = handle_igraph_error_t
igraph_isomorphic.argtypes = [POINTER(igraph_t), POINTER(igraph_t), POINTER(igraph_bool_t)]

igraph_automorphism_group = _lib.igraph_automorphism_group
igraph_automorphism_group.restype = handle_igraph_error_t
igraph_automorphism_group.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_list_t)]

igraph_count_automorphisms = _lib.igraph_count_automorphisms
igraph_count_automorphisms.restype = handle_igraph_error_t
igraph_count_automorphisms.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_real_t)]

igraph_isoclass_subgraph = _lib.igraph_isoclass_subgraph
igraph_isoclass_subgraph.restype = handle_igraph_error_t
igraph_isoclass_subgraph.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_integer_t)]

igraph_isoclass_create = _lib.igraph_isoclass_create
igraph_isoclass_create.restype = handle_igraph_error_t
igraph_isoclass_create.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_integer_t, igraph_bool_t]

igraph_isomorphic_vf2 = _lib.igraph_isomorphic_vf2
igraph_isomorphic_vf2.restype = handle_igraph_error_t
igraph_isomorphic_vf2.argtypes = [POINTER(igraph_t), POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_bool_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), igraph_isocompat_t, igraph_isocompat_t, c_void_p]

igraph_get_isomorphisms_vf2_callback = _lib.igraph_get_isomorphisms_vf2_callback
igraph_get_isomorphisms_vf2_callback.restype = handle_igraph_error_t
igraph_get_isomorphisms_vf2_callback.argtypes = [POINTER(igraph_t), POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), igraph_isohandler_t, igraph_isocompat_t, igraph_isocompat_t, c_void_p]

igraph_count_isomorphisms_vf2 = _lib.igraph_count_isomorphisms_vf2
igraph_count_isomorphisms_vf2.restype = handle_igraph_error_t
igraph_count_isomorphisms_vf2.argtypes = [POINTER(igraph_t), POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_integer_t), igraph_isocompat_t, igraph_isocompat_t, c_void_p]

igraph_get_isomorphisms_vf2 = _lib.igraph_get_isomorphisms_vf2
igraph_get_isomorphisms_vf2.restype = handle_igraph_error_t
igraph_get_isomorphisms_vf2.argtypes = [POINTER(igraph_t), POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_list_t), igraph_isocompat_t, igraph_isocompat_t, c_void_p]

igraph_subisomorphic = _lib.igraph_subisomorphic
igraph_subisomorphic.restype = handle_igraph_error_t
igraph_subisomorphic.argtypes = [POINTER(igraph_t), POINTER(igraph_t), POINTER(igraph_bool_t)]

igraph_subisomorphic_vf2 = _lib.igraph_subisomorphic_vf2
igraph_subisomorphic_vf2.restype = handle_igraph_error_t
igraph_subisomorphic_vf2.argtypes = [POINTER(igraph_t), POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_bool_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), igraph_isocompat_t, igraph_isocompat_t, c_void_p]

igraph_get_subisomorphisms_vf2_callback = _lib.igraph_get_subisomorphisms_vf2_callback
igraph_get_subisomorphisms_vf2_callback.restype = handle_igraph_error_t
igraph_get_subisomorphisms_vf2_callback.argtypes = [POINTER(igraph_t), POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), igraph_isohandler_t, igraph_isocompat_t, igraph_isocompat_t, c_void_p]

igraph_count_subisomorphisms_vf2 = _lib.igraph_count_subisomorphisms_vf2
igraph_count_subisomorphisms_vf2.restype = handle_igraph_error_t
igraph_count_subisomorphisms_vf2.argtypes = [POINTER(igraph_t), POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_integer_t), igraph_isocompat_t, igraph_isocompat_t, c_void_p]

igraph_get_subisomorphisms_vf2 = _lib.igraph_get_subisomorphisms_vf2
igraph_get_subisomorphisms_vf2.restype = handle_igraph_error_t
igraph_get_subisomorphisms_vf2.argtypes = [POINTER(igraph_t), POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_list_t), igraph_isocompat_t, igraph_isocompat_t, c_void_p]

igraph_canonical_permutation = _lib.igraph_canonical_permutation
igraph_canonical_permutation.restype = handle_igraph_error_t
igraph_canonical_permutation.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t)]

igraph_canonical_permutation_bliss = _lib.igraph_canonical_permutation_bliss
igraph_canonical_permutation_bliss.restype = handle_igraph_error_t
igraph_canonical_permutation_bliss.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), igraph_bliss_sh_t, POINTER(igraph_bliss_info_t)]

igraph_permute_vertices = _lib.igraph_permute_vertices
igraph_permute_vertices.restype = handle_igraph_error_t
igraph_permute_vertices.argtypes = [POINTER(igraph_t), POINTER(igraph_t), POINTER(igraph_vector_int_t)]

igraph_isomorphic_bliss = _lib.igraph_isomorphic_bliss
igraph_isomorphic_bliss.restype = handle_igraph_error_t
igraph_isomorphic_bliss.argtypes = [POINTER(igraph_t), POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), POINTER(igraph_bool_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), igraph_bliss_sh_t, POINTER(igraph_bliss_info_t), POINTER(igraph_bliss_info_t)]

igraph_count_automorphisms_bliss = _lib.igraph_count_automorphisms_bliss
igraph_count_automorphisms_bliss.restype = handle_igraph_error_t
igraph_count_automorphisms_bliss.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), igraph_bliss_sh_t, POINTER(igraph_bliss_info_t)]

igraph_automorphism_group_bliss = _lib.igraph_automorphism_group_bliss
igraph_automorphism_group_bliss.restype = handle_igraph_error_t
igraph_automorphism_group_bliss.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_list_t), igraph_bliss_sh_t, POINTER(igraph_bliss_info_t)]

igraph_subisomorphic_lad = _lib.igraph_subisomorphic_lad
igraph_subisomorphic_lad.restype = handle_igraph_error_t
igraph_subisomorphic_lad.argtypes = [POINTER(igraph_t), POINTER(igraph_t), POINTER(igraph_vector_int_list_t), POINTER(igraph_bool_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_list_t), igraph_bool_t]

igraph_simplify_and_colorize = _lib.igraph_simplify_and_colorize
igraph_simplify_and_colorize.restype = handle_igraph_error_t
igraph_simplify_and_colorize.argtypes = [POINTER(igraph_t), POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t)]

igraph_graph_count = _lib.igraph_graph_count
igraph_graph_count.restype = handle_igraph_error_t
igraph_graph_count.argtypes = [igraph_integer_t, igraph_bool_t, POINTER(igraph_integer_t)]

igraph_is_matching = _lib.igraph_is_matching
igraph_is_matching.restype = handle_igraph_error_t
igraph_is_matching.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_bool_t), POINTER(igraph_vector_int_t), POINTER(igraph_bool_t)]

igraph_is_maximal_matching = _lib.igraph_is_maximal_matching
igraph_is_maximal_matching.restype = handle_igraph_error_t
igraph_is_maximal_matching.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_bool_t), POINTER(igraph_vector_int_t), POINTER(igraph_bool_t)]

igraph_maximum_bipartite_matching = _lib.igraph_maximum_bipartite_matching
igraph_maximum_bipartite_matching.restype = handle_igraph_error_t
igraph_maximum_bipartite_matching.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_bool_t), POINTER(igraph_integer_t), POINTER(igraph_real_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_t), igraph_real_t]

igraph_adjacency_spectral_embedding = _lib.igraph_adjacency_spectral_embedding
igraph_adjacency_spectral_embedding.restype = handle_igraph_error_t
igraph_adjacency_spectral_embedding.argtypes = [POINTER(igraph_t), igraph_integer_t, POINTER(igraph_vector_t), igraph_eigen_which_position_t, igraph_bool_t, POINTER(igraph_matrix_t), POINTER(igraph_matrix_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t), POINTER(igraph_arpack_options_t)]

igraph_laplacian_spectral_embedding = _lib.igraph_laplacian_spectral_embedding
igraph_laplacian_spectral_embedding.restype = handle_igraph_error_t
igraph_laplacian_spectral_embedding.argtypes = [POINTER(igraph_t), igraph_integer_t, POINTER(igraph_vector_t), igraph_eigen_which_position_t, igraph_laplacian_spectral_embedding_type_t, igraph_bool_t, POINTER(igraph_matrix_t), POINTER(igraph_matrix_t), POINTER(igraph_vector_t), POINTER(igraph_arpack_options_t)]

igraph_power_law_fit = _lib.igraph_power_law_fit
igraph_power_law_fit.restype = handle_igraph_error_t
igraph_power_law_fit.argtypes = [POINTER(igraph_vector_t), POINTER(igraph_plfit_result_t), igraph_real_t, igraph_bool_t]

igraph_sir = _lib.igraph_sir
igraph_sir.restype = handle_igraph_error_t
igraph_sir.argtypes = [POINTER(igraph_t), igraph_real_t, igraph_real_t, igraph_integer_t, POINTER(igraph_vector_ptr_t)]

igraph_running_mean = _lib.igraph_running_mean
igraph_running_mean.restype = handle_igraph_error_t
igraph_running_mean.argtypes = [POINTER(igraph_vector_t), POINTER(igraph_vector_t), igraph_integer_t]

igraph_random_sample = _lib.igraph_random_sample
igraph_random_sample.restype = handle_igraph_error_t
igraph_random_sample.argtypes = [POINTER(igraph_vector_int_t), igraph_integer_t, igraph_integer_t, igraph_integer_t]

igraph_convex_hull = _lib.igraph_convex_hull
igraph_convex_hull.restype = handle_igraph_error_t
igraph_convex_hull.argtypes = [POINTER(igraph_matrix_t), POINTER(igraph_vector_int_t), POINTER(igraph_matrix_t)]

igraph_dim_select = _lib.igraph_dim_select
igraph_dim_select.restype = handle_igraph_error_t
igraph_dim_select.argtypes = [POINTER(igraph_vector_t), POINTER(igraph_integer_t)]

igraph_almost_equals = _lib.igraph_almost_equals
igraph_almost_equals.restype = igraph_bool_t
igraph_almost_equals.argtypes = [c_double, c_double, c_double]

igraph_cmp_epsilon = _lib.igraph_cmp_epsilon
igraph_cmp_epsilon.restype = c_int
igraph_cmp_epsilon.argtypes = [c_double, c_double, c_double]

igraph_solve_lsap = _lib.igraph_solve_lsap
igraph_solve_lsap.restype = handle_igraph_error_t
igraph_solve_lsap.argtypes = [POINTER(igraph_matrix_t), igraph_integer_t, POINTER(igraph_vector_int_t)]

igraph_find_cycle = _lib.igraph_find_cycle
igraph_find_cycle.restype = handle_igraph_error_t
igraph_find_cycle.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), igraph_neimode_t]

igraph_simple_cycles = _lib.igraph_simple_cycles
igraph_simple_cycles.restype = handle_igraph_error_t
igraph_simple_cycles.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_list_t), POINTER(igraph_vector_int_list_t), igraph_neimode_t, igraph_integer_t, igraph_integer_t]

igraph_simple_cycles_callback = _lib.igraph_simple_cycles_callback
igraph_simple_cycles_callback.restype = handle_igraph_error_t
igraph_simple_cycles_callback.argtypes = [POINTER(igraph_t), igraph_neimode_t, igraph_integer_t, igraph_integer_t, igraph_cycle_handler_t, c_void_p]

igraph_is_eulerian = _lib.igraph_is_eulerian
igraph_is_eulerian.restype = handle_igraph_error_t
igraph_is_eulerian.argtypes = [POINTER(igraph_t), POINTER(igraph_bool_t), POINTER(igraph_bool_t)]

igraph_eulerian_path = _lib.igraph_eulerian_path
igraph_eulerian_path.restype = handle_igraph_error_t
igraph_eulerian_path.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t)]

igraph_eulerian_cycle = _lib.igraph_eulerian_cycle
igraph_eulerian_cycle.restype = handle_igraph_error_t
igraph_eulerian_cycle.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t)]

igraph_fundamental_cycles = _lib.igraph_fundamental_cycles
igraph_fundamental_cycles.restype = handle_igraph_error_t
igraph_fundamental_cycles.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_list_t), igraph_integer_t, igraph_integer_t, POINTER(igraph_vector_t)]

igraph_minimum_cycle_basis = _lib.igraph_minimum_cycle_basis
igraph_minimum_cycle_basis.restype = handle_igraph_error_t
igraph_minimum_cycle_basis.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_list_t), igraph_integer_t, igraph_bool_t, igraph_bool_t, POINTER(igraph_vector_t)]

igraph_is_tree = _lib.igraph_is_tree
igraph_is_tree.restype = handle_igraph_error_t
igraph_is_tree.argtypes = [POINTER(igraph_t), POINTER(igraph_bool_t), POINTER(igraph_integer_t), igraph_neimode_t]

igraph_is_forest = _lib.igraph_is_forest
igraph_is_forest.restype = handle_igraph_error_t
igraph_is_forest.argtypes = [POINTER(igraph_t), POINTER(igraph_bool_t), POINTER(igraph_vector_int_t), igraph_neimode_t]

igraph_from_prufer = _lib.igraph_from_prufer
igraph_from_prufer.restype = handle_igraph_error_t
igraph_from_prufer.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t)]

igraph_to_prufer = _lib.igraph_to_prufer
igraph_to_prufer.restype = handle_igraph_error_t
igraph_to_prufer.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t)]

igraph_tree_from_parent_vector = _lib.igraph_tree_from_parent_vector
igraph_tree_from_parent_vector.restype = handle_igraph_error_t
igraph_tree_from_parent_vector.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), igraph_tree_mode_t]

igraph_is_complete = _lib.igraph_is_complete
igraph_is_complete.restype = handle_igraph_error_t
igraph_is_complete.argtypes = [POINTER(igraph_t), POINTER(igraph_bool_t)]

igraph_minimum_spanning_tree = _lib.igraph_minimum_spanning_tree
igraph_minimum_spanning_tree.restype = handle_igraph_error_t
igraph_minimum_spanning_tree.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), POINTER(igraph_vector_t), igraph_mst_algorithm_t]

igraph_random_spanning_tree = _lib.igraph_random_spanning_tree
igraph_random_spanning_tree.restype = handle_igraph_error_t
igraph_random_spanning_tree.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), igraph_integer_t]

igraph_tree_game = _lib.igraph_tree_game
igraph_tree_game.restype = handle_igraph_error_t
igraph_tree_game.argtypes = [POINTER(igraph_t), igraph_integer_t, igraph_bool_t, igraph_random_tree_t]

igraph_vertex_coloring_greedy = _lib.igraph_vertex_coloring_greedy
igraph_vertex_coloring_greedy.restype = handle_igraph_error_t
igraph_vertex_coloring_greedy.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_int_t), igraph_coloring_greedy_t]

igraph_convergence_degree = _lib.igraph_convergence_degree
igraph_convergence_degree.restype = handle_igraph_error_t
igraph_convergence_degree.argtypes = [POINTER(igraph_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t), POINTER(igraph_vector_t)]

igraph_has_attribute_table = _lib.igraph_has_attribute_table
igraph_has_attribute_table.restype = igraph_bool_t
igraph_has_attribute_table.argtypes = []

igraph_progress = _lib.igraph_progress
igraph_progress.restype = handle_igraph_error_t
igraph_progress.argtypes = [c_char_p, igraph_real_t, c_void_p]

igraph_status = _lib.igraph_status
igraph_status.restype = handle_igraph_error_t
igraph_status.argtypes = [c_char_p, c_void_p]

igraph_strerror = _lib.igraph_strerror
igraph_strerror.restype = c_char_p
igraph_strerror.argtypes = [igraph_error_t]

igraph_expand_path_to_pairs = _lib.igraph_expand_path_to_pairs
igraph_expand_path_to_pairs.restype = handle_igraph_error_t
igraph_expand_path_to_pairs.argtypes = [POINTER(igraph_vector_int_t)]

igraph_invalidate_cache = _lib.igraph_invalidate_cache
igraph_invalidate_cache.restype = None
igraph_invalidate_cache.argtypes = [POINTER(igraph_t)]

igraph_vertex_path_from_edge_path = _lib.igraph_vertex_path_from_edge_path
igraph_vertex_path_from_edge_path.restype = handle_igraph_error_t
igraph_vertex_path_from_edge_path.argtypes = [POINTER(igraph_t), igraph_integer_t, POINTER(igraph_vector_int_t), POINTER(igraph_vector_int_t), igraph_neimode_t]

igraph_version = _lib.igraph_version
igraph_version.restype = None
igraph_version.argtypes = [POINTER(c_char_p), POINTER(c_int), POINTER(c_int), POINTER(c_int)]
