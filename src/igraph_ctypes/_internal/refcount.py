"""Functions related to Python's reference counting."""

from ctypes import pythonapi, py_object
from sys import getrefcount
from typing import Any, TypeVar

__all__ = ("incref", "decref", "refcount")


_c_inc_ref = pythonapi.Py_IncRef
_c_inc_ref.argtypes = [py_object]
_c_dec_ref = pythonapi.Py_DecRef
_c_dec_ref.argtypes = [py_object]

T = TypeVar("T")


def incref(obj: T) -> T:
    """Increases the reference count of the given object and returns it intact."""
    _c_inc_ref(obj)
    return obj


def decref(obj: T) -> T:
    """Decreases the reference count of the given object and returns it intact."""
    _c_dec_ref(obj)
    return obj


def refcount(obj: Any) -> int:
    """Returns the reference count of the given object."""
    # subtract 3 for: function argument, reference in getrefcount, and the
    # function stack
    return getrefcount(obj) - 3
