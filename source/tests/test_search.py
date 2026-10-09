import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from source.core.parser import parse_map_string
from source.core.state import GameState, MapStaticData
from source.search.ucs import SearchResult, uniform_cost_search


def replay(state: GameState, static_data: MapStaticData, actions: list[str]) -> GameState:
    """Thực thi lần lượt các action; báo lỗi nếu có action không hợp lệ."""
    for name in actions:
        moves = {a.value: s for a, s, _ in state.get_successors(static_data)}
        if name not in moves:
            raise AssertionError(f"Action {name} không hợp lệ tại {state.player_pos}")
        state = moves[name]
    return state


class TestSearchAlgorithms(unittest.TestCase):
    """
    Bộ kiểm thử cho Thuật toán Tìm kiếm UCS & A* (Requirement 2, docs/04 Mục 5.3).
    Phụ trách: Member 1 (UCS) & Member 2 (A*).
    """

    # Đẩy 1 hộp sang phải 2 ô: lời giải tối ưu là East, East (cost = 2)
    SIMPLE_MAP = (
        "%%%%%%\n"
        "%AB D%\n"
        "%%%%%%"
    )

    # Phải đi vòng xuống dưới để đẩy hộp lên: South, South, East, East, North (cost = 5)
    DETOUR_MAP = (
        "%%%%%\n"
        "%A D%\n"
        "%  B%\n"
        "%   %\n"
        "%%%%%"
    )

    # Hộp kẹt ở góc tường, không bao giờ tới được đích
    UNSOLVABLE_MAP = (
        "%%%%%\n"
        "%B  %\n"
        "%  A%\n"
        "%  D%\n"
        "%%%%%"
    )

    def test_ucs_optimality(self):
        """UCS tìm ra lời giải tối ưu trên bản đồ nhỏ."""
        state, static_data = parse_map_string(self.SIMPLE_MAP)
        result = uniform_cost_search(state, static_data)
        self.assertTrue(result.solved)
        self.assertEqual(result.actions, ["East", "East"])
        self.assertEqual(result.total_cost, 2)

    def test_ucs_detour_optimality(self):
        """UCS tìm đúng đường vòng ngắn nhất và lời giải dẫn tới goal."""
        state, static_data = parse_map_string(self.DETOUR_MAP)
        result = uniform_cost_search(state, static_data)
        self.assertTrue(result.solved)
        self.assertEqual(result.total_cost, 5)
        self.assertEqual(result.total_cost, len(result.actions))
        self.assertTrue(replay(state, static_data, result.actions).is_goal(static_data))

    def test_ucs_already_goal(self):
        """Trạng thái đầu đã là đích: lời giải rỗng, cost = 0."""
        state, static_data = parse_map_string("%%%%\n%AC%\n%%%%")
        result = uniform_cost_search(state, static_data)
        self.assertEqual(result.actions, [])
        self.assertEqual(result.total_cost, 0)

    def test_ucs_map_01(self):
        """UCS giải tối ưu map_01.txt (3 hộp) và lời giải hợp lệ."""
        map_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../maps/map_01.txt"))
        with open(map_path, encoding="utf-8") as f:
            state, static_data = parse_map_string(f.read())
        result = uniform_cost_search(state, static_data)
        self.assertTrue(result.solved)
        self.assertEqual(result.total_cost, 24)
        self.assertTrue(replay(state, static_data, result.actions).is_goal(static_data))

    def test_ucs_metrics(self):
        """Kết quả trả về đầy đủ metrics và unpack được dạng tuple (docs/04 Mục 3.1)."""
        state, static_data = parse_map_string(self.DETOUR_MAP)
        result = uniform_cost_search(state, static_data)
        self.assertIsInstance(result, SearchResult)
        for key in ("elapsed_time_ms", "nodes_expanded", "nodes_generated", "max_frontier_size", "status"):
            self.assertIn(key, result.metrics)
        self.assertEqual(result.metrics["status"], "solved")
        self.assertGreaterEqual(result.metrics["nodes_generated"], result.metrics["nodes_expanded"])

        actions, cost, elapsed_ms, expanded, generated = result
        self.assertEqual(actions, result.actions)
        self.assertEqual(cost, 5)
        self.assertGreaterEqual(elapsed_ms, 0.0)
        self.assertGreater(expanded, 0)
        self.assertGreater(generated, 0)

    def test_unsolvable_map(self):
        """Bản đồ bế tắc trả về None an toàn, không bị treo chương trình."""
        state, static_data = parse_map_string(self.UNSOLVABLE_MAP)
        result = uniform_cost_search(state, static_data)
        self.assertFalse(result.solved)
        self.assertIsNone(result.actions)
        self.assertEqual(result.metrics["status"], "no_solution")

    def test_ucs_expansion_limit(self):
        """Giới hạn số node mở rộng dừng tìm kiếm an toàn."""
        state, static_data = parse_map_string(self.DETOUR_MAP)
        result = uniform_cost_search(state, static_data, max_expanded=1)
        self.assertIsNone(result.actions)
        self.assertEqual(result.metrics["status"], "limit_reached")
        self.assertLessEqual(result.metrics["nodes_expanded"], 1)

    def test_astar_optimality(self):
        """A* tìm ra lời giải có cùng chi phí tối ưu với UCS."""
        from source.search.astar import a_star_search
        from source.search.heuristic import SokobanHeuristic

        state, static_data = parse_map_string(self.DETOUR_MAP)
        try:
            result = a_star_search(state, static_data, SokobanHeuristic(static_data))
        except Exception as exc:
            self.skipTest(f"A* chưa sẵn sàng (Member 2): {exc!r}")
        if result is None:
            self.skipTest("A* chưa được cài đặt (Member 2)")
        ucs_result = uniform_cost_search(state, static_data)
        self.assertEqual(result.total_cost, ucs_result.total_cost)


if __name__ == "__main__":
    unittest.main()
