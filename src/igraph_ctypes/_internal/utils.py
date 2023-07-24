from ctypes import byref, cast, c_char_p, c_ubyte, POINTER, sizeof
from functools import wraps
from typing import Callable, Union

from .errors import python_exception_to_igraph_error_t

__all__ = ("bytes_to_str",)


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
