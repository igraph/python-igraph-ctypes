import numpy as np

from numpy.typing import DTypeLike
from typing import Any, Iterable, Type

from .enums import AttributeType
from ..types import (
    np_type_of_igraph_bool_t,
    np_type_of_igraph_real_t,
)

__all__ = (
    "igraph_to_numpy_attribute_type",
    "iterable_to_igraph_attribute_type",
    "iterable_to_numpy_attribute_type",
    "python_type_to_igraph_attribute_type",
)


def igraph_to_numpy_attribute_type(type: AttributeType) -> DTypeLike:
    """Converts an igraph attribute type to an equivalent NumPy data type."""
    if type is AttributeType.BOOLEAN:
        return np_type_of_igraph_bool_t
    elif type is AttributeType.NUMERIC:
        return np_type_of_igraph_real_t
    else:
        return np.object_


def iterable_to_igraph_attribute_type(
    it: Iterable[Any],
) -> AttributeType:
    """Determines the appropriate igraph attribute type to store all the items
    found in the given iterable as an attribute.

    When the iterable is empty, the returned attribute type will be unspecified.
    """
    it = iter(it)
    try:
        item = next(it)
    except StopIteration:
        # Iterable empty
        return AttributeType.UNSPECIFIED

    best_fit = python_type_to_igraph_attribute_type(type(item))
    for item in it:
        next_type = python_type_to_igraph_attribute_type(type(item))
        if next_type is AttributeType.BOOLEAN:
            if best_fit == AttributeType.STRING:
                return AttributeType.OBJECT
        elif next_type is AttributeType.NUMERIC:
            if best_fit == AttributeType.STRING:
                return AttributeType.OBJECT
            else:
                best_fit = AttributeType.NUMERIC
        elif next_type is AttributeType.STRING:
            if best_fit != AttributeType.STRING:
                return AttributeType.OBJECT
        else:
            return AttributeType.OBJECT

    return best_fit


def iterable_to_numpy_attribute_type(it: Iterable[Any]) -> DTypeLike:
    """Determines the appropriate NumPy attribute type to store all the items
    found in the given iterable as an attribute.

    This is done by first determining the corresponding igraph attribute type,
    and mapping that type to a NumPy type.

    When the iterable is empty, a numeric attribute will be assumed.
    """
    attr_type = iterable_to_igraph_attribute_type(it)
    if attr_type is AttributeType.UNSPECIFIED:
        attr_type = AttributeType.NUMERIC
    return igraph_to_numpy_attribute_type(attr_type)


def python_object_to_igraph_attribute_type(obj: Any) -> AttributeType:
    """Converts the given Python object into the most fitting igraph attribute
    type.
    """
    if isinstance(obj, (bool, np.bool_)):
        return AttributeType.BOOLEAN
    if isinstance(obj, (int, float, np.number)):
        return AttributeType.NUMERIC
    if isinstance(obj, str):
        return AttributeType.STRING
    return AttributeType.OBJECT


def python_type_to_igraph_attribute_type(obj: Type[Any]) -> AttributeType:
    """Converts the given Python type into the most fitting igraph attribute
    type.
    """
    if issubclass(obj, (bool, np.bool_)):
        return AttributeType.BOOLEAN
    if issubclass(obj, (int, float, np.number)):
        return AttributeType.NUMERIC
    if issubclass(obj, str):
        return AttributeType.STRING
    return AttributeType.OBJECT
