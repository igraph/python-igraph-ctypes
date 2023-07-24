from __future__ import annotations

from ctypes import byref
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    NoReturn,
    Optional,
    Tuple,
    TypedDict,
    TypeVar,
    Type,
    Union,
    cast,
)

from .types import igraph_integer_t


C = TypeVar("C", bound="Boxed")
T = TypeVar("T")


class BoxedConfig(TypedDict):
    """Specification of the configuration dictionary to be added inside the
    definition of a class that uses BoxedMeta as its metaclass.
    """

    ctype: Type
    constructor: Optional[Callable[..., None]]
    destructor: Optional[Callable[..., None]]
    getitem: Optional[Callable]
    len: Optional[Callable[..., Union[int, igraph_integer_t]]]


def _fake_constructor(*args, **kwds) -> NoReturn:
    """Fake constructor that throws an error unconditionally."""
    raise RuntimeError("No default constructor specified")


class BoxedMeta(Generic[T], type):
    """Metaclass for "boxed" classes whose aim is to provide a wrapper for a
    low-level igraph object, calling its constructor and destructor at the
    appropriate times.
    """

    def __new__(cls, name: str, bases: Tuple[Type], classdict: Dict[str, Any]):
        config = cls._get_boxed_config(classdict)
        if config:
            cls._add_constructors(name, bases, classdict, config)
            cls._add_sequence_impl(classdict, config)

        return type.__new__(cls, name, bases, classdict)

    @classmethod
    def _get_boxed_config(cls, classdict: Dict[str, Any]) -> Optional[BoxedConfig]:
        config = classdict.get("boxed_config")
        return cast(BoxedConfig, config) if isinstance(config, dict) else None

    @classmethod
    def _add_constructors(
        cls,
        name: str,
        bases: Tuple[Type],
        classdict: Dict[str, Any],
        config: BoxedConfig,
    ):
        if "__init__" in classdict:
            raise RuntimeError(
                "classes that use BoxedMeta as their metaclass must have no "
                "user-defined constructors and cannot be subclassed once "
                "configured"
            )

        cls_outer = config["ctype"]
        constructor = config.get("constructor") or _fake_constructor
        destructor = config["destructor"]

        def from_param(cls, obj: Any):
            if not isinstance(obj, cls):
                raise TypeError(f"expected {cls!r}, got {type(obj)!r}")
            return obj._as_parameter_

        def create(cls, *args, **kwds):
            instance = cls_outer()
            constructor(byref(instance), *args, **kwds)  # type: ignore
            return cls(instance)

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

            bases[0].__init__(self, instance, destructor, initialized)

        classdict["from_param"] = classmethod(from_param)
        classdict["create"] = classmethod(create)
        classdict["create_with"] = classmethod(create_with)
        classdict["__init__"] = __init__

    @classmethod
    def _add_sequence_impl(
        cls,
        classdict: Dict[str, Any],
        config: BoxedConfig,
    ):
        item_getter = classdict.get("getitem")
        length_getter = classdict.get("len")

        if length_getter:

            def __len__(self) -> int:
                return int(length_getter(byref(self.unwrap())))

            classdict["__len__"] = __len__

        if item_getter:

            def __getitem__(self, index: int):
                return item_getter(byref(self.unwrap()), index)

            classdict["__getitem__"] = __getitem__


class Boxed(Generic[T], metaclass=BoxedMeta):
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
    def from_param(cls, obj: Any):
        raise NotImplementedError

    @classmethod
    def wrap(cls, instance: T) -> Boxed[T]:
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
