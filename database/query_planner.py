"""Simple cost-based query planner for sequential vs index scan."""
from __future__ import annotations
from typing import Dict


def estimate_cost(table_rows: int, selectivity: float = 1.0, has_index: bool = False, index_height: int = 3) -> Dict[str, float]:
    seq_cost = table_rows * 1.0
    result_rows = table_rows * selectivity
    index_cost = index_height + result_rows * 2.0 if has_index else float("inf")
    return {
        "seq_scan": seq_cost,
        "index_scan": index_cost,
        "chosen": "index_scan" if index_cost < seq_cost else "seq_scan",
        "cost": min(seq_cost, index_cost),
    }


def plan_select(table_rows: int, where_selectivity: float, indexed_columns: set, filter_col: str = None) -> str:
    has_idx = filter_col in indexed_columns if filter_col else False
    c = estimate_cost(table_rows, where_selectivity, has_idx)
    return c["chosen"]


if __name__ == "__main__":
    c = estimate_cost(10000, 0.01, has_index=True)
    assert c["chosen"] == "index_scan"
    c2 = estimate_cost(100, 0.9, has_index=True)
    assert c2["chosen"] == "seq_scan"
    print(f"query_planner {c}")
    print("query_planner self-tests passed")
