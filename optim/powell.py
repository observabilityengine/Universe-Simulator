"""Powell's conjugate direction method.

Complexity: O(iters * dim * line_search). Original implementation.
"""
from __future__ import annotations
from typing import Callable, List, Tuple

def powell(
    f: Callable[[List[float]], float],
    x0: List[float],
    max_iter: int = 50,
    tol: float = 1e-6,
) -> Tuple[List[float], float]:
    n = len(x0)
    x = x0[:]
    directions = [[1.0 if i==j else 0.0 for j in range(n)] for i in range(n)]
    fx = f(x)
    for _ in range(max_iter):
        x_start = x[:]
        f_start = fx
        delta = 0.0
        bi = 0
        for i in range(n):
            def line(a, i=i):
                return f([x[j] + a*directions[i][j] for j in range(n)])
            a, b = -1.0, 1.0
            for _ in range(30):
                c = b - (b-a)/1.618
                d = a + (b-a)/1.618
                if line(c) < line(d):
                    b = d
                else:
                    a = c
            a_opt = (a+b)/2
            f_new = line(a_opt)
            if f_start - f_new > delta:
                delta = f_start - f_new
                bi = i
            x = [x[j] + a_opt*directions[i][j] for j in range(n)]
            fx = f_new
        if abs(f_start - fx) < tol:
            break
        new_dir = [x[j] - x_start[j] for j in range(n)]
        directions[bi] = new_dir
    return x, fx

if __name__ == "__main__":
    def sphere(x):
        return sum(v*v for v in x)
    x, v = powell(sphere, [1.0, 2.0, -1.0], max_iter=30)
    assert v < 0.1, v
    print("powell self-tests passed")
