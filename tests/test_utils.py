from numpy import inf, nan, object_

from igraph_ctypes._internal.enums import AttributeType
from igraph_ctypes._internal.types import (
    np_type_of_igraph_bool_t,
    np_type_of_igraph_real_t,
)
from igraph_ctypes._internal.attributes.utils import (
    get_igraph_attribute_type_from_iterable,
    get_numpy_attribute_type_from_iterable,
)

from pytest import mark


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
        (("spam", "ham", "bacon"), object_),
        (("spam", 123), object_),
        ((123, "spam"), object_),
        ((None,), object_),
        (("spam", False), object_),
        ((123, None), object_),
    ],
)
def test_conversion_from_python_to_numpy_array_type(input, expected):
    assert get_numpy_attribute_type_from_iterable(input) == expected


@mark.parametrize(
    ("input", "expected"),
    [
        ((), AttributeType.UNSPECIFIED),
        ((17, -2), AttributeType.NUMERIC),
        ((17.5, -3.5), AttributeType.NUMERIC),
        ((inf, -3.5, nan), AttributeType.NUMERIC),
        ((False, True), AttributeType.BOOLEAN),
        ((False, 123, True), AttributeType.NUMERIC),
        ((123, False, True), AttributeType.NUMERIC),
        (("spam", "ham", "bacon"), AttributeType.STRING),
        (("spam", 123), AttributeType.OBJECT),
        ((123, "spam"), AttributeType.OBJECT),
        ((None,), AttributeType.OBJECT),
        (("spam", False), AttributeType.OBJECT),
        ((123, None), AttributeType.OBJECT),
    ],
)
def test_conversion_from_python_to_igraph_attribute_type(input, expected):
    assert get_igraph_attribute_type_from_iterable(input) == expected
