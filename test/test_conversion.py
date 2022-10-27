import pytest

from numpy import array

from igraph_ctypes._internal.conversion import (
    any_to_igraph_bool_t,
    edgelike_to_igraph_integer_t,
    igraph_vector_t_to_list,
    igraph_vector_t_to_numpy_array,
    igraph_vector_bool_t_to_list,
    igraph_vector_bool_t_to_numpy_array,
    igraph_vector_int_t_to_list,
    igraph_vector_int_t_to_numpy_array,
    iterable_to_igraph_vector_bool_t,
    iterable_to_igraph_vector_int_t,
    iterable_to_igraph_vector_t,
    vertexlike_to_igraph_integer_t,
)
from igraph_ctypes._internal.types import igraph_bool_t, igraph_integer_t
from igraph_ctypes._internal.wrappers import _VectorBool, _VectorInt, _Vector


@pytest.mark.parametrize("test_input", [None, True, False, 1, 0, 1.5, "", [], ()])
def test_any_to_igraph_bool_t(test_input):
    converted = any_to_igraph_bool_t(test_input)
    assert isinstance(converted, igraph_bool_t)
    assert converted.value is bool(test_input)


@pytest.mark.parametrize(
    "test_input,expected_output", [(1, 1), (-6, None), (8.5, None)]
)
def test_edgelike_to_igraph_integer_t(test_input, expected_output):
    if expected_output is None:
        with pytest.raises(ValueError):
            converted = edgelike_to_igraph_integer_t(test_input)
    else:
        converted = edgelike_to_igraph_integer_t(test_input)
        assert isinstance(converted, igraph_integer_t)
        assert converted.value == expected_output


@pytest.mark.parametrize(
    "test_input,expected_output", [(1, 1), (-6, None), (8.5, None)]
)
def test_vertexlike_to_igraph_integer_t(test_input, expected_output):
    if expected_output is None:
        with pytest.raises(ValueError):
            converted = vertexlike_to_igraph_integer_t(test_input)
    else:
        converted = vertexlike_to_igraph_integer_t(test_input)
        assert isinstance(converted, igraph_integer_t)
        assert converted.value == expected_output


def test_bool_vector_roundtrip():
    input = [False, 0, True, False, "", "yes", True]
    expected = [bool(x) for x in input]
    expected_array = array(expected, dtype=bool)

    converted = iterable_to_igraph_vector_bool_t(expected)
    assert isinstance(converted, _VectorBool)

    restored = igraph_vector_bool_t_to_list(converted)
    assert restored == expected

    restored_array = igraph_vector_bool_t_to_numpy_array(converted)
    assert (restored_array == expected_array).all()

    converted = iterable_to_igraph_vector_bool_t(restored_array)
    assert isinstance(converted, _VectorBool)

    restored_array = igraph_vector_bool_t_to_numpy_array(converted)
    assert (restored_array == expected_array).all()


def test_int_vector_roundtrip():
    input = [1, 4, 7, 11, 8, 3, 5, 6, 2, -6]
    expected = list(input)
    expected_array = array(expected)

    converted = iterable_to_igraph_vector_int_t(expected)
    assert isinstance(converted, _VectorInt)

    restored = igraph_vector_int_t_to_list(converted)
    assert restored == expected

    restored_array = igraph_vector_int_t_to_numpy_array(converted)
    assert (restored_array == expected_array).all()

    converted = iterable_to_igraph_vector_int_t(restored_array)
    assert isinstance(converted, _VectorInt)

    restored_array = igraph_vector_int_t_to_numpy_array(converted)
    assert (restored_array == expected_array).all()


def test_real_vector_roundtrip():
    input = [1.23, 4.567, 8.91011, -12.3456]
    expected = list(input)
    expected_array = array(expected)

    converted = iterable_to_igraph_vector_t(expected)
    assert isinstance(converted, _Vector)

    restored = igraph_vector_t_to_list(converted)
    assert restored == expected

    restored_array = igraph_vector_t_to_numpy_array(converted)
    assert (restored_array == expected_array).all()

    converted = iterable_to_igraph_vector_t(restored_array)
    assert isinstance(converted, _Vector)

    restored_array = igraph_vector_t_to_numpy_array(converted)
    assert (restored_array == expected_array).all()
