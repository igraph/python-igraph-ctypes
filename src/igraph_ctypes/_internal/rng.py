from ctypes import pointer
from functools import partial
from numpy.random import Generator, PCG64
from typing import Callable, Optional

from .lib import igraph_rng_set_default
from .types import igraph_rng_type_t, np_type_of_igraph_uint_t
from .wrappers import _RNG

__all__ = ("NumPyRNG",)


class NumPyRNG:
    """Implementation of an igraph RNG that wraps a NumPy RNG."""

    _generator: Generator
    """The wrapped NumPy random number generator."""

    _rng: _RNG
    _rng_type: igraph_rng_type_t

    def __init__(self, generator: Generator):
        # TODO(ntamas): currently we assume that Generator.bit_generator is
        # PCG64
        assert isinstance(generator.bit_generator, PCG64)

        self._generator = generator
        self._rng_type = igraph_rng_type_t(
            name=b"NumPy RNG",
            bits=64,
            init=igraph_rng_type_t.TYPES["init"](self._rng_init),
            destroy=igraph_rng_type_t.TYPES["destroy"](self._rng_destroy),
            seed=igraph_rng_type_t.TYPES["seed"](self._rng_seed),
            get=igraph_rng_type_t.TYPES["get"](self._rng_get),
        )
        self._rng = _RNG.create(pointer(self._rng_type))
        self._rng.unwrap().is_seeded = True

    def _rng_init(self, _state):
        _state[0] = None
        return 0  # IGRAPH_SUCCESS

    def _rng_destroy(self, rng):
        pass

    def _rng_seed(self, _state, value):
        # Ignore, we assume that NumPy RNGs are seeded externally
        return 0

    def _rng_get(self, _state):
        """
        return self._generator.bit_generator.ctypes.next_uint64(
            self._generator.bit_generator.ctypes.state
        )
        """
        return self._generator.integers(
            0, 0xFFFFFFFFFFFFFFFF, dtype=np_type_of_igraph_uint_t, endpoint=True
        )

    def attach(self) -> Callable[[], None]:
        """Attaches this RNG instance as igraph's default RNG.

        Returns:
            a callable that can be called with no arguments to restore the
            RNG that was in effect before this RNG was attached.
        """
        global _igraph_default_rng

        old = igraph_rng_set_default(self._rng)
        _igraph_default_rng = self

        return partial(igraph_rng_set_default, old)


_igraph_default_rng: Optional[NumPyRNG] = None
"""We need to keep a reference to NumPyRNG to keep the underlying low-level
C objects alive, so we use an internal object in this module for that.
"""
