from typing import Optional

from .action import Action


class MapStaticData:


    def __init__(self, walls: set[tuple[int, int]], goals: set[tuple[int, int]], height: int, width: int):
        self.walls: frozenset[tuple[int, int]] = frozenset(walls)
        self.goals: frozenset[tuple[int, int]] = frozenset(goals)
        self.height: int = height
        self.width: int = width


class GameState:


    def __init__(self, player_pos: tuple[int, int], box_positions: set[tuple[int, int]] | frozenset[tuple[int, int]]):
        self.player_pos: tuple[int, int] = player_pos
        self.box_positions: frozenset[tuple[int, int]] = frozenset(box_positions)

    def is_goal(self, static_data: MapStaticData) -> bool:
        """
        Kiểm tra xem tất cả các hộp đã nằm trên các ô đích (goals) hay chưa.
        """
        return all(box_pos in static_data.goals for box_pos in self.box_positions)

    def get_successors(self, static_data: MapStaticData) -> list[tuple[Action, 'GameState', int]]:
        """
        Sinh tất cả các trạng thái hợp lệ tiếp theo từ trạng thái hiện tại.
        Trả về danh sách các tuple: (action, next_state, step_cost)
        """
        successors: list[tuple[Action, 'GameState', int]] = []
        for action in Action:
            dr, dc = action.delta
            next_player = (self.player_pos[0] + dr, self.player_pos[1] + dc)

            if next_player in static_data.walls:
                continue

            if next_player in self.box_positions:
                pushed_box = (next_player[0] + dr, next_player[1] + dc)
                if pushed_box in static_data.walls or pushed_box in self.box_positions:
                    continue

                new_boxes = set(self.box_positions)
                new_boxes.remove(next_player)
                new_boxes.add(pushed_box)
                successors.append((action, GameState(next_player, new_boxes), 1))
            else:
                successors.append((action, GameState(next_player, self.box_positions), 1))

        return successors

    def __eq__(self, other: object) -> bool:

        if not isinstance(other, GameState):
            return NotImplemented
        return self.player_pos == other.player_pos and self.box_positions == other.box_positions

    def __hash__(self) -> int:

        return hash((self.player_pos, self.box_positions))
