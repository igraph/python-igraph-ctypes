from .types import igraph_error_t

__all__ = ("handle_igraph_error_t",)


def handle_igraph_error_t(code: igraph_error_t) -> None:
    """Handles the given igraph error code, raising exceptions appropriately."""
    if code:
        from .setup import _get_last_error_state

        error_state = _get_last_error_state()
        if error_state:
            error_state.raise_error()
        else:
            raise RuntimeError(f"igraph returned error code {code}")
