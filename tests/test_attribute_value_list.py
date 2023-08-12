from igraph_ctypes.enums import AttributeType
from igraph_ctypes._internal.attributes.value_list import (
    AttributeValueList,
    _slice_length,
)

from numpy import array, ndarray, bool_
from numpy.testing import assert_array_equal
from pytest import fixture, mark, raises


AVL = AttributeValueList


@fixture
def items() -> AVL:
    return AVL([1, 2, 3, 4, 5], fixed_length=True)


def test_slice_length():
    data = list(range(5))

    for start in list(range(-10, 10)) + [None]:
        for stop in list(range(-10, 10)) + [None]:
            for step in list(range(-3, 3)) + [None]:
                try:
                    sl = slice(start, stop, step)
                except Exception:
                    continue

                try:
                    expected_length = len(data[sl])
                except Exception:
                    expected_length = None

                if expected_length is None:
                    with raises(IndexError):
                        _slice_length(sl, len(data))
                else:
                    assert _slice_length(sl, len(data)) == expected_length


def test_equality():
    items = AVL([1, 2, 3])
    assert items == items
    assert items == AVL([1, 2, 3], fixed_length=True)
    assert items != [1, 2, 3, 4]
    assert items != [1, 2, 3]
    assert items != (1, 2, 3)


def test_length_query():
    items = AVL()
    assert len(items) == 0

    items = AVL([1, 2, 3])
    assert len(items) == 3

    items = AVL([1, 2, 3, 4, 5], fixed_length=True)
    assert len(items) == 5
    assert items.fixed_length


def test_copy(items: AVL):
    copied = items.copy()
    assert items.fixed_length
    assert copied.fixed_length
    assert list(items) == list(copied)
    assert items == copied
    assert items is not copied


def test_repr(items: AVL):
    assert (
        repr(items)
        == "AttributeValueList([1.0, 2.0, 3.0, 4.0, 5.0], type=1, fixed_length=True)"
    )
    assert repr(items[:]) == "AttributeValueList([1.0, 2.0, 3.0, 4.0, 5.0], type=1)"


def test_getitem_single_index(items: AVL):
    for i in range(len(items)):
        assert items[i] == i + 1

    assert list(items) == list(range(1, 6))


def test_getitem_slice(items: AVL):
    sliced = items[2:4]
    assert isinstance(sliced, AVL)
    assert not sliced.fixed_length
    assert_array_equal(sliced._items, [3, 4])
    assert sliced._items is not items._items


def test_getitem_ellipsis(items: AVL):
    copied = items[...]
    assert copied == items.copy()


def test_getitem_index_sequence(items: AVL):
    sublist = items[()]
    assert isinstance(sublist, AVL)
    assert not sublist
    assert not sublist.fixed_length
    assert list(sublist) == []

    sublist = items[0, 2, 4]
    assert isinstance(sublist, AVL)
    assert not sublist.fixed_length
    assert_array_equal(sublist._items, [1, 3, 5])
    assert sublist._items is not items._items

    indices = [0, 1, 3]
    sublist = items[indices]
    assert isinstance(sublist, AVL)
    assert not sublist.fixed_length
    assert_array_equal(sublist._items, [1, 2, 4])
    assert sublist._items is not items._items


def test_getitem_boolean_mask(items: AVL):
    mask = [False] * len(items)
    sublist = items[mask]
    assert isinstance(sublist, AVL)
    assert not sublist
    assert not sublist.fixed_length
    assert list(sublist) == []

    mask[0] = mask[1] = mask[3] = True
    sublist = items[mask]
    assert isinstance(sublist, AVL)
    assert list(sublist) == [1, 2, 4]
    assert sublist._items is not items._items

    with raises(IndexError, match="boolean index did not match indexed array"):
        mask.pop()
        sublist[mask]


def test_getitem_numpy_array(items: AVL):
    result = items[array((), dtype=int)]
    assert isinstance(result, ndarray)
    assert result.shape == (0,)

    result = items[array((1, 2, 3), dtype=int)]
    assert isinstance(result, ndarray)
    assert result.shape == (3,)
    assert result.tolist() == [2, 3, 4]

    result = items[array([(1, 2, 3), (2, 4, 1), (3, 3, 3), (0, 0, 2)], dtype=int)]
    assert isinstance(result, ndarray)
    assert result.shape == (4, 3)
    assert result.tolist() == [[2, 3, 4], [3, 5, 2], [4, 4, 4], [1, 1, 3]]


