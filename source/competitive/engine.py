from __future__ import annotations

import time
from typing import Optional

from .conflict import ConflictResolver, DIRECTIONS
from .state import CompetitiveState


class TimeoutGuard:
    """
    Bảo vệ giới hạn 1000 ms / quyết định (đề, Requirement 7).
    - Agent được báo SOFT_LIMIT_MS còn lại và phải TỰ dừng tìm kiếm trước mốc đó.
    - Guard không ngắt cưỡng bức: nếu agent chạy quá HARD_LIMIT_MS hoặc báo lỗi
      hoặc trả hành động không hợp lệ thì hành động bị thay bằng 'Wait'.
    """
    HARD_LIMIT_MS = 1000.0
    SOFT_LIMIT_MS = 900.0

    @classmethod
    def ask(cls, agent, state: CompetitiveState) -> str:
        start = time.perf_counter()
        try:
            action = agent.get_next_action(state, cls.SOFT_LIMIT_MS)
        except Exception:
            return "Wait"
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        if elapsed_ms > cls.HARD_LIMIT_MS or action not in DIRECTIONS:
            return "Wait"
        return action


class CompetitiveEngine:
    """
    Điều phối trận đấu: lấy hành động của 2 agent từ CÙNG một trạng thái
    (đồng thời), nhờ ConflictResolver cập nhật, và lưu lịch sử để GUI tiến/lùi.
    """

    def __init__(self, initial_state: CompetitiveState, conflict_resolver: ConflictResolver,
                 agent_a=None, agent_b=None):
        self.state = initial_state
        self.resolver = conflict_resolver
        self.agent_a, self.agent_b = agent_a, agent_b
        self.history: list[CompetitiveState] = [initial_state]   # history[i] = trạng thái sau i bước
        self.actions: list[tuple[str, str]] = []

    def step(self, action_a: Optional[str] = None, action_b: Optional[str] = None) -> CompetitiveState:
        """Thực hiện 1 lượt. Nếu không truyền action thì hỏi agent (qua TimeoutGuard)."""
        if self.state.is_finished():
            return self.state
        snapshot = self.state
        if action_a is None:
            action_a = TimeoutGuard.ask(self.agent_a, snapshot)
        if action_b is None:
            action_b = TimeoutGuard.ask(self.agent_b, snapshot)
        self.state = self.resolver.resolve(snapshot, action_a, action_b)
        self.history.append(self.state)
        self.actions.append((action_a, action_b))
        return self.state

    def run(self) -> CompetitiveState:
        while not self.state.is_finished():
            self.step()
        return self.state

    def get_winner(self) -> str:
        w = self.state.winner()
        return {"A": "Agent A", "B": "Agent B"}.get(w, "Tie")
