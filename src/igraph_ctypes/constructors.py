from .graph import Graph


def create_empty_graph(n: int, directed: bool = False) -> Graph:
    """Creates an empty graph with the given number of vertices.

    Parameters:
        n: the number of vertices
        directed: whether the graph is directed
    """
    return Graph(n, directed)
