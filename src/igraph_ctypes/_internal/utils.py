import numpy as np

from ctypes import byref, cast, c_char_p, c_ubyte, POINTER, sizeof
from functools import wraps
from numpy.typing import DTypeLike
from typing import Any, Callable, Iterable, Union

from .errors import python_exception_to_igraph_error_t
from .types import (
    np_type_of_igraph_bool_t,
    np_type_of_igraph_real_t,
    np_type_of_igraph_string,
)

__all__ = ("bytes_to_str", "get_raw_memory_view", "nop", "protect", "protect_with")


def bytes_to_str(
    value: Union[bytes, c_char_p], encoding: str = "utf-8", errors: str = "replace"
) -> str:
    """Converts a C string represented as a Python bytes object or as a
    ctypes ``c_char_p`` object into a Python string, using the given encoding
    and error handling.
    """
    if isinstance(value, c_char_p):
        wrapped = value.value
        return wrapped.decode(encoding, errors) if wrapped is not None else ""
    else:
        return value.decode(encoding, errors)


def get_numpy_attribute_type_from_iterable(  # noqa: C901
    it: Iterable[Any],
) -> DTypeLike:
    """Determines the appropriate NumPy datatype to store all the items found in
    the given iterable as an attribute.

    This means that this function basically classifies the iterable into one of
    the following data types:

    - np_type_of_igraph_bool_t for Boolean attributes
    - np_type_of_igraph_real_t for numeric attributes
    - np_type_of_igraph_string for string attributes
    - np.object_ for any other (mixed) attribute type

    When the iterable is empty, a numeric attribute will be assumed.
    """
    it = iter(it)
    try:
        item = next(it)
    except StopIteration:
        # Iterable empty
        return np_type_of_igraph_real_t

    best_fit: DTypeLike
    if isinstance(item, bool):
        best_fit = np_type_of_igraph_bool_t
    elif isinstance(item, (int, float, np.number)):
        best_fit = np_type_of_igraph_real_t
    elif isinstance(item, str):
        best_fit = np_type_of_igraph_string
    else:
        return np.object_

    for item in it:
        if isinstance(item, bool):
            if best_fit == np_type_of_igraph_string:
                return np.object_
        elif isinstance(item, (int, float, np.number)):
            if best_fit == np_type_of_igraph_string:
                return np.object_
            else:
                best_fit = np_type_of_igraph_real_t
        elif isinstance(item, str):
            if best_fit != np_type_of_igraph_string:
                return np.object_
        else:
            return np.object_

    return best_fit


def get_raw_memory_view(obj):
    """Returns a view into the raw bytes of a ctypes object."""
    return cast(byref(obj), POINTER(c_ubyte * sizeof(obj))).contents


def nop(*args, **kwds) -> None:
    """Function placeholder that does nothing."""
    pass


def protect(func: Callable[..., None]) -> Callable[..., int]:
    """Decorator that takes a function that can potentially throw a Python
    exception, and turns it into another function that returns an igraph-compatible
    `igraph_error_t` error code instead.
    """

    @wraps(func)
    def wrapped(*args, **kwds) -> int:
        try:
            func(*args, **kwds)
        except Exception as ex:
            return python_exception_to_igraph_error_t(ex)
        else:
            return 0

    return wrapped


def protect_with(
    handler: Callable[[int], int]
) -> Callable[[Callable[..., None]], Callable[..., int]]:
    """Decorator factory that creates a decorator that takes a function that
    can potentially throw a Python exception, and turns it into another function
    that returns an igraph-compatible `igraph_error_t` error code instead,
    piping it through the given handler function.
    """

    def decorator(func: Callable[..., None]) -> Callable[..., int]:
        @wraps(func)
        def wrapped(*args, **kwds) -> int:
            try:
                func(*args, **kwds)
                return 0
            except Exception as ex:
                print(repr(ex))
                code = python_exception_to_igraph_error_t(ex)

            try:
                return handler(code)
            except Exception as ex:
                # TODO(ntamas): warn here!
                print(repr(ex))
                return code

        return wrapped

    return decorator
