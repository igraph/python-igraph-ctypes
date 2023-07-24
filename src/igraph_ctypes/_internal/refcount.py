"""Functions related to Python's reference counting."""

from pycapi import Py_IncRef, Py_DecRef  # type: ignore
from sys import getrefcount
from typing import Any, TypeVar

__all__ = ("incref", "decref", "refcount")


T = TypeVar("T")


def incref(obj: T) -> T:
    """Increases the reference count of the given object and returns it intact."""
    Py_IncRef(obj)
    return obj


def decref(obj: T) -> T:
    """Decreases the reference count of the given object and returns it intact."""
    Py_DecRef(obj)
    return obj


def refcount(obj: Any) -> int:
    """Returns the reference count of the given object."""
    # subtract 3 for: function argument, reference in getrefcount, and the
    # function stack
    return getrefcount(obj) - 3
