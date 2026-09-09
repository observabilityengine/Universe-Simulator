"""Binary tuple serialization."""
from __future__ import annotations
from typing import Any, List, Tuple
import struct


class TupleSchema:
    def __init__(self, fields: List[Tuple[str, str]]):
        self.fields = fields

    def serialize(self, values: List[Any]) -> bytes:
        parts = []
        for (_, typ), val in zip(self.fields, values):
            if typ == "int":
                parts.append(struct.pack("<i", int(val)))
            elif typ == "float":
                parts.append(struct.pack("<d", float(val)))
            elif typ == "str":
                b = str(val).encode("utf-8")
                parts.append(struct.pack("<H", len(b)) + b)
        return b"".join(parts)

    def deserialize(self, data: bytes) -> List[Any]:
        values = []
        offset = 0
        for _, typ in self.fields:
            if typ == "int":
                values.append(struct.unpack_from("<i", data, offset)[0])
                offset += 4
            elif typ == "float":
                values.append(struct.unpack_from("<d", data, offset)[0])
                offset += 8
            elif typ == "str":
                length = struct.unpack_from("<H", data, offset)[0]
                offset += 2
                values.append(data[offset : offset + length].decode("utf-8"))
                offset += length
        return values


if __name__ == "__main__":
    schema = TupleSchema([("id", "int"), ("name", "str"), ("score", "float")])
    raw = schema.serialize([1, "alice", 3.14])
    vals = schema.deserialize(raw)
    assert vals[0] == 1 and vals[1] == "alice" and abs(vals[2] - 3.14) < 1e-6
    print(f"tuple_format {vals}")
    print("tuple_format self-tests passed")
