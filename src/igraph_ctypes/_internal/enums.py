from enum import IntEnum

__all__ = (
    "AdjacencyMode",
    "EdgeSequenceType",
    "Loops",
    "MatrixStorage",
    "NeighborMode",
    "StarMode",
    "TransitivityMode",
    "TreeMode",
    "VertexSequenceType",
    "WheelMode",
)


class AdjacencyMode(IntEnum):
    """Python counterpart of an ``igraph_adjacency_t`` enum."""

    DIRECTED = 0
    UNDIRECTED = 1
    UPPER = 2
    LOWER = 3
    MIN = 4
    PLUS = 5
    MAX = 6


class EdgeSequenceType(IntEnum):
    """Python counterpart of an ``igraph_es_type_t`` enum."""

    ALL = 0
    ALLFROM = 1
    ALLTO = 2
    INCIDENT = 3
    NONE = 4
    ONE = 5
    VECTORPTR = 6
    VECTOR = 7
    RANGE = 8
    PAIRS = 9
    PATH = 10
    UNUSED_WAS_MULTIPAIRS = 11
    ALL_BETWEEN = 12


class Loops(IntEnum):
    """Python counterpart of an ``igraph_loops_t`` enum."""

    IGNORE = 0
    TWICE = 1
    ONCE = 2


class MatrixStorage(IntEnum):
    """Python counterpart of an ``igraph_matrix_storage_t`` enum."""

    ROW_MAJOR = 0
    COLUMN_MAJOR = 1


class NeighborMode(IntEnum):
    """Python counterpart of an ``igraph_neimode_t`` enum."""

    OUT = 1
    IN = 2
    ALL = 3


class StarMode(IntEnum):
    """Python counterpart of an ``igraph_star_mode_t`` enum."""

    OUT = 0
    IN = 1
    UNDIRECTED = 2
    MUTUAL = 3


class TransitivityMode(IntEnum):
    """Python counterpart of an ``igraph_transitivity_mode_t`` enum."""

    NAN = 0
    ZERO = 1


class TreeMode(IntEnum):
    """Python counterpart of an ``igraph_tree_mode_t`` enum."""

    OUT = 0
    IN = 1
    UNDIRECTED = 2


class VertexSequenceType(IntEnum):
    """Python counterpart of an ``igraph_vs_type_t`` enum."""

    ALL = 0
    ADJ = 1
    NONE = 2
    ONE = 3
    VECTORPTR = 4
    VECTOR = 5
    RANGE = 6
    NONADJ = 7


class WheelMode(IntEnum):
    """Python counterpart of an ``igraph_wheel_mode_t`` enum."""

    OUT = 0
    IN = 1
    UNDIRECTED = 2
    MUTUAL = 3
