from typing import Optional
from .action import Action

class MapStaticData:
    """
    Lưu trữ các thành phần tĩnh của bản đồ (walls, goals, kích thước).
    Không thay đổi trong suốt quá trình tìm kiếm.
    Xem quy ước biến tại: docs/14_Shared_Variables_Dictionary.md
    """
    def __init__(self, walls: set[tuple[int, int]], goals: set[tuple[int, int]], height: int, width: int):
        self.walls: frozenset[tuple[int, int]] = frozenset(walls)
        self.goals: frozenset[tuple[int, int]] = frozenset(goals)
        self.height: int = height
        self.width: int = width


class GameState:
    """
    Biểu diễn trạng thái động của game Sokoban (R1).
    Bao gồm: vị trí người chơi, vị trí các hộp.
    Xem quy ước biến tại: docs/14_Shared_Variables_Dictionary.md
    """
    def __init__(self, player_pos: tuple[int, int], box_positions: set[tuple[int, int]] | frozenset[tuple[int, int]]):
        self.player_pos: tuple[int, int] = player_pos
        self.box_positions: frozenset[tuple[int, int]] = frozenset(box_positions)
        # TODO: Member 1 implement thêm hash cache nếu cần

    def is_goal(self, static_data: MapStaticData) -> bool:
        """
        Kiểm tra xem tất cả các hộp đã nằm trên các ô đích (goals) hay chưa.
        """
        # TODO: Member 1 implement
        pass

    def get_successors(self, static_data: MapStaticData) -> list[tuple[Action, 'GameState', int]]:
        """
        Sinh tất cả các trạng thái hợp lệ tiếp theo từ trạng thái hiện tại.
        Trả về danh sách các tuple: (action, next_state, step_cost)
        """
        # TODO: Member 1 implement
        pass

    def __eq__(self, other: object) -> bool:
        """
        So sánh hai trạng thái có tương đương nhau hay không.
        """
        # TODO: Member 1 implement
        pass

    def __hash__(self) -> int:
        """
        Hàm băm canonical để lưu trữ trong visited/explored set.
        """
        # TODO: Member 1 implement
        pass
