from __future__ import annotations

import random
import time

import numpy as np
from scipy.optimize import linear_sum_assignment

from source.agents.base_agent import BaseAgent
from source.agents.pathing import Navigator, StuckBreaker
from source.competitive.state import CompetitiveState

BIG = 10 ** 6


class AgentA(BaseAgent):
    """
    Agent A: phân công Hungarian + tìm đường A*.
    Ý tưởng: lập ma trận chi phí (hộp i -> goal j) = quãng đường đi tới vị trí đẩy
    + số lần đẩy; Hungarian chọn cách ghép hộp-goal có tổng chi phí nhỏ nhất
    (tránh 2 hộp tranh cùng 1 goal); agent thực hiện cặp rẻ nhất trước.
    """

    def __init__(self):
        super().__init__("A", "Hungarian + A*")
        self.rng = random.Random(1)
        self.breaker = StuckBreaker(self.rng)

    def get_next_action(self, state: CompetitiveState, remaining_time_ms: float) -> str:
        me, opp = state.agent_a_pos, state.agent_b_pos
        if self.breaker.should_randomize(me):
            return self.breaker.remember(me, Navigator(state).safe_step(me, opp, self.rng))
        return self.breaker.remember(me, self._decide(state, remaining_time_ms))

    def _decide(self, state: CompetitiveState, remaining_time_ms: float) -> str:
        deadline = time.perf_counter() + min(remaining_time_ms, 850.0) / 1000.0
        nav = Navigator(state)
        me, opp = state.agent_a_pos, state.agent_b_pos
        boxes = [b for b in nav.boxes if b not in nav.goals]
        goals = [g for g in nav.goals if g not in nav.boxes]
        if not boxes or not goals:
            return nav.safe_step(me, opp, self.rng)

        cost = np.full((len(boxes), len(goals)), BIG, dtype=float)
        route = {}
        for i, box in enumerate(boxes):
            plans = nav.push_plans(box, goals)
            for j, goal in enumerate(goals):
                if time.perf_counter() > deadline:
                    break
                if goal in plans:
                    actions = nav.approach(me, box, plans[goal], opp)
                    if actions:
                        cost[i, j], route[i, j] = len(actions), actions

        rows, cols = linear_sum_assignment(cost)
        pairs = [(cost[r, c], r, c) for r, c in zip(rows, cols) if cost[r, c] < BIG]
        if not pairs:
            return nav.safe_step(me, opp, self.rng)
        _, r, c = min(pairs)
        return route[r, c][0]
