from typing import Optional
from .action import Action

class MapStaticData:
    """
    Lưu trữ các thành phần tĩnh của bản đồ (walls, goals, kích thước).
    Không thay đổi trong suốt quá trình tìm kiếm.
    """
    def __init__(
        self,
        walls: set[tuple[int, int]],
        goals: set[tuple[int, int]],
        height: int,
        width: int,
        initial_player_pos: Optional[tuple[int, int]] = None,
        initial_box_positions: Optional[set[tuple[int, int]]] = None
    ):
        self.walls: frozenset[tuple[int, int]] = frozenset(walls)
        self.goals: frozenset[tuple[int, int]] = frozenset(goals)
        self.height: int = height
        self.width: int = width
        self.initial_player_pos: Optional[tuple[int, int]] = initial_player_pos
        self.initial_box_positions: frozenset[tuple[int, int]] = frozenset(initial_box_positions or ())


class GameState:
    """
    Biểu diễn trạng thái động của game Sokoban (R1).
    Bao gồm: vị trí người chơi, vị trí các hộp.
    """
    __slots__ = ('player_pos', 'box_positions', '_hash')

    def __init__(self, player_pos: tuple[int, int], box_positions: set[tuple[int, int]] | frozenset[tuple[int, int]]):
        self.player_pos: tuple[int, int] = player_pos
        self.box_positions: frozenset[tuple[int, int]] = frozenset(box_positions)
        self._hash = hash((self.player_pos, self.box_positions))

    def is_goal(self, static_data: MapStaticData | frozenset[tuple[int, int]]) -> bool:
        """
        Kiểm tra xem tất cả các hộp đã nằm trên các ô đích (goals) hay chưa.
        Nhận vào MapStaticData hoặc trực tiếp tập goals.
        """
        goals = static_data.goals if isinstance(static_data, MapStaticData) else static_data
        return self.box_positions == goals

    def get_successors(self, static_data: MapStaticData) -> list[tuple[Action, 'GameState', int]]:
        """
        Sinh tất cả các trạng thái hợp lệ tiếp theo từ trạng thái hiện tại.
        Trả về danh sách các tuple: (action, next_state, step_cost)
        """
        successors = []
        r, c = self.player_pos
        for action in Action:
            dr, dc = action.delta
            nr, nc = r + dr, c + dc
            if (nr, nc) in static_data.walls:
                continue
            
            if (nr, nc) in self.box_positions:
                nnr, nnc = nr + dr, nc + dc
                if (nnr, nnc) in static_data.walls or (nnr, nnc) in self.box_positions:
                    continue
                new_boxes = set(self.box_positions)
                new_boxes.remove((nr, nc))
                new_boxes.add((nnr, nnc))
                successors.append((action, GameState((nr, nc), new_boxes), 1))
            else:
                successors.append((action, GameState((nr, nc), self.box_positions), 1))
        return successors

    def __eq__(self, other: object) -> bool:
        """
        So sánh hai trạng thái có tương đương nhau hay không.
        """
        if not isinstance(other, GameState):
            return False
        return self.player_pos == other.player_pos and self.box_positions == other.box_positions

    def __hash__(self) -> int:
        """
        Hàm băm canonical để lưu trữ trong visited/explored set.
        """
        return self._hash
