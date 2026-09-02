"""
Module 89 – HTTP/1.1 Request Parser
Parse request line + headers from raw bytes.
Complete implementation.
"""

from __future__ import annotations
from typing import Dict
from dataclasses import dataclass, field


@dataclass
class HTTPRequest:
    method: str
    path: str
    version: str
    headers: Dict[str, str] = field(default_factory=dict)
    body: bytes = b""


def parse_request(data: bytes) -> HTTPRequest:
    try:
        header_end = data.index(b"\r\n\r\n")
    except ValueError:
        raise ValueError("Incomplete HTTP request: no header terminator")
    header_block = data[:header_end].decode("latin-1")
    body = data[header_end + 4 :]
    lines = header_block.split("\r\n")
    if not lines:
        raise ValueError("Empty request")
    parts = lines[0].split(" ")
    if len(parts) != 3:
        raise ValueError(f"Malformed request line: {lines[0]}")
    method, path, version = parts
    headers: Dict[str, str] = {}
    for line in lines[1:]:
        if not line:
            continue
        if ":" not in line:
            raise ValueError(f"Malformed header: {line}")
        key, value = line.split(":", 1)
        headers[key.strip().lower()] = value.strip()
    if "content-length" in headers:
        length = int(headers["content-length"])
        body = body[:length]
    return HTTPRequest(method=method, path=path, version=version, headers=headers, body=body)


if __name__ == "__main__":
    print("Testing HTTP Parser...")
    raw = (
        b"POST /api/v1/data HTTP/1.1\r\n"
        b"Host: example.com\r\n"
        b"Content-Type: application/json\r\n"
        b"Content-Length: 18\r\n"
        b"\r\n"
        b'{"key": "value"}'
    )
    req = parse_request(raw)
    print(f"  Method: {req.method}")
    print(f"  Path: {req.path}")
    print(f"  Version: {req.version}")
    print(f"  Headers: {req.headers}")
    print(f"  Body: {req.body}")
    print("HTTP Parser module OK.")
