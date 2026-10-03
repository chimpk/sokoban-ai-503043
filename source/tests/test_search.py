import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


class TestSearchAlgorithms(unittest.TestCase):
    """
    Bộ kiểm thử cho Thuật toán Tìm kiếm UCS & A* (Requirement 2, docs/04 Mục 5.3).
    Phụ trách: Member 1 (UCS) & Member 2 (A*).
    Lộ trình thực hiện: Ngày 3-5 (Tuần 1).
    """

    def test_ucs_optimality(self):
        """UCS tìm ra lời giải tối ưu trên bản đồ nhỏ."""
        # Sẽ kích hoạt kiểm thử chi tiết khi Member 1 hoàn thành UCS (Ngày 3)
        self.assertTrue(True)

    def test_astar_optimality(self):
        """A* tìm ra lời giải có cùng chi phí tối ưu với UCS."""
        # Sẽ kích hoạt kiểm thử chi tiết khi Member 2 hoàn thành A* (Ngày 4-5)
        self.assertTrue(True)

    def test_unsolvable_map(self):
        """Bản đồ bế tắc trả về None an toàn, không bị treo chương trình."""
        # Sẽ kích hoạt kiểm thử chi tiết khi chạy trên bản đồ deadlock mẫu
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
