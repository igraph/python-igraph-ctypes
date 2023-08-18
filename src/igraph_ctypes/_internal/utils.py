from ctypes import byref, cast, c_char_p, c_ubyte, POINTER, sizeof
from functools import wraps
from traceback import print_exc
from typing import Callable, Union, TypeVar

from .errors import python_exception_to_igraph_error_t

__all__ = (
    "bytes_to_str",
    "get_raw_memory_view",
    "nop",
    "protect",
    "protect_with",
    "protect_with_default",
)


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
            print("Exception in callback invoked from igraph's C core:")
            print_exc()
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
                print("Exception in callback invoked from igraph's C core:")
                print_exc()
                code = python_exception_to_igraph_error_t(ex)

            try:
                return handler(code)
            except Exception:
                print(
                    "\nWhile handling the above exception, another exception occurred:"
                )
                print_exc()
                return code

        return wrapped

    return decorator


T = TypeVar("T")
R = TypeVar("R")


def protect_with_default(
    handler: Callable[[T], R], default: T | Callable[[Exception], T]
) -> Callable[[Callable[..., T]], Callable[..., R]]:
    """Decorator factory that creates a decorator that takes a function that
    can potentially throw a Python exception, and turns it into another function
    that logs these exceptions and passes the result through a converter
    function. This is useful in contexts where igraph's C core is not prepared
    for the case that a function call into a higher level interface can throw an
    exception.

    When the wrapped function throws an exception, the wrapper will assume that
    the wrapped function returned the specified default value instead.

    Args:
        handler: the handler function that converts the result from the Python
            callback into the result type expected by the C core. Typically a
            ctypes type.
        default: the default value to assume from the callback if the callback
            throws an exception. When it is a callable, it will be called with
            the raised exception and its return value will be used instead.
    """

    def decorator(func: Callable[..., T]) -> Callable[..., R]:
        @wraps(func)
        def wrapped(*args, **kwds) -> R:
            try:
                result = func(*args, **kwds)
            except Exception as ex:
                print("Exception in callback invoked from igraph's C core:")
                print_exc()
                result = default(ex) if callable(default) else default

            try:
                return handler(result)
            except Exception:
                print(
                    "\nWhile handling the above exception, another exception occurred:"
                )
                print_exc()
                print("")
                print("This is most likely a bug; please report it to the developers!")
                return result  # type: ignore

        return wrapped

    return decorator
