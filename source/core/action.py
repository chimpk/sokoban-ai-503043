from enum import Enum

class Action(str, Enum):
    """
    4 actions theo quy định của đề bài:
    North, South, West, East
    """
    NORTH = "North"
    SOUTH = "South"
    WEST = "West"
    EAST = "East"

    @property
    def delta(self) -> tuple[int, int]:
        """
        Trả về (delta_row, delta_col) tương ứng với hành động.
        """
        if self == Action.NORTH:
            return (-1, 0)
        elif self == Action.SOUTH:
            return (1, 0)
        elif self == Action.WEST:
            return (0, -1)
        elif self == Action.EAST:
            return (0, 1)
