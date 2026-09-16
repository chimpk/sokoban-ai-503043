from ..core.state import GameState, MapStaticData
from .ucs import SearchResult
from .heuristic import SokobanHeuristic

def a_star_search(
    initial_state: GameState,
    static_data: MapStaticData,
    heuristic: SokobanHeuristic
) -> SearchResult:
    """
    Cài đặt thuật toán A* Search (R2): f(n) = g(n) + h(n).
    """
    # TODO: Member 2 implement A*
    pass
