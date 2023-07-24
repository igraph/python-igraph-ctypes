from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from .lib import (
    igraph_destroy,
    igraph_es_destroy,
    igraph_matrix_destroy,
    igraph_matrix_init,
    igraph_matrix_int_destroy,
    igraph_matrix_int_init,
    igraph_rng_init,
    igraph_rng_destroy,
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
    igraph_vector_ptr_init,
    igraph_vs_destroy,
)
from .metamagic import Boxed
from .types import (
    igraph_t,
    igraph_es_t,
    igraph_matrix_t,
    igraph_matrix_int_t,
    igraph_rng_t,
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
    "_EdgeSelector",
    "_Graph",
    "_Matrix",
    "_MatrixInt",
    "_RNG",
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
    boxed_config = {
        "ctype": igraph_vector_ptr_t,
        "constructor": igraph_vector_ptr_init,
        "destructor": igraph_vector_ptr_destroy,
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


def _create_graph_from_boxed(graph: _Graph) -> Graph:
    from igraph_ctypes.graph import Graph

    return Graph(_wrap=graph.mark_initialized())
