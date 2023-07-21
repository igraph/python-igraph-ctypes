from enum import IntEnum


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


class AttributeElementType(IntEnum):
    """Python counterpart of an ``igraph_attribute_elemtype_t`` enum."""

    GRAPH = 0
    VERTEX = 1
    EDGE = 2


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


class ColoringGreedy(IntEnum):
    """Python counterpart of an ``igraph_coloring_greedy_t`` enum."""

    COLORED_NEIGHBORS = 0
    DSATUR = 1


class PagerankAlgorithm(IntEnum):
    """Python counterpart of an ``igraph_pagerank_algo_t`` enum."""

    ARPACK = 1
    PRPACK = 2


class FloydWarshallAlgorithm(IntEnum):
    """Python counterpart of an ``igraph_floyd_warshall_algorithm_t`` enum."""

    AUTOMATIC = 0
    ORIGINAL = 1
    TREE = 2


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


class VertexIteratorType(IntEnum):
    """Python counterpart of an ``igraph_vit_type_t`` enum."""

    RANGE = 0
    VECTOR = 1
    VECTORPTR = 2


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


class EdgeIteratorType(IntEnum):
    """Python counterpart of an ``igraph_eit_type_t`` enum."""

    RANGE = 0
    VECTOR = 1
    VECTORPTR = 2


class EigenAlgorithm(IntEnum):
    """Python counterpart of an ``igraph_eigen_algorithm_t`` enum."""

    AUTO = 0
    LAPACK = 1
    ARPACK = 2
    COMP_AUTO = 3
    COMP_LAPACK = 4
    COMP_ARPACK = 5


class LaplacianSpectralEmbeddingType(IntEnum):
    """Python counterpart of an ``igraph_laplacian_spectral_embedding_type_t`` enum."""

    D_A = 0
    I_DAD = 1
    DAD = 2
    OAP = 3


class Multiple(IntEnum):
    """Python counterpart of an ``igraph_multiple_t`` enum."""

    NO_MULTIPLE = 0
    MULTIPLE = 1


class Order(IntEnum):
    """Python counterpart of an ``igraph_order_t`` enum."""

    ASCENDING = 0
    DESCENDING = 1


class Optimality(IntEnum):
    """Python counterpart of an ``igraph_optimal_t`` enum."""

    MINIMUM = 0
    MAXIMUM = 1


class NeighborMode(IntEnum):
    """Python counterpart of an ``igraph_neimode_t`` enum."""

    OUT = 1
    IN = 2
    ALL = 3


class Connectedness(IntEnum):
    """Python counterpart of an ``igraph_connectedness_t`` enum."""

    WEAK = 1
    STRONG = 2


class Reciprocity(IntEnum):
    """Python counterpart of an ``igraph_reciprocity_t`` enum."""

    DEFAULT = 0
    RATIO = 1


class AdjacencyMode(IntEnum):
    """Python counterpart of an ``igraph_adjacency_t`` enum."""

    DIRECTED = 0
    UNDIRECTED = 1
    UPPER = 2
    LOWER = 3
    MIN = 4
    PLUS = 5
    MAX = 6


class StarMode(IntEnum):
    """Python counterpart of an ``igraph_star_mode_t`` enum."""

    OUT = 0
    IN = 1
    UNDIRECTED = 2
    MUTUAL = 3


class WheelMode(IntEnum):
    """Python counterpart of an ``igraph_wheel_mode_t`` enum."""

    OUT = 0
    IN = 1
    UNDIRECTED = 2
    MUTUAL = 3


class TreeMode(IntEnum):
    """Python counterpart of an ``igraph_tree_mode_t`` enum."""

    OUT = 0
    IN = 1
    UNDIRECTED = 2


class ErdosRenyi(IntEnum):
    """Python counterpart of an ``igraph_erdos_renyi_t`` enum."""

    GNP = 0
    GNM = 1


class GetAdjacency(IntEnum):
    """Python counterpart of an ``igraph_get_adjacency_t`` enum."""

    UPPER = 0
    LOWER = 1
    BOTH = 2


class DegreeSequenceMode(IntEnum):
    """Python counterpart of an ``igraph_degseq_t`` enum."""

    CONFIGURATION = 0
    VL = 1
    FAST_HEUR_SIMPLE = 2
    CONFIGURATION_SIMPLE = 3
    EDGE_SWITCHING_SIMPLE = 4


class RealizeDegseq(IntEnum):
    """Python counterpart of an ``igraph_realize_degseq_t`` enum."""

    SMALLEST = 0
    LARGEST = 1
    INDEX = 2


class RandomTreeMethod(IntEnum):
    """Python counterpart of an ``igraph_random_tree_t`` enum."""

    PRUFER = 0
    LERW = 1


class FileFormat(IntEnum):
    """Python counterpart of an ``igraph_fileformat_type_t`` enum."""

    EDGELIST = 0
    NCOL = 1
    PAJEK = 2
    LGL = 3
    GRAPHML = 4


class Rewiring(IntEnum):
    """Python counterpart of an ``igraph_rewiring_t`` enum."""

    SIMPLE = 0
    SIMPLE_LOOPS = 1


