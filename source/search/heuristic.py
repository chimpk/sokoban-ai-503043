from ..core.state import GameState, MapStaticData

class SokobanHeuristic:
    """
    Heuristic cho A* (R2).
    LƯU Ý CỰC KỲ QUAN TRỌNG:
    - KHÔNG được dùng Manhattan distance.
    - KHÔNG được dùng Euclidean distance.
    """
    def __init__(self, static_data: MapStaticData):
        # TODO: Member 2 implement precomputation (ví dụ: BFS khoảng cách tĩnh từ goals)
        pass

    def evaluate(self, state: GameState) -> int:
        """
        Ước lượng chi phí từ state hiện tại tới goal.
        """
        # TODO: Member 2 implement heuristic evaluation
        pass
