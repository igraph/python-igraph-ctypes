from __future__ import annotations

from ctypes import cast, c_int, pointer, c_void_p
from math import nan
from typing import Any, Callable, Optional, TYPE_CHECKING

from igraph_ctypes._internal.conversion import (
    igraph_vector_int_t_to_numpy_array_view,
    igraph_vector_int_list_t_to_list_of_numpy_array_view,
    numpy_array_to_igraph_vector_bool_t_view,
    numpy_array_to_igraph_vector_t_view,
)
from igraph_ctypes._internal.enums import AttributeElementType, AttributeType
from igraph_ctypes._internal.functions import igraph_ecount, igraph_vcount
from igraph_ctypes._internal.lib import (
    igraph_attribute_combination_query,
    igraph_error,
    igraph_es_as_vector,
    igraph_vector_resize,
    igraph_vector_set,
    igraph_vector_bool_resize,
    igraph_vector_bool_set,
    igraph_vector_bool_update,
    igraph_vector_int_clear,
    igraph_vector_int_push_back,
    igraph_vector_update,
    igraph_vs_as_vector,
    igraph_strvector_clear,
    igraph_strvector_resize,
    igraph_strvector_push_back,
    igraph_strvector_set,
)
from igraph_ctypes._internal.types import (
    igraph_attribute_table_t,
    igraph_bool_t,
)
from igraph_ctypes._internal.utils import nop, protect_with, protect_with_default

from .combinations import apply_attribute_combinations
from .storage import (
    DictAttributeStorage,
    assign_storage_to_graph,
    detach_storage_from_graph,
    get_storage_from_graph,
)
from .utils import python_object_to_igraph_attribute_type
from .value_list import AttributeValueList

if TYPE_CHECKING:
    from igraph_ctypes._internal.wrappers import _VectorInt

__all__ = (
    "AttributeHandlerBase",
    "AttributeHandler",
)


def _trigger_error(error: int) -> int:
    return int(
        igraph_error(
            b"Attribute handler triggered an error",
            b"<py-attribute-handler>",
            1,
            int(error),
        )
    )


def _are_pointers_equal(foo, bar):
    return cast(foo, c_void_p).value == cast(bar, c_void_p).value


