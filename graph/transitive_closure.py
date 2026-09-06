"""Transitive closure via Floyd-Warshall (boolean).

Complexity: O(n^3).
Input adjacency matrix (0/1); returns reachability matrix. Original implementation.
"""
from __future__ import annotations

from typing import List


def transitive_closure(adj: List[List[int]]) -> List[List[int]]:
    """Boolean Floyd-Warshall. adj[i][j] = 1 if edge i→j."""
    n = len(adj)
    reach = [row[:] for row in adj]
    for i in range(n):
        reach[i][i] = 1
    for k in range(n):
        for i in range(n):
            if reach[i][k]:
                for j in range(n):
                    if reach[k][j]:
                        reach[i][j] = 1
    return reach


if __name__ == "__main__":
    # 0→1→2
    adj = [[0, 1, 0], [0, 0, 1], [0, 0, 0]]
    tc = transitive_closure(adj)
    assert tc[0][2] == 1
    assert tc[0][0] == 1
    assert tc[2][0] == 0
    assert transitive_closure([[0]]) == [[1]]
    print("transitive_closure self-tests passed")
