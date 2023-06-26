from dataclasses import dataclass

from .functions import igraph_strerror
from .lib import igraph_set_error_handler
from .rng import NumPyRNG
from .types import igraph_error_t, igraph_error_handler_t

__all__ = ("setup_igraph_library",)


@dataclass
class IgraphErrorState:
    """Dataclass storing the details of the last error message received from
    igraph.
    """

    message: bytes = b""
    filename: bytes = b""
    line: int = 0
    error: igraph_error_t = igraph_error_t(0)

    def _error_handler(
        self, message: bytes, filename: bytes, line: int, error: igraph_error_t
    ):
        self.message = message
        self.filename = filename
        self.line = line
        self.error = error
        print(repr(self))

    @property
    def has_error(self) -> bool:
        """Returns whether the error state object currently stores an error."""
        return int(self.error) != 0

    def raise_error(self) -> None:
        """Raises an appropriate Python exception if there is an error stored
        in the state object. No-op otherwise.
        """
        code = int(self.error)

        if code == 0:
            return
        elif code == 12:  # IGRAPH_UNIMPLEMENTED
            exc = NotImplementedError
        elif code == 2:  # IGRAPH_ENOMEM
            exc = MemoryError
        else:
            exc = RuntimeError

        msg = self.message
        if msg and msg[-1] not in b".!?":
            msg = msg + b"."

        filename_str = self.filename.decode("utf-8", errors="replace")
        message_str = msg.decode("utf-8", errors="replace")
        error_code_str = igraph_strerror(self.error).decode("utf-8", errors="replace")

        raise exc(
            f"Error at {filename_str}:{self.line}: {message_str} -- {error_code_str}"
        )


_last_error = IgraphErrorState()


@igraph_error_handler_t
def _error_handler(message: bytes, filename: bytes, line: int, error: igraph_error_t):
    global _last_error
    _last_error._error_handler(message, filename, line, error)


def _get_last_error_state() -> IgraphErrorState:
    global _last_error
    return _last_error


def _setup_error_handler() -> None:
    """Sets up the error handler needed to integrate igraph's error handling
    nicely with Python.
    """
    igraph_set_error_handler(_error_handler)


def _setup_rng() -> None:
    """Initializes the random number generator of the igraph library."""
    from numpy.random import default_rng

    NumPyRNG(default_rng()).attach()


def setup_igraph_library() -> None:
    """Integrates the facilities of the igraph library with Python.

    This function is called when the ``igraph_ctypes`` module is imported by the user.
    You should not need to call this function directly.
    """
    _setup_error_handler()
    _setup_rng()
