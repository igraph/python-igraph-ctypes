from abc import ABC, abstractmethod
from ctypes import py_object
from dataclasses import dataclass, field
from typing import Any, MutableMapping, Optional

from igraph_ctypes._internal.refcount import incref, decref
from igraph_ctypes._internal.types import IntArray

from .value_list import AttributeValueList

__all__ = (
    "AttributeStorage",
    "DictAttributeStorage",
    "assign_storage_to_graph",
    "detach_storage_from_graph",
    "get_storage_from_graph",
)


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

    @abstractmethod
    def get_vertex_attribute_map(self) -> MutableMapping[str, AttributeValueList[Any]]:
        """Returns a mutable mapping into the storage area that stores the
        vertex attributes.
        """
        raise NotImplementedError

    @abstractmethod
    def get_edge_attribute_map(self) -> MutableMapping[str, AttributeValueList[Any]]:
        """Returns a mutable mapping into the storage area that stores the
        edge attributes.
        """
        raise NotImplementedError


@dataclass(frozen=True)
class DictAttributeStorage(AttributeStorage):
    """dictionary-based storage area for the graph, vertex and edge attributes
    of a graph.
    """

    graph_attributes: dict[str, Any] = field(default_factory=dict)
    vertex_attributes: dict[str, AttributeValueList[Any]] = field(default_factory=dict)
    edge_attributes: dict[str, AttributeValueList[Any]] = field(default_factory=dict)

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
            {k: v.copy() for k, v in self.vertex_attributes.items()}
            if copy_vertex_attributes
            else {},
            {k: v.copy() for k, v in self.edge_attributes.items()}
            if copy_edge_attributes
            else {},
        )

    def get_graph_attribute_map(self) -> MutableMapping[str, Any]:
        return self.graph_attributes

    def get_vertex_attribute_map(self) -> MutableMapping[str, AttributeValueList[Any]]:
        return self.vertex_attributes

    def get_edge_attribute_map(self) -> MutableMapping[str, AttributeValueList[Any]]:
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
