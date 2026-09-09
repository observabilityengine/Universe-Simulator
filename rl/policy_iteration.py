"""Policy iteration for finite MDPs."""
from __future__ import annotations
from typing import List, Tuple
from .mdp import MDP


def policy_evaluation(mdp: MDP, policy: List[int], theta: float = 1e-6) -> List[float]:
    V = [0.0] * mdp.n_states
    while True:
        delta = 0.0
        for s in range(mdp.n_states):
            a = policy[s]
            v = sum(p * (r + mdp.gamma * V[ns]) for p, ns, r in mdp.transitions(s, a))
            delta = max(delta, abs(v - V[s]))
            V[s] = v
        if delta < theta:
            break
    return V


def policy_iteration(mdp: MDP, max_iter: int = 100) -> Tuple[List[float], List[int]]:
    policy = [0] * mdp.n_states
    for _ in range(max_iter):
        V = policy_evaluation(mdp, policy)
        stable = True
        for s in range(mdp.n_states):
            old = policy[s]
            q = [sum(p * (r + mdp.gamma * V[ns]) for p, ns, r in mdp.transitions(s, a)) for a in range(mdp.n_actions)]
            policy[s] = max(range(mdp.n_actions), key=lambda a: q[a])
            if policy[s] != old:
                stable = False
        if stable:
            break
    return V, policy


if __name__ == "__main__":
    from .mdp import gridworld_mdp
    m = gridworld_mdp(3)
    V, pi = policy_iteration(m)
    assert len(pi) == 9
    print(f"policy_iteration V0={V[0]:.3f}")
    print("policy_iteration self-tests passed")
