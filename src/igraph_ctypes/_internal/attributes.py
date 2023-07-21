from ctypes import c_char_p, c_int, c_void_p, CFUNCTYPE, POINTER, Structure

from .types import (
    igraph_bool_t,
    igraph_error_t,
    igraph_es_t,
    igraph_integer_t,
    igraph_strvector_t,
    igraph_t,
    igraph_vector_bool_t,
    igraph_vector_int_t,
    igraph_vector_int_list_t,
    igraph_vector_ptr_t,
    igraph_vector_t,
    igraph_vs_t,
)


p_igraph_t = POINTER(igraph_t)
p_strvector_t = POINTER(igraph_strvector_t)
p_vector_t = POINTER(igraph_vector_t)
p_vector_bool_t = POINTER(igraph_vector_bool_t)
p_vector_int_t = POINTER(igraph_vector_int_t)
p_vector_int_list_t = POINTER(igraph_vector_int_list_t)
p_vector_ptr_t = POINTER(igraph_vector_ptr_t)


class igraph_attribute_combination_t(Structure):
    """ctypes representation of ``igraph_attribute_combination_t``"""

    _fields_ = [("list", igraph_vector_ptr_t)]


class igraph_attribute_combination_record_t(Structure):
    """ctypes representation of ``igraph_attribute_combination_record_t``"""

    _fields_ = [("name", c_char_p), ("type", c_int), ("func", CFUNCTYPE(c_void_p))]


p_attribute_combination_t = POINTER(igraph_attribute_combination_t)


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
        "get_numeric_graph_attr": CFUNCTYPE(p_igraph_t, c_char_p, p_vector_t),
        "get_string_graph_attr": CFUNCTYPE(p_igraph_t, c_char_p, p_strvector_t),
        "get_bool_graph_attr": CFUNCTYPE(p_igraph_t, c_char_p, p_vector_bool_t),
        "get_numeric_vertex_attr": CFUNCTYPE(
            p_igraph_t, c_char_p, igraph_vs_t, p_vector_t
        ),
        "get_string_vertex_attr": CFUNCTYPE(
            p_igraph_t, c_char_p, igraph_vs_t, p_strvector_t
        ),
        "get_bool_vertex_attr": CFUNCTYPE(
            p_igraph_t, c_char_p, igraph_vs_t, p_vector_bool_t
        ),
        "get_numeric_edge_attr": CFUNCTYPE(
            p_igraph_t, c_char_p, igraph_es_t, p_vector_t
        ),
        "get_string_edge_attr": CFUNCTYPE(
            p_igraph_t, c_char_p, igraph_es_t, p_strvector_t
        ),
        "get_bool_edge_attr": CFUNCTYPE(
            p_igraph_t, c_char_p, igraph_es_t, p_vector_bool_t
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
