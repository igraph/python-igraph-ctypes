from typing import Optional, Type, Union

from .enums import ErrorCode
from .types import igraph_error_t

__all__ = ("handle_igraph_error_t",)


def handle_igraph_error_t(code: igraph_error_t) -> None:
    """Handles the given igraph error code, raising exceptions appropriately."""
    if code:
        from .lib import IGRAPH_FINALLY_FREE
        from .setup import _get_last_error_state

        IGRAPH_FINALLY_FREE()

        error_state = _get_last_error_state()
        if error_state:
            error_state.raise_error()
        elif code == ErrorCode.INTERRUPTED:
            raise KeyboardInterrupt
        else:
            raise RuntimeError(f"igraph returned error code {code}")


def igraph_error_t_to_python_exception_class(code: int) -> Optional[Type[Exception]]:
    """Converts an igraph error code into an appropriate Python exception class.

    See `python_exception_to_igraph_error_t()` for the reverse operation.
    """
    if code == 0:
        return None
    elif code == ErrorCode.UNIMPLEMENTED:
        return NotImplementedError
    elif code == ErrorCode.ENOMEM:
        return MemoryError
    else:
        return RuntimeError


def python_exception_to_igraph_error_t(
    exc: Optional[Union[Exception, Type[Exception]]]
) -> int:
    """Converts a Python exception class into an appropriate igraph error code.

    See `igraph_error_t_to_python_exception_class()` for the reverse operation.
    """
    # TODO(ntamas): more sophisticated conversion, preserving the
    # exception message if possible?

    if exc is None:
        return 0

    if isinstance(exc, Exception):
        exc = exc.__class__

    if issubclass(exc, NotImplementedError):
        return ErrorCode.UNIMPLEMENTED
    elif issubclass(exc, MemoryError):
        return ErrorCode.ENOMEM
    else:
        return ErrorCode.FAILURE
