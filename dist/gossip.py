"""
Universe Simulator - Gossip Protocol
Anti-entropy epidemic dissemination of key-value state.
Push-pull variant with bounded fanout. O(log N) rounds to full propagation
with high probability under uniform random peer selection.
Assumes reliable in-order delivery within a round; no network partitions modeled.
"""

from __future__ import annotations

import random
from typing import Any, Dict, List, Optional, Set, Tuple


class GossipNode:
    def __init__(self, node_id: int, peers: List[int], fanout: int = 3) -> None:
        self.id = node_id
        self.peers = list(peers)
        self.fanout = max(1, fanout)
        self.state: Dict[str, Tuple[Any, int]] = {}  # key -> (value, version)
        self.version = 0
        self.inbox: List[Dict[str, Tuple[Any, int]]] = []
        self.outbox: List[Tuple[int, Dict[str, Tuple[Any, int]]]] = []

    def put(self, key: str, value: Any) -> None:
        """Local update; increments version."""
        self.version += 1
        self.state[key] = (value, self.version)

    def get(self, key: str) -> Optional[Any]:
        entry = self.state.get(key)
        return entry[0] if entry else None

    def _select_peers(self) -> List[int]:
        if not self.peers:
            return []
        k = min(self.fanout, len(self.peers))
        return random.sample(self.peers, k)

    def gossip_round(self) -> None:
        """Push current state to fanout random peers; also pull by exchanging."""
        targets = self._select_peers()
        payload = dict(self.state)
        for t in targets:
            self.outbox.append((t, payload))

    def receive(self, remote_state: Dict[str, Tuple[Any, int]]) -> None:
        """Merge remote state by taking higher version per key."""
        for key, (val, ver) in remote_state.items():
            local = self.state.get(key)
            if local is None or ver > local[1]:
                self.state[key] = (val, ver)

    def deliver_inbox(self) -> None:
        while self.inbox:
            remote = self.inbox.pop(0)
            self.receive(remote)


class GossipCluster:
    """In-memory cluster driving synchronous gossip rounds."""

    def __init__(self, n: int, fanout: int = 3) -> None:
        if n < 1:
            raise ValueError("n must be >= 1")
        self.n = n
        self.nodes = [
            GossipNode(i, [j for j in range(n) if j != i], fanout=fanout)
            for i in range(n)
        ]

    def put(self, node_id: int, key: str, value: Any) -> None:
        self.nodes[node_id].put(key, value)

    def get(self, node_id: int, key: str) -> Optional[Any]:
        return self.nodes[node_id].get(key)

    def round(self) -> None:
        """One full gossip round: all nodes push, then deliver."""
        # Collect outbox
        msgs: List[Tuple[int, int, Dict[str, Tuple[Any, int]]]] = []
        for node in self.nodes:
            node.gossip_round()
            while node.outbox:
                to, payload = node.outbox.pop(0)
                msgs.append((node.id, to, payload))
        # Deliver
        for frm, to, payload in msgs:
            self.nodes[to].inbox.append(payload)
        for node in self.nodes:
            node.deliver_inbox()

    def converged(self, key: str) -> bool:
        """True if every node that has the key holds the same value+version."""
        vals: Set[Tuple[Any, int]] = set()
        for node in self.nodes:
            entry = node.state.get(key)
            if entry is not None:
                vals.add(entry)
        return len(vals) <= 1

    def all_have(self, key: str) -> bool:
        return all(key in node.state for node in self.nodes)


if __name__ == "__main__":
    random.seed(42)

    # Basic propagation
    c = GossipCluster(8, fanout=2)
    c.put(0, "x", 100)
    assert c.get(0, "x") == 100
    assert c.get(1, "x") is None

    for _ in range(15):
        c.round()
        if c.all_have("x") and c.converged("x"):
            break
    assert c.all_have("x")
    assert c.converged("x")
    for i in range(8):
        assert c.get(i, "x") == 100

    # Concurrent updates – higher version wins
    c2 = GossipCluster(5, fanout=2)
    c2.put(0, "k", "a")
    for _ in range(3):
        c2.round()
    # Force a higher version on node 1
    c2.nodes[1].version = 10
    c2.nodes[1].state["k"] = ("b", 10)
    for _ in range(15):
        c2.round()
    assert c2.converged("k")
    assert c2.all_have("k")
    assert c2.get(0, "k") == "b"

    # Single node
    solo = GossipCluster(1)
    solo.put(0, "solo", 42)
    solo.round()
    assert solo.get(0, "solo") == 42

    # Empty key
    assert c.get(0, "missing") is None

    # Multiple keys
    c3 = GossipCluster(6, fanout=3)
    c3.put(2, "a", 1)
    c3.put(4, "b", 2)
    for _ in range(10):
        c3.round()
    assert c3.all_have("a") and c3.all_have("b")
    assert c3.converged("a") and c3.converged("b")

    print("gossip self-test passed")
