import pyglet
import enum

pyglet.resource.path = ["../resources"]
pyglet.resource.reindex()


class TileStatus(enum.Enum):
    Bag = 0
    Hand = 1
    Selected = 2
    PotentialSelection = 3
    BoardThinking = 4  # dragging tile over the board = "thinking" about placing it
    BoardPlaced = 5  # Once tile is placed and on the board


class SpaceStatus(enum.Enum):
    Free = 0
    Selected = 1
    Occupied = 2


class TileColors(enum.Enum):
    Pink = 0
    Purple = 1
    Indigo = 2
    Blue = 3
    Aqua = 4
    Green = 5


class Outlines:
    def __init__(self):
        self.active_outline = pyglet.resource.image("BrightOutline.png")
        self.active_outline.anchor_y = self.active_outline.height / 2
        self.active_outline.anchor_x = self.active_outline.width / 2
        self.option_outline = pyglet.resource.image("DimOutline.png")
        self.option_outline.anchor_y = self.option_outline.height / 2
        self.option_outline.anchor_x = self.option_outline.width / 2
