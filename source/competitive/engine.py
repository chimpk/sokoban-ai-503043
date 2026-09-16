from .state import CompetitiveState
from .conflict import ConflictResolver

class CompetitiveEngine:
    """
    Game Engine điều phối trận đấu đối kháng (R6):
      - Vòng lặp n bước (n do người dùng nhập).
      - Thu thập action từ Agent A và Agent B đồng thời (với time limit <= 1000ms).
      - Áp dụng ConflictResolver để cập nhật trạng thái bàn cờ.
      - Xác định bên chiến thắng (Winner).
    """
    def __init__(self, initial_state: CompetitiveState, conflict_resolver: ConflictResolver):
        # TODO: Member 3 implement
        pass

    def step(self, action_a: str, action_b: str) -> CompetitiveState:
        """Thực hiện 1 lượt đi đồng thời cho cả hai agent."""
        # TODO: Member 3 implement
        pass

    def get_winner(self) -> str:
        """Trả về 'Agent A', 'Agent B', hoặc 'Tie' (Hòa)."""
        # TODO: Member 3 implement
        pass
