from __future__ import annotations

from enum import IntEnum
from typing import Any, ClassVar


class Loops(IntEnum):
    """Python counterpart of an ``igraph_loops_t`` enum."""

    IGNORE = 0
    TWICE = 1
    ONCE = 2


# fmt: off
# The rest of this file is generated
class AttributeType(IntEnum):
    """Python counterpart of an ``igraph_attribute_type_t`` enum."""

    UNSPECIFIED = 0
    NUMERIC = 1
    BOOLEAN = 2
    STRING = 3
    OBJECT = 127

    _string_map: ClassVar[dict[str, AttributeType]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, AttributeType):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to AttributeType") from None


AttributeType._string_map = {
    'boolean': AttributeType.BOOLEAN,
    'numeric': AttributeType.NUMERIC,
    'object': AttributeType.OBJECT,
    'string': AttributeType.STRING,
    'unspecified': AttributeType.UNSPECIFIED,
}


class AttributeElementType(IntEnum):
    """Python counterpart of an ``igraph_attribute_elemtype_t`` enum."""

    GRAPH = 0
    VERTEX = 1
    EDGE = 2

    _string_map: ClassVar[dict[str, AttributeElementType]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, AttributeElementType):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to AttributeElementType") from None


AttributeElementType._string_map = {
    'edge': AttributeElementType.EDGE,
    'graph': AttributeElementType.GRAPH,
    'vertex': AttributeElementType.VERTEX,
}


class AttributeCombinationType(IntEnum):
    """Python counterpart of an ``igraph_attribute_combination_type_t`` enum."""

    IGNORE = 0
    DEFAULT = 1
    FUNCTION = 2
    SUM = 3
    PROD = 4
    MIN = 5
    MAX = 6
    RANDOM = 7
    FIRST = 8
    LAST = 9
    MEAN = 10
    MEDIAN = 11
    CONCAT = 12

    _string_map: ClassVar[dict[str, AttributeCombinationType]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, AttributeCombinationType):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to AttributeCombinationType") from None


AttributeCombinationType._string_map = {
    'concat': AttributeCombinationType.CONCAT,
    'default': AttributeCombinationType.DEFAULT,
    'first': AttributeCombinationType.FIRST,
    'function': AttributeCombinationType.FUNCTION,
    'ignore': AttributeCombinationType.IGNORE,
    'last': AttributeCombinationType.LAST,
    'max': AttributeCombinationType.MAX,
    'mean': AttributeCombinationType.MEAN,
    'median': AttributeCombinationType.MEDIAN,
    'min': AttributeCombinationType.MIN,
    'prod': AttributeCombinationType.PROD,
    'random': AttributeCombinationType.RANDOM,
    'sum': AttributeCombinationType.SUM,
}


class ColoringGreedy(IntEnum):
    """Python counterpart of an ``igraph_coloring_greedy_t`` enum."""

    COLORED_NEIGHBORS = 0
    DSATUR = 1

    _string_map: ClassVar[dict[str, ColoringGreedy]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, ColoringGreedy):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to ColoringGreedy") from None


ColoringGreedy._string_map = {
    'colored_neighbors': ColoringGreedy.COLORED_NEIGHBORS,
    'dsatur': ColoringGreedy.DSATUR,
}


class PagerankAlgorithm(IntEnum):
    """Python counterpart of an ``igraph_pagerank_algo_t`` enum."""

    ARPACK = 1
    PRPACK = 2

    _string_map: ClassVar[dict[str, PagerankAlgorithm]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, PagerankAlgorithm):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to PagerankAlgorithm") from None


PagerankAlgorithm._string_map = {
    'arpack': PagerankAlgorithm.ARPACK,
    'prpack': PagerankAlgorithm.PRPACK,
}


class FloydWarshallAlgorithm(IntEnum):
    """Python counterpart of an ``igraph_floyd_warshall_algorithm_t`` enum."""

    AUTOMATIC = 0
    ORIGINAL = 1
    TREE = 2

    _string_map: ClassVar[dict[str, FloydWarshallAlgorithm]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, FloydWarshallAlgorithm):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to FloydWarshallAlgorithm") from None


FloydWarshallAlgorithm._string_map = {
    'automatic': FloydWarshallAlgorithm.AUTOMATIC,
    'original': FloydWarshallAlgorithm.ORIGINAL,
    'tree': FloydWarshallAlgorithm.TREE,
}


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

    _string_map: ClassVar[dict[str, VertexSequenceType]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, VertexSequenceType):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to VertexSequenceType") from None


VertexSequenceType._string_map = {
    'adj': VertexSequenceType.ADJ,
    'all': VertexSequenceType.ALL,
    'nonadj': VertexSequenceType.NONADJ,
    'none': VertexSequenceType.NONE,
    'one': VertexSequenceType.ONE,
    'range': VertexSequenceType.RANGE,
    'vector': VertexSequenceType.VECTOR,
    'vectorptr': VertexSequenceType.VECTORPTR,
}


