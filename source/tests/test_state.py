import os
import sys
import unittest

# Đảm bảo import được dù chạy trực tiếp file hay qua test runner
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from source.core.action import Action
from source.core.parser import parse_map_file
from source.core.state import GameState, MapStaticData


class TestSokobanState(unittest.TestCase):
    def setUp(self):
        # Map thử nghiệm chuẩn:
        # %%%%%
        # %A B%
        # % D %
        # %%%%%
        self.test_map_path = "test_map_temp.txt"
        with open(self.test_map_path, "w", encoding="utf-8") as f:
            f.write("%%%%%\n%A B%\n% D %\n%%%%%")

    def tearDown(self):
        if os.path.exists(self.test_map_path):
            os.remove(self.test_map_path)

    def test_parser(self):
        """Test đọc map cơ bản."""
        initial_state, static_data = parse_map_file(self.test_map_path)
        self.assertEqual(initial_state.player_pos, (1, 1))
        self.assertEqual(initial_state.box_positions, frozenset({(1, 3)}))
        self.assertEqual(static_data.goals, frozenset({(2, 2)}))
        self.assertIn((0, 0), static_data.walls)

    def test_state_hash_equality(self):
        """Test tính tương đương và hàm băm canonical (bắt buộc cho UCS/A*)."""
        s1 = GameState((1, 1), {(1, 2), (2, 2)})
        s2 = GameState((1, 1), {(2, 2), (1, 2)})  # Thứ tự set khác nhau
        s3 = GameState((1, 2), {(1, 2), (2, 2)})  # Khác vị trí người chơi
        s4 = GameState((1, 1), {(1, 3), (2, 2)})  # Khác vị trí hộp

        self.assertEqual(s1, s2)
        self.assertEqual(hash(s1), hash(s2))
        self.assertNotEqual(s1, s3)
        self.assertNotEqual(s1, s4)
        self.assertNotEqual(s1, "invalid_type")

        # Kiểm tra hoạt động trong set/explored
        visited = {s1}
        self.assertIn(s2, visited)
        self.assertEqual(len(visited), 1)

    def test_valid_move(self):
        """Test di chuyển người chơi vào ô sàn trống."""
        initial_state, static_data = parse_map_file(self.test_map_path)
        successors = initial_state.get_successors(static_data)
        actions = {action: (state, cost) for action, state, cost in successors}

        # Có thể đi East vào (1, 2)
        self.assertIn(Action.EAST, actions)
        next_state, cost = actions[Action.EAST]
        self.assertEqual(next_state.player_pos, (1, 2))
        self.assertEqual(next_state.box_positions, initial_state.box_positions)
        self.assertEqual(cost, 1)

    def test_move_into_wall(self):
        """Test di chuyển vào tường bị chặn đứng."""
        initial_state, static_data = parse_map_file(self.test_map_path)
        successors = initial_state.get_successors(static_data)
        valid_actions = [action for action, _, _ in successors]

        # Vị trí (1, 1): North là (0, 1) tường, West là (1, 0) tường
        self.assertNotIn(Action.NORTH, valid_actions)
        self.assertNotIn(Action.WEST, valid_actions)

    def test_valid_push(self):
        """Test đẩy hộp vào ô trống hợp lệ."""
        walls_custom = {(0, 1), (0, 2), (0, 3), (1, 0), (2, 0), (3, 0), (4, 1), (4, 2), (4, 3), (1, 4), (2, 4), (3, 4)}
        static_custom = MapStaticData(walls_custom, goals={(3, 2)}, height=5, width=5)
        state_push = GameState(player_pos=(1, 2), box_positions={(2, 2)})

        successors = state_push.get_successors(static_custom)
        actions = {action: (state, cost) for action, state, cost in successors}

        self.assertIn(Action.SOUTH, actions)
        next_state, cost = actions[Action.SOUTH]
        self.assertEqual(next_state.player_pos, (2, 2))  # Người tới ô cũ của hộp
        self.assertEqual(next_state.box_positions, frozenset({(3, 2)}))  # Hộp tới ô mới
        self.assertEqual(cost, 1)

    def test_push_into_wall(self):
        """Test đẩy hộp vào tường bị từ chối."""
        # Agent ở (1, 2), hộp ở (1, 3), sau hộp là tường (1, 4)
        walls = {(1, 4)}
        static_data = MapStaticData(walls=walls, goals=set(), height=3, width=5)
        state = GameState(player_pos=(1, 2), box_positions={(1, 3)})

        successors = state.get_successors(static_data)
        actions = [action for action, _, _ in successors]
        self.assertNotIn(Action.EAST, actions)

    def test_push_into_box(self):
        """Test đẩy hộp vào một hộp khác bị từ chối."""
        static_data = MapStaticData(walls=set(), goals=set(), height=5, width=5)
        # Agent ở (1, 1), hộp 1 ở (1, 2), hộp 2 ở (1, 3)
        state = GameState(player_pos=(1, 1), box_positions={(1, 2), (1, 3)})

        successors = state.get_successors(static_data)
        actions = [action for action, _, _ in successors]
        # Không thể đẩy East vì bị vướng hộp ở (1, 3)
        self.assertNotIn(Action.EAST, actions)

    def test_goal_check(self):
        """Test kiểm tra điều kiện về đích."""
        static_data = MapStaticData(walls=set(), goals={(1, 2), (2, 2)}, height=4, width=4)

        # Chưa có hộp nào vào đích
        s0 = GameState((0, 0), {(1, 1), (3, 3)})
        self.assertFalse(s0.is_goal(static_data))

        # Chỉ mới 1 trong 2 hộp vào đích
        s1 = GameState((0, 0), {(1, 2), (3, 3)})
        self.assertFalse(s1.is_goal(static_data))

        # Tất cả các hộp đã vào đích
        s2 = GameState((0, 0), {(1, 2), (2, 2)})
        self.assertTrue(s2.is_goal(static_data))

    def test_immutability(self):
        """Test trạng thái gốc không bị thay đổi sau khi sinh successors."""
        initial_state, static_data = parse_map_file(self.test_map_path)
        orig_player = initial_state.player_pos
        orig_boxes = initial_state.box_positions

        _ = initial_state.get_successors(static_data)

        self.assertEqual(initial_state.player_pos, orig_player)
        self.assertEqual(initial_state.box_positions, orig_boxes)


if __name__ == "__main__":
    unittest.main()
