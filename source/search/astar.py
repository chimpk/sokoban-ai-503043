import heapq
import time
from math import inf, isinf

from ..core.state import GameState, MapStaticData
from .heuristic import SokobanHeuristic
from .ucs import SearchResult


def a_star_search(
    initial_state: GameState,
    static_data: MapStaticData,
    heuristic: SokobanHeuristic
) -> SearchResult:

    start_time = time.perf_counter()
    frontier: list[tuple[float, int, int, GameState]] = []
    counter = 0
    initial_h = heuristic.evaluate(initial_state)
    if isinf(initial_h):
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        return SearchResult([], 0, {
            "elapsed_ms": elapsed_ms,
            "nodes_expanded": 0,
            "nodes_generated": 1,
            "max_frontier_size": 0,
        })

    heapq.heappush(frontier, (initial_h, 0, counter, initial_state))
    counter += 1

    g_score: dict[GameState, float] = {initial_state: 0.0}
    parent: dict[GameState, tuple[GameState | None, object | None]] = {initial_state: (None, None)}
    expanded = 0
    generated = 1
    max_frontier = 1

    while frontier:
        f_score, g_cost, _, state = heapq.heappop(frontier)
        if g_cost > g_score.get(state, inf):
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
            return SearchResult(actions, int(g_cost), metrics)

        for action, next_state, step_cost in state.get_successors(static_data):
            tentative_cost = g_cost + step_cost
            if tentative_cost < g_score.get(next_state, inf):
                g_score[next_state] = tentative_cost
                parent[next_state] = (state, action)
                generated += 1
                h_value = heuristic.evaluate(next_state)
                if isinf(h_value):
                    continue
                heapq.heappush(frontier, (tentative_cost + h_value, tentative_cost, counter, next_state))
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
