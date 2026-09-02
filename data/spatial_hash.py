"""
Universe Simulator – Spatial Hashing Module
observabilityengine/Universe-Simulator

Production-grade 3-D spatial hash (uniform grid + hash table).
Average O(1) insert / remove / update / neighbour query under
uniform distribution. Designed for high-entity-count particle /
body simulations with observability requirements.

Original implementation. No external code reused.
"""

from __future__ import annotations

import math
import threading
from collections import defaultdict
from dataclasses import dataclass
from typing import (
    Dict,
    Iterator,
    List,
    Optional,
    Set,
    Tuple,
)


class SpatialHashError(Exception):
    """Base exception for spatial hashing layer."""


class InvalidParameterError(SpatialHashError):
    """Raised on illegal construction or query parameters."""


class EntityCollisionError(SpatialHashError):
    """Raised when an entity ID is already present (strict mode)."""


Position3D = Tuple[float, float, float]
CellKey = Tuple[int, int, int]


@dataclass(slots=True, frozen=True)
class HashStats:
    """Runtime statistics for observability."""
    entity_count: int
    occupied_cells: int
    max_bucket_size: int
    avg_bucket_size: float
    cell_size: float


class SpatialHash3D:
    """
    Thread-safe 3-D spatial hash based on a uniform grid.

    Complexity (average case, uniform distribution)
    -----------------------------------------------
    insert / remove / update : O(1)
    query_radius             : O(k)  where k = entities in neighbouring cells
    query_aabb               : O(k)
    clear                    : O(n)

    The grid is infinite; only occupied cells consume memory.
    Cell size is fixed at construction time (choose ≈ mean inter-particle distance
    for best performance).
    """

    __slots__ = (
        "_cell_size",
        "_inv_cell",
        "_cells",
        "_entity_to_cell",
        "_lock",
        "_strict",
    )

    def __init__(
        self,
        cell_size: float = 1.0,
        *,
        strict: bool = True,
    ) -> None:
        if not math.isfinite(cell_size) or cell_size <= 0.0:
            raise InvalidParameterError("cell_size must be a finite positive number")
        self._cell_size = float(cell_size)
        self._inv_cell = 1.0 / self._cell_size
        self._cells: Dict[CellKey, Set[str]] = defaultdict(set)
        self._entity_to_cell: Dict[str, CellKey] = {}
        self._lock = threading.RLock()
        self._strict = bool(strict)

    def _key(self, pos: Position3D) -> CellKey:
        x, y, z = pos
        return (
            math.floor(x * self._inv_cell),
            math.floor(y * self._inv_cell),
            math.floor(z * self._inv_cell),
        )

    def _validate_position(self, pos: Position3D) -> None:
        if not (isinstance(pos, (tuple, list)) and len(pos) == 3):
            raise InvalidParameterError("position must be a 3-tuple/list of floats")
        if not all(math.isfinite(c) for c in pos):
            raise InvalidParameterError("position components must be finite")

    def insert(self, entity_id: str, position: Position3D) -> None:
        self._validate_position(position)
        key = self._key(position)
        with self._lock:
            if entity_id in self._entity_to_cell:
                if self._strict:
                    raise EntityCollisionError(f"entity already present: {entity_id}")
                old_key = self._entity_to_cell[entity_id]
                self._cells[old_key].discard(entity_id)
                if not self._cells[old_key]:
                    del self._cells[old_key]
            self._cells[key].add(entity_id)
            self._entity_to_cell[entity_id] = key

    def remove(self, entity_id: str) -> bool:
        with self._lock:
            key = self._entity_to_cell.pop(entity_id, None)
            if key is None:
                return False
            bucket = self._cells[key]
            bucket.discard(entity_id)
            if not bucket:
                del self._cells[key]
            return True

    def update(self, entity_id: str, new_position: Position3D) -> None:
        self._validate_position(new_position)
        new_key = self._key(new_position)
        with self._lock:
            old_key = self._entity_to_cell.get(entity_id)
            if old_key is None:
                self._cells[new_key].add(entity_id)
                self._entity_to_cell[entity_id] = new_key
                return
            if old_key == new_key:
                return
            self._cells[old_key].discard(entity_id)
            if not self._cells[old_key]:
                del self._cells[old_key]
            self._cells[new_key].add(entity_id)
            self._entity_to_cell[entity_id] = new_key

    def clear(self) -> None:
        with self._lock:
            self._cells.clear()
            self._entity_to_cell.clear()

    def query_radius(
        self,
        center: Position3D,
        radius: float,
        *,
        include_self: bool = True,
    ) -> List[str]:
        self._validate_position(center)
        if not math.isfinite(radius) or radius < 0.0:
            raise InvalidParameterError("radius must be a finite non-negative number")

        r_cells = math.ceil(radius * self._inv_cell)
        cx, cy, cz = self._key(center)

        result: List[str] = []
        with self._lock:
            for dx in range(-r_cells, r_cells + 1):
                for dy in range(-r_cells, r_cells + 1):
                    for dz in range(-r_cells, r_cells + 1):
                        key = (cx + dx, cy + dy, cz + dz)
                        bucket = self._cells.get(key)
                        if bucket:
                            result.extend(bucket)
        return result

    def query_aabb(
        self,
        min_corner: Position3D,
        max_corner: Position3D,
    ) -> List[str]:
        self._validate_position(min_corner)
        self._validate_position(max_corner)
        if any(a > b for a, b in zip(min_corner, max_corner)):
            raise InvalidParameterError("min_corner must be component-wise <= max_corner")

        x0, y0, z0 = self._key(min_corner)
        x1, y1, z1 = self._key(max_corner)

        result: List[str] = []
        with self._lock:
            for x in range(x0, x1 + 1):
                for y in range(y0, y1 + 1):
                    for z in range(z0, z1 + 1):
                        bucket = self._cells.get((x, y, z))
                        if bucket:
                            result.extend(bucket)
        return result

    def neighbours(
        self,
        entity_id: str,
        radius: float,
    ) -> List[str]:
        with self._lock:
            key = self._entity_to_cell.get(entity_id)
            if key is None:
                return []
            cs = self._cell_size
            center = (
                (key[0] + 0.5) * cs,
                (key[1] + 0.5) * cs,
                (key[2] + 0.5) * cs,
            )
        ids = self.query_radius(center, radius)
        return [i for i in ids if i != entity_id]

    def stats(self) -> HashStats:
        with self._lock:
            n = len(self._entity_to_cell)
            occupied = len(self._cells)
            if occupied == 0:
                return HashStats(0, 0, 0, 0.0, self._cell_size)
            sizes = [len(b) for b in self._cells.values()]
            return HashStats(
                entity_count=n,
                occupied_cells=occupied,
                max_bucket_size=max(sizes),
                avg_bucket_size=n / occupied,
                cell_size=self._cell_size,
            )

    def __len__(self) -> int:
        with self._lock:
            return len(self._entity_to_cell)

    def __contains__(self, entity_id: str) -> bool:
        with self._lock:
            return entity_id in self._entity_to_cell

    def cells(self) -> Iterator[Tuple[CellKey, Set[str]]]:
        with self._lock:
            items = [(k, set(v)) for k, v in self._cells.items()]
        yield from items


