"""Minimal SQL parser for SELECT/INSERT/CREATE TABLE."""
from __future__ import annotations
from typing import Any, Dict, List, Optional
import re


def parse_sql(sql: str) -> Dict[str, Any]:
    sql = sql.strip().rstrip(";")
    upper = sql.upper()
    if upper.startswith("SELECT"):
        m = re.match(r"SELECT\s+(.+?)\s+FROM\s+(\w+)(?:\s+WHERE\s+(.+))?$", sql, re.I)
        if not m:
            raise ValueError("bad SELECT")
        cols = [c.strip() for c in m.group(1).split(",")]
        return {"type": "select", "columns": cols, "table": m.group(2), "where": m.group(3)}
    if upper.startswith("INSERT"):
        m = re.match(r"INSERT\s+INTO\s+(\w+)\s*\((.+?)\)\s*VALUES\s*\((.+?)\)$", sql, re.I)
        if not m:
            raise ValueError("bad INSERT")
        cols = [c.strip() for c in m.group(2).split(",")]
        vals = [v.strip().strip("'\"") for v in m.group(3).split(",")]
        return {"type": "insert", "table": m.group(1), "columns": cols, "values": vals}
    if upper.startswith("CREATE TABLE"):
        m = re.match(r"CREATE\s+TABLE\s+(\w+)\s*\((.+)\)$", sql, re.I)
        if not m:
            raise ValueError("bad CREATE")
        cols = [c.strip() for c in m.group(2).split(",")]
        return {"type": "create", "table": m.group(1), "columns": cols}
    raise ValueError(f"unsupported: {sql}")


if __name__ == "__main__":
    p = parse_sql("SELECT a, b FROM users WHERE id = 1")
    assert p["type"] == "select" and p["table"] == "users"
    p2 = parse_sql("INSERT INTO t (x, y) VALUES (1, 'hi')")
    assert p2["type"] == "insert"
    print(f"sql_parser {p}")
    print("sql_parser self-tests passed")