def test_getitem_numpy_boolean_mask(items: AVL):
    mask = array([False] * len(items))
    sublist = items[mask]
    assert isinstance(sublist, ndarray)
    assert sublist.shape == (0,)

    mask[0] = mask[1] = mask[3] = True
    sublist = items[mask]
    assert isinstance(sublist, ndarray)
    assert sublist.tolist() == [1, 2, 4]

    with raises(IndexError, match="boolean dimension"):
        mask = array([False] * (len(items) - 1))
        sublist[mask]


def test_getitem_invalid_index(items: AVL):
    with raises(IndexError, match="valid indices"):
        items[RuntimeError]  # type: ignore


def test_getitem_negative_indexing(items: AVL):
    items = items[:]
    items._extend_length_by(1)

    # Now the backing storage has 10 items, but the list has only 6 active items.
    # Indexing with negative indices should not allow us to get into the
    # inactive part
    assert len(items) == 6
    assert len(items._items) >= 6
    assert items[-1] == 0
    assert items[-2] == 5


def test_setitem_single_index(items: AVL):
    items[2] = 42
    assert list(items) == [1, 2, 42, 4, 5]

    items[-2] = 21
    assert list(items) == [1, 2, 42, 21, 5]

    with raises(IndexError):
        items[6] = 42


def test_setitem_slice(items: AVL):
    items[1:4] = [22, 33, 44]
    assert list(items) == [1, 22, 33, 44, 5]

    items[1:4] = 222
    assert list(items) == [1, 222, 222, 222, 5]

    with raises(ValueError, match="length"):
        items[1:4] = [17, 48, 12, 66]


def test_setitem_ellipsis(items: AVL):
    items[...] = [11, 22, 33, 44, 55]
    assert list(items) == [11, 22, 33, 44, 55]
    assert items.fixed_length

    with raises(ValueError, match="length"):
        items[...] = [11, 22, 33]


def test_setitem_index_sequence(items: AVL):
    items[()] = []
    assert list(items) == [1, 2, 3, 4, 5]
    assert items.fixed_length

    items[0, 2, 4] = 77
    assert list(items) == [77, 2, 77, 4, 77]
    assert items.fixed_length

    items[0, 2, 4] = array([[11], [33], [55]])
    assert list(items) == [11, 2, 33, 4, 55]
    assert items.fixed_length

    with raises(ValueError):
        items[()] = [1, 2]

    with raises(ValueError):
        items[1, 2, 3] = [1, 2]

    with raises(ValueError):
        items[(1,)] = []

    with raises(IndexError):
        items[(1.0,)] = [1]  # type: ignore

    with raises(ValueError):
        items[1, 2] = array([1, 2, 3])


def test_setitem_boolean_mask(items: AVL):
    mask = [False] * len(items)
    items[mask] = ()
    assert list(items) == [1, 2, 3, 4, 5]
    assert items.fixed_length

    mask[0] = mask[1] = mask[3] = True
    items[mask] = 77
    assert list(items) == [77, 77, 3, 77, 5]

    items[mask] = [11, 22, 44]
    assert list(items) == [11, 22, 3, 44, 5]

    items = items[:]
    items[mask] = iter([44, 11, 22])
    assert list(items) == [44, 11, 3, 22, 5]

    with raises(ValueError):
        items[mask] = (44, 1)


def test_setitem_numpy_array(items: AVL):
    empty = array((), dtype=int)
    items[empty] = 123
    assert 123 not in items
    assert items.fixed_length

    items[array((1, 2, 3), dtype=int)] = 22
    assert list(items) == [1, 22, 22, 22, 5]
    assert items.fixed_length

    items[array((1, 2, 3), dtype=int)] = [22, 33, 44]
    assert list(items) == [1, 22, 33, 44, 5]
    assert items.fixed_length

    indices = array([(1, 2, 3), (2, 4, 1), (3, 3, 3), (0, 0, 2)], dtype=int)
    values = array([(11, 12, 13), (21, 22, 23), (31, 32, 33), (41, 42, 43)])
    items[indices] = values
    assert list(items) == [42, 23, 43, 33, 22]
    assert items.fixed_length

    items[:] = 0

    indices = array([(1, 2, 3), (2, 4, 1), (3, 3, 3), (0, 0, 2)], dtype=int)
    values = iter(array([(11, 12, 13), (21, 22, 23), (31, 32, 33), (41, 42, 43)]).flat)
    items[indices] = values
    assert list(items) == [42, 23, 43, 33, 22]
    assert items.fixed_length

    with raises(ValueError, match="could not be broadcast"):
        items[array([(1, 2)], dtype=int)] = [22, 33, 44]


