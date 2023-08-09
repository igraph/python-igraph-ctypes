import numpy as np

from numpy.typing import DTypeLike
from typing import Any, Iterable

from .enums import AttributeType
from ..types import (
    np_type_of_igraph_bool_t,
    np_type_of_igraph_real_t,
)

__all__ = (
    "get_igraph_attribute_type_from_iterable",
    "get_numpy_attribute_type_from_iterable",
    "igraph_to_numpy_attribute_type",
)


def get_igraph_attribute_type_from_iterable(  # noqa: C901
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

    best_fit: AttributeType
    if isinstance(item, bool):
        best_fit = AttributeType.BOOLEAN
    elif isinstance(item, (int, float, np.number)):
        best_fit = AttributeType.NUMERIC
    elif isinstance(item, str):
        best_fit = AttributeType.STRING
    else:
        return AttributeType.OBJECT

    for item in it:
        if isinstance(item, bool):
            if best_fit == AttributeType.STRING:
                return AttributeType.OBJECT
        elif isinstance(item, (int, float, np.number)):
            if best_fit == AttributeType.STRING:
                return AttributeType.OBJECT
            else:
                best_fit = AttributeType.NUMERIC
        elif isinstance(item, str):
            if best_fit != AttributeType.STRING:
                return AttributeType.OBJECT
        else:
            return AttributeType.OBJECT

    return best_fit


def get_numpy_attribute_type_from_iterable(
    it: Iterable[Any],
) -> DTypeLike:
    """Determines the appropriate NumPy attribute type to store all the items
    found in the given iterable as an attribute.

    This is done by first determining the corresponding igraph attribute type,
    and mapping that type to a NumPy type.

    When the iterable is empty, a numeric attribute will be assumed.
    """
    attr_type = get_igraph_attribute_type_from_iterable(it)
    if attr_type is AttributeType.UNSPECIFIED:
        attr_type = AttributeType.NUMERIC
    return igraph_to_numpy_attribute_type(attr_type)


def igraph_to_numpy_attribute_type(type: AttributeType) -> DTypeLike:
    """Converts an igraph attribute type to an equivalent NumPy data type."""
    if type is AttributeType.BOOLEAN:
        return np_type_of_igraph_bool_t
    elif type is AttributeType.NUMERIC:
        return np_type_of_igraph_real_t
    else:
        return np.object_
