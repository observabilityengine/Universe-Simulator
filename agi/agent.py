"""
Module 5 – Agent Core
Autonomous agent with observe → plan → act loop.
Fully functional. Original implementation.
"""

from __future__ import annotations

import time
import uuid
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class Observation:
    timestamp: float
    data: Dict[str, Any]


@dataclass
class Action:
    name: str
    params: Dict[str, Any] = field(default_factory=dict)
    score: float = 0.0


class Agent:
    def __init__(self, name: str):
        self.id = str(uuid.uuid4())[:8]
        self.name = name
        self.sensors: Dict[str, Callable[[], Any]] = {}
        self.actuators: Dict[str, Callable[..., Any]] = {}
        self.goals: List[str] = []
        self.running = False
        self.cycle_count = 0
        self.last_action: Optional[Action] = None
        self.memory: List[Dict] = []

    def add_sensor(self, name: str, func: Callable[[], Any]) -> None:
        self.sensors[name] = func

    def add_actuator(self, name: str, func: Callable[..., Any]) -> None:
        self.actuators[name] = func

    def add_goal(self, goal: str) -> None:
        if goal not in self.goals:
            self.goals.append(goal)

    def observe(self) -> Observation:
        data = {}
        for name, sensor in self.sensors.items():
            try:
                data[name] = sensor()
            except Exception as e:
                data[name] = {"error": str(e)}
        obs = Observation(timestamp=time.time(), data=data)
        self.memory.append({"type": "observation", "data": data})
        return obs

    def plan(self, obs: Observation) -> Optional[Action]:
        candidates: List[Action] = []
        if "status" in self.actuators:
            candidates.append(Action("status", score=0.1))
        for goal in self.goals:
            if goal in self.actuators:
                candidates.append(Action(goal, score=1.0))
        if not candidates:
            return None
        candidates.sort(key=lambda a: a.score, reverse=True)
        return candidates[0]

    def act(self, action: Action) -> Any:
        if action.name not in self.actuators:
            raise KeyError(f"No actuator for action '{action.name}'")
        result = self.actuators[action.name](**action.params)
        self.memory.append({"type": "action", "name": action.name, "result": str(result)[:200]})
        self.last_action = action
        return result

    def cycle(self) -> Dict[str, Any]:
        self.cycle_count += 1
        obs = self.observe()
        action = self.plan(obs)
        result = None
        if action is not None:
            result = self.act(action)
        return {"cycle": self.cycle_count, "observation": obs.data, "action": action.name if action else None, "result": result}

    def run(self, cycles: int = 10) -> List[Dict[str, Any]]:
        self.running = True
        history = []
        for _ in range(cycles):
            if not self.running:
                break
            history.append(self.cycle())
        self.running = False
        return history


if __name__ == "__main__":
    print("Testing Agent Core...")
    agent = Agent("explorer")
    state = {"energy": 100, "position": 0}
    agent.add_sensor("energy", lambda: state["energy"])
    agent.add_sensor("position", lambda: state["position"])
    agent.add_actuator("status", lambda: f"energy={state['energy']} pos={state['position']}")
    agent.add_actuator("move", lambda: state.update({"position": state["position"] + 1}) or state["position"])
    agent.add_goal("move")
    history = agent.run(cycles=5)
    for h in history:
        print(f"  cycle {h['cycle']}: action={h['action']} result={h['result']}")
    print("Agent Core module OK.")
