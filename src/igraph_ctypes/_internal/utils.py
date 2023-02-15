from ctypes import c_char_p


def bytes_to_str(value: bytes, encoding: str = "utf-8", errors: str = "replace") -> str:
    """Converts a C string represented as a Python bytes object or as a
    ctypes ``c_char_p`` object into a Python string, using the given encoding
    and error handling.
    """
    if isinstance(value, c_char_p):
        wrapped = value.value
        return wrapped.decode(encoding, errors) if wrapped is not None else ""
    else:
        return value.decode(encoding, errors)