class AttributeHandlerBase:
    """Base class for igraph attribute handlers."""

    _table: Optional[igraph_attribute_table_t] = None
    _table_ptr = None

    def _get_attribute_handler_functions(self) -> dict[str, Callable]:
        """Returns an ``igraph_attribute_table_t`` instance that can be used
        to register this attribute handler in the core igraph library.
        """
        protectors: dict[str, Callable] = {
            "has_attr": protect_with_default(igraph_bool_t, False)
        }
        protect = protect_with(_trigger_error)

        return {
            key: igraph_attribute_table_t.TYPES[key](
                protect(getattr(self, key, nop))
                if key not in protectors
                else protectors[key](getattr(self, key, nop))  # type: ignore
            )
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


class AttributeHandler(AttributeHandlerBase):
    """Attribute handler implementation that uses a DictAttributeStorage_
    as its storage backend.
    """

    _indices: _VectorInt

    def init(self, graph, attr):
        from igraph_ctypes._internal.wrappers import _VectorInt

        assign_storage_to_graph(graph, DictAttributeStorage())
        self._indices = _VectorInt.create(0)

    def destroy(self, graph) -> None:
        storage = get_storage_from_graph(graph)
        if storage:
            storage.clear()

        detach_storage_from_graph(graph)

    def copy(
        self,
        to,
        graph,
        copy_graph_attributes: bool,
        copy_vertex_attributes: bool,
        copy_edge_attributes: bool,
    ):
        storage = get_storage_from_graph(graph)

        if copy_vertex_attributes:
            new_vcount = -1
        else:
            new_vcount = int(igraph_vcount(to))

        if copy_edge_attributes:
            new_ecount = -1
        else:
            new_ecount = int(igraph_ecount(to))

        new_storage = storage.copy(copy_graph_attributes, new_vcount, new_ecount)
        assign_storage_to_graph(to, new_storage)

    def add_vertices(self, graph, n: int, attr) -> None:
        # attr will only ever be NULL here so raise an error if it is not
        if attr:
            raise RuntimeError(
                "add_vertices() attribute handler called with non-null attr; "
                "this is most likely a bug"
            )  # pragma: no cover

        # Extend the existing attribute containers
        get_storage_from_graph(graph).add_vertices(graph, n)

    def permute_vertices(self, graph, to, mapping):
        mapping_array = igraph_vector_int_t_to_numpy_array_view(mapping)

        old_attrs = get_storage_from_graph(graph).get_vertex_attribute_map()
        new_attrs = get_storage_from_graph(to).get_vertex_attribute_map()

        # The code below works for graph == to and graph != to as well
        for name, values in old_attrs.items():
            new_attrs.set(name, values[mapping_array], _check_length=False)

    def combine_vertices(self, graph, to, mapping, combinations):
        assert not _are_pointers_equal(graph, to)

    def add_edges(self, graph, edges, attr) -> None:
        # attr will only ever be NULL here so raise an error if it is not
        if attr:
            raise RuntimeError(
                "add_edges() attribute handler called with non-null attr; "
                "this is most likely a bug"
            )  # pragma: no cover

        # Extend the existing attribute containers
        edge_array = igraph_vector_int_t_to_numpy_array_view(edges).reshape((-1, 2))
        get_storage_from_graph(graph).add_edges(graph, edge_array)

    def permute_edges(self, graph, to, mapping):
        mapping_array = igraph_vector_int_t_to_numpy_array_view(mapping)

        old_attrs = get_storage_from_graph(graph).get_edge_attribute_map()
        new_attrs = get_storage_from_graph(to).get_edge_attribute_map()

        # The code below works for graph == to and graph != to as well
        for name, values in old_attrs.items():
            new_attrs.set(name, values[mapping_array], _check_length=False)

    def combine_edges(self, graph, to, mapping, combinations):
        assert not _are_pointers_equal(graph, to)

        mapping_arrays = igraph_vector_int_list_t_to_list_of_numpy_array_view(mapping)

        old_attrs = get_storage_from_graph(graph).get_edge_attribute_map()
        new_attrs = get_storage_from_graph(to).get_edge_attribute_map()

        for name, values in old_attrs.items():
            comb_type = c_int()
            comb_func = c_void_p()

            igraph_attribute_combination_query(
                combinations,
                name.encode("utf-8"),
                comb_type,
                comb_func,
            )

            new_values = apply_attribute_combinations(
                values, mapping_arrays, comb_type.value, comb_func
            )
            if new_values is not None:
                new_attrs.set(name, new_values, type=values.type, _check_length=False)

    def get_info(self, graph, gnames, gtypes, vnames, vtypes, enames, etypes):
        storage = get_storage_from_graph(graph)

        igraph_strvector_clear(gnames)
        igraph_vector_int_clear(gtypes)
        for name, value in storage.get_graph_attribute_map().items():
            igraph_strvector_push_back(gnames, name.encode("utf-8"))
            igraph_vector_int_push_back(
                gtypes, python_object_to_igraph_attribute_type(value)
            )

        igraph_strvector_clear(vnames)
        igraph_vector_int_clear(vtypes)
        for name, value in storage.get_vertex_attribute_map().items():
            igraph_strvector_push_back(vnames, name.encode("utf-8"))
            igraph_vector_int_push_back(vtypes, value.type)

        igraph_strvector_clear(enames)
        igraph_vector_int_clear(etypes)
        for name, value in storage.get_edge_attribute_map().items():
            igraph_strvector_push_back(enames, name.encode("utf-8"))
            igraph_vector_int_push_back(etypes, value.type)

    def has_attr(self, graph, type: int, name: bytes) -> bool:
        storage = get_storage_from_graph(graph)
        name_str = name.decode("utf-8")

        if type == AttributeElementType.GRAPH:
            map = storage.get_graph_attribute_map()
        elif type == AttributeElementType.VERTEX:
            map = storage.get_vertex_attribute_map()
        elif type == AttributeElementType.EDGE:
            map = storage.get_edge_attribute_map()
        else:
            return False  # pragma: no cover

        return name_str in map

    def get_type(self, graph, type, elemtype, name):
        storage = get_storage_from_graph(graph)
        name_str = name.decode("utf-8")

        if elemtype == AttributeElementType.GRAPH:
            map = storage.get_graph_attribute_map()
            result = (
                python_object_to_igraph_attribute_type(map[name_str])
                if name_str in map
                else AttributeType.UNSPECIFIED
            )
        elif elemtype == AttributeElementType.VERTEX:
            map = storage.get_vertex_attribute_map()
            result = (
                map[name_str].type if name_str in map else AttributeType.UNSPECIFIED
            )
        elif elemtype == AttributeElementType.EDGE:
            map = storage.get_edge_attribute_map()
            result = (
                map[name_str].type if name_str in map else AttributeType.UNSPECIFIED
            )
        else:
            result = AttributeType.UNSPECIFIED  # pragma: no cover

        type.contents.value = result

    def get_numeric_graph_attr(self, graph, name: bytes, value):
        map = get_storage_from_graph(graph).get_graph_attribute_map()
        igraph_vector_resize(value, 1)
        igraph_vector_set(value, 0, self._to_numeric(map[name.decode("utf-8")]))

    def get_string_graph_attr(self, graph, name: bytes, value):
        map = get_storage_from_graph(graph).get_graph_attribute_map()
        igraph_strvector_resize(value, 1)
        igraph_strvector_set(value, 0, self._to_bytes(map[name.decode("utf-8")]))

    def get_bool_graph_attr(self, graph, name: bytes, value):
        map = get_storage_from_graph(graph).get_graph_attribute_map()
        igraph_vector_bool_resize(value, 1)
        igraph_vector_bool_set(value, 0, bool(map[name.decode("utf-8")]))

    def get_numeric_vertex_attr(self, graph, name: bytes, vs, value):
        map = get_storage_from_graph(graph).get_vertex_attribute_map()

        igraph_vs_as_vector(graph, vs, self._indices)
        values = self._get_values_by_index(map[name.decode("utf-8")], self._indices)
        igraph_vector_update(value, numpy_array_to_igraph_vector_t_view(values))

    def get_string_vertex_attr(self, graph, name: bytes, vs, value):
        map = get_storage_from_graph(graph).get_vertex_attribute_map()

        igraph_vs_as_vector(graph, vs, self._indices)
        values = self._get_values_by_index(map[name.decode("utf-8")], self._indices)

        igraph_strvector_resize(value, len(values))
        for i, v in enumerate(values):
            igraph_strvector_set(value, i, self._to_bytes(v))

    def get_bool_vertex_attr(self, graph, name: bytes, vs, value):
        map = get_storage_from_graph(graph).get_vertex_attribute_map()

        igraph_vs_as_vector(graph, vs, self._indices)
        values = self._get_values_by_index(map[name.decode("utf-8")], self._indices)
        igraph_vector_bool_update(
            value, numpy_array_to_igraph_vector_bool_t_view(values)
        )

    def get_numeric_edge_attr(self, graph, name: bytes, es, value):
        map = get_storage_from_graph(graph).get_edge_attribute_map()

        igraph_es_as_vector(graph, es, self._indices)
        values = self._get_values_by_index(map[name.decode("utf-8")], self._indices)
        igraph_vector_update(value, numpy_array_to_igraph_vector_t_view(values))

    def get_string_edge_attr(self, graph, name: bytes, es, value):
        map = get_storage_from_graph(graph).get_edge_attribute_map()

        igraph_es_as_vector(graph, es, self._indices)
        values = self._get_values_by_index(map[name.decode("utf-8")], self._indices)

        igraph_strvector_resize(value, len(values))
        for i, v in enumerate(values):
            igraph_strvector_set(value, i, self._to_bytes(v))

    def get_bool_edge_attr(self, graph, name: bytes, es, value):
        map = get_storage_from_graph(graph).get_edge_attribute_map()

        igraph_es_as_vector(graph, es, self._indices)
        values = self._get_values_by_index(map[name.decode("utf-8")], self._indices)
        igraph_vector_bool_update(
            value, numpy_array_to_igraph_vector_bool_t_view(values)
        )

    @staticmethod
    def _get_values_by_index(values: AttributeValueList, indices: _VectorInt):
        index_array = igraph_vector_int_t_to_numpy_array_view(indices)
        return values[index_array]

    @staticmethod
    def _to_bytes(value: Any) -> bytes:
        """Converts an arbitrary Python object into a byte-level representation,
        assuming UTF-8 encoding for strings. Returns an empty byte string if the
        conversion fails.
        """
        try:
            value_str = str(value)
            return value_str.encode("utf-8", errors="replace")
        except Exception:  # pragma: no cover
            return b""

    @staticmethod
    def _to_numeric(value: Any) -> float:
        """Converts an arbitrary Python object into a floating-point value,
        returning NaN if the conversion fails.
        """
        try:
            return float(value)  # type: ignore
        except Exception:  # pragma: no cover
            return nan
