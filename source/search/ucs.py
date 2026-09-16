from ..core.state import GameState, MapStaticData

class SearchResult:
    """
    Kết quả tìm kiếm chứa:
      - actions: danh sách tên hành động ('North', 'East', ...)
      - total_cost: tổng chi phí đường đi
      - metrics: thời gian chạy, số node sinh ra, số node duyệt, độ lớn frontier tối đa
    """
    def __init__(self, actions: list[str], total_cost: int, metrics: dict):
        self.actions = actions
        self.total_cost = total_cost
        self.metrics = metrics

def uniform_cost_search(initial_state: GameState, static_data: MapStaticData) -> SearchResult:
    """
    Cài đặt thuật toán Uniform-Cost Search (UCS) cho Sokoban (R2).
    """
    # TODO: Member 1 implement UCS
    pass
