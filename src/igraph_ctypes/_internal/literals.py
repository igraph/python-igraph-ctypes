"""String literal types that the public API uses in place of the enums of the
C core of igraph.

Each type alias in this module lists the strings that are accepted for the
corresponding enum. The conversion to the C enum happens in the ``from_()``
class methods of the enums in ``._internal.enums``, which also accept the
enum members and integers.
"""

from __future__ import annotations

from typing import Iterable, Literal, TypeAlias

# fmt: off
# The rest of this file is generated
AddWeights: TypeAlias = Literal["no", "yes", "if_present"] | bool
"""String literals accepted where a value of the ``AddWeights`` enum is expected. ``True`` and ``False`` are equivalent to ``"yes"`` and ``"no"``."""

AdjacencyMode: TypeAlias = Literal["directed", "undirected", "upper", "lower", "min", "plus", "max"]
"""String literals accepted where a value of the ``AdjacencyMode`` enum is expected."""

AllowedEdgeTypes: TypeAlias = Literal["simple", "loops", "multi"] | Iterable[Literal["simple", "loops", "multi"]]
"""String literals accepted where a combination of flags of the ``AllowedEdgeTypes`` enum is expected."""

ArpackError: TypeAlias = Literal["no_error", "prod", "npos", "nevnpos", "ncvsmall", "nonposi", "whichinv", "bmatinv", "worklsmall", "triderr", "zerostart", "modeinv", "modebmat", "ishift", "nevbe", "nofact", "failed", "howmny", "howmnys", "evdiff", "shur", "lapack", "unknown", "maxit", "noshift", "reorder"]
"""String literals accepted where a value of the ``ArpackError`` enum is expected."""

AttributeCombinationType: TypeAlias = Literal["ignore", "default", "function", "sum", "prod", "min", "max", "random", "first", "last", "mean", "median", "concat"]
"""String literals accepted where a value of the ``AttributeCombinationType`` enum is expected."""

AttributeElementType: TypeAlias = Literal["graph", "vertex", "edge"]
"""String literals accepted where a value of the ``AttributeElementType`` enum is expected."""

AttributeType: TypeAlias = Literal["unspecified", "numeric", "boolean", "string", "object"]
"""String literals accepted where a value of the ``AttributeType`` enum is expected."""

BLISSSplittingHeuristics: TypeAlias = Literal["f", "fl", "fs", "fm", "flm", "fsm"]
"""String literals accepted where a value of the ``BLISSSplittingHeuristics`` enum is expected."""

BarabasiAlgorithm: TypeAlias = Literal["bag", "psumtree", "psumtree_multiple"]
"""String literals accepted where a value of the ``BarabasiAlgorithm`` enum is expected."""

ChungLu: TypeAlias = Literal["original", "maxent", "nr"]
"""String literals accepted where a value of the ``ChungLu`` enum is expected."""

CommunityComparison: TypeAlias = Literal["vi", "nmi", "split_join", "rand", "adjusted_rand"]
"""String literals accepted where a value of the ``CommunityComparison`` enum is expected."""

Connectedness: TypeAlias = Literal["weak", "strong"]
"""String literals accepted where a value of the ``Connectedness`` enum is expected."""

DRLLayoutPreset: TypeAlias = Literal["default", "coarsen", "coarsest", "refine", "final"]
"""String literals accepted where a value of the ``DRLLayoutPreset`` enum is expected."""

DegreeSequenceMode: TypeAlias = Literal["configuration", "vl", "fast_heur_simple", "configuration_simple", "edge_switching_simple"]
"""String literals accepted where a value of the ``DegreeSequenceMode`` enum is expected."""

EdgeIteratorType: TypeAlias = Literal["range", "vector", "vectorptr"]
"""String literals accepted where a value of the ``EdgeIteratorType`` enum is expected."""

EdgeOrder: TypeAlias = Literal["id", "from", "to"]
"""String literals accepted where a value of the ``EdgeOrder`` enum is expected."""

EdgeSequenceType: TypeAlias = Literal["all", "allfrom", "allto", "incident", "none", "one", "vectorptr", "vector", "range", "pairs", "path", "all_between"]
"""String literals accepted where a value of the ``EdgeSequenceType`` enum is expected."""

