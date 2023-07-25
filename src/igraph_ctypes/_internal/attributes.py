from abc import ABC, abstractmethod
from ctypes import (
    pointer,
    py_object,
)
from dataclasses import dataclass, field
from math import nan
from typing import Any, Callable, MutableMapping, Optional

from .conversion import igraph_vector_int_t_to_numpy_array_view
from .lib import (
    igraph_error,
    igraph_vector_resize,
    igraph_vector_set,
    igraph_vector_bool_resize,
    igraph_vector_bool_set,
    igraph_vector_int_clear,
    igraph_strvector_clear,
    igraph_strvector_resize,
    igraph_strvector_set,
)
from .refcount import incref, decref
from .types import igraph_attribute_table_t, IntArray
from .utils import nop, protect_with

__all__ = ("AttributeHandlerBase", "AttributeHandler", "AttributeStorage")


################################################################################


def _trigger_error(error: int) -> int:
    return int(
        igraph_error(
            b"Attribute handler triggered an error",
            b"<py-attribute-handler>",
            1,
            int(error),
        )
    )


class AttributeHandlerBase:
    """Base class for igraph attribute handlers."""

    _table: Optional[igraph_attribute_table_t] = None
    _table_ptr = None

    def _get_attribute_handler_functions(self) -> dict[str, Callable]:
        """Returns an ``igraph_attribute_table_t`` instance that can be used
        to register this attribute handler in the core igraph library.
        """
        protect = protect_with(_trigger_error)
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


class AttributeStorage(ABC):
    """Interface specification for objects that store graph, vertex and edge
    attributes.
    """

    @abstractmethod
    def add_vertices(self, graph, n: int) -> None:
        """Notifies the attribute storage object that the given number of
        new vertices were added to the graph.
        """
        raise NotImplementedError

    @abstractmethod
    def add_edges(self, graph, edges) -> None:
        """Notifies the attribute storage object that the given edges were
        added to the graph.
        """
        raise NotImplementedError

    @abstractmethod
    def clear(self):
        """Clears the storage area, removing all attributes."""
        raise NotImplementedError

    @abstractmethod
    def copy(
        self,
        copy_graph_attributes: bool = True,
        copy_vertex_attributes: bool = True,
        copy_edge_attributes: bool = True,
    ):
        """Creates a shallow copy of the storage area."""
        raise NotImplementedError

    @abstractmethod
    def get_graph_attribute_map(self) -> MutableMapping[str, Any]:
        """Returns a mutable mapping into the storage area that stores the graph
        attributes.
        """
        raise NotImplementedError


@dataclass(frozen=True)
class DictAttributeStorage(AttributeStorage):
    """dictionary-based storage area for the graph, vertex and edge attributes
    of a graph.
    """

    graph_attributes: dict[str, Any] = field(default_factory=dict)
    vertex_attributes: dict[str, list[Any]] = field(default_factory=dict)
    edge_attributes: dict[str, list[Any]] = field(default_factory=dict)

    def add_vertices(self, graph, n: int) -> None:
        pass

    def add_edges(self, graph, edges: IntArray) -> None:
        pass

    def clear(self) -> None:
        self.graph_attributes.clear()
        self.vertex_attributes.clear()
        self.edge_attributes.clear()

    def copy(
        self,
        copy_graph_attributes: bool = True,
        copy_vertex_attributes: bool = True,
        copy_edge_attributes: bool = True,
    ):
        return self.__class__(
            self.graph_attributes.copy() if copy_graph_attributes else {},
            self.vertex_attributes.copy() if copy_vertex_attributes else {},
            self.edge_attributes.copy() if copy_edge_attributes else {},
        )

    def get_graph_attribute_map(self) -> MutableMapping[str, Any]:
        return self.graph_attributes


def _assign_storage_to_graph(graph, storage: Optional[AttributeStorage] = None) -> None:
    """Assigns an attribute storage object to a graph, taking care of
    increasing or decreasing the reference count of the storage object if needed.
    """
    try:
        old_storage = graph.contents.attr
    except ValueError:
        # No storage yet, this is OK
        old_storage = None

    if old_storage is storage:
        # Nothing to do
        return

    if old_storage is not None:
        decref(old_storage)

    if storage is not None:
        graph.contents.attr = py_object(incref(storage))
    else:
        graph.contents.attr = py_object()


