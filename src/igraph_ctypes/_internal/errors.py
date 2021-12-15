from .types import igraph_error_t


def handle_igraph_error_t(code: igraph_error_t) -> None:
    """Handles the given igraph error code, raising exceptions appropriately."""
    if code:
        raise RuntimeError(f"igraph returned error code {code}")