class VertexIteratorType(IntEnum):
    """Python counterpart of an ``igraph_vit_type_t`` enum."""

    RANGE = 0
    VECTOR = 1
    VECTORPTR = 2

    _string_map: ClassVar[dict[str, VertexIteratorType]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, VertexIteratorType):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to VertexIteratorType") from None


VertexIteratorType._string_map = {
    'range': VertexIteratorType.RANGE,
    'vector': VertexIteratorType.VECTOR,
    'vectorptr': VertexIteratorType.VECTORPTR,
}


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
    ALL_BETWEEN = 11

    _string_map: ClassVar[dict[str, EdgeSequenceType]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, EdgeSequenceType):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to EdgeSequenceType") from None


EdgeSequenceType._string_map = {
    'all': EdgeSequenceType.ALL,
    'all_between': EdgeSequenceType.ALL_BETWEEN,
    'allfrom': EdgeSequenceType.ALLFROM,
    'allto': EdgeSequenceType.ALLTO,
    'incident': EdgeSequenceType.INCIDENT,
    'none': EdgeSequenceType.NONE,
    'one': EdgeSequenceType.ONE,
    'pairs': EdgeSequenceType.PAIRS,
    'path': EdgeSequenceType.PATH,
    'range': EdgeSequenceType.RANGE,
    'vector': EdgeSequenceType.VECTOR,
    'vectorptr': EdgeSequenceType.VECTORPTR,
}


class EdgeIteratorType(IntEnum):
    """Python counterpart of an ``igraph_eit_type_t`` enum."""

    RANGE = 0
    VECTOR = 1
    VECTORPTR = 2

    _string_map: ClassVar[dict[str, EdgeIteratorType]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, EdgeIteratorType):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to EdgeIteratorType") from None


EdgeIteratorType._string_map = {
    'range': EdgeIteratorType.RANGE,
    'vector': EdgeIteratorType.VECTOR,
    'vectorptr': EdgeIteratorType.VECTORPTR,
}


class EigenAlgorithm(IntEnum):
    """Python counterpart of an ``igraph_eigen_algorithm_t`` enum."""

    AUTO = 0
    LAPACK = 1
    ARPACK = 2
    COMP_AUTO = 3
    COMP_LAPACK = 4
    COMP_ARPACK = 5

    _string_map: ClassVar[dict[str, EigenAlgorithm]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, EigenAlgorithm):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to EigenAlgorithm") from None


EigenAlgorithm._string_map = {
    'arpack': EigenAlgorithm.ARPACK,
    'auto': EigenAlgorithm.AUTO,
    'comp_arpack': EigenAlgorithm.COMP_ARPACK,
    'comp_auto': EigenAlgorithm.COMP_AUTO,
    'comp_lapack': EigenAlgorithm.COMP_LAPACK,
    'lapack': EigenAlgorithm.LAPACK,
}


class LaplacianSpectralEmbeddingType(IntEnum):
    """Python counterpart of an ``igraph_laplacian_spectral_embedding_type_t`` enum."""

    D_A = 0
    I_DAD = 1
    DAD = 2
    OAP = 3

    _string_map: ClassVar[dict[str, LaplacianSpectralEmbeddingType]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, LaplacianSpectralEmbeddingType):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to LaplacianSpectralEmbeddingType") from None


LaplacianSpectralEmbeddingType._string_map = {
    'd_a': LaplacianSpectralEmbeddingType.D_A,
    'dad': LaplacianSpectralEmbeddingType.DAD,
    'i_dad': LaplacianSpectralEmbeddingType.I_DAD,
    'oap': LaplacianSpectralEmbeddingType.OAP,
}


class Multiple(IntEnum):
    """Python counterpart of an ``igraph_multiple_t`` enum."""

    NO_MULTIPLE = 0
    MULTIPLE = 1

    _string_map: ClassVar[dict[str, Multiple]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, Multiple):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to Multiple") from None


Multiple._string_map = {
    'multiple': Multiple.MULTIPLE,
    'no_multiple': Multiple.NO_MULTIPLE,
}


class Order(IntEnum):
    """Python counterpart of an ``igraph_order_t`` enum."""

    ASCENDING = 0
    DESCENDING = 1

    _string_map: ClassVar[dict[str, Order]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, Order):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to Order") from None


Order._string_map = {
    'ascending': Order.ASCENDING,
    'descending': Order.DESCENDING,
}


class Optimality(IntEnum):
    """Python counterpart of an ``igraph_optimal_t`` enum."""

    MINIMUM = 0
    MAXIMUM = 1

    _string_map: ClassVar[dict[str, Optimality]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, Optimality):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to Optimality") from None


Optimality._string_map = {
    'maximum': Optimality.MAXIMUM,
    'minimum': Optimality.MINIMUM,
}


class NeighborMode(IntEnum):
    """Python counterpart of an ``igraph_neimode_t`` enum."""

    OUT = 1
    IN = 2
    ALL = 3

    _string_map: ClassVar[dict[str, NeighborMode]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, NeighborMode):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to NeighborMode") from None


