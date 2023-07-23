from numpy import array
from numpy.testing import assert_array_equal
from pytest import raises

from igraph_ctypes.constructors import create_square_lattice
from igraph_ctypes.paths import shortest_path


def test_shortest_path():
    g = create_square_lattice([4, 3])

    path = shortest_path(g, 0, 11)
    assert_array_equal(path, array([0, 1, 2, 3, 7, 11]))

    weights = [2] * g.ecount()
    expected_path = [0, 4, 5, 6, 7, 11]
    for u, v in zip(expected_path, expected_path[1:]):
        weights[g.get_edge_id(u, v)] = 1

    path = shortest_path(g, 0, 11, weights=weights)
    assert_array_equal(path, array(expected_path))

    path = shortest_path(g, 0, 11, weights=weights, method="dijkstra")
    assert_array_equal(path, array(expected_path))

    path = shortest_path(g, 0, 11, weights=weights, method="bellman-ford")
    assert_array_equal(path, array(expected_path))

    with raises(ValueError, match="unknown method"):
        shortest_path(g, 0, 11, weights=weights, method="spam")
