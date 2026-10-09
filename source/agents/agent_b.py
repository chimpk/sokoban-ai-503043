from __future__ import annotations

import random
import time

from source.agents.base_agent import BaseAgent
from source.agents.pathing import MOVES, Navigator, StuckBreaker
from source.competitive.state import CompetitiveState

# Tài liệu thiết kế nêu ưu tiên cướp hộp nếu khoảng cách không quá 4 bước.
STEAL_PRIORITY_RANGE = 4
STEAL_BONUS = 4


class AgentB(BaseAgent):
    """Agent B dùng Greedy Best-First Search và ưu tiên phá điểm của Agent A."""

    def __init__(self):
        super().__init__("B", "Greedy Best-First + Disruption")
        self.rng = random.Random(2)
        self.breaker = StuckBreaker(self.rng)

    def get_next_action(self, state: CompetitiveState, remaining_time_ms: float) -> str:
        me, opp = state.agent_b_pos, state.agent_a_pos
        if remaining_time_ms <= 1:
            return "Wait"
        if self.breaker.should_randomize(me):
            return self.breaker.remember(
                me, Navigator(state).safe_step(me, opp, self.rng)
            )
        return self.breaker.remember(me, self._decide(state, remaining_time_ms))

    def _decide(self, state: CompetitiveState, remaining_time_ms: float) -> str:
        deadline = time.perf_counter() + max(0.0, min(remaining_time_ms, 850.0)) / 1000.0
        nav = Navigator(state)
        me, opp = state.agent_b_pos, state.agent_a_pos
        best = self._score(state, nav, me, opp, deadline)
        if best is None and time.perf_counter() < deadline:
            best = self._push_off(state, nav, me, opp, deadline)
        return best[0] if best else nav.safe_step(me, opp, self.rng)

    def _score(self, state, nav, me, opp, deadline):
        goals = [g for g in nav.goals if g not in nav.boxes]
        best, best_key = None, None

        for box in nav.boxes:
            if time.perf_counter() >= deadline:
                break
            stealing = state.box_owners.get(box) == "A"
            if box in nav.goals and not stealing:
                continue

            plans = nav.push_plans(box, goals, deadline=deadline)
            for plan in plans.values():
                if time.perf_counter() >= deadline:
                    break
                actions = nav.approach(
                    me, box, plan, opp, greedy=True, deadline=deadline
                )
                if not actions:
                    continue

                # Chỉ cộng ưu tiên lớn cho hộp A ở gần; vẫn có thể cướp xa hơn
                # nếu đó là lựa chọn khả thi tốt nhất.
                bonus = STEAL_BONUS if stealing and len(actions) <= STEAL_PRIORITY_RANGE else 0
                key = len(actions) - bonus
                if best_key is None or key < best_key:
                    best, best_key = actions, key

        return best

    def _push_off(self, state, nav, me, opp, deadline):
        """Nếu không có đường ghi điểm, thử đẩy hộp A rời khỏi đích."""
        best = None
        for box, owner in state.box_owners.items():
            if time.perf_counter() >= deadline:
                break
            if owner != "A":
                continue
            for action, (dr, dc) in MOVES.items():
                if time.perf_counter() >= deadline:
                    break
                dest = (box[0] + dr, box[1] + dc)
                if not nav.free(dest) or dest in nav.boxes:
                    continue
                actions = nav.approach(
                    me, box, [action], opp, greedy=True, deadline=deadline
                )
                if actions and (best is None or len(actions) < len(best)):
                    best = actions
        return best
