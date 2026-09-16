class CompetitiveState:
    """
    Biểu diễn trạng thái của trận đấu đối kháng giữa 2 Agents (R6).
    Xem quy ước biến tại: docs/14_Shared_Variables_Dictionary.md
    """
    def __init__(
        self,
        agent_a_pos: tuple[int, int],
        agent_b_pos: tuple[int, int],
        boxes_a: set[tuple[int, int]] | frozenset[tuple[int, int]],
        boxes_b: set[tuple[int, int]] | frozenset[tuple[int, int]],
        goals: set[tuple[int, int]] | frozenset[tuple[int, int]],
        max_steps: int,
        current_step: int = 0
    ):
        self.agent_a_pos: tuple[int, int] = agent_a_pos
        self.agent_b_pos: tuple[int, int] = agent_b_pos
        self.boxes_a: frozenset[tuple[int, int]] = frozenset(boxes_a)
        self.boxes_b: frozenset[tuple[int, int]] = frozenset(boxes_b)
        self.goals: frozenset[tuple[int, int]] = frozenset(goals)
        self.max_steps: int = max_steps
        self.current_step: int = current_step

    def get_scores(self) -> tuple[int, int]:
        """Trả về (score_a, score_b) - số hộp mỗi agent đã đưa vào goal."""
        # TODO: Member 3 implement
        pass

    def is_game_over(self) -> bool:
        """Kiểm tra trận đấu đã hoàn thành (hết n bước hoặc toàn bộ hộp vào đích)."""
        # TODO: Member 3 implement
        pass
