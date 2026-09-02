"""
Module 33 – Hash Chain
Tamper-evident append-only hash chain.
Original implementation.
"""

from __future__ import annotations
import hashlib
import json
import time
from typing import Any, Dict, List, Optional


class HashChain:
    def __init__(self):
        self._blocks: List[Dict[str, Any]] = []

    def _hash(self, data: str) -> str:
        return hashlib.sha256(data.encode()).hexdigest()

    def append(self, payload: Any) -> str:
        prev = self._blocks[-1]["hash"] if self._blocks else "0" * 64
        block = {"index": len(self._blocks), "timestamp": time.time(), "payload": payload, "prev": prev}
        raw = json.dumps(block, sort_keys=True, default=str)
        block["hash"] = self._hash(raw)
        self._blocks.append(block)
        return block["hash"]

    def verify(self) -> bool:
        for i, block in enumerate(self._blocks):
            expected_prev = self._blocks[i - 1]["hash"] if i > 0 else "0" * 64
            if block["prev"] != expected_prev:
                return False
            check = {k: v for k, v in block.items() if k != "hash"}
            raw = json.dumps(check, sort_keys=True, default=str)
            if self._hash(raw) != block["hash"]:
                return False
        return True

    def __len__(self) -> int:
        return len(self._blocks)


if __name__ == "__main__":
    print("Testing Hash Chain...")
    chain = HashChain()
    h1 = chain.append({"msg": "genesis"})
    h2 = chain.append({"msg": "second", "value": 42})
    h3 = chain.append({"msg": "third"})
    print(f"  Length: {len(chain)}")
    print(f"  Verify: {chain.verify()}")
    chain._blocks[1]["payload"]["value"] = 99
    print(f"  After tamper verify: {chain.verify()}")
    print("Hash Chain module OK.")
