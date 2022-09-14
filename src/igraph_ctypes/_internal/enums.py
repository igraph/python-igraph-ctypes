from enum import IntEnum

__all__ = ("NeighborMode", "StarMode", "WheelMode")


class NeighborMode(IntEnum):
    """Python counterpart of an ``igraph_neimode_t`` enum."""

    OUT = 1
    IN = 2
    ALL = 3


class StarMode(IntEnum):
    """Python counterpart of an ``igraph_star_mode_t`` enum."""

    OUT = 0
    IN = 1
    UNDIRECTED = 2
    MUTUAL = 3


class WheelMode(IntEnum):
    """Python counterpart of an ``igraph_wheel_mode_t`` enum."""

    OUT = 0
    IN = 1
    UNDIRECTED = 2
    MUTUAL = 3
