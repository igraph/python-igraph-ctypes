from numpy import array
from numpy.testing import assert_array_equal

from igraph_ctypes.constructors import create_square_lattice
from igraph_ctypes.conversion import get_edge_list


def test_get_edge_list():
    g = create_square_lattice([4, 3])

    edges = get_edge_list(g)
    assert_array_equal(
        edges,
        array(
            [
                [0, 1],
                [0, 4],
                [1, 2],
                [1, 5],
                [2, 3],
                [2, 6],
                [3, 7],
                [4, 5],
                [4, 8],
                [5, 6],
                [5, 9],
                [6, 7],
                [6, 10],
                [7, 11],
                [8, 9],
                [9, 10],
                [10, 11],
            ]
        ),
    )