EigenAlgorithm: TypeAlias = Literal["auto", "lapack", "arpack", "comp_auto", "comp_lapack", "comp_arpack"]
"""String literals accepted where a value of the ``EigenAlgorithm`` enum is expected."""

EigenWhichPosition: TypeAlias = Literal["lm", "sm", "la", "sa", "be", "lr", "sr", "li", "si", "all", "interval", "select"]
"""String literals accepted where a value of the ``EigenWhichPosition`` enum is expected."""

ErrorCode: TypeAlias = Literal["success", "failure", "enomem", "parseerror", "einval", "exists", "einvvid", "einveid", "einvmode", "efile", "unimplemented", "interrupted", "diverged", "earpack", "enegcycle", "einternal", "eattrcombine", "eoverflow", "eunderflow", "erwstuck", "stop", "erange", "enosol"]
"""String literals accepted where a value of the ``ErrorCode`` enum is expected."""

FeedbackArcSetAlgorithm: TypeAlias = Literal["exact_ip", "approx_eades", "exact_ip_cg", "exact_ip_ti"]
"""String literals accepted where a value of the ``FeedbackArcSetAlgorithm`` enum is expected."""

FloydWarshallAlgorithm: TypeAlias = Literal["automatic", "original", "tree"]
"""String literals accepted where a value of the ``FloydWarshallAlgorithm`` enum is expected."""

FvsAlgorithm: TypeAlias = Literal["exact_ip"]
"""String literals accepted where a value of the ``FvsAlgorithm`` enum is expected."""

GetAdjacency: TypeAlias = Literal["upper", "lower", "both"]
"""String literals accepted where a value of the ``GetAdjacency`` enum is expected."""

GreedyColoringHeuristics: TypeAlias = Literal["colored_neighbors", "dsatur", "neighbors"]
"""String literals accepted where a value of the ``GreedyColoringHeuristics`` enum is expected."""

LaplacianNormalization: TypeAlias = Literal["unnormalized", "symmetric", "left", "right"]
"""String literals accepted where a value of the ``LaplacianNormalization`` enum is expected."""

LaplacianSpectralEmbeddingType: TypeAlias = Literal["d_a", "i_dad", "dad", "oap"]
"""String literals accepted where a value of the ``LaplacianSpectralEmbeddingType`` enum is expected."""

LayoutGrid: TypeAlias = Literal["grid", "nogrid", "autogrid", "no_grid", "auto_grid"]
"""String literals accepted where a value of the ``LayoutGrid`` enum is expected."""

LeadingEigenvectorCommunityHistory: TypeAlias = Literal["split", "failed", "start_full", "start_given"]
"""String literals accepted where a value of the ``LeadingEigenvectorCommunityHistory`` enum is expected."""

LeidenObjective: TypeAlias = Literal["modularity", "cpm", "er"]
"""String literals accepted where a value of the ``LeidenObjective`` enum is expected."""

Loops: TypeAlias = Literal["ignore", "twice", "once"]
"""String literals accepted where a value of the ``Loops`` enum is expected."""

LpaVariant: TypeAlias = Literal["dominance", "retention", "fast"]
"""String literals accepted where a value of the ``LpaVariant`` enum is expected."""

MatrixStorage: TypeAlias = Literal["row_major", "column_major"]
"""String literals accepted where a value of the ``MatrixStorage`` enum is expected."""

Metric: TypeAlias = Literal["euclidean", "manhattan"]
"""String literals accepted where a value of the ``Metric`` enum is expected."""

MstAlgorithm: TypeAlias = Literal["automatic", "unweighted", "prim", "kruskal"]
"""String literals accepted where a value of the ``MstAlgorithm`` enum is expected."""

NeighborMode: TypeAlias = Literal["out", "in", "all"]
"""String literals accepted where a value of the ``NeighborMode`` enum is expected."""

Order: TypeAlias = Literal["ascending", "descending"]
"""String literals accepted where a value of the ``Order`` enum is expected."""

PagerankAlgorithm: TypeAlias = Literal["arpack", "prpack"]
"""String literals accepted where a value of the ``PagerankAlgorithm`` enum is expected."""

Product: TypeAlias = Literal["cartesian", "lexicographic", "strong", "tensor", "modular"]
"""String literals accepted where a value of the ``Product`` enum is expected."""

RandomTreeMethod: TypeAlias = Literal["prufer", "lerw"]
"""String literals accepted where a value of the ``RandomTreeMethod`` enum is expected."""

