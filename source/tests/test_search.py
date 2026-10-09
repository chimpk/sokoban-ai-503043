import unittest

from source.core.state import GameState, MapStaticData
from source.experiment.admissibility import verify_admissibility, verify_consistency
from source.search.astar import a_star_search
from source.search.heuristic import SokobanHeuristic
from source.search.ucs import uniform_cost_search


def enclosed_map(
    height: int,
    width: int,
    interior_walls: set[tuple[int, int]],
    goals: set[tuple[int, int]],
) -> MapStaticData:
    border = {
        (row, col)
        for row in range(height)
        for col in range(width)
        if row == 0 or row == height - 1 or col == 0 or col == width - 1
    }
    return MapStaticData(border | interior_walls, goals, height, width)


class TestSearch(unittest.TestCase):
    def test_maze_distance_and_matching(self):
        static_data = enclosed_map(
            5,
            7,
            {(1, 3), (2, 3)},
            {(1, 1), (1, 5)},
        )
        state = GameState((3, 1), {(2, 1), (2, 2)})

        heuristic = SokobanHeuristic(static_data)

        self.assertEqual(heuristic.evaluate(state), 7)

    def test_corner_deadlock_and_goal_corner(self):
        static_data = enclosed_map(5, 5, set(), {(3, 3)})
        heuristic = SokobanHeuristic(static_data)

        self.assertEqual(heuristic.evaluate(GameState((2, 2), {(1, 1)})), float("inf"))
        self.assertEqual(heuristic.evaluate(GameState((2, 2), {(3, 3)})), 0)

    def test_astar_optimality(self):
        static_data = enclosed_map(5, 6, set(), {(2, 4)})
        initial = GameState((2, 2), {(2, 3)})
        heuristic = SokobanHeuristic(static_data)

        astar_result = a_star_search(initial, static_data, heuristic)
        ucs_result = uniform_cost_search(initial, static_data)

        self.assertTrue(astar_result.actions)
        self.assertEqual(astar_result.total_cost, ucs_result.total_cost)
        self.assertEqual(len(astar_result.actions), astar_result.total_cost)

    def test_unsolvable_map(self):
        static_data = enclosed_map(5, 5, set(), {(3, 3)})
        initial = GameState((2, 2), {(1, 1)})
        heuristic = SokobanHeuristic(static_data)

        astar_result = a_star_search(initial, static_data, heuristic)
        ucs_result = uniform_cost_search(initial, static_data)

        self.assertFalse(astar_result.actions)
        self.assertFalse(ucs_result.actions)
        self.assertEqual(astar_result.metrics["nodes_expanded"], 0)

    def test_admissibility_skips_unsolvable_samples(self):
        static_data = enclosed_map(5, 6, set(), {(2, 4)})
        heuristic = SokobanHeuristic(static_data)
        goal_state = GameState((2, 2), {(2, 4)})
        solvable_state = GameState((2, 2), {(2, 3)})
        deadlocked_state = GameState((2, 2), {(1, 1)})

        report = verify_admissibility(
            [goal_state, solvable_state, deadlocked_state], static_data, heuristic
        )

        self.assertEqual(report["states_requested"], 3)
        self.assertEqual(report["states_checked"], 2)
        self.assertEqual(report["states_unsolved"], 1)
        self.assertEqual(report["violations"], 0)

    def test_consistency_on_sample_transitions(self):
        static_data = enclosed_map(5, 6, set(), {(2, 4)})
        state = GameState((2, 2), {(2, 3)})
        report = verify_consistency(
            [state], static_data, SokobanHeuristic(static_data)
        )

        self.assertGreater(report["transitions_checked"], 0)
        self.assertEqual(report["violations"], 0)


if __name__ == "__main__":
    unittest.main()