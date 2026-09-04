"""
Universe Simulator - Simple Link-Cut Tree (path aggregate)
Original splay-based preferred-path representation for connectivity.
"""

from __future__ import annotations

from typing import Dict, Optional

class LCTNode:
    def __init__(self, key: int):
        self.key = key
        self.left: Optional["LCTNode"] = None
        self.right: Optional["LCTNode"] = None
        self.parent: Optional["LCTNode"] = None
        self.rev = False

class LinkCutTree:
    def __init__(self) -> None:
        self.nodes: Dict[int, LCTNode] = {}

    def _get(self, key: int) -> LCTNode:
        if key not in self.nodes:
            self.nodes[key] = LCTNode(key)
        return self.nodes[key]

    def _push(self, x: Optional[LCTNode]) -> None:
        if x and x.rev:
            x.left, x.right = x.right, x.left
            if x.left: x.left.rev ^= True
            if x.right: x.right.rev ^= True
            x.rev = False

    def _rotate(self, x: LCTNode) -> None:
        p = x.parent
        if not p:
            return
        g = p.parent
        self._push(p)
        self._push(x)
        if p.left is x:
            p.left = x.right
            if x.right: x.right.parent = p
            x.right = p
        else:
            p.right = x.left
            if x.left: x.left.parent = p
            x.left = p
        p.parent = x
        x.parent = g
        if g:
            if g.left is p: g.left = x
            elif g.right is p: g.right = x

    def splay(self, x: LCTNode) -> None:
        while x.parent:
            p = x.parent
            g = p.parent
            if g:
                if (g.left is p) == (p.left is x):
                    self._rotate(p)
                else:
                    self._rotate(x)
            self._rotate(x)

    def access(self, key: int) -> None:
        x = self._get(key)
        last = None
        while x:
            self.splay(x)
            x.right = last
            last = x
            x = x.parent
        self.splay(self._get(key))

    def link(self, a: int, b: int) -> None:
        self.access(a)
        self.access(b)
        na, nb = self._get(a), self._get(b)
        na.parent = nb

    def connected(self, a: int, b: int) -> bool:
        self.access(a)
        self.access(b)
        return self._get(a).parent is not None or a == b

if __name__ == "__main__":
    lct = LinkCutTree()
    lct.link(1, 2)
    lct.link(2, 3)
    assert lct.connected(1, 3)
    print("splay_link self-test passed")
