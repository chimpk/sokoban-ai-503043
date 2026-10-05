from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
from typing import Optional

from source.core.state import MapStaticData


@dataclass
class CompetitiveState:
    """
    Trạng thái của trận đấu 2 agent (khớp docs/04 mục 4.1).

    box_owners: chỉ có giá trị 'A' hoặc 'B' khi hộp đang nằm trên goal
                (agent nào đẩy hộp vào goal thì sở hữu hộp đó), còn lại là None.
    score_a / score_b luôn bằng số hộp mà mỗi agent đang sở hữu.
    """
    agent_a_pos: tuple[int, int]
    agent_b_pos: tuple[int, int]
    box_positions: frozenset[tuple[int, int]]
    box_owners: dict[tuple[int, int], Optional[str]]
    score_a: int
    score_b: int
    current_step: int
    max_steps: int
    static_data: MapStaticData

    @classmethod
    def from_map_file(cls, file_path: str | Path, max_steps: int) -> "CompetitiveState":
        """
        Đọc map có đúng 2 ký tự 'A'. Parser của Member 1 chỉ giữ 1 vị trí người chơi
        nên Member 3 tự đọc map riêng (không sửa source/core).
        Quy ước: 'A' đầu tiên (theo thứ tự đọc) là Agent A, 'A' thứ hai là Agent B.
        """
        lines = Path(file_path).read_text(encoding="utf-8").splitlines()
        walls, goals, boxes, agents = set(), set(), set(), []
        for r, line in enumerate(lines):
            for c, ch in enumerate(line):
                pos = (r, c)
                if ch == "%":
                    walls.add(pos)
                elif ch == "A":
                    agents.append(pos)
                elif ch == "B":
                    boxes.add(pos)
                elif ch == "D":
                    goals.add(pos)
                elif ch == "C":  # hộp đã nằm sẵn trên goal
                    boxes.add(pos)
                    goals.add(pos)
        if len(agents) != 2:
            raise ValueError(f"Map đối kháng cần đúng 2 ký tự 'A', tìm thấy {len(agents)}")
        if not boxes:
            raise ValueError("Map đối kháng cần ít nhất một hộp")
        static = MapStaticData(walls, goals, len(lines), max(len(l) for l in lines))
        return cls(agents[0], agents[1], frozenset(boxes), {b: None for b in boxes},
                   0, 0, 0, max_steps, static)

    # ---- tương thích với API của stub cũ trên GitHub (get_scores / is_game_over / goals / boxes_a / boxes_b) ----
    @property
    def goals(self) -> frozenset[tuple[int, int]]:
        return self.static_data.goals

    @property
    def boxes_a(self) -> frozenset[tuple[int, int]]:
        return frozenset(b for b, o in self.box_owners.items() if o == "A")

    @property
    def boxes_b(self) -> frozenset[tuple[int, int]]:
        return frozenset(b for b, o in self.box_owners.items() if o == "B")

    def get_scores(self) -> tuple[int, int]:
        return self.score_a, self.score_b

    def is_game_over(self) -> bool:
        return self.is_finished()

    def copy(self) -> "CompetitiveState":
        return replace(self, box_owners=dict(self.box_owners))

    def is_finished(self) -> bool:
        """Kết thúc khi hết n bước, hoặc mọi hộp đã vào goal và đều có chủ."""
        if self.current_step >= self.max_steps:
            return True
        all_done = all(b in self.static_data.goals and self.box_owners.get(b) is not None
                       for b in self.box_positions)
        return all_done

    def winner(self) -> Optional[str]:
        if self.score_a > self.score_b:
            return "A"
        if self.score_b > self.score_a:
            return "B"
        return None