NeighborMode._string_map = {
    'all': NeighborMode.ALL,
    'in': NeighborMode.IN,
    'out': NeighborMode.OUT,
}


class Connectedness(IntEnum):
    """Python counterpart of an ``igraph_connectedness_t`` enum."""

    WEAK = 1
    STRONG = 2

    _string_map: ClassVar[dict[str, Connectedness]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, Connectedness):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to Connectedness") from None


Connectedness._string_map = {
    'strong': Connectedness.STRONG,
    'weak': Connectedness.WEAK,
}


class Reciprocity(IntEnum):
    """Python counterpart of an ``igraph_reciprocity_t`` enum."""

    DEFAULT = 0
    RATIO = 1

    _string_map: ClassVar[dict[str, Reciprocity]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, Reciprocity):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to Reciprocity") from None


Reciprocity._string_map = {
    'default': Reciprocity.DEFAULT,
    'ratio': Reciprocity.RATIO,
}


class AdjacencyMode(IntEnum):
    """Python counterpart of an ``igraph_adjacency_t`` enum."""

    DIRECTED = 0
    UNDIRECTED = 1
    UPPER = 2
    LOWER = 3
    MIN = 4
    PLUS = 5
    MAX = 6

    _string_map: ClassVar[dict[str, AdjacencyMode]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, AdjacencyMode):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to AdjacencyMode") from None


AdjacencyMode._string_map = {
    'directed': AdjacencyMode.DIRECTED,
    'lower': AdjacencyMode.LOWER,
    'max': AdjacencyMode.MAX,
    'min': AdjacencyMode.MIN,
    'plus': AdjacencyMode.PLUS,
    'undirected': AdjacencyMode.UNDIRECTED,
    'upper': AdjacencyMode.UPPER,
}


class StarMode(IntEnum):
    """Python counterpart of an ``igraph_star_mode_t`` enum."""

    OUT = 0
    IN = 1
    UNDIRECTED = 2
    MUTUAL = 3

    _string_map: ClassVar[dict[str, StarMode]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, StarMode):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to StarMode") from None


StarMode._string_map = {
    'in': StarMode.IN,
    'mutual': StarMode.MUTUAL,
    'out': StarMode.OUT,
    'undirected': StarMode.UNDIRECTED,
}


class WheelMode(IntEnum):
    """Python counterpart of an ``igraph_wheel_mode_t`` enum."""

    OUT = 0
    IN = 1
    UNDIRECTED = 2
    MUTUAL = 3

    _string_map: ClassVar[dict[str, WheelMode]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, WheelMode):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to WheelMode") from None


WheelMode._string_map = {
    'in': WheelMode.IN,
    'mutual': WheelMode.MUTUAL,
    'out': WheelMode.OUT,
    'undirected': WheelMode.UNDIRECTED,
}


class TreeMode(IntEnum):
    """Python counterpart of an ``igraph_tree_mode_t`` enum."""

    OUT = 0
    IN = 1
    UNDIRECTED = 2

    _string_map: ClassVar[dict[str, TreeMode]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, TreeMode):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to TreeMode") from None


TreeMode._string_map = {
    'in': TreeMode.IN,
    'out': TreeMode.OUT,
    'undirected': TreeMode.UNDIRECTED,
}


class ErdosRenyi(IntEnum):
    """Python counterpart of an ``igraph_erdos_renyi_t`` enum."""

    GNP = 0
    GNM = 1

    _string_map: ClassVar[dict[str, ErdosRenyi]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, ErdosRenyi):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to ErdosRenyi") from None


ErdosRenyi._string_map = {
    'gnm': ErdosRenyi.GNM,
    'gnp': ErdosRenyi.GNP,
}


class GetAdjacency(IntEnum):
    """Python counterpart of an ``igraph_get_adjacency_t`` enum."""

    UPPER = 0
    LOWER = 1
    BOTH = 2

    _string_map: ClassVar[dict[str, GetAdjacency]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, GetAdjacency):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to GetAdjacency") from None


GetAdjacency._string_map = {
    'both': GetAdjacency.BOTH,
    'lower': GetAdjacency.LOWER,
    'upper': GetAdjacency.UPPER,
}


class DegreeSequenceMode(IntEnum):
    """Python counterpart of an ``igraph_degseq_t`` enum."""

    CONFIGURATION = 0
    VL = 1
    FAST_HEUR_SIMPLE = 2
    CONFIGURATION_SIMPLE = 3
    EDGE_SWITCHING_SIMPLE = 4

    _string_map: ClassVar[dict[str, DegreeSequenceMode]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, DegreeSequenceMode):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to DegreeSequenceMode") from None