if __name__ == "__main__":
    import unittest

    class TestSpatialHash3D(unittest.TestCase):
        def setUp(self) -> None:
            self.h = SpatialHash3D(cell_size=2.0, strict=True)

        def test_insert_remove_contains(self) -> None:
            self.h.insert("a", (0.5, 0.5, 0.5))
            self.assertIn("a", self.h)
            self.assertEqual(len(self.h), 1)
            self.assertTrue(self.h.remove("a"))
            self.assertNotIn("a", self.h)
            self.assertFalse(self.h.remove("a"))

        def test_strict_collision(self) -> None:
            self.h.insert("a", (1.0, 1.0, 1.0))
            with self.assertRaises(EntityCollisionError):
                self.h.insert("a", (3.0, 3.0, 3.0))

        def test_update_moves_cell(self) -> None:
            self.h.insert("p", (0.1, 0.1, 0.1))
            self.h.update("p", (2.1, 0.1, 0.1))
            hits = self.h.query_radius((2.0, 0.0, 0.0), 1.0)
            self.assertIn("p", hits)

        def test_query_radius_returns_neighbours(self) -> None:
            self.h.insert("c", (0.0, 0.0, 0.0))
            self.h.insert("n1", (1.5, 0.0, 0.0))
            self.h.insert("far", (10.0, 0.0, 0.0))
            hits = set(self.h.query_radius((0.0, 0.0, 0.0), 2.0))
            self.assertIn("c", hits)
            self.assertIn("n1", hits)
            self.assertNotIn("far", hits)

        def test_stats(self) -> None:
            self.h.insert("x", (0.0, 0.0, 0.0))
            self.h.insert("y", (0.1, 0.1, 0.1))
            s = self.h.stats()
            self.assertEqual(s.entity_count, 2)
            self.assertEqual(s.occupied_cells, 1)
            self.assertEqual(s.max_bucket_size, 2)

    unittest.main(verbosity=2)
