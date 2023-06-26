from ctypes import byref
from typing import Any, Callable, Generic, NoReturn, Optional, Type, TypeVar

from .lib import (
    igraph_destroy,
    igraph_es_destroy,
    igraph_matrix_destroy,
    igraph_matrix_init,
    igraph_matrix_int_destroy,
    igraph_matrix_int_init,
    igraph_vector_destroy,
    igraph_vector_init,
    igraph_vector_bool_destroy,
    igraph_vector_bool_init,
    igraph_vector_int_destroy,
    igraph_vector_int_init,
    igraph_vector_int_list_destroy,
    igraph_vector_int_list_init,
    igraph_vector_list_destroy,
    igraph_vector_list_init,
    igraph_vs_destroy,
)
from .types import (
    igraph_t,
    igraph_es_t,
    igraph_matrix_t,
    igraph_matrix_int_t,
    igraph_vector_t,
    igraph_vector_bool_t,
    igraph_vector_int_t,
    igraph_vector_int_list_t,
    igraph_vector_list_t,
    igraph_vs_t,
)

__all__ = (
    "_EdgeSelector",
    "_Graph",
    "_Matrix",
    "_MatrixInt",
    "_Vector",
    "_VectorBool",
    "_VectorInt",
    "_VectorIntList",
    "_VectorList",
    "_VertexSelector",
)


C = TypeVar("C", bound="Boxed")
T = TypeVar("T")


class Boxed(Generic[T]):
    """Wrapper for a ctypes structure that may automatically call a destructor
    on the structure when it is garbage-collected.

    The destructor is called only when the boxed object is marked as
    _initialized_. Call `mark_initialized()` to mark the boxed object as
    initialized.
    """

    __c_instance: T
    __destructor: Optional[Callable[[T], None]] = None
    __initialized: bool = False

    @classmethod
    def create(cls, *args, **kwds):
        raise NotImplementedError

    @classmethod
    def create_with(cls, func, *args, **kwds):
        raise NotImplementedError

    @classmethod
    def from_param(cls, obj: Any) -> T:
        raise NotImplementedError

    @classmethod
    def wrap(cls, instance: T):
        return cls(instance)

    def __init__(
        self,
        instance: Optional[T] = None,
        destructor: Optional[Callable[[T], None]] = None,
        initialized: bool = True,
    ):
        """Constructor."""
        # Constructor arg is declared as Optional[T] because subclasses can be
        # invoked with no instance, but we need to prevent None from actually
        # being stored in the class instance
        if instance is None:
            raise ValueError("instance must not be None")

        self.__c_instance = instance
        self.__destructor = destructor
        self.__initialized = bool(initialized)

    def __del__(self):
        self._destroy()

    @property
    def _as_parameter_(self):
        return byref(self.__c_instance)  # type: ignore

    def _destroy(self) -> None:
        if self.__initialized:
            if self.__destructor:
                self.__destructor(byref(self.__c_instance))  # type: ignore
            self.__initialized = False

    def _set_wrapped_instance(self, value: T):
        assert not self.__initialized
        self.__c_instance = value

    def mark_initialized(self: C) -> C:
        self.__initialized = True
        return self

    def release(self) -> None:
        self.__initialized = False

    def unwrap(self) -> T:
        return self.__c_instance


def _fake_constructor(*args, **kwds) -> NoReturn:
    """Fake constructor that throws an error unconditionally."""
    raise RuntimeError("No default constructor specified")


def create_boxed(
    name: str,
    cls: Type[T],
    *,
    constructor: Optional[Callable[..., T]] = None,
    destructor: Optional[Callable[[T], None]] = None,
) -> Type[Boxed[T]]:
    cls_outer = cls

    if constructor is None:
        constructor = _fake_constructor

    class BoxedClass(Boxed):
        @classmethod
        def from_param(cls, obj: Any) -> T:
            if not isinstance(obj, cls):
                raise TypeError(f"expected {cls!r}, got {type(obj)!r}")
            return obj._as_parameter_  # type: ignore

        @classmethod
        def create(cls, *args, **kwds):
            instance = cls_outer()
            constructor(byref(instance), *args, **kwds)  # type: ignore
            return cls(instance)

        @classmethod
        def create_with(cls, func, *args, **kwds):
            instance = cls_outer()
            func(byref(instance), *args, **kwds)  # type: ignore
            return cls(instance)

        def __init__(self, instance: Optional[T] = None):
            """Constructor."""
            if instance is None:
                instance = cls_outer()
                initialized = False
            elif not isinstance(instance, cls_outer):
                raise TypeError(
                    f"{name} must wrap an object of type {cls_outer!r}, "
                    f"got {type(instance)!r}"
                )
            else:
                initialized = True
            super().__init__(instance, destructor, initialized)

    BoxedClass.__name__ = name
    return BoxedClass


# This trickery is needed to ensure that Pyright does to trip up on _Graph annotations
class _Graph(create_boxed("_Graph", igraph_t, destructor=igraph_destroy)):
    pass


_Matrix = create_boxed(
    "_Matrix",
    igraph_matrix_t,
    constructor=igraph_matrix_init,
    destructor=igraph_matrix_destroy,
)
_MatrixInt = create_boxed(
    "_MatrixInt",
    igraph_matrix_int_t,
    constructor=igraph_matrix_int_init,
    destructor=igraph_matrix_int_destroy,
)
_Vector = create_boxed(
    "_Vector",
    igraph_vector_t,
    constructor=igraph_vector_init,
    destructor=igraph_vector_destroy,
)
_VectorBool = create_boxed(
    "_VectorBool",
    igraph_vector_bool_t,
    constructor=igraph_vector_bool_init,
    destructor=igraph_vector_bool_destroy,
)
_VectorInt = create_boxed(
    "_VectorInt",
    igraph_vector_int_t,
    constructor=igraph_vector_int_init,
    destructor=igraph_vector_int_destroy,
)
_VectorIntList = create_boxed(
    "_VectorIntList",
    igraph_vector_int_list_t,
    constructor=igraph_vector_int_list_init,
    destructor=igraph_vector_int_list_destroy,
)
_VectorList = create_boxed(
    "_VectorList",
    igraph_vector_list_t,
    constructor=igraph_vector_list_init,
    destructor=igraph_vector_list_destroy,
)
_VertexSelector = create_boxed(
    "_VertexSelector",
    igraph_vs_t,
    destructor=igraph_vs_destroy,
)
_EdgeSelector = create_boxed(
    "_EdgeSelector",
    igraph_es_t,
    destructor=igraph_es_destroy,
)
