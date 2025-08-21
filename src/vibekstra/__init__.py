from . import ai
from typing import List


def vibekstra(n: int, s: int, edges: List[List[int]]) -> List[int]:
    """
    Calculate the shortest distance from s to each point in the graph.
    Args:
    n: The number of vertices in the graph
    s: Source vertex (numbered from 1)
    Edges: a list containing [u, v, w], indicating that there is an edge with a weight of w from u to v
    Returns:
    A list containing the shortest distance from s to each point
    """
    return ai.vibekstra(n=n, source=s, edges=edges)