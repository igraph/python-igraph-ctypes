from ctypes import (
    c_char_p,
    c_int,
    c_void_p,
    pointer,
    py_object,
    CFUNCTYPE,
    POINTER,
    Structure,
)
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional

from .refcount import incref, decref
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
from .utils import nop, protect

__all__ = ("AttributeHandlerBase", "DictAttributeHandler")


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


################################################################################


class AttributeHandlerBase:
    """Base class for igraph attribute handlers."""

    _table: Optional[igraph_attribute_table_t] = None
    _table_ptr = None

    def _get_attribute_handler_functions(self) -> Dict[str, Callable]:
        """Returns an ``igraph_attribute_table_t`` instance that can be used
        to register this attribute handler in the core igraph library.
        """
        return {
            key: igraph_attribute_table_t.TYPES[key](protect(getattr(self, key, nop)))
            for key in igraph_attribute_table_t.TYPES.keys()
        }

    @property
    def _as_parameter_(self):
        if self._table_ptr is None:
            self._table = igraph_attribute_table_t(
                **self._get_attribute_handler_functions()
            )
            self._table_ptr = pointer(self._table)
        return self._table_ptr


@dataclass(frozen=True)
class _DictAttributeStorage:
    """Dictionary-based storage area for the graph, vertex and edge attributes
    of a graph.
    """

    graph_attributes: Dict[str, Any] = field(default_factory=dict)
    vertex_attributes: Dict[str, Any] = field(default_factory=dict)
    edge_attributes: Dict[str, Any] = field(default_factory=dict)

    def clear(self) -> None:
        """Clears the storage area, removing all attributes from the
        attribute dictionaries.
        """
        self.graph_attributes.clear()
        self.vertex_attributes.clear()
        self.edge_attributes.clear()

    def copy(
        self,
        copy_graph_attributes: bool = True,
        copy_vertex_attributes: bool = True,
        copy_edge_attributes: bool = True,
    ):
        """Creates a shallow copy of the storage area."""
        return self.__class__(
            self.graph_attributes.copy() if copy_graph_attributes else {},
            self.vertex_attributes.copy() if copy_vertex_attributes else {},
            self.edge_attributes.copy() if copy_edge_attributes else {},
        )


_MISSING = object()


def _assign_storage_to_graph(graph, storage: Any = _MISSING):
    """Assigns an attribute storage object to a graph, taking care of
    increasing or decreasing the reference count of the storage object if needed.
    """
    try:
        old_storage = graph.contents.attr
    except ValueError:
        # No storage yet, this is OK
        old_storage = _MISSING

    if old_storage is storage:
        # Nothing to do
        return

    if old_storage is not _MISSING:
        decref(old_storage)

    if storage is not _MISSING:
        graph.contents.attr = py_object(incref(storage))
    else:
        graph.contents.attr = py_object()


def _detach_storage_from_graph(graph):
    return _assign_storage_to_graph(graph, _MISSING)


class DictAttributeHandler(AttributeHandlerBase):
    """Attribute handler implementation that stores graph, vertex and edge
    attributes in dictionaries.
    """

    def init(self, graph, attr):
        _assign_storage_to_graph(graph, _DictAttributeStorage())

    def destroy(self, graph) -> None:
        storage: _DictAttributeStorage = graph.contents.attr
        storage.clear()
        _detach_storage_from_graph(graph)

    def copy(
        self,
        to,
        graph,
        copy_graph_attributes: bool,
        copy_vertex_attributes: bool,
        copy_edge_attributes: bool,
    ):
        try:
            storage = incref(
                graph.contents.attr.copy(
                    copy_graph_attributes, copy_vertex_attributes, copy_edge_attributes
                )
            )
            to.contents.attr = py_object(storage)
        except Exception as ex:
            print(repr(ex))
            raise

    def add_vertices(self, graph, n: int, attr) -> None:
        pass

    def permute_vertices(self, graph, to, mapping):
        pass

    def combine_vertices(self, graph, to, mapping, combinations):
        pass

    def add_edges(self, graph, edges, attr) -> None:
        pass

    def permute_edges(self, graph, to, mapping):
        pass

    def combine_edges(self, graph, to, mapping, combinations):
        pass

    def get_info(self, graph, gnames, gtypes, vnames, vtypes, enames, etypes):
        pass

    def has_attr(self, graph, type, name) -> bool:
        return False

    def get_type(self, graph, type, elemtype, name):
        pass

    def get_numeric_graph_attr(self, graph, name, value):
        pass

    def get_string_graph_attr(self, graph, name, value):
        pass

    def get_boolean_graph_attr(self, graph, name, value):
        pass

    def get_numeric_vertex_attr(self, graph, name, vs, value):
        pass

    def get_string_vertex_attr(self, graph, name, vs, value):
        pass

    def get_boolean_vertex_attr(self, graph, name, vs, value):
        pass

    def get_numeric_edge_attr(self, graph, name, es, value):
        pass

    def get_string_edge_attr(self, graph, name, es, value):
        pass

    def get_boolean_edge_attr(self, graph, name, es, value):
        pass
