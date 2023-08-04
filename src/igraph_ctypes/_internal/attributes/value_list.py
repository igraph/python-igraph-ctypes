import numpy as np

from itertools import repeat
from math import ceil, floor
from numpy.typing import NDArray
from types import EllipsisType
from typing import Any, cast, Iterable, NoReturn, Sequence, Sized, TypeVar, overload

__all__ = ("AttributeValueList",)

C = TypeVar("C", bound="AttributeValueList")
T = TypeVar("T")


BoolLike = bool | np.bool_
IntLike = int | np.integer
IndexLike = (
    IntLike
    | slice
    | EllipsisType
    | Sequence[BoolLike | IntLike]
    | NDArray[np.bool_]
    | NDArray[np.integer]
)


class AttributeValueList(Sequence[T]):
    """List-like data structure that stores the values of a vertex or an edge
    attribute for every vertex and edge in the graph, while supporting
    NumPy-style fancy indexing operations.

    The following data types are supported for indexing:

    - single numeric indices
    - slices
    - ellipsis (meaning the entire list)
    - Boolean masks
    - sequences of numeric indices
    - NumPy arrays of numeric indices

    When _retrieving_ data from the list, all the index types above return
    _another_ AttributeValueList_ instance and _not_ a view into this instance.
    The only exception is NumPy arrays where we return a NumPy array of the
    same shape.

    _Setting_ items directly is possible via any of the above indexing methods.
    Slices, Boolean masks and sequences of numeric indices require a value
    that is also a sequence of the same size. When using NumPy arrays of
    numeric indices, the value must be a NumPy array of the same shape as well.
    For convenience, you can also use a single number, string, Boolean value
    or ``None`` as the right hand side of the assignment; when using these
    atomic values with an index that refers to multiple items in the list, the
    same atomic value is assigned to all items in the list.

    Instances of this class may be fixed or variable length. Indexing into
    an instance with fixed length will return a copy that is variable length.
    Typically, the only case when you encounter a fixed length list is when
    retrieving the vertex or edge attributes of a graph because in this case
    the length of the list is dictated by the number of vertices or edges in
    the graph.
    """

    _items: list[T]
    """The items in the list."""

    _fixed_length: bool
    """Whether the length of the list is fixed."""

    def __init__(self, items: Iterable[T] | None = None, *, fixed_length: bool = False):
        """Constructor."""
        self._items = list(items) if items is not None else []
        self._fixed_length = bool(fixed_length)

    def copy(self: C) -> C:
        """Returns a shallow copy of the list."""
        return self.__class__(self._items, fixed_length=self._fixed_length)

    @property
    def fixed_length(self) -> bool:
        """Returns whether the list is fixed-length."""
        return self._fixed_length

    def __eq__(self, other: Any) -> bool:
        """Returns whether the list is equal to some other sequence of items.

        This list is equal to another attribute value list of items if their
        length is the same and all items are the same, in the same order. It
        does not matter whether the lists are fixed-length or not.

        Attribute value lists are not equal to other sequences (lists or tuples).
        """
        if other is self:
            return True
        if isinstance(other, AttributeValueList):
            return self._items == other._items
        return False

    def __delitem__(self, index: IntLike) -> None:  # noqa: C901
        if index is ...:
            if not self.fixed_length:
                self._items.clear()
                return

        elif isinstance(index, (int, np.integer, slice)):
            if not self.fixed_length:
                del self._items[index]
                return

        elif hasattr(index, "__getitem__"):
            if isinstance(index, np.ndarray):
                if len(index) > 0 and isinstance(index[0], (np.bool_, bool)):
                    to_delete = sorted(np.flatnonzero(index))  # type: ignore
                else:
                    to_delete = sorted(index.flat)  # type: ignore
            else:
                if len(index) > 0 and isinstance(index[0], (np.bool_, bool)):
                    to_delete = [i for i, j in enumerate(index) if j]
                else:
                    to_delete = sorted(set(index))  # type: ignore

            if not self.fixed_length or not to_delete:
                to_delete.reverse()
                for i in to_delete:
                    del self._items[i]  # type: ignore
                return

        else:
            self._raise_invalid_index_error()

        raise RuntimeError("cannot delete items from a fixed-length list")

    @overload
    def __getitem__(self, index: IntLike) -> T:
        ...

    @overload
    def __getitem__(
        self: C, index: slice | EllipsisType | Sequence[BoolLike | IntLike]
    ) -> C:
        ...

    @overload
    def __getitem__(self, index: NDArray[np.bool_] | NDArray[np.integer]) -> NDArray:
        ...

    def __getitem__(self, index: IndexLike):
        items = self._items

        if isinstance(index, (int, np.integer)):
            return items[index]

        elif isinstance(index, slice):
            return self.__class__(items[index])

        elif index is ...:
            return self.copy()

        elif isinstance(index, Sequence):
            if self._check_boolean_mask(index):
                return self.__class__(
                    item for item, mask in zip(items, index, strict=True) if mask
                )
            else:
                return self.__class__(items[i] for i in cast(Sequence[IntLike], index))

        elif isinstance(index, np.ndarray):
            return np.asarray(self._items)[index]

        self._raise_invalid_index_error()

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:
        fl = ", fixed_length=True" if self._fixed_length else ""
        return f"{self.__class__.__name__}({self._items!r}{fl})"

    def __setitem__(  # noqa: C901
        self, index: IndexLike, value: T | Sequence[T] | NDArray
    ) -> None:
        items = self._items
        if index is ...:
            index = slice(None)

        if isinstance(index, (int, np.integer)):
            items[index] = value  # type: ignore
            return

        # All the remaining options assume that the value is either an atomic
        # value or a sequence / iterable of values. We need to distinguish
        # between them
        is_seq = isinstance(value, Sequence) or isinstance(value, np.ndarray)
        is_iterable = isinstance(value, Iterable) if not is_seq else True
        if is_iterable and not is_seq and self._fixed_length:
            # For fixed-length lists, we need to expand the iterable into
            # a sequence so we can check its length
            value = list(value)  # type: ignore
            is_seq = True

        if not is_iterable:
            # Atomic value
            value = cast(T, value)

            if isinstance(index, slice):
                num_indices = _slice_length(index, len(self))
                self._items[index] = repeat(value, num_indices)  # type: ignore

            elif isinstance(index, Sequence):
                if self._check_boolean_mask(index):
                    gen = (i for i, item in enumerate(index) if item)
                else:
                    gen = index
                for i in gen:
                    self._items[i] = value  # type: ignore

            elif isinstance(index, np.ndarray):
                if index.dtype in (bool, np.bool_):
                    index = np.flatnonzero(index)
                for i in index.flat:
                    self._items[i] = value  # type: ignore
            else:
                self._raise_invalid_index_error()

            return

        # Value is iterable and possibly a sequence
        if isinstance(index, slice):
            if self._fixed_length:
                num_indices = _slice_length(index, len(self))
                if len(value) != num_indices:  # type: ignore
                    raise ValueError(
                        "assignment would change length of a fixed-length list"
                    )
            self._items[index] = value  # type: ignore

        elif isinstance(index, Sequence):
            if isinstance(value, np.ndarray):
                value = value.ravel()
            else:
                if not isinstance(value, Sequence):
                    value = list(value)  # type: ignore

            assert isinstance(value, Sized)
            num_values = len(value)

            if self._check_boolean_mask(index):
                mask_size = index.count(True)  # also works for np.bool_
                if not is_seq:
                    value = list(value)  # type: ignore

                if num_values != mask_size:
                    raise ValueError(
                        # similar to NumPy
                        f"indexing assignment cannot assign {num_values} input "
                        f"value(s) to the {mask_size} output value(s) where the "
                        f"mask is true"
                    )

                gen = (i for i, item in enumerate(index) if item)
            else:
                gen = index

            for i, v in zip(gen, value, strict=True):  # type: ignore
                self._items[i] = v  # type: ignore

        elif isinstance(index, np.ndarray):
            if isinstance(value, np.ndarray):
                value = value.ravel()
            else:
                if not isinstance(value, Sequence):
                    value = list(value)  # type: ignore

            assert isinstance(value, Sized)
            num_values = len(value)

            if index.dtype in (bool, np.bool_):
                # Boolean mask
                index = np.flatnonzero(index)

            if num_values != index.size:
                raise ValueError(
                    # similar to NumPy
                    f"indexing assignment cannot assign {num_values} input "
                    f"value(s) to {index.size} slot(s)"
                )

            for i, j in enumerate(index.flat):
                self._items[j] = value[i]  # type: ignore

        else:
            self._raise_invalid_index_error()

    def _check_boolean_mask(self, index: Sequence[Any]) -> bool:
        """Checks whether the given sequence is a Boolean mask by evaluating
        its first item and assuming that all the items are of the same type.
        """
        if len(index) == 0:
            return False

        first = index[0]
        if isinstance(first, (bool, np.bool_)):
            if len(index) != len(self):
                self._raise_mask_mismatch_error(index)
            return True
        elif isinstance(first, (int, np.integer)):
            return False
        else:
            self._raise_invalid_index_error()

    def _extend_length(self, n: int) -> None:
        """Extends the list with a given number of new items at the end, even
        if the list is marked as fixed-length.

        Do not use this method unless you know what you are doing.
        """
        self._items.extend([None] * n)  # type: ignore

    def _raise_invalid_index_error(self) -> NoReturn:
        # Wording of error message similar to NumPy
        raise IndexError(
            "only integers, slices (`:`), ellipsis (`...`) and integer or "
            "boolean arrays are valid indices"
        )

    def _raise_mask_mismatch_error(self, index: Sized) -> NoReturn:
        # Wording of error message similar to NumPy
        raise IndexError(
            f"boolean index did not match indexed list; list "
            f"length is {len(self)} but boolean index length "
            f"is {len(index)}"
        )


def _slice_length(s: slice, length: int) -> int:
    """Helper function to determine the number of items in a slice, given the
    slice itself and the length of the container it is applied on.
    """
    start, stop, step = s.start, s.stop, s.step

    if step is None:
        step = 1

    if start is None:
        start = length - 1 if step < 0 else 0
    elif start < 0:
        start += length

    if stop is None:
        stop = -1 if step < 0 else length
    elif stop < 0:
        stop += length

    if step == 0:
        raise IndexError("slice step cannot be zero")

    if step > 0:
        start = max(0, start)
        stop = min(stop, length)
        return int(ceil((stop - start) / step)) if stop > start else 0
    else:
        start = min(start, length - 1)
        stop = max(stop, -1)
        return int(ceil((stop - start) / step)) if stop < start else 0
