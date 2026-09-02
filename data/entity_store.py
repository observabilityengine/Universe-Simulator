"""
Universe Simulator - Core Entity Store
observabilityengine/Universe-Simulator

Thread-safe entity store with spatial indexing via SpatialHash3D,
versioned snapshots, async bulk operations.
Original implementation for high-entity universe simulation.
"""

from __future__ import annotations

import asyncio
import math
import time
import uuid
from dataclasses import dataclass, field
from typing import (
    Any,
    AsyncIterator,
    Dict,
    Iterable,
    List,
    Optional,
    Tuple,
)
import threading

from data.spatial_hash import SpatialHash3D, Position3D, InvalidParameterError


class UniverseDataError(Exception):
    """Base exception for data-structure layer."""


class EntityNotFoundError(UniverseDataError):
    """Raised when an entity ID does not exist."""


class DuplicateEntityError(UniverseDataError):
    """Raised on attempt to insert an already-existing ID."""


class ConcurrencyError(UniverseDataError):
    """Raised on conflicting concurrent mutations."""


@dataclass(slots=True, frozen=True)
class EntitySnapshot:
    entity_id: str
    position: Position3D
    velocity: Position3D
    mass: float
    properties: Dict[str, Any]
    timestamp: float
    version: int


@dataclass(slots=True)
class Entity:
    entity_id: str
    position: Position3D
    velocity: Position3D = (0.0, 0.0, 0.0)
    mass: float = 1.0
    properties: Dict[str, Any] = field(default_factory=dict)
    version: int = 0
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)

    def snapshot(self) -> EntitySnapshot:
        return EntitySnapshot(
            entity_id=self.entity_id,
            position=self.position,
            velocity=self.velocity,
            mass=self.mass,
            properties=dict(self.properties),
            timestamp=self.updated_at,
            version=self.version,
        )


