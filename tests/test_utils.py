from numpy import inf, nan, object_

from igraph_ctypes._internal.types import (
    np_type_of_igraph_bool_t,
    np_type_of_igraph_string,
    np_type_of_igraph_real_t,
)
from igraph_ctypes._internal.utils import get_numpy_attribute_type_from_iterable

from pytest import mark


get = get_numpy_attribute_type_from_iterable


@mark.parametrize(
    ("input", "expected"),
    [
        ((), np_type_of_igraph_real_t),
        ((17, -2), np_type_of_igraph_real_t),
        ((17.5, -3.5), np_type_of_igraph_real_t),
        ((inf, -3.5, nan), np_type_of_igraph_real_t),
        ((False, True), np_type_of_igraph_bool_t),
        ((False, 123, True), np_type_of_igraph_real_t),
        ((123, False, True), np_type_of_igraph_real_t),
        (("spam", "ham", "bacon"), np_type_of_igraph_string),
        (("spam", 123), object_),
        ((123, "spam"), object_),
        ((None,), object_),
        (("spam", False), object_),
        ((123, None), object_),
    ],
)
def test_empty(input, expected):
    assert get(input) == expected
