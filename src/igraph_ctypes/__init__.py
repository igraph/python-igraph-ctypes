from .version import __version__

from .graph import Graph
from ._internal.setup import setup_igraph_library

__all__ = ("Graph", "__version__")

setup_igraph_library()
