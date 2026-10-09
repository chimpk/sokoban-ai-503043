import heapq
import time
from math import inf

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

    start_time = time.perf_counter()
    frontier: list[tuple[int, int, GameState]] = []
    counter = 0
    heapq.heappush(frontier, (0, counter, initial_state))
    counter += 1

    g_cost: dict[GameState, int] = {initial_state: 0}
    parent: dict[GameState, tuple[GameState | None, object | None]] = {initial_state: (None, None)}
    expanded = 0
    generated = 1
    max_frontier = 1

    while frontier:
        current_cost, _, state = heapq.heappop(frontier)
        if current_cost > g_cost.get(state, inf):
            continue

        expanded += 1
        if state.is_goal(static_data):
            actions: list[str] = []
            current = state
            while parent[current][0] is not None:
                prev_state, action = parent[current]
                actions.append(action.value if hasattr(action, 'value') else str(action))
                current = prev_state
            actions.reverse()

            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            metrics = {
                "elapsed_ms": elapsed_ms,
                "nodes_expanded": expanded,
                "nodes_generated": generated,
                "max_frontier_size": max_frontier,
            }
            return SearchResult(actions, current_cost, metrics)

        for action, next_state, step_cost in state.get_successors(static_data):
            tentative_cost = current_cost + step_cost
            if tentative_cost < g_cost.get(next_state, inf):
                g_cost[next_state] = tentative_cost
                parent[next_state] = (state, action)
                generated += 1
                heapq.heappush(frontier, (tentative_cost, counter, next_state))
                counter += 1
                if len(frontier) > max_frontier:
                    max_frontier = len(frontier)

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    metrics = {
        "elapsed_ms": elapsed_ms,
        "nodes_expanded": expanded,
        "nodes_generated": generated,
        "max_frontier_size": max_frontier,
    }
    return SearchResult([], 0, metrics)
