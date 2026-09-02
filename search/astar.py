"""
Module 15 – A* Pathfinding
Grid-based A* with 4 or 8 connectivity.
Original, executable implementation.
"""

from __future__ import annotations
import heapq
from typing import Dict, List, Optional, Tuple

Coord = Tuple[int, int]


class AStar:
    def __init__(self, grid: List[List[int]], allow_diagonal: bool = False):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows else 0
        self.allow_diagonal = allow_diagonal

    def _in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < self.rows and 0 <= c < self.cols

    def _passable(self, r: int, c: int) -> bool:
        return self._in_bounds(r, c) and self.grid[r][c] == 0

    def _neighbors(self, node: Coord) -> List[Coord]:
        r, c = node
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if self.allow_diagonal:
            dirs += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        result = []
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if self._passable(nr, nc):
                result.append((nr, nc))
        return result

    def _heuristic(self, a: Coord, b: Coord) -> float:
        if self.allow_diagonal:
            return max(abs(a[0] - b[0]), abs(a[1] - b[1]))
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def search(self, start: Coord, goal: Coord) -> Optional[List[Coord]]:
        if not self._passable(*start) or not self._passable(*goal):
            return None
        open_set: List[Tuple[float, int, Coord]] = []
        counter = 0
        heapq.heappush(open_set, (0.0, counter, start))
        came_from: Dict[Coord, Coord] = {}
        g_score: Dict[Coord, float] = {start: 0.0}
        while open_set:
            _, _, current = heapq.heappop(open_set)
            if current == goal:
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()
                return path
            for neighbor in self._neighbors(current):
                tentative = g_score[current] + 1.0
                if tentative < g_score.get(neighbor, float("inf")):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative
                    f = tentative + self._heuristic(neighbor, goal)
                    counter += 1
                    heapq.heappush(open_set, (f, counter, neighbor))
        return None


if __name__ == "__main__":
    print("Testing A* Pathfinding...")
    grid = [
        [0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
    ]
    astar = AStar(grid, allow_diagonal=False)
    path = astar.search((0, 0), (5, 5))
    print("Path found:", path is not None)
    if path:
        print("  Length:", len(path))
        print("  Path:", path)
    print("A* Pathfinding module OK.")
