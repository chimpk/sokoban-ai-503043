from __future__ import annotations

import random
import time

from source.agents.base_agent import BaseAgent
from source.agents.pathing import MOVES, Navigator, StuckBreaker
from source.competitive.state import CompetitiveState

DISRUPT_RANGE = 14   # chỉ phá hộp của A nếu tốn không quá ngần này bước
STEAL_BONUS = 4      # cướp hộp của A rồi đặt vào goal khác: B +1 và A -1, nên ưu tiên hơn


class AgentB(BaseAgent):
    """
    Agent B: Greedy Best-First Search + chiến thuật cướp hộp.
    1) Xét mọi hộp chưa có chủ và cả hộp A đang giữ trên goal; với mỗi hộp tìm goal trống
       có kế hoạch đẩy thực hiện được. Hộp của A được trừ STEAL_BONUS vào chi phí vì cướp
       thành công làm A mất 1 điểm và B được 1 điểm.
    2) Chọn cặp có chi phí nhỏ nhất (tham lam) rồi đi đẩy.
    3) Nếu không có kế hoạch nào, đẩy tạm hộp của A ra khỏi goal (A mất điểm).
    Đường đi được tìm bằng GBFS (chỉ dùng h), nhanh nhưng không cần tối ưu.
    """

    def __init__(self):
        super().__init__("B", "Greedy Best-First + Steal")
        self.rng = random.Random(2)
        self.breaker = StuckBreaker(self.rng)

    def get_next_action(self, state: CompetitiveState, remaining_time_ms: float) -> str:
        me, opp = state.agent_b_pos, state.agent_a_pos
        if self.breaker.should_randomize(me):
            return self.breaker.remember(me, Navigator(state).safe_step(me, opp, self.rng))
        return self.breaker.remember(me, self._decide(state, remaining_time_ms))

    def _decide(self, state: CompetitiveState, remaining_time_ms: float) -> str:
        deadline = time.perf_counter() + min(remaining_time_ms, 850.0) / 1000.0
        nav = Navigator(state)
        me, opp = state.agent_b_pos, state.agent_a_pos
        best = self._score(state, nav, me, opp, deadline)
        if best is None:
            best = self._push_off(state, nav, me, opp, deadline)
        return best[0] if best else nav.safe_step(me, opp, self.rng)

    def _score(self, state, nav, me, opp, deadline):
        goals = [g for g in nav.goals if g not in nav.boxes]
        best, best_key = None, None
        for box in nav.boxes:
            stealing = state.box_owners.get(box) == "A"
            if box in nav.goals and not stealing:
                continue
            for plan in nav.push_plans(box, goals).values():
                if time.perf_counter() > deadline:
                    return best
                actions = nav.approach(me, box, plan, opp, greedy=True)
                if not actions:
                    continue
                key = len(actions) - (STEAL_BONUS if stealing else 0)
                if best_key is None or key < best_key:
                    best, best_key = actions, key
        return best

    def _push_off(self, state, nav, me, opp, deadline):
        """Dự phòng: đẩy hộp của A ra khỏi goal sang bất kỳ ô trống nào."""
        best = None
        for box, owner in state.box_owners.items():
            if owner != "A":
                continue
            for action, (dr, dc) in MOVES.items():
                dest = (box[0] + dr, box[1] + dc)
                if not nav.free(dest) or dest in nav.boxes or time.perf_counter() > deadline:
                    continue
                actions = nav.approach(me, box, [action], opp, greedy=True)
                if actions and len(actions) <= DISRUPT_RANGE and (best is None or len(actions) < len(best)):
                    best = actions
        return best
