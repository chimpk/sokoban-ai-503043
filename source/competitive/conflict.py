from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .state import CompetitiveState

Cell = tuple[int, int]

DIRECTIONS: dict[str, Cell] = {
    "North": (-1, 0), "South": (1, 0), "West": (0, -1), "East": (0, 1), "Wait": (0, 0),
}


@dataclass
class Move:
    """Ý định di chuyển của một agent trong 1 bước."""
    start: Cell
    target: Cell                      # ô agent muốn đứng sau bước đi
    box_from: Optional[Cell] = None   # nếu đẩy hộp: vị trí hộp trước / sau khi đẩy
    box_to: Optional[Cell] = None

    @property
    def active(self) -> bool:
        return self.target != self.start

    def cancel(self) -> None:
        self.target, self.box_from, self.box_to = self.start, None, None


class ConflictResolver:
    """
    Trọng tài cho 2 hành động đồng thời. Quy tắc (mọi vi phạm -> huỷ bước đi):
      1. Cùng vào một ô, hoặc đi vào ô đối thủ đang đứng yên -> bước đi bị huỷ.
      2. Đổi chỗ cho nhau (đi xuyên qua nhau) -> cả hai bị huỷ.
      3. Cùng đẩy một hộp, hoặc hai hộp bị đẩy vào cùng một ô -> cả hai bị huỷ.
      4. Đẩy hộp vào ô đối thủ đang đứng/đi tới -> bị huỷ (nếu đối thủ rời đi thì được).
    Sau khi huỷ, các quy tắc được kiểm tra lại cho đến khi không còn xung đột.
    """

    def __init__(self, walls):
        self.walls = frozenset(walls)

    # ---------- Bước 1: mỗi agent đề xuất bước đi theo luật Sokoban ----------
    def _propose(self, state: CompetitiveState, pos: Cell, action: str) -> Move:
        move = Move(pos, pos)
        dr, dc = DIRECTIONS.get(action, (0, 0))
        if (dr, dc) == (0, 0):
            return move
        target = (pos[0] + dr, pos[1] + dc)
        if self._blocked(state, target):
            return move
        if target not in state.box_positions:
            return Move(pos, target)
        beyond = (target[0] + dr, target[1] + dc)
        if self._blocked(state, beyond) or beyond in state.box_positions:
            return move
        return Move(pos, target, target, beyond)

    def _blocked(self, state: CompetitiveState, cell: Cell) -> bool:
        sd = state.static_data
        out = not (0 <= cell[0] < sd.height and 0 <= cell[1] < sd.width)
        return out or cell in self.walls

    # ---------- Bước 2: phát hiện xung đột ----------
    @staticmethod
    def _to_cancel(a: Move, b: Move) -> list[Move]:
        bad: list[Move] = []
        if a.target == b.target:                                   # luật 1
            bad += [m for m in (a, b) if m.active]
        if a.target == b.start and b.target == a.start:            # luật 2
            bad += [a, b]
        if a.box_from is not None and (a.box_from == b.box_from    # luật 3
                                       or a.box_to == b.box_to):
            bad += [a, b]
        for me, other in ((a, b), (b, a)):                         # luật 4
            if me.box_to is None:
                continue
            if me.box_to == other.target:
                bad.append(me)
                if other.active:
                    bad.append(other)
        return [m for m in bad if m.active]

    def resolve(self, state: CompetitiveState, action_a: str, action_b: str) -> CompetitiveState:
        """Trả về trạng thái MỚI (không sửa state đầu vào)."""
        a = self._propose(state, state.agent_a_pos, action_a)
        b = self._propose(state, state.agent_b_pos, action_b)
        while True:
            bad = self._to_cancel(a, b)
            if not bad:
                break
            for move in bad:
                move.cancel()
        return self._apply(state, a, b)

    # ---------- Bước 3: áp dụng bước đi và cập nhật chủ sở hữu / điểm ----------
    @staticmethod
    def _apply(state: CompetitiveState, a: Move, b: Move) -> CompetitiveState:
        new = state.copy()
        boxes, owners = set(state.box_positions), dict(state.box_owners)
        for move, agent in ((a, "A"), (b, "B")):
            if move.box_from is None:
                continue
            boxes.remove(move.box_from)
            owners.pop(move.box_from, None)
            boxes.add(move.box_to)
            # chỉ có chủ khi hộp nằm trên goal; đẩy ra khỏi goal thì mất chủ
            owners[move.box_to] = agent if move.box_to in state.static_data.goals else None
        new.agent_a_pos, new.agent_b_pos = a.target, b.target
        new.box_positions, new.box_owners = frozenset(boxes), owners
        new.score_a = sum(1 for o in owners.values() if o == "A")
        new.score_b = sum(1 for o in owners.values() if o == "B")
        new.current_step += 1
        return new
