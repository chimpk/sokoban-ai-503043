from __future__ import annotations

import heapq
import time
from collections import deque
from typing import Optional

from source.competitive.conflict import DIRECTIONS
from source.competitive.state import CompetitiveState

Cell = tuple[int, int]
MOVES = {a: d for a, d in DIRECTIONS.items() if a != "Wait"}


class Navigator:
    """Tìm đường và lập kế hoạch đẩy hộp; các vòng tìm kiếm hỗ trợ deadline mềm."""

    def __init__(self, state: CompetitiveState):
        sd = state.static_data
        self.walls, self.height, self.width = sd.walls, sd.height, sd.width
        self.goals = sd.goals
        self.boxes = state.box_positions
        self._h_cache: dict[Cell, dict[Cell, int]] = {}

    def free(self, cell: Cell) -> bool:
        return (
            0 <= cell[0] < self.height
            and 0 <= cell[1] < self.width
            and cell not in self.walls
        )

    def neighbors(self, cell: Cell):
        for action, (dr, dc) in MOVES.items():
            nxt = (cell[0] + dr, cell[1] + dc)
            if self.free(nxt):
                yield action, nxt

    def heuristic_map(self, target: Cell, deadline: Optional[float] = None) -> dict[Cell, int]:
        """BFS từ đích, chỉ xét tường; trả về khoảng cách mê cung chính xác."""
        if target not in self._h_cache:
            dist, queue = {target: 0}, deque([target])
            while queue:
                if deadline is not None and time.perf_counter() >= deadline:
                    break
                cur = queue.popleft()
                for _, nxt in self.neighbors(cur):
                    if nxt not in dist:
                        dist[nxt] = dist[cur] + 1
                        queue.append(nxt)
            # Chỉ cache bản đồ hoàn chỉnh; tránh lưu heuristic dở dang khi hết giờ.
            if not queue:
                self._h_cache[target] = dist
            return dist
        return self._h_cache[target]

    def a_star(self, start: Cell, goal: Cell, blocked, deadline: Optional[float] = None) -> Optional[list[str]]:
        return self._best_first(start, goal, blocked, use_g=True, deadline=deadline)

    def greedy(self, start: Cell, goal: Cell, blocked, deadline: Optional[float] = None) -> Optional[list[str]]:
        return self._best_first(start, goal, blocked, use_g=False, deadline=deadline)

    def _best_first(self, start, goal, blocked, use_g: bool,
                    deadline: Optional[float] = None) -> Optional[list[str]]:
        if start == goal:
            return []
        if deadline is not None and time.perf_counter() >= deadline:
            return None
        h = self.heuristic_map(goal, deadline)
        if deadline is not None and time.perf_counter() >= deadline:
            return None
        if start not in h or goal not in h:
            return None

        tie = 0
        g_score = {start: 0}
        parent: dict[Cell, tuple[Cell, str] | None] = {start: None}
        frontier = [((g_score[start] if use_g else 0) + h[start], tie, 0, start)]

        while frontier:
            if deadline is not None and time.perf_counter() >= deadline:
                return None
            _, _, pushed_g, cur = heapq.heappop(frontier)
            if pushed_g != g_score.get(cur):
                continue
            if cur == goal:
                path = []
                node = cur
                while parent[node] is not None:
                    prev, action = parent[node]
                    path.append(action)
                    node = prev
                return path[::-1]

            for action, nxt in self.neighbors(cur):
                if nxt in blocked:
                    continue
                tentative_g = g_score[cur] + 1
                if tentative_g >= g_score.get(nxt, 10**18):
                    continue
                g_score[nxt] = tentative_g
                parent[nxt] = (cur, action)
                tie += 1
                priority = (tentative_g if use_g else 0) + h.get(nxt, 10**6)
                heapq.heappush(frontier, (priority, tie, tentative_g, nxt))
        return None

    def _dead_corner(self, cell: Cell) -> bool:
        r, c = cell
        # Ngoài biên bản đồ cũng được xem là vật cản.
        vert = not self.free((r - 1, c)) or not self.free((r + 1, c))
        horiz = not self.free((r, c - 1)) or not self.free((r, c + 1))
        return vert and horiz and cell not in self.goals

    def push_plans(self, box: Cell, targets, deadline: Optional[float] = None) -> dict[Cell, list[str]]:
        """BFS trên vị trí hộp; các hộp còn lại được xem như vật cản."""
        others = self.boxes - {box}
        parent: dict[Cell, tuple[Cell, str] | None] = {box: None}
        queue = deque([box])
        while queue:
            if deadline is not None and time.perf_counter() >= deadline:
                break
            cur = queue.popleft()
            for action, (dr, dc) in MOVES.items():
                nxt = (cur[0] + dr, cur[1] + dc)
                stand = (cur[0] - dr, cur[1] - dc)
                if (
                    nxt in parent or not self.free(nxt) or nxt in others
                    or not self.free(stand) or stand in others
                    or self._dead_corner(nxt)
                ):
                    continue
                parent[nxt] = (cur, action)
                queue.append(nxt)

        plans = {}
        for target in targets:
            if target in parent and target != box:
                cur, seq = target, []
                while parent[cur] is not None:
                    cur, action = parent[cur]
                    seq.append(action)
                plans[target] = seq[::-1]
        return plans

    def approach(self, me: Cell, box: Cell, pushes: list[str], opponent: Cell,
                 greedy: bool = False, deadline: Optional[float] = None) -> Optional[list[str]]:
        """Chuyển chuỗi đẩy thành chuỗi đi/đẩy hợp lệ; dừng sớm khi hết ngân sách."""
        search = self.greedy if greedy else self.a_star
        others = self.boxes - {box}
        actions: list[str] = []
        agent, current_box = me, box

        for push in pushes:
            if deadline is not None and time.perf_counter() >= deadline:
                return None
            if push not in MOVES:
                return None
            dr, dc = MOVES[push]
            stand = (current_box[0] - dr, current_box[1] - dc)
            dest = (current_box[0] + dr, current_box[1] + dc)

            if not self.free(dest) or dest in others:
                return None
            if agent != stand:
                # Đối thủ hiện tại được xem là vật cản trong toàn bộ kế hoạch.
                blocked = set(others) | {current_box, opponent}
                walk = search(agent, stand, blocked, deadline=deadline)
                if walk is None:
                    return None
                actions.extend(walk)
            actions.append(push)
            agent, current_box = current_box, dest

        return actions

    def safe_step(self, me: Cell, opponent: Cell, rng) -> str:
        options = [
            action for action, nxt in self.neighbors(me)
            if nxt not in self.boxes and nxt != opponent
        ]
        return rng.choice(options) if options else "Wait"


class StuckBreaker:
    """Phá bế tắc lặp lại bằng lựa chọn ngẫu nhiên có seed cố định."""

    def __init__(self, rng):
        self.rng, self.last, self.count = rng, None, 0

    def should_randomize(self, me: Cell) -> bool:
        stuck = self.last is not None and self.last[0] == me and self.last[1] != "Wait"
        self.count = self.count + 1 if stuck else 0
        return self.count >= 2 and self.rng.random() < 0.5

    def remember(self, me: Cell, action: str) -> str:
        self.last = (me, action)
        return action