def test_setitem_numpy_boolean_mask(items: AVL):
    mask = array([False] * len(items), dtype=bool)
    items[mask] = ()
    assert list(items) == [1, 2, 3, 4, 5]
    assert items.fixed_length

    mask[0] = mask[1] = mask[3] = True
    items[mask] = 77
    assert list(items) == [77, 77, 3, 77, 5]

    items[mask] = [11, 22, 44]
    assert list(items) == [11, 22, 3, 44, 5]

    items = items[:]
    items[mask] = iter([44, 11, 22])
    assert list(items) == [44, 11, 3, 22, 5]


def test_setitem_invalid_index(items: AVL):
    with raises(IndexError, match="valid indices"):
        items[RuntimeError] = 123  # type: ignore
    with raises(IndexError, match="valid indices"):
        items[RuntimeError] = (123,)  # type: ignore


@mark.parametrize(
    ("to_delete", "expected"),
    [
        (2, [1, 2, 4, 5]),
        (..., []),
        (slice(2, 0), [1, 2, 3, 4, 5]),
        (slice(2, 4), [1, 2, 5]),
        (slice(None), []),
        ((), [1, 2, 3, 4, 5]),
        ((0, 2, 4), [2, 4]),
        ((False, False, False, False, False), [1, 2, 3, 4, 5]),
        ((False, False, True, False, True), [1, 2, 4]),
        (array((), dtype=int), [1, 2, 3, 4, 5]),
        (array((2, 4), dtype=int), [1, 2, 4]),
        (array((False, False, False, False, False), dtype=bool_), [1, 2, 3, 4, 5]),
        (array((False, False, True, False, True), dtype=bool_), [1, 2, 4]),
    ],
    ids=(
        "single_index",
        "ellipsis",
        "empty_slice",
        "slice",
        "whole_slice",
        "empty_tuple",
        "tuple",
        "empty_bool_mask",
        "bool_mask",
        "empty_numpy_index_array",
        "numpy_index_array",
        "empty_numpy_bool_mask",
        "numpy_bool_mask",
    ),
)
def test_delitem(items: AVL, to_delete, expected: list[int]):
    if expected != [1.0, 2.0, 3.0, 4.0, 5.0]:
        # List will change so we cannot delete from a fixed-length list
        with raises(RuntimeError, match="fixed-length"):
            del items[to_delete]  # type: ignore
    else:
        # List stays the same so we can delete
        del items[to_delete]  # type: ignore
        assert list(items) == [float(x) for x in expected]

    items = items[:]
    del items[to_delete]  # type: ignore
    assert list(items) == [float(x) for x in expected]
    assert not items.fixed_length


def test_delitem_invalid_index(items: AVL):
    with raises(IndexError, match="valid indices"):
        del items[RuntimeError]  # type: ignore


def test__extend_length_with(items: AVL):
    assert len(items) == 5 and items.fixed_length
    items._extend_length_by(3)
    assert len(items) == 8 and items.fixed_length
    items._extend_length_by(0)
    assert len(items) == 8 and items.fixed_length


def test_type_getter():
    items = AVL([1, 2, 3, 4, 5])
    assert items.type == AttributeType.NUMERIC

    items = AVL([False, False, True])
    assert items.type == AttributeType.BOOLEAN

    items = AVL(["foo", "bar", "baz"])
    assert items.type == AttributeType.STRING

    items = AVL(["foo", "bar", False, 42])
    assert items.type == AttributeType.OBJECT


def test_casting():
    items = AVL([0, 1, 2, 0, 4])
    items.cast(bool)

    assert items.type == AttributeType.BOOLEAN
    assert list(items) == [False, True, True, False, True]

    items.cast(str)

    assert items.type == AttributeType.STRING
    assert list(items) == ["False", "True", "True", "False", "True"]

    items.cast(object)

    assert items.type == AttributeType.OBJECT
    assert list(items) == ["False", "True", "True", "False", "True"]