DegreeSequenceMode._string_map = {
    'configuration': DegreeSequenceMode.CONFIGURATION,
    'configuration_simple': DegreeSequenceMode.CONFIGURATION_SIMPLE,
    'edge_switching_simple': DegreeSequenceMode.EDGE_SWITCHING_SIMPLE,
    'fast_heur_simple': DegreeSequenceMode.FAST_HEUR_SIMPLE,
    'vl': DegreeSequenceMode.VL,
}


class RealizeDegseq(IntEnum):
    """Python counterpart of an ``igraph_realize_degseq_t`` enum."""

    SMALLEST = 0
    LARGEST = 1
    INDEX = 2

    _string_map: ClassVar[dict[str, RealizeDegseq]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, RealizeDegseq):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to RealizeDegseq") from None


RealizeDegseq._string_map = {
    'index': RealizeDegseq.INDEX,
    'largest': RealizeDegseq.LARGEST,
    'smallest': RealizeDegseq.SMALLEST,
}


class RandomTreeMethod(IntEnum):
    """Python counterpart of an ``igraph_random_tree_t`` enum."""

    PRUFER = 0
    LERW = 1

    _string_map: ClassVar[dict[str, RandomTreeMethod]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, RandomTreeMethod):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to RandomTreeMethod") from None


RandomTreeMethod._string_map = {
    'lerw': RandomTreeMethod.LERW,
    'prufer': RandomTreeMethod.PRUFER,
}


class FileFormat(IntEnum):
    """Python counterpart of an ``igraph_fileformat_type_t`` enum."""

    EDGELIST = 0
    NCOL = 1
    PAJEK = 2
    LGL = 3
    GRAPHML = 4

    _string_map: ClassVar[dict[str, FileFormat]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, FileFormat):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to FileFormat") from None


FileFormat._string_map = {
    'edgelist': FileFormat.EDGELIST,
    'graphml': FileFormat.GRAPHML,
    'lgl': FileFormat.LGL,
    'ncol': FileFormat.NCOL,
    'pajek': FileFormat.PAJEK,
}


class Rewiring(IntEnum):
    """Python counterpart of an ``igraph_rewiring_t`` enum."""

    SIMPLE = 0
    SIMPLE_LOOPS = 1

    _string_map: ClassVar[dict[str, Rewiring]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, Rewiring):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to Rewiring") from None


Rewiring._string_map = {
    'simple': Rewiring.SIMPLE,
    'simple_loops': Rewiring.SIMPLE_LOOPS,
}


class EdgeOrder(IntEnum):
    """Python counterpart of an ``igraph_edgeorder_type_t`` enum."""

    ID = 0
    FROM = 1
    TO = 2

    _string_map: ClassVar[dict[str, EdgeOrder]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, EdgeOrder):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to EdgeOrder") from None


EdgeOrder._string_map = {
    'from': EdgeOrder.FROM,
    'id': EdgeOrder.ID,
    'to': EdgeOrder.TO,
}


class ToDirected(IntEnum):
    """Python counterpart of an ``igraph_to_directed_t`` enum."""

    ARBITRARY = 0
    MUTUAL = 1
    RANDOM = 2
    ACYCLIC = 3

    _string_map: ClassVar[dict[str, ToDirected]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, ToDirected):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to ToDirected") from None


ToDirected._string_map = {
    'acyclic': ToDirected.ACYCLIC,
    'arbitrary': ToDirected.ARBITRARY,
    'mutual': ToDirected.MUTUAL,
    'random': ToDirected.RANDOM,
}


class ToUndirected(IntEnum):
    """Python counterpart of an ``igraph_to_undirected_t`` enum."""

    EACH = 0
    COLLAPSE = 1
    MUTUAL = 2

    _string_map: ClassVar[dict[str, ToUndirected]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, ToUndirected):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to ToUndirected") from None


ToUndirected._string_map = {
    'collapse': ToUndirected.COLLAPSE,
    'each': ToUndirected.EACH,
    'mutual': ToUndirected.MUTUAL,
}


class VconnNei(IntEnum):
    """Python counterpart of an ``igraph_vconn_nei_t`` enum."""

    ERROR = 0
    NUMBER_OF_NODES = 1
    IGNORE = 2
    NEGATIVE = 3

    _string_map: ClassVar[dict[str, VconnNei]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, VconnNei):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to VconnNei") from None


VconnNei._string_map = {
    'error': VconnNei.ERROR,
    'ignore': VconnNei.IGNORE,
    'negative': VconnNei.NEGATIVE,
    'number_of_nodes': VconnNei.NUMBER_OF_NODES,
}


class SpinglassUpdateMode(IntEnum):
    """Python counterpart of an ``igraph_spincomm_update_t`` enum."""

    SIMPLE = 0
    CONFIG = 1

    _string_map: ClassVar[dict[str, SpinglassUpdateMode]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, SpinglassUpdateMode):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to SpinglassUpdateMode") from None


SpinglassUpdateMode._string_map = {
    'config': SpinglassUpdateMode.CONFIG,
    'simple': SpinglassUpdateMode.SIMPLE,
}


