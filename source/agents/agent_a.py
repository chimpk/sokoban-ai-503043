from __future__ import annotations

import random
import time

import numpy as np
from scipy.optimize import linear_sum_assignment

from source.agents.base_agent import BaseAgent
from source.agents.pathing import Navigator, StuckBreaker
from source.competitive.state import CompetitiveState

BIG = 10**6


class AgentA(BaseAgent):
    """Agent A dùng ghép Hungarian để phân công hộp-đích và A* để đi/đẩy."""

    def __init__(self):
        super().__init__("A", "Hungarian + A*")
        self.rng = random.Random(1)
        self.breaker = StuckBreaker(self.rng)

    def get_next_action(self, state: CompetitiveState, remaining_time_ms: float) -> str:
        me, opp = state.agent_a_pos, state.agent_b_pos
        if remaining_time_ms <= 1:
            return "Wait"
        if self.breaker.should_randomize(me):
            return self.breaker.remember(
                me, Navigator(state).safe_step(me, opp, self.rng)
            )
        return self.breaker.remember(me, self._decide(state, remaining_time_ms))

    def _decide(self, state: CompetitiveState, remaining_time_ms: float) -> str:
        # Giữ khoảng đệm cho việc trả kết quả về engine.
        deadline = time.perf_counter() + max(0.0, min(remaining_time_ms, 850.0)) / 1000.0
        nav = Navigator(state)
        me, opp = state.agent_a_pos, state.agent_b_pos

        # Hộp tự do và hộp đang thuộc B đều là mục tiêu tiềm năng.
        # Hộp đã ghi điểm cho A không cần được A đẩy lại.
        boxes = [
            b for b in nav.boxes
            if b not in nav.goals or state.box_owners.get(b) == "B"
        ]
        goals = [g for g in nav.goals if g not in nav.boxes]
        if not boxes or not goals:
            return nav.safe_step(me, opp, self.rng)

        cost = np.full((len(boxes), len(goals)), BIG, dtype=float)
        routes: dict[tuple[int, int], list[str]] = {}

        for i, box in enumerate(boxes):
            if time.perf_counter() >= deadline:
                break
            plans = nav.push_plans(box, goals, deadline=deadline)
            for j, goal in enumerate(goals):
                if time.perf_counter() >= deadline:
                    break
                pushes = plans.get(goal)
                if not pushes:
                    continue
                actions = nav.approach(me, box, pushes, opp, deadline=deadline)
                if actions:
                    cost[i, j] = len(actions)
                    routes[i, j] = actions

        if time.perf_counter() >= deadline or not routes:
            # Không trả một phần kế hoạch có thể đã hết ngân sách; hành động an toàn.
            return nav.safe_step(me, opp, self.rng)

        rows, cols = linear_sum_assignment(cost)
        pairs = [
            (cost[r, c], r, c)
            for r, c in zip(rows, cols)
            if cost[r, c] < BIG and (r, c) in routes
        ]
        if not pairs:
            return nav.safe_step(me, opp, self.rng)

        _, r, c = min(pairs)
        route = routes[(r, c)]
        return route[0] if route else nav.safe_step(me, opp, self.rng)