class EdgeOrder(IntEnum):
    """Python counterpart of an ``igraph_edgeorder_type_t`` enum."""

    ID = 0
    FROM = 1
    TO = 2


class ToDirected(IntEnum):
    """Python counterpart of an ``igraph_to_directed_t`` enum."""

    ARBITRARY = 0
    MUTUAL = 1
    RANDOM = 2
    ACYCLIC = 3


class ToUndirected(IntEnum):
    """Python counterpart of an ``igraph_to_undirected_t`` enum."""

    EACH = 0
    COLLAPSE = 1
    MUTUAL = 2


class VconnNei(IntEnum):
    """Python counterpart of an ``igraph_vconn_nei_t`` enum."""

    ERROR = 0
    NUMBER_OF_NODES = 1
    IGNORE = 2
    NEGATIVE = 3


class SpinglassUpdateMode(IntEnum):
    """Python counterpart of an ``igraph_spincomm_update_t`` enum."""

    SIMPLE = 0
    CONFIG = 1


class LazyAdjacencyListSimplify(IntEnum):
    """Python counterpart of an ``igraph_lazy_adlist_simplify_t`` enum."""

    DONT_SIMPLIFY = 0
    SIMPLIFY = 1


class TransitivityMode(IntEnum):
    """Python counterpart of an ``igraph_transitivity_mode_t`` enum."""

    NAN = 0
    ZERO = 1


class SpinglassImplementation(IntEnum):
    """Python counterpart of an ``igraph_spinglass_implementation_t`` enum."""

    ORIG = 0
    NEG = 1


class CommunityComparison(IntEnum):
    """Python counterpart of an ``igraph_community_comparison_t`` enum."""

    VI = 0
    NMI = 1
    SPLIT_JOIN = 2
    RAND = 3
    ADJUSTED_RAND = 4


class AddWeights(IntEnum):
    """Python counterpart of an ``igraph_add_weights_t`` enum."""

    NO = 0
    YES = 1
    IF_PRESENT = 2


class BarabasiAlgorithm(IntEnum):
    """Python counterpart of an ``igraph_barabasi_algorithm_t`` enum."""

    BAG = 0
    PSUMTREE = 1
    PSUMTREE_MULTIPLE = 2


class FeedbackArcSetAlgorithm(IntEnum):
    """Python counterpart of an ``igraph_fas_algorithm_t`` enum."""

    EXACT_IP = 0
    APPROX_EADES = 1


class SubgraphImplementation(IntEnum):
    """Python counterpart of an ``igraph_subgraph_implementation_t`` enum."""

    AUTO = 0
    COPY_AND_DELETE = 1
    CREATE_FROM_SCRATCH = 2


class ImitateAlgorithm(IntEnum):
    """Python counterpart of an ``igraph_imitate_algorithm_t`` enum."""

    AUGMENTED = 0
    BLIND = 1
    CONTRACTED = 2


class LayoutGrid(IntEnum):
    """Python counterpart of an ``igraph_layout_grid_t`` enum."""

    GRID = 0
    NOGRID = 1
    AUTOGRID = 2


class RandomWalkStuck(IntEnum):
    """Python counterpart of an ``igraph_random_walk_stuck_t`` enum."""

    ERROR = 0
    RETURN = 1


class VoronoiTiebreaker(IntEnum):
    """Python counterpart of an ``igraph_voronoi_tiebreaker_t`` enum."""

    FIRST = 0
    LAST = 1
    RANDOM = 2


class MatrixStorage(IntEnum):
    """Python counterpart of an ``igraph_matrix_storage_t`` enum."""

    ROW_MAJOR = 0
    COLUMN_MAJOR = 1


class ErrorType(IntEnum):
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


class SparseMatrixType(IntEnum):
    """Python counterpart of an ``igraph_sparsemat_type_t`` enum."""

    TRIPLET = 0
    CC = 1


class SparseMatrixSolver(IntEnum):
    """Python counterpart of an ``igraph_sparsemat_solve_t`` enum."""

    LU = 0
    QR = 1


class DRLLayoutPreset(IntEnum):
    """Python counterpart of an ``igraph_layout_drl_default_t`` enum."""

    DEFAULT = 0
    COARSEN = 1
    COARSEST = 2
    REFINE = 3
    FINAL = 4


class RootChoice(IntEnum):
    """Python counterpart of an ``igraph_root_choice_t`` enum."""

    DEGREE = 0
    ECCENTRICITY = 1


class BLISSSplittingHeuristics(IntEnum):
    """Python counterpart of an ``igraph_bliss_sh_t`` enum."""

    F = 0
    FL = 1
    FS = 2
    FM = 3
    FLM = 4
    FSM = 5


class LaplacianNormalization(IntEnum):
    """Python counterpart of an ``igraph_laplacian_normalization_t`` enum."""

    UNNORMALIZED = 0
    SYMMETRIC = 1
    LEFT = 2
    RIGHT = 3


class LeadingEigenvectorCommunityHistory(IntEnum):
    """Python counterpart of an ``igraph_leading_eigenvector_community_history_t`` enum."""

    SPLIT = 1
    FAILED = 2
    START_FULL = 3
    START_GIVEN = 4


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
    'ErrorType',
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
