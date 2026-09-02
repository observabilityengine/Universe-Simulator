"""
Module 12 – Universe State Serializer
Checkpoint and restore of arbitrary Python object graphs.
Fully functional. Original implementation.
"""

from __future__ import annotations
import pickle
import time
from pathlib import Path
from typing import Any, Dict, Optional, List
import tempfile


class StateSerializer:
    def __init__(self, base_dir: str = "./checkpoints"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _checkpoint_path(self, name: str) -> Path:
        safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)
        return self.base_dir / f"{safe}.ckpt"

    def save(self, name: str, state: Any, meta: Optional[Dict] = None) -> str:
        path = self._checkpoint_path(name)
        payload = {"timestamp": time.time(), "meta": meta or {}, "state": state}
        with open(path, "wb") as f:
            pickle.dump(payload, f, protocol=pickle.HIGHEST_PROTOCOL)
        return str(path)

    def load(self, name: str) -> Any:
        path = self._checkpoint_path(name)
        if not path.exists():
            raise FileNotFoundError(f"No checkpoint named '{name}'")
        with open(path, "rb") as f:
            payload = pickle.load(f)
        return payload["state"]

    def list_checkpoints(self) -> List[Dict[str, Any]]:
        results = []
        for p in sorted(self.base_dir.glob("*.ckpt")):
            try:
                with open(p, "rb") as f:
                    payload = pickle.load(f)
                results.append({"name": p.stem, "path": str(p), "timestamp": payload.get("timestamp"), "meta": payload.get("meta", {}), "size_bytes": p.stat().st_size})
            except Exception:
                continue
        return results

    def delete(self, name: str) -> bool:
        path = self._checkpoint_path(name)
        if path.exists():
            path.unlink()
            return True
        return False


if __name__ == "__main__":
    print("Testing State Serializer...")
    with tempfile.TemporaryDirectory() as tmp:
        ser = StateSerializer(tmp)
        state = {"positions": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]], "generation": 42, "agents": ["alpha", "beta"]}
        path = ser.save("test_run", state, meta={"note": "unit test"})
        print("Saved to:", path)
        loaded = ser.load("test_run")
        assert loaded["generation"] == 42
        print("Loaded OK:", loaded)
        print("Checkpoints:", ser.list_checkpoints())
        ser.delete("test_run")
        print("Deleted. Exists?", ser._checkpoint_path("test_run").exists())
    print("State Serializer module OK.")
