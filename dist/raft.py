"""
Universe Simulator - Toy Raft Consensus
Leader election + log replication for a fixed set of nodes.
Simulates network via explicit message delivery (no threads).
Complexity O(N) message fan-out per step.
Limitations: no snapshotting, no membership change, deterministic timeouts,
             no persistent storage, single-threaded simulation only.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple


class Role(Enum):
    FOLLOWER = auto()
    CANDIDATE = auto()
    LEADER = auto()


@dataclass
class LogEntry:
    term: int
    command: Any


@dataclass
class RequestVote:
    term: int
    candidate_id: int
    last_log_index: int
    last_log_term: int


@dataclass
class RequestVoteReply:
    term: int
    vote_granted: bool


@dataclass
class AppendEntries:
    term: int
    leader_id: int
    prev_log_index: int
    prev_log_term: int
    entries: List[LogEntry]
    leader_commit: int


@dataclass
class AppendEntriesReply:
    term: int
    success: bool
    match_index: int


class Raft:
    """Single Raft node. Messages are delivered explicitly by the simulator."""

    def __init__(self, node_id: int, peers: List[int]) -> None:
        self.id = node_id
        self.peers = peers
        self.role = Role.FOLLOWER
        self.term = 0
        self.voted_for: Optional[int] = None
        self.log: List[LogEntry] = []
        self.commit_index = -1
        self.last_applied = -1
        self.next_index: Dict[int, int] = {p: 0 for p in peers}
        self.match_index: Dict[int, int] = {p: -1 for p in peers}
        self.votes = 0
        self.election_elapsed = 0
        self.election_timeout = 5 + (node_id % 5)
        self.heartbeat_elapsed = 0
        self.heartbeat_interval = 2
        self.outbox: List[Tuple[int, Any]] = []
        self.applied: List[Any] = []

    def _last_idx(self) -> int:
        return len(self.log) - 1

    def _last_term(self) -> int:
        return self.log[-1].term if self.log else 0

    def _send(self, to: int, msg: Any) -> None:
        self.outbox.append((to, msg))

    def start_election(self) -> None:
        self.role = Role.CANDIDATE
        self.term += 1
        self.voted_for = self.id
        self.votes = 1
        self.election_elapsed = 0
        for p in self.peers:
            self._send(p, RequestVote(
                term=self.term,
                candidate_id=self.id,
                last_log_index=self._last_idx(),
                last_log_term=self._last_term(),
            ))
        if self.votes > (len(self.peers) + 1) // 2:
            self.become_leader()

    def become_leader(self) -> None:
        self.role = Role.LEADER
        for p in self.peers:
            self.next_index[p] = len(self.log)
            self.match_index[p] = -1
        self.heartbeat_elapsed = 0
        self._heartbeat()

    def _heartbeat(self) -> None:
        for p in self.peers:
            prev = self.next_index[p] - 1
            prev_term = self.log[prev].term if 0 <= prev < len(self.log) else 0
            entries = self.log[self.next_index[p]:]
            self._send(p, AppendEntries(
                term=self.term,
                leader_id=self.id,
                prev_log_index=prev,
                prev_log_term=prev_term,
                entries=entries,
                leader_commit=self.commit_index,
            ))

    def on_tick(self) -> None:
        if self.role == Role.LEADER:
            self.heartbeat_elapsed += 1
            if self.heartbeat_elapsed >= self.heartbeat_interval:
                self._heartbeat()
                self.heartbeat_elapsed = 0
        else:
            self.election_elapsed += 1
            if self.election_elapsed >= self.election_timeout:
                self.start_election()

    def on_message(self, from_id: int, msg: Any) -> None:
        if isinstance(msg, RequestVote):
            self._on_request_vote(from_id, msg)
        elif isinstance(msg, RequestVoteReply):
            self._on_vote_reply(from_id, msg)
        elif isinstance(msg, AppendEntries):
            self._on_append(from_id, msg)
        elif isinstance(msg, AppendEntriesReply):
            self._on_append_reply(from_id, msg)
        self._apply()

    def _on_request_vote(self, from_id: int, msg: RequestVote) -> None:
        if msg.term > self.term:
            self.term = msg.term
            self.role = Role.FOLLOWER
            self.voted_for = None
        grant = False
        if msg.term == self.term:
            if self.voted_for is None or self.voted_for == msg.candidate_id:
                if (msg.last_log_term > self._last_term() or
                        (msg.last_log_term == self._last_term() and
                         msg.last_log_index >= self._last_idx())):
                    grant = True
                    self.voted_for = msg.candidate_id
                    self.election_elapsed = 0
        self._send(from_id, RequestVoteReply(term=self.term, vote_granted=grant))

    def _on_vote_reply(self, from_id: int, msg: RequestVoteReply) -> None:
        if self.role != Role.CANDIDATE:
            return
        if msg.term > self.term:
            self.term = msg.term
            self.role = Role.FOLLOWER
            self.voted_for = None
            return
        if msg.term == self.term and msg.vote_granted:
            self.votes += 1
            if self.votes > (len(self.peers) + 1) // 2:
                self.become_leader()

    def _on_append(self, from_id: int, msg: AppendEntries) -> None:
        if msg.term > self.term:
            self.term = msg.term
            self.voted_for = None
        success = False
        match = -1
        if msg.term == self.term:
            self.role = Role.FOLLOWER
            self.election_elapsed = 0
            if msg.prev_log_index == -1 or (
                msg.prev_log_index < len(self.log) and
                (msg.prev_log_index < 0 or
                 self.log[msg.prev_log_index].term == msg.prev_log_term)
            ):
                idx = msg.prev_log_index + 1
                self.log = self.log[:idx]
                self.log.extend(msg.entries)
                match = len(self.log) - 1
                if msg.leader_commit > self.commit_index:
                    self.commit_index = min(msg.leader_commit, match)
                success = True
        self._send(from_id, AppendEntriesReply(
            term=self.term, success=success, match_index=match
        ))

    def _on_append_reply(self, from_id: int, msg: AppendEntriesReply) -> None:
        if self.role != Role.LEADER:
            return
        if msg.term > self.term:
            self.term = msg.term
            self.role = Role.FOLLOWER
            self.voted_for = None
            return
        if msg.term != self.term:
            return
        if msg.success:
            self.match_index[from_id] = msg.match_index
            self.next_index[from_id] = msg.match_index + 1
            for idx in range(len(self.log) - 1, self.commit_index, -1):
                if self.log[idx].term != self.term:
                    continue
                count = 1
                for p in self.peers:
                    if self.match_index.get(p, -1) >= idx:
                        count += 1
                if count > (len(self.peers) + 1) // 2:
                    self.commit_index = idx
                    break
        else:
            self.next_index[from_id] = max(0, self.next_index[from_id] - 1)

    def _apply(self) -> None:
        while self.last_applied < self.commit_index:
            self.last_applied += 1
            self.applied.append(self.log[self.last_applied].command)

    def client_append(self, command: Any) -> bool:
        if self.role != Role.LEADER:
            return False
        self.log.append(LogEntry(term=self.term, command=command))
        if not self.peers:
            self.commit_index = len(self.log) - 1
            self._apply()
        else:
            self._heartbeat()
        return True


class RaftSimulator:
    """Drive a set of Raft nodes with explicit message delivery."""

    def __init__(self, n: int = 3) -> None:
        if n < 1:
            raise ValueError("n must be >= 1")
        self.n = n
        self.nodes = [Raft(i, [j for j in range(n) if j != i]) for i in range(n)]

    def tick(self) -> None:
        for node in self.nodes:
            node.on_tick()
        self._deliver()

    def _deliver(self) -> None:
        msgs: List[Tuple[int, int, Any]] = []
        for node in self.nodes:
            while node.outbox:
                to, msg = node.outbox.pop(0)
                msgs.append((node.id, to, msg))
        for frm, to, msg in msgs:
            self.nodes[to].on_message(frm, msg)

    def submit(self, command: Any) -> bool:
        for node in self.nodes:
            if node.role == Role.LEADER:
                return node.client_append(command)
        return False

    def leader(self) -> Optional[int]:
        for node in self.nodes:
            if node.role == Role.LEADER:
                return node.id
        return None

    def committed(self) -> List[Any]:
        from collections import Counter
        c: Counter = Counter()
        for n in self.nodes:
            for cmd in n.applied:
                c[cmd] += 1
        return [cmd for cmd, cnt in c.items() if cnt > self.n // 2]


if __name__ == "__main__":
    # Election + commit
    sim = RaftSimulator(3)
    for _ in range(30):
        sim.tick()
        if sim.leader() is not None:
            break
    assert sim.leader() is not None, "no leader elected"

    assert sim.submit("cmd1")
    assert sim.submit("cmd2")
    for _ in range(20):
        sim.tick()

    committed = sim.committed()
    assert "cmd1" in committed
    assert "cmd2" in committed

    # Safety: applied prefixes agree
    applied_lists = [n.applied for n in sim.nodes if n.applied]
    if applied_lists:
        min_len = min(len(a) for a in applied_lists)
        for i in range(min_len):
            vals = {a[i] for a in applied_lists}
            assert len(vals) == 1, "divergent applied logs"

    # Single-node
    solo = RaftSimulator(1)
    for _ in range(10):
        solo.tick()
    assert solo.leader() == 0
    assert solo.submit("solo-cmd")
    for _ in range(5):
        solo.tick()
    assert "solo-cmd" in solo.nodes[0].applied

    # Larger cluster eventually elects
    big = RaftSimulator(5)
    assert big.leader() is None
    for _ in range(40):
        big.tick()
    assert big.leader() is not None

    print("raft self-test passed")
