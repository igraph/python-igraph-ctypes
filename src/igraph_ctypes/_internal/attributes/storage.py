from abc import ABC, abstractmethod
from ctypes import py_object
from dataclasses import dataclass, field
from typing import Any, MutableMapping, Optional, TypeVar

from igraph_ctypes._internal.refcount import incref, decref
from igraph_ctypes._internal.types import IntArray

from .map import AttributeMap

__all__ = (
    "AttributeStorage",
    "DictAttributeStorage",
    "assign_storage_to_graph",
    "detach_storage_from_graph",
    "get_storage_from_graph",
)


C = TypeVar("C", bound="AttributeStorage")


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
    def add_edges(self, graph, edges: IntArray) -> None:
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
        self: C,
        copy_graph_attributes: bool = True,
        new_vcount: int = -1,
        new_ecount: int = -1,
    ) -> C:
        """Creates a shallow copy of the storage area."""
        raise NotImplementedError

    @abstractmethod
    def get_graph_attribute_map(self) -> MutableMapping[str, Any]:
        """Returns a mutable mapping into the storage area that stores the graph
        attributes.
        """
        raise NotImplementedError

    @abstractmethod
    def get_vertex_attribute_map(self) -> AttributeMap:
        """Returns an attribute map corresponding to the storage area that
        stores the vertex attributes.
        """
        raise NotImplementedError

    @abstractmethod
    def get_edge_attribute_map(self) -> AttributeMap:
        """Returns an attribute map corresponding to the storage area that
        stores the edge attributes.
        """
        raise NotImplementedError


@dataclass(frozen=True)
class DictAttributeStorage(AttributeStorage):
    """dictionary-based storage area for the graph, vertex and edge attributes
    of a graph.
    """

    graph_attributes: dict[str, Any] = field(default_factory=dict)
    vertex_attributes: AttributeMap[Any] = field(
        default_factory=AttributeMap.wrap_empty_dict
    )
    edge_attributes: AttributeMap[Any] = field(
        default_factory=AttributeMap.wrap_empty_dict
    )

    def add_vertices(self, graph, n: int) -> None:
        self.vertex_attributes._extend_common_length(n)

    def add_edges(self, graph, edges: IntArray) -> None:
        self.edge_attributes._extend_common_length(edges.shape[0])

    def clear(self) -> None:
        self.graph_attributes.clear()
        self.vertex_attributes.clear()
        self.edge_attributes.clear()

    def copy(
        self,
        copy_graph_attributes: bool = True,
        new_vertex_count: int = -1,
        new_edge_count: int = -1,
    ):
        return self.__class__(
            self.graph_attributes.copy() if copy_graph_attributes else {},
            self.vertex_attributes.copy()
            if new_vertex_count < 0
            else self.vertex_attributes.copy_empty(new_vertex_count),
            self.edge_attributes.copy()
            if new_edge_count < 0
            else self.edge_attributes.copy_empty(new_edge_count),
        )

    def get_graph_attribute_map(self) -> MutableMapping[str, Any]:
        return self.graph_attributes

    def get_vertex_attribute_map(self) -> AttributeMap:
        return self.vertex_attributes

    def get_edge_attribute_map(self) -> AttributeMap:
        return self.edge_attributes


def assign_storage_to_graph(graph, storage: Optional[AttributeStorage] = None) -> None:
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


def get_storage_from_graph(graph) -> AttributeStorage:
    return graph.contents.attr


def detach_storage_from_graph(graph) -> None:
    return assign_storage_to_graph(graph, None)
