from typing import Literal, get_args, get_origin

import pytest

from igraph_ctypes import enums
from igraph_ctypes._internal import enums as _enums
from igraph_ctypes._internal.functions import (
    erdos_renyi_game_gnm,
    is_bipartite_coloring,
    is_graphical,
    neighbors,
    ring,
)


def test_public_enums_are_string_literals():
    assert set(get_args(enums.NeighborMode)) == {"out", "in", "all"}
    assert set(get_args(enums.Loops)) == {"ignore", "once", "twice"}
    assert "exact_ip" in get_args(enums.FvsAlgorithm)


def _string_literals_of(alias) -> tuple[str, ...]:
    if get_origin(alias) is Literal:
        return get_args(alias)
    else:
        return tuple(s for arg in get_args(alias) for s in _string_literals_of(arg))


@pytest.mark.parametrize("name", enums.__all__)
def test_every_literal_is_accepted_by_its_enum(name):
    enum_class = getattr(_enums, name)
    strings = _string_literals_of(getattr(enums, name))
    assert strings
    for value in strings:
        assert isinstance(enum_class.from_(value), enum_class)


def test_add_weights_accepts_booleans():
    assert bool in get_args(enums.AddWeights)
    assert _enums.AddWeights.from_(True) is _enums.AddWeights.from_("yes")
    assert _enums.AddWeights.from_(False) is _enums.AddWeights.from_("no")


def test_strings_as_enum_arguments():
    g = ring(3, True, False, True)
    assert neighbors(g, 0, "out").tolist() == [1]
    assert neighbors(g, 0, "in").tolist() == [2]
    assert sorted(neighbors(g, 0, "all").tolist()) == [1, 2]


def test_enum_members_and_ints_are_still_accepted():
    g = ring(3, True, False, True)
    assert neighbors(g, 0, _enums.NeighborMode.IN).tolist() == [2]
    assert neighbors(g, 0, int(_enums.NeighborMode.IN)).tolist() == [2]


def test_invalid_string_is_rejected():
    g = ring(3, True, False, True)
    with pytest.raises(ValueError, match="cannot be converted to NeighborMode"):
        neighbors(g, 0, "sideways")  # type: ignore


def test_flags_from_strings_and_iterables():
    assert not is_graphical([2, 2])
    assert is_graphical([2, 2], None, "loops")

    # [4, 2] needs a self-loop on vertex 0 and two parallel edges
    assert not is_graphical([4, 2], None, "loops")
    assert not is_graphical([4, 2], None, "multi")
    assert is_graphical([4, 2], None, ("loops", "multi"))
    assert is_graphical([4, 2], None, ["multi", "loops"])

    g = erdos_renyi_game_gnm(5, 30, False, "multi")
    assert g.ecount() == 30

    with pytest.raises(ValueError, match="cannot be converted to AllowedEdgeTypes"):
        is_graphical([2, 2], None, ("loops", "multiple"))  # type: ignore


def test_enum_output_is_converted_to_string():
    g = ring(4, False, False, True)
    is_coloring, mode = is_bipartite_coloring(g, [False, True, False, True])
    assert is_coloring
    assert mode in get_args(enums.NeighborMode)
