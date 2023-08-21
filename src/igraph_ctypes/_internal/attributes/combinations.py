from ctypes import c_void_p
from numpy import mean, median
from typing import Any, Callable, Iterable

from igraph_ctypes._internal.enums import AttributeCombinationType, AttributeType
from igraph_ctypes._internal.types import IntArray

from .value_list import AttributeValueList


Handler = Callable[[AttributeValueList, list[IntArray], c_void_p], Iterable[Any] | None]


def apply_attribute_combinations(
    values: AttributeValueList,
    mapping: list[IntArray],
    comb_type: int,
    comb_func: c_void_p,
) -> Iterable[Any] | None:
    """Applies an igraph attribute combination specification entry to a
    vector of attributes.

    Args:
        values: an attribute value list from the old graph where the entries have
            to be combined into a new atribute value list
        mapping: list of integer arrays where the i-th entry lists the indices
            from the values array that are to be merged into the i-th entry of
            the returned value list
        comb_type: type of attribute combination to apply; one of the constants
            from the AttributeCombinationType_ enum
        comb_func: pointer to a Python function to invoke for custom, user-defined
            attribute combinations (i.e. when comb_type is equal to
            `AttributeCombinationType.FUNCTION`)

    Returns:
        an iterable of the combined values or `None` if the values should be ignored
        (i.e. when `comb_type` is `AttributeCombinationType.IGNORE`)
    """
    if comb_type == AttributeCombinationType.IGNORE:
        return None

    try:
        handler = _handlers[comb_type]
    except IndexError:
        handler = _combine_ignore

    return handler(values, mapping, comb_func)


def _combine_ignore(
    values: AttributeValueList,
    mapping: list[IntArray],
    comb_func: c_void_p,
) -> None:
    return None


def _combine_with_function(
    values: AttributeValueList,
    mapping: list[IntArray],
    comb_func: c_void_p,
) -> None:
    raise NotImplementedError  # TODO(ntamas)


def _combine_sum(
    values: AttributeValueList,
    mapping: list[IntArray],
    comb_func: c_void_p,
) -> Iterable[Any]:
    return (values[item].sum() for item in mapping)


def _combine_prod(
    values: AttributeValueList,
    mapping: list[IntArray],
    comb_func: c_void_p,
) -> Iterable[Any]:
    return (values[item].prod() for item in mapping)


def _combine_min(
    values: AttributeValueList,
    mapping: list[IntArray],
    comb_func: c_void_p,
) -> Iterable[Any]:
    return (values[item].min() for item in mapping)


def _combine_max(
    values: AttributeValueList,
    mapping: list[IntArray],
    comb_func: c_void_p,
) -> Iterable[Any]:
    return (values[item].min() for item in mapping)


def _combine_random(
    values: AttributeValueList,
    mapping: list[IntArray],
    comb_func: c_void_p,
) -> Iterable[Any]:
    raise NotImplementedError  # TODO(ntamas)


def _combine_first(
    values: AttributeValueList,
    mapping: list[IntArray],
    comb_func: c_void_p,
) -> Iterable[Any]:
    indices = [item[0] for item in mapping]
    return values[indices]


def _combine_last(
    values: AttributeValueList,
    mapping: list[IntArray],
    comb_func: c_void_p,
) -> Iterable[Any]:
    indices = [item[-1] for item in mapping]
    return values[indices]


def _combine_mean(
    values: AttributeValueList,
    mapping: list[IntArray],
    comb_func: c_void_p,
) -> Iterable[Any]:
    return (mean(values[item]) for item in mapping)


def _combine_median(
    values: AttributeValueList,
    mapping: list[IntArray],
    comb_func: c_void_p,
) -> Iterable[Any]:
    return (median(values[item]) for item in mapping)


def _combine_concat(
    values: AttributeValueList,
    mapping: list[IntArray],
    comb_func: c_void_p,
) -> Iterable[Any]:
    if values.type != AttributeType.STRING:
        raise TypeError(f"cannot concatenate attributes of type {values.type}")
    return ("".join(values[item]) for item in mapping)


_handlers: list[Handler] = [
    _combine_ignore,
    _combine_first,
    _combine_with_function,
    _combine_sum,
    _combine_prod,
    _combine_min,
    _combine_max,
    _combine_random,
    _combine_first,
    _combine_last,
    _combine_mean,
    _combine_median,
    _combine_concat,
]
"""Table of attribute combination handler functions."""
