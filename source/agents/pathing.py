from __future__ import annotations

import heapq
from collections import deque
from typing import Optional

from source.competitive.conflict import DIRECTIONS
from source.competitive.state import CompetitiveState

Cell = tuple[int, int]
MOVES = {a: d for a, d in DIRECTIONS.items() if a != "Wait"}


class Navigator:
    """
    Công cụ tìm đường dùng chung cho 2 agent (BFS, A*, GBFS, lập kế hoạch đẩy hộp).
    Heuristic của A*/GBFS là khoảng cách mê cung (BFS từ đích, chỉ tính tường),
    nên không dùng Manhattan/Euclid, luôn admissible và consistent.
    """

    def __init__(self, state: CompetitiveState):
        sd = state.static_data
        self.walls, self.height, self.width = sd.walls, sd.height, sd.width
        self.goals = sd.goals
        self.boxes = state.box_positions
        self._h_cache: dict[Cell, dict[Cell, int]] = {}

    # ---------- lưới ----------
    def free(self, cell: Cell) -> bool:
        return 0 <= cell[0] < self.height and 0 <= cell[1] < self.width and cell not in self.walls

    def neighbors(self, cell: Cell):
        for action, (dr, dc) in MOVES.items():
            nxt = (cell[0] + dr, cell[1] + dc)
            if self.free(nxt):
                yield action, nxt

    def heuristic_map(self, target: Cell) -> dict[Cell, int]:
        """Khoảng cách thật từ mọi ô tới target khi chỉ có tường."""
        if target not in self._h_cache:
            dist, queue = {target: 0}, deque([target])
            while queue:
                cur = queue.popleft()
                for _, nxt in self.neighbors(cur):
                    if nxt not in dist:
                        dist[nxt] = dist[cur] + 1
                        queue.append(nxt)
            self._h_cache[target] = dist
        return self._h_cache[target]

    # ---------- tìm đường cho agent ----------
    def a_star(self, start: Cell, goal: Cell, blocked) -> Optional[list[str]]:
        return self._best_first(start, goal, blocked, use_g=True)

    def greedy(self, start: Cell, goal: Cell, blocked) -> Optional[list[str]]:
        return self._best_first(start, goal, blocked, use_g=False)

    def _best_first(self, start, goal, blocked, use_g: bool) -> Optional[list[str]]:
        h = self.heuristic_map(goal)
        if start not in h:
            return None
        tie = 0
        frontier = [(h[start], tie, start)]
        g, parent = {start: 0}, {start: None}
        while frontier:
            _, _, cur = heapq.heappop(frontier)
            if cur == goal:
                path = []
                while parent[cur] is not None:
                    cur, action = parent[cur]
                    path.append(action)
                return path[::-1]
            for action, nxt in self.neighbors(cur):
                if nxt in blocked or nxt in parent:
                    continue
                g[nxt] = g[cur] + 1
                parent[nxt] = (cur, action)
                tie += 1
                heapq.heappush(frontier, ((g[nxt] if use_g else 0) + h.get(nxt, 10 ** 6), tie, nxt))
        return None

    # ---------- kế hoạch đẩy hộp ----------
    def _dead_corner(self, cell: Cell) -> bool:
        r, c = cell
        vert = (r - 1, c) in self.walls or (r + 1, c) in self.walls
        horiz = (r, c - 1) in self.walls or (r, c + 1) in self.walls
        return vert and horiz and cell not in self.goals

    def push_plans(self, box: Cell, targets) -> dict[Cell, list[str]]:
        """
        BFS trên vị trí hộp (các hộp khác coi như tường) -> với mỗi ô trong targets
        trả về chuỗi hướng đẩy ngắn nhất. Bỏ qua ô góc chết.
        """
        others = self.boxes - {box}
        parent, queue = {box: None}, deque([box])
        while queue:
            cur = queue.popleft()
            for action, (dr, dc) in MOVES.items():
                nxt, stand = (cur[0] + dr, cur[1] + dc), (cur[0] - dr, cur[1] - dc)
                if (nxt in parent or not self.free(nxt) or nxt in others
                        or not self.free(stand) or stand in others or self._dead_corner(nxt)):
                    continue
                parent[nxt] = (cur, action)
                queue.append(nxt)
        plans = {}
        for t in targets:
            if t in parent and t != box:
                cur, seq = t, []
                while parent[cur] is not None:
                    cur, action = parent[cur]
                    seq.append(action)
                plans[t] = seq[::-1]
        return plans

    def approach(self, me: Cell, box: Cell, pushes: list[str], opponent: Cell,
                 greedy: bool = False) -> Optional[list[str]]:
        """
        Biến chuỗi hướng đẩy thành chuỗi hành động THỰC SỰ thực hiện được.
        Trước mỗi lần đẩy, nếu agent chưa đứng đúng ô phía sau hộp (ví dụ vừa đổi
        hướng East -> South) thì chèn thêm đoạn đường đi vòng (A*/GBFS) tới ô đó.
        Sau mỗi lần đẩy, agent đứng ở vị trí cũ của hộp. Trả về None nếu một đoạn
        không đi tới được (kế hoạch bất khả thi).
        """
        search = self.greedy if greedy else self.a_star
        others = self.boxes - {box}
        actions: list[str] = []
        agent = me
        for i, push in enumerate(pushes):
            dr, dc = MOVES[push]
            stand = (box[0] - dr, box[1] - dc)
            if agent != stand:
                blocked = others | {box} | ({opponent} if i == 0 else set())
                walk = search(agent, stand, blocked)
                if walk is None:
                    return None
                actions += walk
            actions.append(push)
            agent, box = box, (box[0] + dr, box[1] + dc)
        return actions

    def safe_step(self, me: Cell, opponent: Cell, rng) -> str:
        """Bước dự phòng: đi ngẫu nhiên sang ô trống (không đẩy hộp)."""
        options = [a for a, n in self.neighbors(me) if n not in self.boxes and n != opponent]
        return rng.choice(options) if options else "Wait"


class StuckBreaker:
    """
    Phá thế bế tắc đối xứng (ví dụ 2 agent cùng đẩy một hộp từ hai phía, bước đi bị huỷ
    mãi). Nhớ vị trí/hành động bước trước; nếu đứng yên dù đã ra lệnh đi 2 lần liên tiếp
    thì đôi khi đổi sang bước ngẫu nhiên. Kết quả vẫn lặp lại được vì dùng rng có seed.
    """

    def __init__(self, rng):
        self.rng, self.last, self.count = rng, None, 0

    def should_randomize(self, me: Cell) -> bool:
        stuck = self.last is not None and self.last[0] == me and self.last[1] != "Wait"
        self.count = self.count + 1 if stuck else 0
        return self.count >= 2 and self.rng.random() < 0.5

    def remember(self, me: Cell, action: str) -> str:
        self.last = (me, action)
        return action
