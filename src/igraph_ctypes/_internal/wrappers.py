from ctypes import byref
from typing import Any, Callable, Generic, NoReturn, Optional, Type, TypeVar

from .lib import igraph_destroy, igraph_vector_destroy, igraph_vector_init
from .types import igraph_t, igraph_vector_t

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
    def from_param(cls, obj: Any) -> T:
        if not isinstance(obj, cls):
            raise TypeError(f"expected igraph_t, got {type(obj)!r}")
        return obj._as_parameter_  # type: ignore

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

    def mark_initialized(self: C) -> C:
        self.__initialized = True
        return self

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

        def __init__(self, instance: Optional[T] = None):
            """Constructor."""
            if instance is None:
                instance = cls_outer()
                initialized = False
            elif not isinstance(instance, cls_outer):
                raise TypeError(f"{name} must wrap an object of type {cls_outer!r}")
            else:
                initialized = True
            super().__init__(instance, destructor, initialized)

    BoxedClass.__name__ = name
    return BoxedClass


_Graph = create_boxed("_Graph", igraph_t, destructor=igraph_destroy)
_Vector = create_boxed(
    "_Vector",
    igraph_vector_t,
    constructor=igraph_vector_init,
    destructor=igraph_vector_destroy,
)
