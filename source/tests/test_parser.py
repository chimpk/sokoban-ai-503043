import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from source.core.parser import MapFormatError, parse_map_file, parse_map_string


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

    def test_static_data_initial_positions(self):
        """MapStaticData lưu kích thước và vị trí ban đầu (docs/02 Mục 2.3)."""
        # Dòng trống cuối file bị bỏ qua khi tính height
        state, static_data = parse_map_string("%%%%%\n%A B%\n% D %\n%%%%%\n\n")
        self.assertEqual(static_data.height, 4)
        self.assertEqual(static_data.width, 5)
        self.assertEqual(static_data.initial_player_pos, state.player_pos)
        self.assertEqual(static_data.initial_box_positions, state.box_positions)

    def test_unbalanced_boxes_goals(self):
        """Phát hiện lỗi khi số lượng hộp khác số lượng đích."""
        with self.assertRaises(MapFormatError):
            parse_map_string("%%%%%\n%ABB%\n% D %\n%%%%%")

    def test_missing_player(self):
        """Báo lỗi khi thiếu vị trí người chơi A."""
        with self.assertRaises(MapFormatError):
            parse_map_string("%%%%%\n% B %\n% D %\n%%%%%")

    def test_multiple_players(self):
        """Báo lỗi khi có nhiều hơn 1 người chơi A."""
        with self.assertRaises(MapFormatError):
            parse_map_string("%%%%%\n%AB %\n%AD %\n%%%%%")

    def test_invalid_character(self):
        """Báo lỗi khi gặp ký tự không thuộc bảng ký hiệu của đề."""
        with self.assertRaises(MapFormatError):
            parse_map_string("%%%%%\n%AB#%\n% D %\n%%%%%")

    def test_all_map_files(self):
        """Mọi file trong source/maps (trừ map đối kháng) đều hợp lệ."""
        maps_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../maps"))
        for name in sorted(os.listdir(maps_dir)):
            if name.endswith(".txt") and "competitive" not in name:
                with self.subTest(map=name):
                    state, static_data = parse_map_file(os.path.join(maps_dir, name))
                    self.assertEqual(len(state.box_positions), len(static_data.goals))


if __name__ == "__main__":
    unittest.main()