class LazyAdjacencyListSimplify(IntEnum):
    """Python counterpart of an ``igraph_lazy_adlist_simplify_t`` enum."""

    DONT_SIMPLIFY = 0
    SIMPLIFY = 1

    _string_map: ClassVar[dict[str, LazyAdjacencyListSimplify]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, LazyAdjacencyListSimplify):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to LazyAdjacencyListSimplify") from None


LazyAdjacencyListSimplify._string_map = {
    'dont_simplify': LazyAdjacencyListSimplify.DONT_SIMPLIFY,
    'simplify': LazyAdjacencyListSimplify.SIMPLIFY,
}


class TransitivityMode(IntEnum):
    """Python counterpart of an ``igraph_transitivity_mode_t`` enum."""

    NAN = 0
    ZERO = 1

    _string_map: ClassVar[dict[str, TransitivityMode]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, TransitivityMode):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to TransitivityMode") from None


TransitivityMode._string_map = {
    'nan': TransitivityMode.NAN,
    'zero': TransitivityMode.ZERO,
}


class SpinglassImplementation(IntEnum):
    """Python counterpart of an ``igraph_spinglass_implementation_t`` enum."""

    ORIG = 0
    NEG = 1

    _string_map: ClassVar[dict[str, SpinglassImplementation]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, SpinglassImplementation):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to SpinglassImplementation") from None


SpinglassImplementation._string_map = {
    'neg': SpinglassImplementation.NEG,
    'orig': SpinglassImplementation.ORIG,
}


class CommunityComparison(IntEnum):
    """Python counterpart of an ``igraph_community_comparison_t`` enum."""

    VI = 0
    NMI = 1
    SPLIT_JOIN = 2
    RAND = 3
    ADJUSTED_RAND = 4

    _string_map: ClassVar[dict[str, CommunityComparison]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, CommunityComparison):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to CommunityComparison") from None


CommunityComparison._string_map = {
    'adjusted_rand': CommunityComparison.ADJUSTED_RAND,
    'nmi': CommunityComparison.NMI,
    'rand': CommunityComparison.RAND,
    'split_join': CommunityComparison.SPLIT_JOIN,
    'vi': CommunityComparison.VI,
}


class AddWeights(IntEnum):
    """Python counterpart of an ``igraph_add_weights_t`` enum."""

    NO = 0
    YES = 1
    IF_PRESENT = 2

    _string_map: ClassVar[dict[str, AddWeights]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, AddWeights):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to AddWeights") from None


AddWeights._string_map = {
    'if_present': AddWeights.IF_PRESENT,
    'no': AddWeights.NO,
    'yes': AddWeights.YES,
}


class BarabasiAlgorithm(IntEnum):
    """Python counterpart of an ``igraph_barabasi_algorithm_t`` enum."""

    BAG = 0
    PSUMTREE = 1
    PSUMTREE_MULTIPLE = 2

    _string_map: ClassVar[dict[str, BarabasiAlgorithm]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, BarabasiAlgorithm):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to BarabasiAlgorithm") from None


BarabasiAlgorithm._string_map = {
    'bag': BarabasiAlgorithm.BAG,
    'psumtree': BarabasiAlgorithm.PSUMTREE,
    'psumtree_multiple': BarabasiAlgorithm.PSUMTREE_MULTIPLE,
}


class FeedbackArcSetAlgorithm(IntEnum):
    """Python counterpart of an ``igraph_fas_algorithm_t`` enum."""

    EXACT_IP = 0
    APPROX_EADES = 1

    _string_map: ClassVar[dict[str, FeedbackArcSetAlgorithm]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, FeedbackArcSetAlgorithm):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to FeedbackArcSetAlgorithm") from None


FeedbackArcSetAlgorithm._string_map = {
    'approx_eades': FeedbackArcSetAlgorithm.APPROX_EADES,
    'exact_ip': FeedbackArcSetAlgorithm.EXACT_IP,
}


class SubgraphImplementation(IntEnum):
    """Python counterpart of an ``igraph_subgraph_implementation_t`` enum."""

    AUTO = 0
    COPY_AND_DELETE = 1
    CREATE_FROM_SCRATCH = 2

    _string_map: ClassVar[dict[str, SubgraphImplementation]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, SubgraphImplementation):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to SubgraphImplementation") from None


SubgraphImplementation._string_map = {
    'auto': SubgraphImplementation.AUTO,
    'copy_and_delete': SubgraphImplementation.COPY_AND_DELETE,
    'create_from_scratch': SubgraphImplementation.CREATE_FROM_SCRATCH,
}


class ImitateAlgorithm(IntEnum):
    """Python counterpart of an ``igraph_imitate_algorithm_t`` enum."""

    AUGMENTED = 0
    BLIND = 1
    CONTRACTED = 2

    _string_map: ClassVar[dict[str, ImitateAlgorithm]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, ImitateAlgorithm):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to ImitateAlgorithm") from None


