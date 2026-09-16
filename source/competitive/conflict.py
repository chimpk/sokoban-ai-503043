from .state import CompetitiveState

class ConflictResolver:
    """
    Xử lý xung đột khi 2 Agent thực hiện hành động đồng thời (Simultaneous Actions - R6):
      - Cùng đi vào 1 ô đích -> Cả hai bị chặn đứng.
      - Đi xuyên qua nhau (swap positions) -> Cả hai bị chặn.
      - Cùng đẩy 1 hộp -> Cả hai bị chặn.
      - Đẩy hộp vào vị trí agent đối thủ -> Bị chặn nếu đối thủ không di chuyển đi nơi khác.
    """
    def __init__(self, walls: set[tuple[int, int]]):
        # TODO: Member 3 implement
        pass

    def resolve(
        self,
        current_state: CompetitiveState,
        action_a: str,
        action_b: str
    ) -> CompetitiveState:
        """
        Nhận vào 2 hành động đồng thời của Agent A và Agent B.
        Áp dụng quy tắc xử lý xung đột và trả về CompetitiveState mới.
        """
        # TODO: Member 3 implement
        pass
