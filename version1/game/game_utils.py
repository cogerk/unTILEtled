import enum


class TileStatus(enum.Enum):
    Bag = 0
    Hand = 1
    BoardThinking = 2  # dragging tile over the board = "thinking" about placing it
    BoardPlaced = 3  # Once tile is placed and on the board


class SpaceStatus(enum.Enum):
    Free = 0
    Selected = 1
    Occupied = 2