def _get_storage_from_graph(graph) -> AttributeStorage:
    return graph.contents.attr


def _detach_storage_from_graph(graph) -> None:
    return _assign_storage_to_graph(graph, None)


class AttributeHandler(AttributeHandlerBase):
    """Attribute handler implementation that uses a DictAttributeStorage_
    as its storage backend.
    """

    def init(self, graph, attr):
        _assign_storage_to_graph(graph, DictAttributeStorage())

    def destroy(self, graph) -> None:
        storage = _get_storage_from_graph(graph)
        if storage:
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
        storage = _get_storage_from_graph(graph)
        new_storage = storage.copy(
            copy_graph_attributes, copy_vertex_attributes, copy_edge_attributes
        )
        _assign_storage_to_graph(to, new_storage)

    def add_vertices(self, graph, n: int, attr) -> None:
        # attr will only ever be NULL here so raise an error if it is not
        if attr:
            raise RuntimeError(
                "add_vertices() attribute handler called with non-null attr; "
                "this is most likely a bug"
            )

        # Extend the existing attribute containers
        _get_storage_from_graph(graph).add_vertices(graph, n)

    def permute_vertices(self, graph, to, mapping):
        pass

    def combine_vertices(self, graph, to, mapping, combinations):
        pass

    def add_edges(self, graph, edges, attr) -> None:
        # attr will only ever be NULL here so raise an error if it is not
        if attr:
            raise RuntimeError(
                "add_edges() attribute handler called with non-null attr; "
                "this is most likely a bug"
            )

        # Extend the existing attribute containers
        edge_array = igraph_vector_int_t_to_numpy_array_view(edges).reshape((-1, 2))
        _get_storage_from_graph(graph).add_edges(graph, edge_array)

    def permute_edges(self, graph, to, mapping):
        pass

    def combine_edges(self, graph, to, mapping, combinations):
        pass

    def get_info(self, graph, gnames, gtypes, vnames, vtypes, enames, etypes):
        # TODO(ntamas): fill the names and the types
        igraph_strvector_clear(gnames)
        igraph_vector_int_clear(gtypes)

        igraph_strvector_clear(vnames)
        igraph_vector_int_clear(vtypes)

        igraph_strvector_clear(enames)
        igraph_vector_int_clear(etypes)

    def has_attr(self, graph, type, name) -> bool:
        return False

    def get_type(self, graph, type, elemtype, name):
        pass

    def get_numeric_graph_attr(self, graph, name, value):
        vec = value.contents
        igraph_vector_resize(vec, 1)
        igraph_vector_set(
            vec,
            0,
            self._to_numeric(
                _get_storage_from_graph(graph).get_graph_attribute_map()[name]
            ),
        )

    def get_string_graph_attr(self, graph, name, value):
        vec = value.contents
        igraph_strvector_resize(vec, 1)
        igraph_strvector_set(
            vec,
            0,
            self._to_bytes(
                _get_storage_from_graph(graph).get_graph_attribute_map()[name]
            ),
        )

    def get_bool_graph_attr(self, graph, name, value):
        vec = value.contents
        igraph_vector_bool_resize(vec, 1)
        igraph_vector_bool_set(
            vec,
            0,
            bool(_get_storage_from_graph(graph).get_graph_attribute_map()[name]),
        )

    def get_numeric_vertex_attr(self, graph, name, vs, value):
        pass

    def get_string_vertex_attr(self, graph, name, vs, value):
        pass

    def get_bool_vertex_attr(self, graph, name, vs, value):
        pass

    def get_numeric_edge_attr(self, graph, name, es, value):
        pass

    def get_string_edge_attr(self, graph, name, es, value):
        pass

    def get_bool_edge_attr(self, graph, name, es, value):
        pass

    @staticmethod
    def _to_bytes(value: Any) -> bytes:
        """Converts an arbitrary Python object into a byte-level representation,
        assuming UTF-8 encoding for strings. Returns an empty byte string if the
        conversion fails.
        """
        try:
            value_str = str(value)
            return value_str.encode("utf-8", errors="replace")
        except Exception:
            return b""

    @staticmethod
    def _to_numeric(value: Any) -> float:
        """Converts an arbitrary Python object into a floating-point value,
        returning NaN if the conversion fails.
        """
        try:
            return float(value)  # type: ignore
        except Exception:
            return nan
