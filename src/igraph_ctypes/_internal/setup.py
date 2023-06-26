from .rng import NumPyRNG

__all__ = ("setup_igraph_library",)


def setup_igraph_library() -> None:
    """Initializes the random number generator of the igraph library.

    This function is called when the ``igraph_ctypes`` module is imported by the user.
    """
    from numpy.random import default_rng

    NumPyRNG(default_rng()).attach()
