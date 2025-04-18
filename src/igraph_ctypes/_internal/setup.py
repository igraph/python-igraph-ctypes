import sys

from ctypes import pythonapi
from dataclasses import dataclass
from typing import Optional
from warnings import warn

from .attributes import AttributeHandler
from .errors import igraph_error_t_to_python_exception_class, IgraphWarning
from .functions import strerror
from .lib import (
    IGRAPH_FINALLY_FREE,
    igraph_set_attribute_table,
    igraph_set_error_handler,
    igraph_set_fatal_handler,
    igraph_set_interruption_handler,
    igraph_set_warning_handler,
)
from .rng import NumPyRNG
from .types import (
    igraph_error_handler_t,
    igraph_fatal_handler_t,
    igraph_interruption_handler_t,
    igraph_warning_handler_t,
)

__all__ = ("setup_igraph_library", "_get_last_error_state")


# Expose the PyErr_CheckSignals function from the Python C API
PyErr_CheckSignals = pythonapi.PyErr_CheckSignals
PyErr_CheckSignals.restype = int
PyErr_CheckSignals.argtypes = []


@dataclass
class IgraphErrorState:
    """Dataclass storing the details of the last error message received from
    igraph.
    """

    message: bytes = b""
    filename: bytes = b""
    line: int = 0
    error: int = 0

    def _error_handler(self, message: bytes, filename: bytes, line: int, error: int):
        self.message = message
        self.filename = filename
        self.line = line
        self.error = error

    def _reset(self):
        self.message = b""
        self.filename = b""
        self.line = 0
        self.error = 0

    @property
    def has_error(self) -> bool:
        """Returns whether the error state object currently stores an error."""
        return int(self.error) != 0

    def raise_error(self) -> None:
        """Raises an appropriate Python exception if there is an error stored
        in the state object. No-op otherwise.
        """
        code = self.error
        exc = igraph_error_t_to_python_exception_class(code)
        if exc is None:
            return

        msg = self.message
        if msg and msg[-1] not in b".!?":
            msg = msg + b"."

        filename_str = self.filename.decode("utf-8", errors="replace")
        message_str = msg.decode("utf-8", errors="replace")
        error_code_str = strerror(self.error)
        line = self.line

        self._reset()

        raise exc(
            f"Error at {filename_str}:{line}: {message_str} -- {error_code_str}"
            if message_str
            else f"Error at {filename_str}:{line} -- {error_code_str}"
        )


_attribute_handler = AttributeHandler()
_last_error = IgraphErrorState()


@igraph_error_handler_t
def _error_handler(message: bytes, filename: bytes, line: int, error: int):
    global _last_error
    IGRAPH_FINALLY_FREE()
    _last_error._error_handler(message, filename, line, error)


@igraph_fatal_handler_t
def _fatal_handler(message: bytes, filename: bytes, line: int):
    filename_str = filename.decode("utf-8", "replace")
    message_str = message.decode("utf-8", "replace")
    print(
        f"Fatal igraph error at {filename_str}:{line}: {message_str}", file=sys.stderr
    )


@igraph_warning_handler_t
def _warning_handler(message: bytes, filename: bytes, line: int):
    filename_str = filename.decode("utf-8", "replace")
    message_str = message.decode("utf-8", "replace")
    warn(
        f"Warning at {filename_str}:{line}: {message_str}", IgraphWarning, stacklevel=1
    )


def _get_last_error_state() -> Optional[IgraphErrorState]:
    global _last_error
    return _last_error if _last_error.has_error else None


def _setup_error_handlers() -> None:
    """Sets up the error handlers needed to integrate igraph's error handling
    nicely with Python.
    """
    igraph_set_error_handler(_error_handler)
    igraph_set_fatal_handler(_fatal_handler)
    igraph_set_warning_handler(_warning_handler)


@igraph_interruption_handler_t
def _interruption_handler() -> bool:
    try:
        # If there is a pending Ctrl-C waiting to be handled, PyErr_CheckSignals
        # will trigger a KeyboardInterrupt, which we catch and return True.
        # Otherwise we return False as we don't want to interrupt igraph if
        # PyErr_CheckSignals() returns True because of other signals (say,
        # SIGALRM)
        PyErr_CheckSignals()
        return False
    except KeyboardInterrupt:
        # Calling PyErr_CheckSignals might trigger a KeyboardInterrupt on its
        # own so we catch it here
        return True


def _setup_interruption_handler() -> None:
    igraph_set_interruption_handler(_interruption_handler)


def _setup_rng() -> None:
    """Initializes the random number generator of the igraph library."""
    from numpy.random import default_rng

    NumPyRNG(default_rng()).attach()


def _setup_attribute_table() -> None:
    """Initializes the attribute handler table that is responsible for telling
    the core C igraph library how to deal with attributes of graphs created
    from Python.
    """
    igraph_set_attribute_table(_attribute_handler)


def setup_igraph_library() -> None:
    """Integrates the facilities of the igraph library with Python.

    This function is called when the ``igraph_ctypes`` module is imported by the user.
    You should not need to call this function directly.
    """
    _setup_error_handlers()
    _setup_interruption_handler()
    _setup_rng()
    _setup_attribute_table()
