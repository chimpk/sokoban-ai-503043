from math import inf

from ..core.state import GameState, MapStaticData
from ..search.heuristic import SokobanHeuristic
from ..search.ucs import uniform_cost_search


def verify_admissibility(states: list[GameState], static_data: MapStaticData, heuristic: SokobanHeuristic) -> dict:
    checked = 0
    unsolved = 0
    violations = 0

    for state in states:
        result = uniform_cost_search(state, static_data)
        if not state.is_goal(static_data) and not result.actions:
            unsolved += 1
            continue

        checked += 1
        h_value = heuristic.evaluate(state)
        optimal_cost = result.total_cost
        if h_value > optimal_cost + 1e-9:
            violations += 1

    violation_rate = (violations / checked) if checked else 0.0
    return {
        "states_requested": len(states),
        "states_checked": checked,
        "states_unsolved": unsolved,
        "violations": violations,
        "violation_rate": violation_rate,
    }


def verify_consistency(states: list[GameState], static_data: MapStaticData, heuristic: SokobanHeuristic) -> dict:
    checked = 0
    violations = 0

    for state in states:
        for _, next_state, step_cost in state.get_successors(static_data):
            checked += 1
            h_current = heuristic.evaluate(state)
            h_next = heuristic.evaluate(next_state)
            if h_current > step_cost + h_next + 1e-9:
                violations += 1

    violation_rate = (violations / checked) if checked else 0.0
    return {
        "transitions_checked": checked,
        "violations": violations,
        "violation_rate": violation_rate,
    }
