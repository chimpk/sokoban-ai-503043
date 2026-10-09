from collections import deque

import numpy as np
from scipy.optimize import linear_sum_assignment

from ..core.state import GameState, MapStaticData


class SokobanHeuristic:
    """
    Heuristic cho A* (R2).
    LƯU Ý CỰC KỲ QUAN TRỌNG:
    - KHÔNG được dùng Manhattan distance.
    - KHÔNG được dùng Euclidean distance.
    """

    def __init__(self, static_data: MapStaticData):
        self.static_data = static_data
        self.goal_distances: dict[tuple[int, int], dict[tuple[int, int], int]] = {}
        self._precompute_goal_distances()

    def _precompute_goal_distances(self) -> None:
        for goal in self.static_data.goals:
            dist: dict[tuple[int, int], int] = {goal: 0}
            queue: deque[tuple[int, int]] = deque([goal])

            while queue:
                cell = queue.popleft()
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    next_cell = (cell[0] + dr, cell[1] + dc)
                    if next_cell in self.static_data.walls:
                        continue
                    if 0 <= next_cell[0] < self.static_data.height and 0 <= next_cell[1] < self.static_data.width:
                        if next_cell not in dist:
                            dist[next_cell] = dist[cell] + 1
                            queue.append(next_cell)

            self.goal_distances[goal] = dist

    def _is_corner_deadlock(self, box_pos: tuple[int, int]) -> bool:
        if box_pos in self.static_data.goals:
            return False

        row, col = box_pos

        def is_blocked(cell: tuple[int, int]) -> bool:
            cell_row, cell_col = cell
            return (
                cell in self.static_data.walls
                or cell_row < 0
                or cell_row >= self.static_data.height
                or cell_col < 0
                or cell_col >= self.static_data.width
            )

        blocked_vertically = (
            is_blocked((row - 1, col)) or is_blocked((row + 1, col))
        )
        blocked_horizontally = (
            is_blocked((row, col - 1)) or is_blocked((row, col + 1))
        )
        return blocked_vertically and blocked_horizontally

    def evaluate(self, state: GameState) -> int | float:
        boxes = sorted(state.box_positions)
        goals = sorted(self.static_data.goals)

        if not boxes:
            return 0
        if any(self._is_corner_deadlock(box) for box in boxes):
            return float("inf")
        if not goals:
            return float("inf")

        n_boxes = len(boxes)
        n_goals = len(goals)
        if n_boxes > n_goals:
            return float("inf")

        max_cost = self.static_data.height * self.static_data.width + 1
        cost_matrix = np.full((n_boxes, n_goals), max_cost, dtype=float)

        for i, box_pos in enumerate(boxes):
            for j, goal in enumerate(goals):
                dist = self.goal_distances.get(goal, {}).get(box_pos)
                if dist is None:
                    continue
                cost_matrix[i, j] = float(dist)

        if any(not (cost_matrix[i] < max_cost).any() for i in range(n_boxes)):
            return float("inf")

        row_idx, col_idx = linear_sum_assignment(cost_matrix)
        total_cost = float(cost_matrix[row_idx, col_idx].sum())
        if np.isinf(total_cost) or (cost_matrix[row_idx, col_idx] >= max_cost).any():
            return float("inf")
        return int(total_cost)
