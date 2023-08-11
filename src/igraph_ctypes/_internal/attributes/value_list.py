import numpy as np

from math import ceil
from numpy.typing import NDArray
from types import EllipsisType
from typing import (
    Any,
    cast,
    Iterable,
    Iterator,
    NoReturn,
    Sequence,
    Sized,
    TypeVar,
    overload,
)

from .enums import AttributeType
from .utils import (
    get_igraph_attribute_type_from_iterable,
    igraph_to_numpy_attribute_type,
)

__all__ = ("AttributeValueList",)

C = TypeVar("C", bound="AttributeValueList")
T = TypeVar("T", covariant=True)


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


class AttributeValueList(Sequence[T | None]):
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

    Internally, this class uses a NumPy typed array with an appropriate type.
    The type of the array is decided at construction time if a type is provided;
    otherwise the class will attempt to determine the most appropriate type
    based on the initial items. If there are no items, a numeric list will be
    created.
    """

    _buffer: NDArray
    """NumPy array acting as a backing store for the ``_items`` array. The size
    of the ``_buffer`` doubles every time we need more space to store the items.
    This allows us to have better performance when appending items to the
    ``_items`` array because most of the time we can just change ``_items`` to
    be a view into a longer part of the ``_buffer`` without having to
    re-allocate the buffer.
    """

    _items: NDArray
    """NumPy array view of the internal storage area of the items in the list.
    This array is a view into ``_buffer``.
    """

    _type: AttributeType
    """The types of the attributes that can be stored in this list."""

    _fixed_length: bool
    """Whether the length of the list is fixed."""

    def __init__(
        self,
        items: Iterable[T] | None = None,
        *,
        type: AttributeType | None = None,
        fixed_length: bool = False,
        _wrap: bool = False,
    ):
        """Constructor."""
        if _wrap:
            # Special case, not for public use. items is a NumPy array and
            # we can wrap it as is. Must be called only when no one else has
            # a reference to this array.
            if type is None:
                raise RuntimeError("no type specified")
            if not isinstance(items, np.ndarray):
                raise RuntimeError("input is not a NumPy array")

            array = items
        else:
            # Normal, public constructor path
            if type is None:
                type = (
                    AttributeType.NUMERIC
                    if items is None
                    else get_igraph_attribute_type_from_iterable(items)
                )

            dtype = igraph_to_numpy_attribute_type(type)
            array = np.fromiter(items if items is not None else (), dtype=dtype)

        # Now we have a NumPy array, but what we actually want is a chunk of
        # memory that we manage ourselves, and a NumPy view on top of it
        self._buffer = array
        self._items = self._buffer[:]
        self._type = type
        self._fixed_length = bool(fixed_length)

    def compact(self) -> None:
        """Compacts the list in-place, reclaiming any memory that was used
        earlier for storage when the list was longer.
        """
        num_items = len(self._items)
        if len(self._buffer) > num_items:
            # refcheck=False is potentially dangerous but I think we are okay
            # with it here
            self._buffer.resize((num_items,), refcheck=False)

    def copy(self: C) -> C:
        """Returns a shallow copy of the list."""
        return self.__class__(
            self._items, type=self._type, fixed_length=self._fixed_length
        )

    @property
    def fixed_length(self) -> bool:
        """Returns whether the list is fixed-length."""
        return self._fixed_length

    @property
    def type(self) -> AttributeType:
        """Returns the igraph attribute type of this list."""
        return self._type

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
            return np.array_equal(self._items, other._items)
        return False

    def __delitem__(self, index: IndexLike) -> None:  # noqa: C901
        if index is ...:
            if not self.fixed_length:
                self._items = self._buffer[:0]
                return

        elif isinstance(index, (int, np.integer)):
            if not self.fixed_length:
                self._items[index:-1] = self._items[(index + 1) :]
                self._items = self._buffer[: len(self._items) - 1]
                return

        elif isinstance(index, slice):
            slice_len = _slice_length(index, len(self))
            if slice_len <= 0:
                # Nothing to delete, this is allowed
                return

            if not self.fixed_length:
                # There are probably quite a few more special cases that we could
                # treat here more efficiently
                if (
                    index.start is None
                    and index.stop is None
                    and index.step in (None, 1, -1)
                ):
                    del self[...]
                else:
                    tmp = np.delete(self._items, index)
                    self._buffer = tmp
                    self._items = self._buffer[:]
                return

        elif hasattr(index, "__getitem__"):
            if isinstance(index, Sized) and len(index) == 0:
                # Nothing to delete, this is allowed
                return

            tmp = np.delete(self._items, index)  # type: ignore
            if not self.fixed_length:
                self._buffer = tmp
                self._items = self._buffer[:]
                return
            else:
                # Try to delete anyway, check if the length remains the same
                if len(tmp) == len(self._items):
                    # This is okay
                    return

        else:
            self._raise_invalid_index_error()

        raise RuntimeError("cannot delete items from a fixed-length list")

    @overload
    def __getitem__(self, index: IntLike) -> T | None:
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
            return self.__class__(items[index].copy(), type=self._type, _wrap=True)

        elif index is ...:
            return self.copy()

        elif isinstance(index, Sequence):
            return self.__class__(
                self._items[index,], type=self._type, _wrap=True  # type: ignore
            )

        elif isinstance(index, np.ndarray):
            return self._items[index]

        self._raise_invalid_index_error()

    def __iter__(self) -> Iterable[T]:
        return iter(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:
        fl = ", fixed_length=True" if self._fixed_length else ""
        return (
            f"{self.__class__.__name__}({self._items.tolist()!r}, "
            f"type={int(self._type)}{fl})"
        )

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
                self._items[index] = value  # type: ignore
            elif isinstance(index, (slice, Sequence, np.ndarray)):
                self._items[index,] = value  # type: ignore
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

        elif isinstance(index, (Sequence, np.ndarray)):
            if isinstance(index, np.ndarray):
                index = index.ravel()
            if isinstance(value, np.ndarray):
                value = value.ravel()
            if isinstance(value, Iterator):
                value = list(value)
            self._items[index,] = value

        else:
            self._raise_invalid_index_error()

    def _extend_length_by(self, n: int) -> None:
        """Extends the list with a given number of new items at the end, even
        if the list is marked as fixed-length.

        Do not use this method unless you know what you are doing.
        """
        current_length = len(self)
        target_length = current_length + n
        if len(self._buffer) < target_length:
            # We do not have enough space pre-allocated, find the nearest
            # power of two that will suffice
            new_length = 2 ** int(np.ceil(np.log2(target_length)))
            if self._type is AttributeType.BOOLEAN:
                default_value = False
            elif self._type is AttributeType.NUMERIC:
                default_value = 0.0
            elif self._type is AttributeType.STRING:
                default_value = ""
            else:
                default_value = None

            self._buffer.resize((new_length,), refcheck=False)
            self._buffer[current_length:new_length] = default_value

        self._items = self._buffer[:target_length]

    def _raise_invalid_index_error(self) -> NoReturn:
        # Wording of error message similar to NumPy
        raise IndexError(
            "only integers, slices (`:`), ellipsis (`...`) and integer or "
            "boolean arrays are valid indices"
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
