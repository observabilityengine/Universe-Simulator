"""Simple macro expansion (#define style)."""
from __future__ import annotations
import re
from typing import Dict


def expand_macros(source: str, macros: Dict[str, str] = None) -> str:
    macros = macros or {}
    for name, body in macros.items():
        source = re.sub(rf"\b{name}\b", body, source)
    return source


if __name__ == "__main__":
    out = expand_macros("PI * r * r", {"PI": "3.14"})
    assert "3.14" in out
    print(f"macro_expansion {out}")
    print("macro_expansion self-tests passed")
