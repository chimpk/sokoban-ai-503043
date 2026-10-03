from typing import Optional
from .action import Action
from .state import GameState

class SearchNode:
    """
    Biểu diễn Node trong cây/đồ thị tìm kiếm.
    """
    __slots__ = ('state', 'parent', 'action', 'g', 'h', 'f')

    def __init__(
        self,
        state: GameState,
        parent: Optional['SearchNode'] = None,
        action: Optional[Action] = None,
        g: int = 0,
        h: int = 0
    ):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = g
        self.h = h
        self.f = g + h

    def __lt__(self, other: 'SearchNode') -> bool:
        """
        So sánh phục vụ cho Priority Queue.
        """
        return self.f < other.f

    def reconstruct_actions(self) -> list[str]:
        """
        Truy vết ngược từ node hiện tại về root để lấy danh sách action:
        ['North', 'East', ...]
        """
        actions = []
        curr = self
        while curr.parent is not None:
            actions.append(curr.action.value if hasattr(curr.action, 'value') else curr.action)
            curr = curr.parent
        actions.reverse()
        return actions