class UniverseEntityStore:
    """
    Thread-safe, async-capable central data structure for the Universe Simulator.
    """

    def __init__(
        self,
        cell_size: float = 10.0,
        max_entities: Optional[int] = None,
    ) -> None:
        self._entities: Dict[str, Entity] = {}
        self._spatial = SpatialHash3D(cell_size=cell_size, strict=False)
        self._lock = threading.RLock()
        self._max_entities = max_entities

    def create(
        self,
        position: Position3D,
        velocity: Position3D = (0.0, 0.0, 0.0),
        mass: float = 1.0,
        properties: Optional[Dict[str, Any]] = None,
        entity_id: Optional[str] = None,
    ) -> str:
        if mass <= 0.0:
            raise ValueError("mass must be > 0")
        if not all(math.isfinite(c) for c in position):
            raise ValueError("position components must be finite")

        eid = entity_id or str(uuid.uuid4())
        with self._lock:
            if eid in self._entities:
                raise DuplicateEntityError(f"entity already exists: {eid}")
            if self._max_entities is not None and len(self._entities) >= self._max_entities:
                raise UniverseDataError("max_entities limit reached")

            entity = Entity(
                entity_id=eid,
                position=position,
                velocity=velocity,
                mass=mass,
                properties=dict(properties or {}),
                version=0,
            )
            self._entities[eid] = entity
            self._spatial.insert(eid, position)
            return eid

    def get(self, entity_id: str) -> EntitySnapshot:
        with self._lock:
            entity = self._entities.get(entity_id)
            if entity is None:
                raise EntityNotFoundError(entity_id)
            return entity.snapshot()

    def update(
        self,
        entity_id: str,
        position: Optional[Position3D] = None,
        velocity: Optional[Position3D] = None,
        mass: Optional[float] = None,
        properties: Optional[Dict[str, Any]] = None,
        expected_version: Optional[int] = None,
    ) -> EntitySnapshot:
        with self._lock:
            entity = self._entities.get(entity_id)
            if entity is None:
                raise EntityNotFoundError(entity_id)

            if expected_version is not None and entity.version != expected_version:
                raise ConcurrencyError(
                    f"version mismatch: expected {expected_version}, actual {entity.version}"
                )

            if position is not None:
                if not all(math.isfinite(c) for c in position):
                    raise ValueError("position components must be finite")
                self._spatial.update(entity_id, position)
                entity.position = position

            if velocity is not None:
                entity.velocity = velocity
            if mass is not None:
                if mass <= 0.0:
                    raise ValueError("mass must be > 0")
                entity.mass = mass
            if properties is not None:
                entity.properties.update(properties)

            entity.version += 1
            entity.updated_at = time.time()
            return entity.snapshot()

    def delete(self, entity_id: str) -> None:
        with self._lock:
            if entity_id not in self._entities:
                raise EntityNotFoundError(entity_id)
            del self._entities[entity_id]
            self._spatial.remove(entity_id)

    def query_radius(
        self, center: Position3D, radius: float
    ) -> List[EntitySnapshot]:
        with self._lock:
            candidates = self._spatial.query_radius(center, radius)
            result: List[EntitySnapshot] = []
            r2 = radius * radius
            cx, cy, cz = center
            for eid in candidates:
                entity = self._entities.get(eid)
                if entity is None:
                    continue
                px, py, pz = entity.position
                dist2 = (px - cx) ** 2 + (py - cy) ** 2 + (pz - cz) ** 2
                if dist2 <= r2:
                    result.append(entity.snapshot())
            return result

    def count(self) -> int:
        with self._lock:
            return len(self._entities)

    def clear(self) -> None:
        with self._lock:
            self._entities.clear()
            self._spatial.clear()

    async def create_async(self, *args: Any, **kwargs: Any) -> str:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: self.create(*args, **kwargs))

    async def export_snapshots_async(
        self,
        entity_ids: Optional[Iterable[str]] = None,
    ) -> List[EntitySnapshot]:
        loop = asyncio.get_running_loop()

        def _export() -> List[EntitySnapshot]:
            with self._lock:
                if entity_ids is None:
                    return [e.snapshot() for e in self._entities.values()]
                out: List[EntitySnapshot] = []
                for eid in entity_ids:
                    e = self._entities.get(eid)
                    if e is not None:
                        out.append(e.snapshot())
                return out

        return await loop.run_in_executor(None, _export)


if __name__ == "__main__":
    import unittest

    class TestUniverseEntityStore(unittest.TestCase):
        def setUp(self) -> None:
            self.store = UniverseEntityStore(cell_size=5.0)

        def test_create_get_delete(self) -> None:
            eid = self.store.create(position=(1.0, 2.0, 3.0), mass=10.0)
            snap = self.store.get(eid)
            self.assertEqual(snap.position, (1.0, 2.0, 3.0))
            self.assertEqual(snap.mass, 10.0)
            self.assertEqual(self.store.count(), 1)
            self.store.delete(eid)
            self.assertEqual(self.store.count(), 0)
            with self.assertRaises(EntityNotFoundError):
                self.store.get(eid)

        def test_spatial_query_radius(self) -> None:
            e1 = self.store.create(position=(0.0, 0.0, 0.0))
            e2 = self.store.create(position=(3.0, 0.0, 0.0))
            e3 = self.store.create(position=(20.0, 0.0, 0.0))
            hits = self.store.query_radius(center=(0.0, 0.0, 0.0), radius=5.0)
            ids = {h.entity_id for h in hits}
            self.assertIn(e1, ids)
            self.assertIn(e2, ids)
            self.assertNotIn(e3, ids)

        def test_optimistic_concurrency(self) -> None:
            eid = self.store.create(position=(0.0, 0.0, 0.0))
            snap = self.store.get(eid)
            self.store.update(eid, position=(1.0, 0.0, 0.0), expected_version=snap.version)
            with self.assertRaises(ConcurrencyError):
                self.store.update(
                    eid,
                    position=(2.0, 0.0, 0.0),
                    expected_version=snap.version,
                )

    unittest.main(verbosity=2)
