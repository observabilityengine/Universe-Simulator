"""Value iteration for finite MDPs."""
from __future__ import annotations
from typing import List, Tuple
from .mdp import MDP


def value_iteration(mdp: MDP, theta: float = 1e-6, max_iter: int = 1000) -> Tuple[List[float], List[int]]:
    V = [0.0] * mdp.n_states
    for _ in range(max_iter):
        delta = 0.0
        for s in range(mdp.n_states):
            q_values = []
            for a in range(mdp.n_actions):
                q = sum(p * (r + mdp.gamma * V[ns]) for p, ns, r in mdp.transitions(s, a))
                q_values.append(q)
            best = max(q_values) if q_values else 0.0
            delta = max(delta, abs(best - V[s]))
            V[s] = best
        if delta < theta:
            break
    policy = []
    for s in range(mdp.n_states):
        q_values = [sum(p * (r + mdp.gamma * V[ns]) for p, ns, r in mdp.transitions(s, a)) for a in range(mdp.n_actions)]
        policy.append(max(range(mdp.n_actions), key=lambda a: q_values[a]) if q_values else 0)
    return V, policy


if __name__ == "__main__":
    from .mdp import gridworld_mdp
    m = gridworld_mdp(3)
    V, pi = value_iteration(m)
    assert V[-1] >= V[0]
    print(f"value_iteration V_goal={V[-1]:.3f}")
    print("value_iteration self-tests passed")