ImitateAlgorithm._string_map = {
    'augmented': ImitateAlgorithm.AUGMENTED,
    'blind': ImitateAlgorithm.BLIND,
    'contracted': ImitateAlgorithm.CONTRACTED,
}


class LayoutGrid(IntEnum):
    """Python counterpart of an ``igraph_layout_grid_t`` enum."""

    GRID = 0
    NOGRID = 1
    AUTOGRID = 2

    _string_map: ClassVar[dict[str, LayoutGrid]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, LayoutGrid):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to LayoutGrid") from None


LayoutGrid._string_map = {
    'autogrid': LayoutGrid.AUTOGRID,
    'grid': LayoutGrid.GRID,
    'nogrid': LayoutGrid.NOGRID,
}


class RandomWalkStuck(IntEnum):
    """Python counterpart of an ``igraph_random_walk_stuck_t`` enum."""

    ERROR = 0
    RETURN = 1

    _string_map: ClassVar[dict[str, RandomWalkStuck]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, RandomWalkStuck):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to RandomWalkStuck") from None


RandomWalkStuck._string_map = {
    'error': RandomWalkStuck.ERROR,
    'return': RandomWalkStuck.RETURN,
}


class VoronoiTiebreaker(IntEnum):
    """Python counterpart of an ``igraph_voronoi_tiebreaker_t`` enum."""

    FIRST = 0
    LAST = 1
    RANDOM = 2

    _string_map: ClassVar[dict[str, VoronoiTiebreaker]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, VoronoiTiebreaker):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to VoronoiTiebreaker") from None


VoronoiTiebreaker._string_map = {
    'first': VoronoiTiebreaker.FIRST,
    'last': VoronoiTiebreaker.LAST,
    'random': VoronoiTiebreaker.RANDOM,
}


class MatrixStorage(IntEnum):
    """Python counterpart of an ``igraph_matrix_storage_t`` enum."""

    ROW_MAJOR = 0
    COLUMN_MAJOR = 1

    _string_map: ClassVar[dict[str, MatrixStorage]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, MatrixStorage):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to MatrixStorage") from None


MatrixStorage._string_map = {
    'column_major': MatrixStorage.COLUMN_MAJOR,
    'row_major': MatrixStorage.ROW_MAJOR,
}


class ErrorCode(IntEnum):
    """Python counterpart of an ``igraph_error_type_t`` enum."""

    SUCCESS = 0
    FAILURE = 1
    ENOMEM = 2
    PARSEERROR = 3
    EINVAL = 4
    EXISTS = 5
    EINVEVECTOR = 6
    EINVVID = 7
    NONSQUARE = 8
    EINVMODE = 9
    EFILE = 10
    UNIMPLEMENTED = 12
    INTERRUPTED = 13
    DIVERGED = 14
    ARPACK_PROD = 15
    ARPACK_NPOS = 16
    ARPACK_NEVNPOS = 17
    ARPACK_NCVSMALL = 18
    ARPACK_NONPOSI = 19
    ARPACK_WHICHINV = 20
    ARPACK_BMATINV = 21
    ARPACK_WORKLSMALL = 22
    ARPACK_TRIDERR = 23
    ARPACK_ZEROSTART = 24
    ARPACK_MODEINV = 25
    ARPACK_MODEBMAT = 26
    ARPACK_ISHIFT = 27
    ARPACK_NEVBE = 28
    ARPACK_NOFACT = 29
    ARPACK_FAILED = 30
    ARPACK_HOWMNY = 31
    ARPACK_HOWMNYS = 32
    ARPACK_EVDIFF = 33
    ARPACK_SHUR = 34
    ARPACK_LAPACK = 35
    ARPACK_UNKNOWN = 36
    ENEGLOOP = 37
    EINTERNAL = 38
    ARPACK_MAXIT = 39
    ARPACK_NOSHIFT = 40
    ARPACK_REORDER = 41
    EDIVZERO = 42
    GLP_EBOUND = 43
    GLP_EROOT = 44
    GLP_ENOPFS = 45
    GLP_ENODFS = 46
    GLP_EFAIL = 47
    GLP_EMIPGAP = 48
    GLP_ETMLIM = 49
    GLP_ESTOP = 50
    EATTRIBUTES = 51
    EATTRCOMBINE = 52
    ELAPACK = 53
    EDRL = 54
    EOVERFLOW = 55
    EGLP = 56
    CPUTIME = 57
    EUNDERFLOW = 58
    ERWSTUCK = 59
    STOP = 60
    ERANGE = 61
    ENOSOL = 62

    _string_map: ClassVar[dict[str, ErrorCode]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, ErrorCode):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to ErrorCode") from None


