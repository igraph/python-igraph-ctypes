from __future__ import annotations

from enum import IntEnum
from typing import Any


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
                return _AttributeType_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to AttributeType") from None


_AttributeType_string_map: dict[str, AttributeType] = {
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
                return _AttributeElementType_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to AttributeElementType") from None


_AttributeElementType_string_map: dict[str, AttributeElementType] = {
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
                return _AttributeCombinationType_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to AttributeCombinationType") from None


_AttributeCombinationType_string_map: dict[str, AttributeCombinationType] = {
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


class GreedyColoringHeuristics(IntEnum):
    """Python counterpart of an ``igraph_coloring_greedy_t`` enum."""

    COLORED_NEIGHBORS = 0
    DSATUR = 1
    NEIGHBORS = COLORED_NEIGHBORS

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, GreedyColoringHeuristics):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return _GreedyColoringHeuristics_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to GreedyColoringHeuristics") from None


_GreedyColoringHeuristics_string_map: dict[str, GreedyColoringHeuristics] = {
    'colored_neighbors': GreedyColoringHeuristics.COLORED_NEIGHBORS,
    'dsatur': GreedyColoringHeuristics.DSATUR,
    'neighbors': GreedyColoringHeuristics.COLORED_NEIGHBORS,
}


class PagerankAlgorithm(IntEnum):
    """Python counterpart of an ``igraph_pagerank_algo_t`` enum."""

    ARPACK = 1
    PRPACK = 2

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
                return _PagerankAlgorithm_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to PagerankAlgorithm") from None


_PagerankAlgorithm_string_map: dict[str, PagerankAlgorithm] = {
    'arpack': PagerankAlgorithm.ARPACK,
    'prpack': PagerankAlgorithm.PRPACK,
}


class FloydWarshallAlgorithm(IntEnum):
    """Python counterpart of an ``igraph_floyd_warshall_algorithm_t`` enum."""

    AUTOMATIC = 0
    ORIGINAL = 1
    TREE = 2

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
                return _FloydWarshallAlgorithm_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to FloydWarshallAlgorithm") from None


_FloydWarshallAlgorithm_string_map: dict[str, FloydWarshallAlgorithm] = {
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
                return _VertexSequenceType_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to VertexSequenceType") from None


_VertexSequenceType_string_map: dict[str, VertexSequenceType] = {
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
                return _VertexIteratorType_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to VertexIteratorType") from None


_VertexIteratorType_string_map: dict[str, VertexIteratorType] = {
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
                return _EdgeSequenceType_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to EdgeSequenceType") from None


_EdgeSequenceType_string_map: dict[str, EdgeSequenceType] = {
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
                return _EdgeIteratorType_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to EdgeIteratorType") from None


_EdgeIteratorType_string_map: dict[str, EdgeIteratorType] = {
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
                return _EigenAlgorithm_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to EigenAlgorithm") from None


_EigenAlgorithm_string_map: dict[str, EigenAlgorithm] = {
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
                return _LaplacianSpectralEmbeddingType_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to LaplacianSpectralEmbeddingType") from None


_LaplacianSpectralEmbeddingType_string_map: dict[str, LaplacianSpectralEmbeddingType] = {
    'd_a': LaplacianSpectralEmbeddingType.D_A,
    'dad': LaplacianSpectralEmbeddingType.DAD,
    'i_dad': LaplacianSpectralEmbeddingType.I_DAD,
    'oap': LaplacianSpectralEmbeddingType.OAP,
}


class BLISSSplittingHeuristics(IntEnum):
    """Python counterpart of an ``igraph_bliss_sh_t`` enum."""

    F = 0
    FL = 1
    FS = 2
    FM = 3
    FLM = 4
    FSM = 5

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
                return _BLISSSplittingHeuristics_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to BLISSSplittingHeuristics") from None


_BLISSSplittingHeuristics_string_map: dict[str, BLISSSplittingHeuristics] = {
    'f': BLISSSplittingHeuristics.F,
    'fl': BLISSSplittingHeuristics.FL,
    'flm': BLISSSplittingHeuristics.FLM,
    'fm': BLISSSplittingHeuristics.FM,
    'fs': BLISSSplittingHeuristics.FS,
    'fsm': BLISSSplittingHeuristics.FSM,
}


class Multiple(IntEnum):
    """Python counterpart of an ``igraph_multiple_t`` enum."""

    NO_MULTIPLE = 0
    MULTIPLE = 1

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
                return _Multiple_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to Multiple") from None


_Multiple_string_map: dict[str, Multiple] = {
    'multiple': Multiple.MULTIPLE,
    'no_multiple': Multiple.NO_MULTIPLE,
}


class Order(IntEnum):
    """Python counterpart of an ``igraph_order_t`` enum."""

    ASCENDING = 0
    DESCENDING = 1

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
                return _Order_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to Order") from None


_Order_string_map: dict[str, Order] = {
    'ascending': Order.ASCENDING,
    'descending': Order.DESCENDING,
}


class Optimality(IntEnum):
    """Python counterpart of an ``igraph_optimal_t`` enum."""

    MINIMUM = 0
    MAXIMUM = 1

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
                return _Optimality_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to Optimality") from None


_Optimality_string_map: dict[str, Optimality] = {
    'maximum': Optimality.MAXIMUM,
    'minimum': Optimality.MINIMUM,
}


class NeighborMode(IntEnum):
    """Python counterpart of an ``igraph_neimode_t`` enum."""

    OUT = 1
    IN = 2
    ALL = 3

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
                return _NeighborMode_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to NeighborMode") from None


_NeighborMode_string_map: dict[str, NeighborMode] = {
    'all': NeighborMode.ALL,
    'in': NeighborMode.IN,
    'out': NeighborMode.OUT,
}


class Connectedness(IntEnum):
    """Python counterpart of an ``igraph_connectedness_t`` enum."""

    WEAK = 1
    STRONG = 2

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
                return _Connectedness_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to Connectedness") from None


_Connectedness_string_map: dict[str, Connectedness] = {
    'strong': Connectedness.STRONG,
    'weak': Connectedness.WEAK,
}


class Reciprocity(IntEnum):
    """Python counterpart of an ``igraph_reciprocity_t`` enum."""

    DEFAULT = 0
    RATIO = 1

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
                return _Reciprocity_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to Reciprocity") from None


_Reciprocity_string_map: dict[str, Reciprocity] = {
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
                return _AdjacencyMode_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to AdjacencyMode") from None


_AdjacencyMode_string_map: dict[str, AdjacencyMode] = {
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
                return _StarMode_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to StarMode") from None


_StarMode_string_map: dict[str, StarMode] = {
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
                return _WheelMode_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to WheelMode") from None


_WheelMode_string_map: dict[str, WheelMode] = {
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
                return _TreeMode_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to TreeMode") from None


_TreeMode_string_map: dict[str, TreeMode] = {
    'in': TreeMode.IN,
    'out': TreeMode.OUT,
    'undirected': TreeMode.UNDIRECTED,
}


class ErdosRenyiType(IntEnum):
    """Python counterpart of an ``igraph_erdos_renyi_t`` enum."""

    GNP = 0
    GNM = 1

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, ErdosRenyiType):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return _ErdosRenyiType_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to ErdosRenyiType") from None


_ErdosRenyiType_string_map: dict[str, ErdosRenyiType] = {
    'gnm': ErdosRenyiType.GNM,
    'gnp': ErdosRenyiType.GNP,
}


class GetAdjacency(IntEnum):
    """Python counterpart of an ``igraph_get_adjacency_t`` enum."""

    UPPER = 0
    LOWER = 1
    BOTH = 2

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
                return _GetAdjacency_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to GetAdjacency") from None


_GetAdjacency_string_map: dict[str, GetAdjacency] = {
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
                return _DegreeSequenceMode_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to DegreeSequenceMode") from None


_DegreeSequenceMode_string_map: dict[str, DegreeSequenceMode] = {
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
                return _RealizeDegseq_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to RealizeDegseq") from None


_RealizeDegseq_string_map: dict[str, RealizeDegseq] = {
    'index': RealizeDegseq.INDEX,
    'largest': RealizeDegseq.LARGEST,
    'smallest': RealizeDegseq.SMALLEST,
}


class RandomTreeMethod(IntEnum):
    """Python counterpart of an ``igraph_random_tree_t`` enum."""

    PRUFER = 0
    LERW = 1

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
                return _RandomTreeMethod_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to RandomTreeMethod") from None


_RandomTreeMethod_string_map: dict[str, RandomTreeMethod] = {
    'lerw': RandomTreeMethod.LERW,
    'prufer': RandomTreeMethod.PRUFER,
}


class Rewiring(IntEnum):
    """Python counterpart of an ``igraph_rewiring_t`` enum."""

    SIMPLE = 0
    SIMPLE_LOOPS = 1

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
                return _Rewiring_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to Rewiring") from None


_Rewiring_string_map: dict[str, Rewiring] = {
    'simple': Rewiring.SIMPLE,
    'simple_loops': Rewiring.SIMPLE_LOOPS,
}


class EdgeOrder(IntEnum):
    """Python counterpart of an ``igraph_edgeorder_type_t`` enum."""

    ID = 0
    FROM = 1
    TO = 2

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
                return _EdgeOrder_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to EdgeOrder") from None


_EdgeOrder_string_map: dict[str, EdgeOrder] = {
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
                return _ToDirected_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to ToDirected") from None


_ToDirected_string_map: dict[str, ToDirected] = {
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
                return _ToUndirected_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to ToUndirected") from None


_ToUndirected_string_map: dict[str, ToUndirected] = {
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
                return _VconnNei_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to VconnNei") from None


_VconnNei_string_map: dict[str, VconnNei] = {
    'error': VconnNei.ERROR,
    'ignore': VconnNei.IGNORE,
    'negative': VconnNei.NEGATIVE,
    'number_of_nodes': VconnNei.NUMBER_OF_NODES,
}


class SpinglassUpdateMode(IntEnum):
    """Python counterpart of an ``igraph_spincomm_update_t`` enum."""

    SIMPLE = 0
    CONFIG = 1

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
                return _SpinglassUpdateMode_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to SpinglassUpdateMode") from None


_SpinglassUpdateMode_string_map: dict[str, SpinglassUpdateMode] = {
    'config': SpinglassUpdateMode.CONFIG,
    'simple': SpinglassUpdateMode.SIMPLE,
}


class LazyAdjacencyListSimplify(IntEnum):
    """Python counterpart of an ``igraph_lazy_adlist_simplify_t`` enum."""

    DONT_SIMPLIFY = 0
    SIMPLIFY = 1

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
                return _LazyAdjacencyListSimplify_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to LazyAdjacencyListSimplify") from None


_LazyAdjacencyListSimplify_string_map: dict[str, LazyAdjacencyListSimplify] = {
    'dont_simplify': LazyAdjacencyListSimplify.DONT_SIMPLIFY,
    'simplify': LazyAdjacencyListSimplify.SIMPLIFY,
}


class TransitivityMode(IntEnum):
    """Python counterpart of an ``igraph_transitivity_mode_t`` enum."""

    NAN = 0
    ZERO = 1

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
                return _TransitivityMode_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to TransitivityMode") from None


_TransitivityMode_string_map: dict[str, TransitivityMode] = {
    'nan': TransitivityMode.NAN,
    'zero': TransitivityMode.ZERO,
}


class SpinglassImplementation(IntEnum):
    """Python counterpart of an ``igraph_spinglass_implementation_t`` enum."""

    ORIG = 0
    NEG = 1

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
                return _SpinglassImplementation_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to SpinglassImplementation") from None


_SpinglassImplementation_string_map: dict[str, SpinglassImplementation] = {
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
                return _CommunityComparison_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to CommunityComparison") from None


_CommunityComparison_string_map: dict[str, CommunityComparison] = {
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
                return _AddWeights_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to AddWeights") from None


_AddWeights_string_map: dict[str, AddWeights] = {
    'if_present': AddWeights.IF_PRESENT,
    'no': AddWeights.NO,
    'yes': AddWeights.YES,
}


class BarabasiAlgorithm(IntEnum):
    """Python counterpart of an ``igraph_barabasi_algorithm_t`` enum."""

    BAG = 0
    PSUMTREE = 1
    PSUMTREE_MULTIPLE = 2

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
                return _BarabasiAlgorithm_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to BarabasiAlgorithm") from None


_BarabasiAlgorithm_string_map: dict[str, BarabasiAlgorithm] = {
    'bag': BarabasiAlgorithm.BAG,
    'psumtree': BarabasiAlgorithm.PSUMTREE,
    'psumtree_multiple': BarabasiAlgorithm.PSUMTREE_MULTIPLE,
}


class FeedbackArcSetAlgorithm(IntEnum):
    """Python counterpart of an ``igraph_fas_algorithm_t`` enum."""

    EXACT_IP = 0
    APPROX_EADES = 1
    EXACT_IP_CG = 2
    EXACT_IP_TI = 3

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
                return _FeedbackArcSetAlgorithm_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to FeedbackArcSetAlgorithm") from None


_FeedbackArcSetAlgorithm_string_map: dict[str, FeedbackArcSetAlgorithm] = {
    'approx_eades': FeedbackArcSetAlgorithm.APPROX_EADES,
    'exact_ip': FeedbackArcSetAlgorithm.EXACT_IP,
    'exact_ip_cg': FeedbackArcSetAlgorithm.EXACT_IP_CG,
    'exact_ip_ti': FeedbackArcSetAlgorithm.EXACT_IP_TI,
}


class FvsAlgorithm(IntEnum):
    """Python counterpart of an ``igraph_fvs_algorithm_t`` enum."""

    IP = 0

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, FvsAlgorithm):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return _FvsAlgorithm_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to FvsAlgorithm") from None


_FvsAlgorithm_string_map: dict[str, FvsAlgorithm] = {
    'ip': FvsAlgorithm.IP,
}


class SubgraphImplementation(IntEnum):
    """Python counterpart of an ``igraph_subgraph_implementation_t`` enum."""

    AUTO = 0
    COPY_AND_DELETE = 1
    CREATE_FROM_SCRATCH = 2

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
                return _SubgraphImplementation_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to SubgraphImplementation") from None


_SubgraphImplementation_string_map: dict[str, SubgraphImplementation] = {
    'auto': SubgraphImplementation.AUTO,
    'copy_and_delete': SubgraphImplementation.COPY_AND_DELETE,
    'create_from_scratch': SubgraphImplementation.CREATE_FROM_SCRATCH,
}


class ImitateAlgorithm(IntEnum):
    """Python counterpart of an ``igraph_imitate_algorithm_t`` enum."""

    AUGMENTED = 0
    BLIND = 1
    CONTRACTED = 2

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
                return _ImitateAlgorithm_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to ImitateAlgorithm") from None


_ImitateAlgorithm_string_map: dict[str, ImitateAlgorithm] = {
    'augmented': ImitateAlgorithm.AUGMENTED,
    'blind': ImitateAlgorithm.BLIND,
    'contracted': ImitateAlgorithm.CONTRACTED,
}


class LayoutGrid(IntEnum):
    """Python counterpart of an ``igraph_layout_grid_t`` enum."""

    GRID = 0
    NOGRID = 1
    AUTOGRID = 2
    NO_GRID = NOGRID
    AUTO_GRID = AUTOGRID

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
                return _LayoutGrid_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to LayoutGrid") from None


_LayoutGrid_string_map: dict[str, LayoutGrid] = {
    'auto_grid': LayoutGrid.AUTOGRID,
    'autogrid': LayoutGrid.AUTOGRID,
    'grid': LayoutGrid.GRID,
    'no_grid': LayoutGrid.NOGRID,
    'nogrid': LayoutGrid.NOGRID,
}


class RandomWalkStuck(IntEnum):
    """Python counterpart of an ``igraph_random_walk_stuck_t`` enum."""

    ERROR = 0
    RETURN = 1

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
                return _RandomWalkStuck_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to RandomWalkStuck") from None


_RandomWalkStuck_string_map: dict[str, RandomWalkStuck] = {
    'error': RandomWalkStuck.ERROR,
    'return': RandomWalkStuck.RETURN,
}


class VoronoiTiebreaker(IntEnum):
    """Python counterpart of an ``igraph_voronoi_tiebreaker_t`` enum."""

    FIRST = 0
    LAST = 1
    RANDOM = 2

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
                return _VoronoiTiebreaker_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to VoronoiTiebreaker") from None


_VoronoiTiebreaker_string_map: dict[str, VoronoiTiebreaker] = {
    'first': VoronoiTiebreaker.FIRST,
    'last': VoronoiTiebreaker.LAST,
    'random': VoronoiTiebreaker.RANDOM,
}


class ChungLu(IntEnum):
    """Python counterpart of an ``igraph_chung_lu_t`` enum."""

    ORIGINAL = 0
    MAXENT = 1
    NR = 2

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, ChungLu):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return _ChungLu_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to ChungLu") from None


_ChungLu_string_map: dict[str, ChungLu] = {
    'maxent': ChungLu.MAXENT,
    'nr': ChungLu.NR,
    'original': ChungLu.ORIGINAL,
}


class MatrixStorage(IntEnum):
    """Python counterpart of an ``igraph_matrix_storage_t`` enum."""

    ROW_MAJOR = 0
    COLUMN_MAJOR = 1

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
                return _MatrixStorage_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to MatrixStorage") from None


_MatrixStorage_string_map: dict[str, MatrixStorage] = {
    'column_major': MatrixStorage.COLUMN_MAJOR,
    'row_major': MatrixStorage.ROW_MAJOR,
}


class MstAlgorithm(IntEnum):
    """Python counterpart of an ``igraph_mst_algorithm_t`` enum."""

    AUTOMATIC = 0
    UNWEIGHTED = 1
    PRIM = 2
    KRUSKAL = 3

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, MstAlgorithm):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return _MstAlgorithm_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to MstAlgorithm") from None


_MstAlgorithm_string_map: dict[str, MstAlgorithm] = {
    'automatic': MstAlgorithm.AUTOMATIC,
    'kruskal': MstAlgorithm.KRUSKAL,
    'prim': MstAlgorithm.PRIM,
    'unweighted': MstAlgorithm.UNWEIGHTED,
}


class LpaVariant(IntEnum):
    """Python counterpart of an ``igraph_lpa_variant_t`` enum."""

    DOMINANCE = 0
    RETENTION = 1
    FAST = 2

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, LpaVariant):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return _LpaVariant_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to LpaVariant") from None


_LpaVariant_string_map: dict[str, LpaVariant] = {
    'dominance': LpaVariant.DOMINANCE,
    'fast': LpaVariant.FAST,
    'retention': LpaVariant.RETENTION,
}


class ErrorCode(IntEnum):
    """Python counterpart of an ``igraph_error_type_t`` enum."""

    SUCCESS = 0
    FAILURE = 1
    ENOMEM = 2
    PARSEERROR = 3
    EINVAL = 4
    EXISTS = 5
    EINVVID = 7
    EINVEID = 8
    EINVMODE = 9
    EFILE = 10
    UNIMPLEMENTED = 12
    INTERRUPTED = 13
    DIVERGED = 14
    EARPACK = 15
    ENEGLOOP = 37
    EINTERNAL = 38
    EATTRCOMBINE = 52
    EOVERFLOW = 55
    EUNDERFLOW = 58
    ERWSTUCK = 59
    STOP = 60
    ERANGE = 61
    ENOSOL = 62

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
                return _ErrorCode_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to ErrorCode") from None


_ErrorCode_string_map: dict[str, ErrorCode] = {
    'diverged': ErrorCode.DIVERGED,
    'earpack': ErrorCode.EARPACK,
    'eattrcombine': ErrorCode.EATTRCOMBINE,
    'efile': ErrorCode.EFILE,
    'einternal': ErrorCode.EINTERNAL,
    'einval': ErrorCode.EINVAL,
    'einveid': ErrorCode.EINVEID,
    'einvmode': ErrorCode.EINVMODE,
    'einvvid': ErrorCode.EINVVID,
    'enegloop': ErrorCode.ENEGLOOP,
    'enomem': ErrorCode.ENOMEM,
    'enosol': ErrorCode.ENOSOL,
    'eoverflow': ErrorCode.EOVERFLOW,
    'erange': ErrorCode.ERANGE,
    'erwstuck': ErrorCode.ERWSTUCK,
    'eunderflow': ErrorCode.EUNDERFLOW,
    'exists': ErrorCode.EXISTS,
    'failure': ErrorCode.FAILURE,
    'interrupted': ErrorCode.INTERRUPTED,
    'parseerror': ErrorCode.PARSEERROR,
    'stop': ErrorCode.STOP,
    'success': ErrorCode.SUCCESS,
    'unimplemented': ErrorCode.UNIMPLEMENTED,
}


class SparseMatrixType(IntEnum):
    """Python counterpart of an ``igraph_sparsemat_type_t`` enum."""

    TRIPLET = 0
    CC = 1

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
                return _SparseMatrixType_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to SparseMatrixType") from None


_SparseMatrixType_string_map: dict[str, SparseMatrixType] = {
    'cc': SparseMatrixType.CC,
    'triplet': SparseMatrixType.TRIPLET,
}


class SparseMatrixSolver(IntEnum):
    """Python counterpart of an ``igraph_sparsemat_solve_t`` enum."""

    LU = 0
    QR = 1

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
                return _SparseMatrixSolver_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to SparseMatrixSolver") from None


_SparseMatrixSolver_string_map: dict[str, SparseMatrixSolver] = {
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
                return _DRLLayoutPreset_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to DRLLayoutPreset") from None


_DRLLayoutPreset_string_map: dict[str, DRLLayoutPreset] = {
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
                return _RootChoice_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to RootChoice") from None


_RootChoice_string_map: dict[str, RootChoice] = {
    'degree': RootChoice.DEGREE,
    'eccentricity': RootChoice.ECCENTRICITY,
}


class ArpackError(IntEnum):
    """Python counterpart of an ``igraph_arpack_error_t`` enum."""

    NO_ERROR = 0
    PROD = 15
    NPOS = 16
    NEVNPOS = 17
    NCVSMALL = 18
    NONPOSI = 19
    WHICHINV = 20
    BMATINV = 21
    WORKLSMALL = 22
    TRIDERR = 23
    ZEROSTART = 24
    MODEINV = 25
    MODEBMAT = 26
    ISHIFT = 27
    NEVBE = 28
    NOFACT = 29
    FAILED = 30
    HOWMNY = 31
    HOWMNYS = 32
    EVDIFF = 33
    SHUR = 34
    LAPACK = 35
    UNKNOWN = 36
    MAXIT = 39
    NOSHIFT = 40
    REORDER = 41

    @classmethod
    def from_(cls, value: Any):
        """Converts an arbitrary Python object into this enum.

        Raises:
            ValueError: if the object cannot be converted
        """
        if isinstance(value, ArpackError):
            return value
        elif isinstance(value, int):
            return cls(value)
        else:
            try:
                return _ArpackError_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to ArpackError") from None


_ArpackError_string_map: dict[str, ArpackError] = {
    'bmatinv': ArpackError.BMATINV,
    'evdiff': ArpackError.EVDIFF,
    'failed': ArpackError.FAILED,
    'howmny': ArpackError.HOWMNY,
    'howmnys': ArpackError.HOWMNYS,
    'ishift': ArpackError.ISHIFT,
    'lapack': ArpackError.LAPACK,
    'maxit': ArpackError.MAXIT,
    'modebmat': ArpackError.MODEBMAT,
    'modeinv': ArpackError.MODEINV,
    'ncvsmall': ArpackError.NCVSMALL,
    'nevbe': ArpackError.NEVBE,
    'nevnpos': ArpackError.NEVNPOS,
    'no_error': ArpackError.NO_ERROR,
    'nofact': ArpackError.NOFACT,
    'nonposi': ArpackError.NONPOSI,
    'noshift': ArpackError.NOSHIFT,
    'npos': ArpackError.NPOS,
    'prod': ArpackError.PROD,
    'reorder': ArpackError.REORDER,
    'shur': ArpackError.SHUR,
    'triderr': ArpackError.TRIDERR,
    'unknown': ArpackError.UNKNOWN,
    'whichinv': ArpackError.WHICHINV,
    'worklsmall': ArpackError.WORKLSMALL,
    'zerostart': ArpackError.ZEROSTART,
}


class LaplacianNormalization(IntEnum):
    """Python counterpart of an ``igraph_laplacian_normalization_t`` enum."""

    UNNORMALIZED = 0
    SYMMETRIC = 1
    LEFT = 2
    RIGHT = 3

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
                return _LaplacianNormalization_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to LaplacianNormalization") from None


_LaplacianNormalization_string_map: dict[str, LaplacianNormalization] = {
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
                return _LeadingEigenvectorCommunityHistory_string_map[value]
            except KeyError:
                raise ValueError(f"{value!r} cannot be converted to LeadingEigenvectorCommunityHistory") from None


_LeadingEigenvectorCommunityHistory_string_map: dict[str, LeadingEigenvectorCommunityHistory] = {
    'failed': LeadingEigenvectorCommunityHistory.FAILED,
    'split': LeadingEigenvectorCommunityHistory.SPLIT,
    'start_full': LeadingEigenvectorCommunityHistory.START_FULL,
    'start_given': LeadingEigenvectorCommunityHistory.START_GIVEN,
}


__all__ = (
    'AddWeights',
    'AdjacencyMode',
    'ArpackError',
    'AttributeCombinationType',
    'AttributeElementType',
    'AttributeType',
    'BLISSSplittingHeuristics',
    'BarabasiAlgorithm',
    'ChungLu',
    'CommunityComparison',
    'Connectedness',
    'DRLLayoutPreset',
    'DegreeSequenceMode',
    'EdgeIteratorType',
    'EdgeOrder',
    'EdgeSequenceType',
    'EigenAlgorithm',
    'ErdosRenyiType',
    'ErrorCode',
    'FeedbackArcSetAlgorithm',
    'FloydWarshallAlgorithm',
    'FvsAlgorithm',
    'GetAdjacency',
    'GreedyColoringHeuristics',
    'ImitateAlgorithm',
    'LaplacianNormalization',
    'LaplacianSpectralEmbeddingType',
    'LayoutGrid',
    'LazyAdjacencyListSimplify',
    'LeadingEigenvectorCommunityHistory',
    'Loops',
    'LpaVariant',
    'MatrixStorage',
    'MstAlgorithm',
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
