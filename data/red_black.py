"""
Universe Simulator - Red-Black Tree
Original insert + search implementation with color fixes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

RED, BLACK = True, False

@dataclass
class RBNode:
    key: int
    color: bool = RED
    left: Optional["RBNode"] = None
    right: Optional["RBNode"] = None
    parent: Optional["RBNode"] = None

class RedBlackTree:
    def __init__(self) -> None:
        self.nil = RBNode(key=0, color=BLACK)
        self.root = self.nil

    def search(self, key: int) -> bool:
        x = self.root
        while x is not self.nil:
            if key == x.key:
                return True
            x = x.left if key < x.key else x.right
        return False

    def insert(self, key: int) -> None:
        z = RBNode(key=key, color=RED, left=self.nil, right=self.nil)
        y = self.nil
        x = self.root
        while x is not self.nil:
            y = x
            x = x.left if z.key < x.key else x.right
        z.parent = y
        if y is self.nil:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        self._fix_insert(z)

    def _left_rotate(self, x: RBNode) -> None:
        y = x.right
        x.right = y.left
        if y.left is not self.nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is self.nil:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, y: RBNode) -> None:
        x = y.left
        y.left = x.right
        if x.right is not self.nil:
            x.right.parent = y
        x.parent = y.parent
        if y.parent is self.nil:
            self.root = x
        elif y is y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x

    def _fix_insert(self, z: RBNode) -> None:
        while z.parent.color == RED:
            if z.parent is z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z is z.parent.right:
                        z = z.parent
                        self._left_rotate(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self._right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z is z.parent.left:
                        z = z.parent
                        self._right_rotate(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self._left_rotate(z.parent.parent)
            if z is self.root:
                break
        self.root.color = BLACK

if __name__ == "__main__":
    t = RedBlackTree()
    for k in [7, 3, 18, 10, 22, 8, 11, 26]:
        t.insert(k)
    assert t.search(10) and t.search(26) and not t.search(5)
    print("red_black self-test passed")
