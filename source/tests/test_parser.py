import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from source.core.parser import parse_map_file


class TestMapParser(unittest.TestCase):
    """
    Bộ kiểm thử cho Parser bản đồ (Requirement 1, docs/04 Mục 5.1).
    Phụ trách: Member 1.
    """
    def setUp(self):
        self.temp_map = "temp_parser_test.txt"

    def tearDown(self):
        if os.path.exists(self.temp_map):
            os.remove(self.temp_map)

    def test_valid_parsing(self):
        """Đọc chuẩn xác các ký tự %, A, B, D, C và khoảng trắng."""
        content = (
            "%%%%%\n"
            "%A B%\n"
            "% C %\n"
            "%  D%\n"
            "%%%%%"
        )
        with open(self.temp_map, "w", encoding="utf-8") as f:
            f.write(content)

        state, static_data = parse_map_file(self.temp_map)
        self.assertEqual(state.player_pos, (1, 1))
        # B ở (1, 3), C ở (2, 2) -> 2 hộp
        self.assertIn((1, 3), state.box_positions)
        self.assertIn((2, 2), state.box_positions)
        # C ở (2, 2), D ở (3, 3) -> 2 đích
        self.assertIn((2, 2), static_data.goals)
        self.assertIn((3, 3), static_data.goals)
        self.assertEqual(len(state.box_positions), 2)
        self.assertEqual(len(static_data.goals), 2)

    def test_example_map_file(self):
        """Đọc file bản đồ chuẩn example_map.txt (7 hộp, 7 đích)."""
        map_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../maps/example_map.txt"))
        if os.path.exists(map_path):
            state, static_data = parse_map_file(map_path)
            self.assertEqual(len(state.box_positions), 7)
            self.assertEqual(len(static_data.goals), 7)
            self.assertNotEqual(state.player_pos, (-1, -1))


if __name__ == "__main__":
    unittest.main()