ErrorCode._string_map = {
    'arpack_bmatinv': ErrorCode.ARPACK_BMATINV,
    'arpack_evdiff': ErrorCode.ARPACK_EVDIFF,
    'arpack_failed': ErrorCode.ARPACK_FAILED,
    'arpack_howmny': ErrorCode.ARPACK_HOWMNY,
    'arpack_howmnys': ErrorCode.ARPACK_HOWMNYS,
    'arpack_ishift': ErrorCode.ARPACK_ISHIFT,
    'arpack_lapack': ErrorCode.ARPACK_LAPACK,
    'arpack_maxit': ErrorCode.ARPACK_MAXIT,
    'arpack_modebmat': ErrorCode.ARPACK_MODEBMAT,
    'arpack_modeinv': ErrorCode.ARPACK_MODEINV,
    'arpack_ncvsmall': ErrorCode.ARPACK_NCVSMALL,
    'arpack_nevbe': ErrorCode.ARPACK_NEVBE,
    'arpack_nevnpos': ErrorCode.ARPACK_NEVNPOS,
    'arpack_nofact': ErrorCode.ARPACK_NOFACT,
    'arpack_nonposi': ErrorCode.ARPACK_NONPOSI,
    'arpack_noshift': ErrorCode.ARPACK_NOSHIFT,
    'arpack_npos': ErrorCode.ARPACK_NPOS,
    'arpack_prod': ErrorCode.ARPACK_PROD,
    'arpack_reorder': ErrorCode.ARPACK_REORDER,
    'arpack_shur': ErrorCode.ARPACK_SHUR,
    'arpack_triderr': ErrorCode.ARPACK_TRIDERR,
    'arpack_unknown': ErrorCode.ARPACK_UNKNOWN,
    'arpack_whichinv': ErrorCode.ARPACK_WHICHINV,
    'arpack_worklsmall': ErrorCode.ARPACK_WORKLSMALL,
    'arpack_zerostart': ErrorCode.ARPACK_ZEROSTART,
    'cputime': ErrorCode.CPUTIME,
    'diverged': ErrorCode.DIVERGED,
    'eattrcombine': ErrorCode.EATTRCOMBINE,
    'eattributes': ErrorCode.EATTRIBUTES,
    'edivzero': ErrorCode.EDIVZERO,
    'edrl': ErrorCode.EDRL,
    'efile': ErrorCode.EFILE,
    'eglp': ErrorCode.EGLP,
    'einternal': ErrorCode.EINTERNAL,
    'einval': ErrorCode.EINVAL,
    'einvevector': ErrorCode.EINVEVECTOR,
    'einvmode': ErrorCode.EINVMODE,
    'einvvid': ErrorCode.EINVVID,
    'elapack': ErrorCode.ELAPACK,
    'enegloop': ErrorCode.ENEGLOOP,
    'enomem': ErrorCode.ENOMEM,
    'enosol': ErrorCode.ENOSOL,
    'eoverflow': ErrorCode.EOVERFLOW,
    'erange': ErrorCode.ERANGE,
    'erwstuck': ErrorCode.ERWSTUCK,
    'eunderflow': ErrorCode.EUNDERFLOW,
    'exists': ErrorCode.EXISTS,
    'failure': ErrorCode.FAILURE,
    'glp_ebound': ErrorCode.GLP_EBOUND,
    'glp_efail': ErrorCode.GLP_EFAIL,
    'glp_emipgap': ErrorCode.GLP_EMIPGAP,
    'glp_enodfs': ErrorCode.GLP_ENODFS,
    'glp_enopfs': ErrorCode.GLP_ENOPFS,
    'glp_eroot': ErrorCode.GLP_EROOT,
    'glp_estop': ErrorCode.GLP_ESTOP,
    'glp_etmlim': ErrorCode.GLP_ETMLIM,
    'interrupted': ErrorCode.INTERRUPTED,
    'nonsquare': ErrorCode.NONSQUARE,
    'parseerror': ErrorCode.PARSEERROR,
    'stop': ErrorCode.STOP,
    'success': ErrorCode.SUCCESS,
    'unimplemented': ErrorCode.UNIMPLEMENTED,
}


class SparseMatrixType(IntEnum):
    """Python counterpart of an ``igraph_sparsemat_type_t`` enum."""

    TRIPLET = 0
    CC = 1

    _string_map: ClassVar[dict[str, SparseMatrixType]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, SparseMatrixType):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to SparseMatrixType") from None


SparseMatrixType._string_map = {
    'cc': SparseMatrixType.CC,
    'triplet': SparseMatrixType.TRIPLET,
}


class SparseMatrixSolver(IntEnum):
    """Python counterpart of an ``igraph_sparsemat_solve_t`` enum."""

    LU = 0
    QR = 1

    _string_map: ClassVar[dict[str, SparseMatrixSolver]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, SparseMatrixSolver):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to SparseMatrixSolver") from None


SparseMatrixSolver._string_map = {
    'lu': SparseMatrixSolver.LU,
    'qr': SparseMatrixSolver.QR,
}


class DRLLayoutPreset(IntEnum):
    """Python counterpart of an ``igraph_layout_drl_default_t`` enum."""

    DEFAULT = 0
    COARSEN = 1
    COARSEST = 2
    REFINE = 3
    FINAL = 4

    _string_map: ClassVar[dict[str, DRLLayoutPreset]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, DRLLayoutPreset):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to DRLLayoutPreset") from None


