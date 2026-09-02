"""
Module 3 – Knowledge Graph
Persistent, queryable knowledge store using NetworkX + SQLite.
Fully functional. Original implementation.
"""

from __future__ import annotations
import sqlite3
import json
import time
import hashlib
from typing import Any, Dict, List, Optional, Tuple
import networkx as nx


class KnowledgeGraph:
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.graph = nx.MultiDiGraph()
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_schema()
        self._load()

    def _init_schema(self) -> None:
        cur = self._conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS nodes (id TEXT PRIMARY KEY, data TEXT NOT NULL, created REAL NOT NULL, updated REAL NOT NULL)")
        cur.execute("CREATE TABLE IF NOT EXISTS edges (id TEXT PRIMARY KEY, source TEXT NOT NULL, target TEXT NOT NULL, key TEXT NOT NULL, data TEXT NOT NULL, created REAL NOT NULL)")
        self._conn.commit()

    def add_node(self, node_id: str, **attrs: Any) -> None:
        node_id = str(node_id)
        now = time.time()
        data = json.dumps(attrs)
        self.graph.add_node(node_id, **attrs)
        self._conn.execute("INSERT OR REPLACE INTO nodes (id, data, created, updated) VALUES (?, ?, COALESCE((SELECT created FROM nodes WHERE id=?), ?), ?)", (node_id, data, node_id, now, now))
        self._conn.commit()

    def add_edge(self, source: str, target: str, key: str = "related", **attrs: Any) -> str:
        source, target = str(source), str(target)
        if source not in self.graph:
            self.add_node(source)
        if target not in self.graph:
            self.add_node(target)
        eid = hashlib.sha256(f"{source}|{target}|{key}".encode()).hexdigest()[:16]
        now = time.time()
        data = json.dumps(attrs)
        self.graph.add_edge(source, target, key=key, **attrs)
        self._conn.execute("INSERT OR REPLACE INTO edges (id, source, target, key, data, created) VALUES (?, ?, ?, ?, ?, ?)", (eid, source, target, key, data, now))
        self._conn.commit()
        return eid

    def get_neighbors(self, node_id: str) -> List[Tuple[str, str, Dict]]:
        node_id = str(node_id)
        results = []
        for _, target, key, data in self.graph.out_edges(node_id, keys=True, data=True):
            results.append((target, key, dict(data)))
        return results

    def path(self, source: str, target: str) -> Optional[List[str]]:
        try:
            return nx.shortest_path(self.graph, str(source), str(target))
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return None

    def stats(self) -> Dict[str, int]:
        return {"nodes": self.graph.number_of_nodes(), "edges": self.graph.number_of_edges()}

    def _load(self) -> None:
        cur = self._conn.cursor()
        for row in cur.execute("SELECT id, data FROM nodes"):
            self.graph.add_node(row[0], **json.loads(row[1]))
        for row in cur.execute("SELECT source, target, key, data FROM edges"):
            self.graph.add_edge(row[0], row[1], key=row[2], **json.loads(row[3]))

    def close(self) -> None:
        self._conn.close()


if __name__ == "__main__":
    print("Testing Knowledge Graph...")
    kg = KnowledgeGraph(":memory:")
    kg.add_node("sun", type="star", mass=1.0)
    kg.add_node("earth", type="planet", mass=3e-6)
    kg.add_edge("sun", "earth", key="orbits", distance=1.0)
    print("Neighbors of sun:", kg.get_neighbors("sun"))
    print("Path sun → earth:", kg.path("sun", "earth"))
    print("Stats:", kg.stats())
    kg.close()
    print("Knowledge Graph module OK.")
