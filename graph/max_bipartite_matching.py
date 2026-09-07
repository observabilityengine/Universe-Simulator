"""Maximum bipartite matching via DFS augmenting paths (Kuhn).

Complexity: O(V E). Original implementation.
"""
from __future__ import annotations
from typing import List, Tuple

def max_bipartite_matching(
    n_left: int, n_right: int, edges: List[Tuple[int, int]],
) -> int:
    adj = [[] for _ in range(n_left)]
    for u, v in edges:
        adj[u].append(v)
    pair_u = [-1] * n_left
    pair_v = [-1] * n_right

    def dfs(u, seen):
        for v in adj[u]:
            if seen[v]: continue
            seen[v] = True
            if pair_v[v] < 0 or dfs(pair_v[v], seen):
                pair_u[u] = v
                pair_v[v] = u
                return True
        return False

    matching = 0
    for u in range(n_left):
        seen = [False] * n_right
        if dfs(u, seen):
            matching += 1
    return matching

if __name__ == "__main__":
    edges = [(0,0),(0,1),(1,0),(1,1)]
    assert max_bipartite_matching(2, 2, edges) == 2
    assert max_bipartite_matching(3, 2, [(0,0),(1,0),(2,1)]) == 2
    print("max_bipartite_matching self-tests passed")
