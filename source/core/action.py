from enum import Enum


class Action(str, Enum):


    NORTH = "North"
    SOUTH = "South"
    WEST = "West"
    EAST = "East"

    @property
    def delta(self) -> tuple[int, int]:

        deltas = {
            Action.NORTH: (-1, 0),
            Action.SOUTH: (1, 0),
            Action.WEST: (0, -1),
            Action.EAST: (0, 1),
        }
        return deltas[self]
