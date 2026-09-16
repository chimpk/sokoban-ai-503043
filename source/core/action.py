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
        # TODO: Member 1 implement
        pass
