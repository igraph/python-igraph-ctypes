from collections.abc import MutableMapping
from typing import Iterable, Iterator, TypeVar

from .enums import AttributeType
from .value_list import AttributeValueList

__all__ = ("AttributeMap",)


T = TypeVar("T")
C = TypeVar("C", bound="AttributeMap")


class AttributeMap(MutableMapping[str, AttributeValueList[T]]):
    """Helper object that provides a mutable mapping-like interface to access
    the vertex or edge attributes of a graph.

    Enforces that values assigned to keys in the map are of type
    AttributeValueList_ and that they have the right length.
    """

    _items: dict[str, AttributeValueList[T]]
    _common_length_of_values: int = 0

    @classmethod
    def wrap_empty_dict(cls, length: int = 0):
        return cls({}, length)

    def __init__(self, items: dict[str, AttributeValueList[T]], length: int) -> None:
        self._common_length_of_values = length
        self._items = items

        assert all(v.fixed_length and len(v) == length for v in items.values())

    def copy(self: C) -> C:
        """Returns a shallow copy of the attribute map.

        Note that unlike with regular dictionaries, this function makes a
        shallow copy of the _values_ as well.
        """
        return self.__class__(
            {k: v.copy() for k, v in self._items.items()},
            self._common_length_of_values,
        )

    def copy_empty(self: C, expected_length: int = -1) -> C:
        """Returns another, empty attribute map with the given expected length
        for any items being assigned in the future.

        Args:
            expected_length: the expected length for any items being assigned
                to the new copy in the future; negative if the expected length
                should be the same as for this instance
        """
        return self.__class__.wrap_empty_dict(
            expected_length if expected_length >= 0 else self._common_length_of_values
        )

    def remove(self, key: str) -> None:
        del self._items[key]

    def set(
        self,
        key: str,
        value: T | Iterable[T],
        type: AttributeType | None = None,
        _check_length: bool = True,
    ) -> None:
        """Assigns a value to _all_ the attribute values corresponding to the
        given attribute.

        This function is also available as the ``__setitem__`` magic method,
        making it possible to use the class as if it was a dictionary.

        Args:
            key: the name of the attribute to set
            value: the new value of the attribute. When it is an iterable
                that is not a string or a bytes object, it is assumed to
                contain the values for all items (vertices or edges)
                individually, and its length will be checked against the
                number of vertices or edges. WHen it is not an iterable, or
                it is a string or bytes object, it is assumed to be a common
                value for all vertices or edges.
        """
        length = self._common_length_of_values

        if isinstance(value, (bytes, str)):
            # strings and bytes are iterable but they are treated as if not
            avl = AttributeValueList(
                [value] * length, type=type, fixed_length=True
            )  # type: ignore
        elif isinstance(value, Iterable):
            # iterables are mapped to an AttributeValueList. Note that this
            # also takes care of copying existing AttributeValueList instances
            avl = AttributeValueList(value, type=type, fixed_length=True)  # type: ignore
            if _check_length and len(avl) != length:
                raise RuntimeError(
                    f"attribute value list length must be {length}, got {len(avl)}"
                )
        else:
            # all other values are assumed to be a common value for all
            # vertices or edges
            avl = AttributeValueList(
                [value] * length, type=type, fixed_length=True
            )  # type: ignore

        assert avl.fixed_length
        assert not _check_length or len(avl) == length

        self._items[key] = avl

    def _extend_common_length(self, n: int) -> None:
        self._common_length_of_values += n
        for value_list in self._items.values():
            value_list._extend_length_by(n)

    def __getitem__(self, key: str) -> AttributeValueList[T]:
        return self._items[key]

    def __iter__(self) -> Iterator[str]:
        return self._items.__iter__()

    def __len__(self) -> int:
        return len(self._items)

    __delitem__ = remove
    __setitem__ = set  # type: ignore
