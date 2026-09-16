from typing import Optional
from .action import Action
from .state import GameState

class SearchNode:
    """
    Biểu diễn Node trong cây/đồ thị tìm kiếm.
    """
    def __init__(
        self,
        state: GameState,
        parent: Optional['SearchNode'] = None,
        action: Optional[Action] = None,
        g: int = 0,
        h: int = 0
    ):
        # TODO: Member 1 implement
        pass

    def __lt__(self, other: 'SearchNode') -> bool:
        """
        So sánh phục vụ cho Priority Queue.
        """
        # TODO: Member 1 implement
        pass

    def reconstruct_actions(self) -> list[str]:
        """
        Truy vết ngược từ node hiện tại về root để lấy danh sách action:
        ['North', 'East', ...]
        """
        # TODO: Member 1 implement
        pass