DRLLayoutPreset._string_map = {
    'coarsen': DRLLayoutPreset.COARSEN,
    'coarsest': DRLLayoutPreset.COARSEST,
    'default': DRLLayoutPreset.DEFAULT,
    'final': DRLLayoutPreset.FINAL,
    'refine': DRLLayoutPreset.REFINE,
}


class RootChoice(IntEnum):
    """Python counterpart of an ``igraph_root_choice_t`` enum."""

    DEGREE = 0
    ECCENTRICITY = 1

    _string_map: ClassVar[dict[str, RootChoice]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, RootChoice):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to RootChoice") from None


RootChoice._string_map = {
    'degree': RootChoice.DEGREE,
    'eccentricity': RootChoice.ECCENTRICITY,
}


class BLISSSplittingHeuristics(IntEnum):
    """Python counterpart of an ``igraph_bliss_sh_t`` enum."""

    F = 0
    FL = 1
    FS = 2
    FM = 3
    FLM = 4
    FSM = 5

    _string_map: ClassVar[dict[str, BLISSSplittingHeuristics]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, BLISSSplittingHeuristics):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to BLISSSplittingHeuristics") from None


BLISSSplittingHeuristics._string_map = {
    'f': BLISSSplittingHeuristics.F,
    'fl': BLISSSplittingHeuristics.FL,
    'flm': BLISSSplittingHeuristics.FLM,
    'fm': BLISSSplittingHeuristics.FM,
    'fs': BLISSSplittingHeuristics.FS,
    'fsm': BLISSSplittingHeuristics.FSM,
}


class LaplacianNormalization(IntEnum):
    """Python counterpart of an ``igraph_laplacian_normalization_t`` enum."""

    UNNORMALIZED = 0
    SYMMETRIC = 1
    LEFT = 2
    RIGHT = 3

    _string_map: ClassVar[dict[str, LaplacianNormalization]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, LaplacianNormalization):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to LaplacianNormalization") from None


LaplacianNormalization._string_map = {
    'left': LaplacianNormalization.LEFT,
    'right': LaplacianNormalization.RIGHT,
    'symmetric': LaplacianNormalization.SYMMETRIC,
    'unnormalized': LaplacianNormalization.UNNORMALIZED,
}


class LeadingEigenvectorCommunityHistory(IntEnum):
    """Python counterpart of an ``igraph_leading_eigenvector_community_history_t`` enum."""

    SPLIT = 1
    FAILED = 2
    START_FULL = 3
    START_GIVEN = 4

    _string_map: ClassVar[dict[str, LeadingEigenvectorCommunityHistory]]

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, LeadingEigenvectorCommunityHistory):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return cls._string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to LeadingEigenvectorCommunityHistory") from None


LeadingEigenvectorCommunityHistory._string_map = {
    'failed': LeadingEigenvectorCommunityHistory.FAILED,
    'split': LeadingEigenvectorCommunityHistory.SPLIT,
    'start_full': LeadingEigenvectorCommunityHistory.START_FULL,
    'start_given': LeadingEigenvectorCommunityHistory.START_GIVEN,
}


__all__ = (
    'AddWeights',
    'AdjacencyMode',
    'AttributeCombinationType',
    'AttributeElementType',
    'AttributeType',
    'BLISSSplittingHeuristics',
    'BarabasiAlgorithm',
    'ColoringGreedy',
    'CommunityComparison',
    'Connectedness',
    'DRLLayoutPreset',
    'DegreeSequenceMode',
    'EdgeIteratorType',
    'EdgeOrder',
    'EdgeSequenceType',
    'EigenAlgorithm',
    'ErdosRenyi',
    'ErrorCode',
    'FeedbackArcSetAlgorithm',
    'FileFormat',
    'FloydWarshallAlgorithm',
    'GetAdjacency',
    'ImitateAlgorithm',
    'LaplacianNormalization',
    'LaplacianSpectralEmbeddingType',
    'LayoutGrid',
    'LazyAdjacencyListSimplify',
    'LeadingEigenvectorCommunityHistory',
    'Loops',
    'MatrixStorage',
    'Multiple',
    'NeighborMode',
    'Optimality',
    'Order',
    'PagerankAlgorithm',
    'RandomTreeMethod',
    'RandomWalkStuck',
    'RealizeDegseq',
    'Reciprocity',
    'Rewiring',
    'RootChoice',
    'SparseMatrixSolver',
    'SparseMatrixType',
    'SpinglassImplementation',
    'SpinglassUpdateMode',
    'StarMode',
    'SubgraphImplementation',
    'ToDirected',
    'ToUndirected',
    'TransitivityMode',
    'TreeMode',
    'VconnNei',
    'VertexIteratorType',
    'VertexSequenceType',
    'VoronoiTiebreaker',
    'WheelMode',
)
