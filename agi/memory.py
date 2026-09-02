"""
Module 7 – Memory System
Hierarchical memory: episodic, semantic, procedural.
Fully functional. Original implementation.
"""

from __future__ import annotations
import time
import hashlib
import json
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class MemoryItem:
    content: Any
    timestamp: float
    importance: float = 1.0
    tags: List[str] = field(default_factory=list)
    access_count: int = 0

    def touch(self) -> None:
        self.access_count += 1


class EpisodicMemory:
    def __init__(self, capacity: int = 1000):
        self.capacity = capacity
        self._items: OrderedDict[str, MemoryItem] = OrderedDict()

    def _key(self, content: Any) -> str:
        raw = json.dumps(content, sort_keys=True, default=str)
        return hashlib.sha256(raw.encode()).hexdigest()[:12]

    def store(self, content: Any, importance: float = 1.0, tags: Optional[List[str]] = None) -> str:
        key = self._key(content)
        item = MemoryItem(content=content, timestamp=time.time(), importance=importance, tags=tags or [])
        if key in self._items:
            del self._items[key]
        self._items[key] = item
        while len(self._items) > self.capacity:
            self._items.popitem(last=False)
        return key

    def retrieve_recent(self, n: int = 10) -> List[MemoryItem]:
        items = list(self._items.values())[-n:]
        for it in items:
            it.touch()
        return items

    def __len__(self) -> int:
        return len(self._items)


class SemanticMemory:
    def __init__(self):
        self._facts: Dict[str, Any] = {}

    def store(self, key: str, value: Any) -> None:
        self._facts[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._facts.get(key, default)

    def keys(self) -> List[str]:
        return list(self._facts.keys())


class ProceduralMemory:
    def __init__(self):
        self._skills: Dict[str, callable] = {}

    def register(self, name: str, func: callable) -> None:
        self._skills[name] = func

    def execute(self, name: str, *args, **kwargs) -> Any:
        if name not in self._skills:
            raise KeyError(f"Unknown skill: {name}")
        return self._skills[name](*args, **kwargs)

    def list_skills(self) -> List[str]:
        return list(self._skills.keys())


class MemorySystem:
    def __init__(self, episodic_capacity: int = 2000):
        self.episodic = EpisodicMemory(capacity=episodic_capacity)
        self.semantic = SemanticMemory()
        self.procedural = ProceduralMemory()

    def remember_event(self, event: Any, importance: float = 1.0, tags: Optional[List[str]] = None) -> str:
        return self.episodic.store(event, importance, tags)

    def recall_recent(self, n: int = 5) -> List[Any]:
        return [it.content for it in self.episodic.retrieve_recent(n)]

    def know(self, key: str, value: Any) -> None:
        self.semantic.store(key, value)

    def recall_fact(self, key: str, default: Any = None) -> Any:
        return self.semantic.get(key, default)

    def learn_skill(self, name: str, func: callable) -> None:
        self.procedural.register(name, func)

    def use_skill(self, name: str, *args, **kwargs) -> Any:
        return self.procedural.execute(name, *args, **kwargs)

    def stats(self) -> Dict[str, int]:
        return {"episodic": len(self.episodic), "semantic": len(self.semantic.keys()), "procedural": len(self.procedural.list_skills())}


if __name__ == "__main__":
    print("Testing Memory System...")
    mem = MemorySystem(episodic_capacity=10)
    mem.remember_event({"action": "observe", "object": "star"}, tags=["vision"])
    mem.know("sun_mass", 1.0)
    mem.learn_skill("double", lambda x: x * 2)
    print("Recent events:", mem.recall_recent(2))
    print("Sun mass:", mem.recall_fact("sun_mass"))
    print("double(21) =", mem.use_skill("double", 21))
    print("Stats:", mem.stats())
    print("Memory System module OK.")
