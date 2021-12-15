from ctypes import cdll


def _load_igraph_c_library():
    """Imports the low-level igraph C library using `ctypes`."""
    # lib = cdll.LoadLibrary("libigraph.so.0")
    lib = cdll.LoadLibrary("/Users/tamas/dev/igraph/igraph/build/src/libigraph.0.dylib")
    return lib


igraph_c_library = _load_igraph_c_library()