RandomWalkStuck: TypeAlias = Literal["error", "return"]
"""String literals accepted where a value of the ``RandomWalkStuck`` enum is expected."""

RealizeDegseq: TypeAlias = Literal["smallest", "largest", "index"]
"""String literals accepted where a value of the ``RealizeDegseq`` enum is expected."""

Reciprocity: TypeAlias = Literal["default", "ratio"]
"""String literals accepted where a value of the ``Reciprocity`` enum is expected."""

RootChoice: TypeAlias = Literal["degree", "eccentricity"]
"""String literals accepted where a value of the ``RootChoice`` enum is expected."""

SparseMatrixSolver: TypeAlias = Literal["lu", "qr"]
"""String literals accepted where a value of the ``SparseMatrixSolver`` enum is expected."""

SparseMatrixType: TypeAlias = Literal["triplet", "cc"]
"""String literals accepted where a value of the ``SparseMatrixType`` enum is expected."""

SpinglassImplementation: TypeAlias = Literal["orig", "neg"]
"""String literals accepted where a value of the ``SpinglassImplementation`` enum is expected."""

SpinglassUpdateMode: TypeAlias = Literal["simple", "config"]
"""String literals accepted where a value of the ``SpinglassUpdateMode`` enum is expected."""

StarMode: TypeAlias = Literal["out", "in", "undirected", "mutual"]
"""String literals accepted where a value of the ``StarMode`` enum is expected."""

SubgraphImplementation: TypeAlias = Literal["auto", "copy_and_delete", "create_from_scratch"]
"""String literals accepted where a value of the ``SubgraphImplementation`` enum is expected."""

ToDirected: TypeAlias = Literal["arbitrary", "mutual", "random", "acyclic"]
"""String literals accepted where a value of the ``ToDirected`` enum is expected."""

ToUndirected: TypeAlias = Literal["each", "collapse", "mutual"]
"""String literals accepted where a value of the ``ToUndirected`` enum is expected."""

TransitivityMode: TypeAlias = Literal["nan", "zero"]
"""String literals accepted where a value of the ``TransitivityMode`` enum is expected."""

TreeMode: TypeAlias = Literal["out", "in", "undirected"]
"""String literals accepted where a value of the ``TreeMode`` enum is expected."""

VconnNei: TypeAlias = Literal["error", "number_of_nodes", "ignore", "negative"]
"""String literals accepted where a value of the ``VconnNei`` enum is expected."""

VertexIteratorType: TypeAlias = Literal["range", "vector", "vectorptr"]
"""String literals accepted where a value of the ``VertexIteratorType`` enum is expected."""

VertexSequenceType: TypeAlias = Literal["all", "adj", "none", "one", "vectorptr", "vector", "range", "nonadj"]
"""String literals accepted where a value of the ``VertexSequenceType`` enum is expected."""

VoronoiTiebreaker: TypeAlias = Literal["first", "last", "random"]
"""String literals accepted where a value of the ``VoronoiTiebreaker`` enum is expected."""

WheelMode: TypeAlias = Literal["out", "in", "undirected", "mutual"]
"""String literals accepted where a value of the ``WheelMode`` enum is expected."""

WriteGMLOptions: TypeAlias = Literal["default", "encode_only_quot"] | Iterable[Literal["default", "encode_only_quot"]]
"""String literals accepted where a combination of flags of the ``WriteGMLOptions`` enum is expected."""


__all__ = (
    'AddWeights',
    'AdjacencyMode',
    'AllowedEdgeTypes',
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
    'EigenWhichPosition',
    'ErrorCode',
    'FeedbackArcSetAlgorithm',
    'FloydWarshallAlgorithm',
    'FvsAlgorithm',
    'GetAdjacency',
    'GreedyColoringHeuristics',
    'LaplacianNormalization',
    'LaplacianSpectralEmbeddingType',
    'LayoutGrid',
    'LeadingEigenvectorCommunityHistory',
    'LeidenObjective',
    'Loops',
    'LpaVariant',
    'MatrixStorage',
    'Metric',
    'MstAlgorithm',
    'NeighborMode',
    'Order',
    'PagerankAlgorithm',
    'Product',
    'RandomTreeMethod',
    'RandomWalkStuck',
    'RealizeDegseq',
    'Reciprocity',
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
    'WriteGMLOptions',
)
