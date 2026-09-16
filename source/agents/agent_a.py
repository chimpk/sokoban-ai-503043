class AgentA:
    """
    Agent A - Competitive Mode (Requirement 7 & 8).
    File mã nguồn độc lập do Member 3 phụ trách.
    Có thể mang file này đi thi đấu với các nhóm khác.

    Yêu cầu:
      - Thời gian phản hồi: <= 1000 ms / bước đi.
      - Trả về 1 trong 4 hành động: 'North', 'South', 'West', 'East'.
    """
    def __init__(self, name: str = "AgentA"):
        self.name = name

    def choose_action(self, state, time_limit_ms: int = 1000) -> str:
        """
        Nhận vào trạng thái bàn cờ hiện tại, trả về hành động của Agent A.
        """
        # TODO: Member 3 implement AI algorithm (GBFS / A* / BFS...)
        return "North"
