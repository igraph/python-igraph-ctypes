from __future__ import annotations

from ctypes import c_void_p, cast
from typing import TYPE_CHECKING, Any, TypeVar

from .lib import (
    igraph_attribute_combination_init,
    igraph_attribute_combination_destroy,
    igraph_destroy,
    igraph_es_destroy,
    igraph_graph_list_destroy,
    igraph_graph_list_init,
    igraph_matrix_destroy,
    igraph_matrix_init,
    igraph_matrix_int_destroy,
    igraph_matrix_int_init,
    igraph_matrix_list_destroy,
    igraph_matrix_list_init,
    igraph_rng_init,
    igraph_rng_destroy,
    igraph_sir_destroy,
    igraph_strvector_destroy,
    igraph_strvector_init,
    igraph_vector_destroy,
    igraph_vector_init,
    igraph_vector_bool_destroy,
    igraph_vector_bool_init,
    igraph_vector_int_destroy,
    igraph_vector_int_init,
    igraph_vector_int_list_destroy,
    igraph_vector_int_list_init,
    igraph_vector_list_destroy,
    igraph_vector_list_init,
    igraph_vector_ptr_destroy,
    igraph_vector_ptr_destroy_all,
    igraph_vector_ptr_init,
    igraph_vector_ptr_set_item_destructor,
    igraph_vector_ptr_get,
    igraph_vector_ptr_size,
    igraph_vs_destroy,
)
from .metamagic import Boxed
from .types import (
    igraph_t,
    igraph_attribute_combination_t,
    igraph_es_t,
    igraph_graph_list_t,
    igraph_matrix_t,
    igraph_matrix_int_t,
    igraph_matrix_list_t,
    igraph_rng_t,
    igraph_strvector_t,
    igraph_vector_t,
    igraph_vector_bool_t,
    igraph_vector_int_t,
    igraph_vector_int_list_t,
    igraph_vector_list_t,
    igraph_vector_ptr_t,
    igraph_vs_t,
)

if TYPE_CHECKING:
    from igraph_ctypes.graph import Graph

__all__ = (
    "_AttributeCombination",
    "_EdgeSelector",
    "_Graph",
    "_GraphList",
    "_Matrix",
    "_MatrixInt",
    "_MatrixList",
    "_RNG",
    "_SIRList",
    "_StrVector",
    "_Vector",
    "_VectorBool",
    "_VectorInt",
    "_VectorIntList",
    "_VectorList",
    "_VectorPtr",
    "_VertexSelector",
    "_create_graph_from_boxed",
)


T = TypeVar("T")


class _Graph(Boxed[igraph_t]):
    boxed_config = {"ctype": igraph_t, "destructor": igraph_destroy}


class _GraphList(Boxed[igraph_graph_list_t]):
    boxed_config = {
        "ctype": igraph_graph_list_t,
        "constructor": igraph_graph_list_init,
        "destructor": igraph_graph_list_destroy,
    }


class _Matrix(Boxed[igraph_matrix_t]):
    boxed_config = {
        "ctype": igraph_matrix_t,
        "constructor": igraph_matrix_init,
        "destructor": igraph_matrix_destroy,
    }


class _MatrixInt(Boxed[igraph_matrix_t]):
    boxed_config = {
        "ctype": igraph_matrix_int_t,
        "constructor": igraph_matrix_int_init,
        "destructor": igraph_matrix_int_destroy,
    }


class _MatrixList(Boxed[igraph_matrix_list_t]):
    boxed_config = {
        "ctype": igraph_matrix_list_t,
        "constructor": igraph_matrix_list_init,
        "destructor": igraph_matrix_list_destroy,
    }


class _StrVector(Boxed[igraph_strvector_t]):
    boxed_config = {
        "ctype": igraph_strvector_t,
        "constructor": igraph_strvector_init,
        "destructor": igraph_strvector_destroy,
    }


class _Vector(Boxed[igraph_vector_t]):
    boxed_config = {
        "ctype": igraph_vector_t,
        "constructor": igraph_vector_init,
        "destructor": igraph_vector_destroy,
    }


class _VectorBool(Boxed[igraph_vector_bool_t]):
    boxed_config = {
        "ctype": igraph_vector_bool_t,
        "constructor": igraph_vector_bool_init,
        "destructor": igraph_vector_bool_destroy,
    }


class _VectorInt(Boxed[igraph_vector_int_t]):
    boxed_config = {
        "ctype": igraph_vector_int_t,
        "constructor": igraph_vector_int_init,
        "destructor": igraph_vector_int_destroy,
    }


class _VectorIntList(Boxed[igraph_vector_int_list_t]):
    boxed_config = {
        "ctype": igraph_vector_int_list_t,
        "constructor": igraph_vector_int_list_init,
        "destructor": igraph_vector_int_list_destroy,
    }


class _VectorList(Boxed[igraph_vector_list_t]):
    boxed_config = {
        "ctype": igraph_vector_list_t,
        "constructor": igraph_vector_list_init,
        "destructor": igraph_vector_list_destroy,
    }


class _VectorPtr(Boxed[igraph_vector_ptr_t]):
    _keepalive: Any = None
    """Python objects that the pointers in the vector point into, and that must
    therefore be kept alive as long as the vector itself is alive.
    """

    boxed_config = {
        "ctype": igraph_vector_ptr_t,
        "constructor": igraph_vector_ptr_init,
        "destructor": igraph_vector_ptr_destroy,
        "getitem": igraph_vector_ptr_get,
        "len": igraph_vector_ptr_size,
    }


def _destroy_sir_list(sir_list: Any) -> None:
    # igraph_sir() allocates the igraph_sir_t elements of the list but does not
    # set an item destructor for them
    igraph_vector_ptr_set_item_destructor(sir_list, cast(igraph_sir_destroy, c_void_p))
    igraph_vector_ptr_destroy_all(sir_list)


class _SIRList(Boxed[igraph_vector_ptr_t]):
    """Pointer vector holding ``igraph_sir_t`` objects, as returned by
    ``igraph_sir()``.
    """

    boxed_config = {
        "ctype": igraph_vector_ptr_t,
        "constructor": igraph_vector_ptr_init,
        "destructor": _destroy_sir_list,
    }


class _VertexSelector(Boxed[igraph_vs_t]):
    boxed_config = {
        "ctype": igraph_vs_t,
        "destructor": igraph_vs_destroy,
    }


class _EdgeSelector(Boxed[igraph_es_t]):
    boxed_config = {
        "ctype": igraph_es_t,
        "destructor": igraph_es_destroy,
    }


class _RNG(Boxed[igraph_rng_t]):
    boxed_config = {
        "ctype": igraph_rng_t,
        "constructor": igraph_rng_init,
        "destructor": igraph_rng_destroy,
    }


class _AttributeCombination(Boxed[igraph_attribute_combination_t]):
    boxed_config = {
        "ctype": igraph_attribute_combination_t,
        "constructor": igraph_attribute_combination_init,
        "destructor": igraph_attribute_combination_destroy,
    }


def _create_graph_from_boxed(graph: _Graph) -> Graph:
    from igraph_ctypes.graph import Graph

    return Graph(_wrap=graph.mark_initialized())
