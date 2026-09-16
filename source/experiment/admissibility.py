from ..core.state import GameState, MapStaticData
from ..search.heuristic import SokobanHeuristic

def verify_admissibility(states: list[GameState], static_data: MapStaticData, heuristic: SokobanHeuristic) -> dict:
    """
    Kiểm tra tính Admissible: h(n) <= h*(n) với h*(n) là cost UCS (R4).
    Trả về: thống kê số trạng thái kiểm tra, số lần vi phạm, tỉ lệ vi phạm.
    """
    # TODO: Member 2 implement
    pass

def verify_consistency(states: list[GameState], static_data: MapStaticData, heuristic: SokobanHeuristic) -> dict:
    """
    Kiểm tra tính Consistent: h(n) <= c(n, a, n') + h(n') với mọi bước chuyển hợp lệ (R4).
    Trả về: thống kê số bước chuyển kiểm tra, số lần vi phạm, tỉ lệ vi phạm.
    """
    # TODO: Member 2 implement
    pass
