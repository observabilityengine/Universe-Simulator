"""
Universe Simulator - Consistent Hashing
Ring-based placement with virtual nodes for load balance.
O(log N) lookup via sorted ring. Handles node add/remove with minimal remapping.
"""

from __future__ import annotations

import hashlib
from typing import Any, Dict, List, Optional


def _hash(key: Any) -> int:
    """Stable 64-bit hash from key string representation."""
    h = hashlib.sha256(str(key).encode("utf-8")).digest()
    return int.from_bytes(h[:8], "big")


class ConsistentHash:
    def __init__(self, nodes: List[Any] | None = None, vnodes: int = 100) -> None:
        if vnodes < 1:
            raise ValueError("vnodes must be >= 1")
        self.vnodes = vnodes
        self.ring: Dict[int, Any] = {}  # hash -> node
        self.sorted_keys: List[int] = []
        self.nodes: set[Any] = set()
        if nodes:
            for n in nodes:
                self.add(n)

    def add(self, node: Any) -> None:
        if node in self.nodes:
            return
        self.nodes.add(node)
        for i in range(self.vnodes):
            h = _hash(f"{node}#{i}")
            self.ring[h] = node
            self.sorted_keys.append(h)
        self.sorted_keys.sort()

    def remove(self, node: Any) -> None:
        if node not in self.nodes:
            return
        self.nodes.discard(node)
        to_del = [h for h, n in self.ring.items() if n == node]
        for h in to_del:
            del self.ring[h]
        self.sorted_keys = [h for h in self.sorted_keys if h in self.ring]

    def get(self, key: Any) -> Optional[Any]:
        """Return the node responsible for key, or None if ring empty."""
        if not self.sorted_keys:
            return None
        h = _hash(key)
        # Binary search for first key >= h
        lo, hi = 0, len(self.sorted_keys)
        while lo < hi:
            mid = (lo + hi) // 2
            if self.sorted_keys[mid] < h:
                lo = mid + 1
            else:
                hi = mid
        if lo == len(self.sorted_keys):
            lo = 0  # wrap around
        return self.ring[self.sorted_keys[lo]]

    def get_n(self, key: Any, n: int) -> List[Any]:
        """Return up to n distinct nodes for key (for replication)."""
        if not self.sorted_keys or n <= 0:
            return []
        h = _hash(key)
        lo, hi = 0, len(self.sorted_keys)
        while lo < hi:
            mid = (lo + hi) // 2
            if self.sorted_keys[mid] < h:
                lo = mid + 1
            else:
                hi = mid
        result = []
        seen = set()
        idx = lo % len(self.sorted_keys)
        for _ in range(len(self.sorted_keys)):
            node = self.ring[self.sorted_keys[idx]]
            if node not in seen:
                result.append(node)
                seen.add(node)
                if len(result) >= n:
                    break
            idx = (idx + 1) % len(self.sorted_keys)
        return result


if __name__ == "__main__":
    ch = ConsistentHash(["A", "B", "C"], vnodes=50)
    assert ch.get("user1") is not None
    assert ch.get("user1") in {"A", "B", "C"}

    # Same key always same node
    n1 = ch.get("key42")
    n2 = ch.get("key42")
    assert n1 == n2

    # Add node – most keys stay
    before = {k: ch.get(k) for k in range(200)}
    ch.add("D")
    moved = sum(1 for k in range(200) if before[k] != ch.get(k))
    assert moved < 80  # roughly 1/4 should move with 4 nodes

    # Remove
    ch.remove("B")
    assert "B" not in {ch.get(k) for k in range(50)}

    # Empty
    empty = ConsistentHash()
    assert empty.get("x") is None

    # get_n
    nodes = ch.get_n("shard", 2)
    assert len(nodes) == 2
    assert len(set(nodes)) == 2

    # Single node
    s = ConsistentHash(["solo"], vnodes=10)
    assert s.get("anything") == "solo"
    assert s.get_n("x", 3) == ["solo"]

    print("consistent_hash self-test passed")
