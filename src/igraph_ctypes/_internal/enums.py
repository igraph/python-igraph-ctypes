from enum import IntEnum

__all__ = ("NeighborMode",)


class NeighborMode(IntEnum):
    """Python counterpart of an ``igraph_neimode_t`` enum."""

    OUT = 1
    IN = 2
    ALL = 3
