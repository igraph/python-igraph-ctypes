try:
    from ._version import __version__
except ImportError:
    # during development when _version.py is not generated
    __version__ = "0.0.0"

from .graph import Graph
from ._internal.setup import setup_igraph_library

__all__ = ("Graph", "__version__")

setup_igraph_library()
