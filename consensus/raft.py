"""Raft consensus – leader election and log replication (single-threaded sim)."""
from __future__ import annotations
import random
from typing import Any, Dict, List, Optional


class RaftNode:
    def __init__(self, node_id: int, peers: List[int], seed: int = 42):
        self.id = node_id
        self.peers = peers
        self.state = "follower"
        self.term = 0
        self.voted_for: Optional[int] = None
        self.log: List[Dict] = []
        self.commit_index = -1
        self.rng = random.Random(seed + node_id)

    def request_vote(self, term: int, candidate: int) -> bool:
        if term > self.term:
            self.term = term
            self.state = "follower"
            self.voted_for = None
        if term == self.term and (self.voted_for is None or self.voted_for == candidate):
            self.voted_for = candidate
            return True
        return False

    def append_entries(self, term: int, leader: int, entries: List[Dict], leader_commit: int) -> bool:
        if term < self.term:
            return False
        self.term = term
        self.state = "follower"
        self.log.extend(entries)
        if leader_commit > self.commit_index:
            self.commit_index = min(leader_commit, len(self.log) - 1)
        return True

    def start_election(self, cluster: Dict[int, "RaftNode"]) -> bool:
        self.term += 1
        self.state = "candidate"
        self.voted_for = self.id
        votes = 1
        for p in self.peers:
            if cluster[p].request_vote(self.term, self.id):
                votes += 1
        if votes > (len(self.peers) + 1) // 2:
            self.state = "leader"
            return True
        self.state = "follower"
        return False

    def replicate(self, cmd: Any, cluster: Dict[int, "RaftNode"]) -> bool:
        if self.state != "leader":
            return False
        entry = {"term": self.term, "cmd": cmd}
        self.log.append(entry)
        acks = 1
        for p in self.peers:
            if cluster[p].append_entries(self.term, self.id, [entry], self.commit_index):
                acks += 1
        if acks > (len(self.peers) + 1) // 2:
            self.commit_index = len(self.log) - 1
            for p in self.peers:
                cluster[p].commit_index = self.commit_index
            return True
        return False


if __name__ == "__main__":
    nodes = {i: RaftNode(i, [j for j in range(3) if j != i], seed=i) for i in range(3)}
    elected = nodes[0].start_election(nodes)
    assert elected and nodes[0].state == "leader"
    assert nodes[0].replicate("SET x=1", nodes)
    assert nodes[1].commit_index >= 0
    print(f"raft leader={nodes[0].id} commit={nodes[0].commit_index}")
    print("raft self-tests passed")
