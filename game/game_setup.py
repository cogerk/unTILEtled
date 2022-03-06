from __future__ import annotations
from ctypes.wintypes import PULONG
from typing import TYPE_CHECKING, Type
from curses.ascii import SP  # type: ignore
import numpy as np

import pyglet
from game.game_utils import TileStatus, SpaceStatus, TileColors, Outlines
import game.game_actions

pyglet.resource.path = ["../resources"]
pyglet.resource.reindex()


# Load all block and gem images into a matrix of images 2 x 6 in size
class GameAssets:
    def __init__(self):
        # Create list of block and gem resources, respectively
        self.block_list = []
        self.gem_list = []
        for color in TileColors:
            # Build File Names
            block_file_name = f"Block_{color.name}.png"
            gem_file_name = f"Gem_{color.name}.png"
            # Inject into resources
            block = pyglet.resource.image(block_file_name)
            gem = pyglet.resource.image(gem_file_name)
            # Set anchor to bottom center so that it's easy to align tiles to game board later
            block.anchor_x = block.width / 2
            gem.anchor_x = gem.width / 2
            # Save Filename, convenient for unit testing
            block.color = color
            gem.color = color
            # Populate Lists
            self.block_list.append(block)
            self.gem_list.append(gem)
        return


class GamePiece:
    """
    Contains gem and block images (not sprites!)
    Used to create a game piece sprite
    Also describes status of each tile.
    """

    def __init__(
        self,
        gem: pyglet.image.TextureRegion,
        block: pyglet.image.TextureRegion,
        tile_status: TileStatus,
    ):
        self.gem = gem
        self.gem_color = gem.color  # type: ignore
        self.block_color = block.color  # type: ignore
        self.block = block
        self.tile_status = tile_status


class BoardSpace(pyglet.shapes.Polygon):
    """
    Describes a space on the board that tiles can be placed on.
    A diamond-shaped polygon with four coordinates, bottom, left, top, and right
    """

    def __init__(
        self,
        bottom: list[int],
        width_divisons: int,
        height_divisons: int,
        color: tuple[int],
        batch: pyglet.graphics.Batch,
        visible: bool = False,
        space_status: SpaceStatus = SpaceStatus.Free,
    ):
        # Use that to define left, right, top, coordinates, see GameBoardMath.png
        left = [bottom[0] - width_divisons, bottom[1] + height_divisons]
        right = [bottom[0] + width_divisons, bottom[1] + height_divisons]
        top = [bottom[0], bottom[1] + 2 * height_divisons]

        super().__init__(bottom, left, top, right, color=color, batch=batch)
        # TODO: Is this intended behavoir?
        self.visible = visible  # set visibility of space (probably False because shapes get drawn over sprites)

        # Params for mouse over event
        self.vertex_list = [tuple(x) for x in [bottom, left, top, right]]
        self.width_divisions = width_divisons
        self.height_divisions = height_divisons

        # Board spaces start out unoccupied
        self.space_status = space_status

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        """
        On mouse drag, determine if a space is actively selected
        """
        self.space_status = game.game_actions.is_board_space_selected(
            x, y, self.vertex_list, self.space_status  # type: ignore
        )


# class GameBoard:
#     """
#     Describes window and sprites in that window
#     """

#     def __init__(
#         self,
#         game_window: pyglet.window.Window = pyglet.window.Window(800, 600),
#         player_hand: list = [],
#         batch: pyglet.graphics.Batch = pyglet.graphics.Batch(),
#         color: tuple = (9, 4, 10),
#         tiles_per_row: int = 6,
#     ):
#         self.game_window = game_window
#         self.batch = batch
#         self.player_hand = player_hand
#         self.color = color
#         self.tiles_per_row = tiles_per_row
#         self.board_spaces: np.ndarray = np.empty(
#             (self.tiles_per_row, self.tiles_per_row), dtype=object
#         )  # No board spaced until drawn

#     def add_game_board_sprite(self, board_scale: float = 2):
#         """
#         Adds Game Board sprite to window
#         """
#         # Get Game Board Img
#         game_board_img = pyglet.resource.image("GameBoard.png")
#         # Place Anchor at image center
#         game_board_img.anchor_x = game_board_img.width / 2
#         game_board_img.anchor_y = game_board_img.height / 2

#         # Put in Sprite
#         self.game_board_sprite = pyglet.sprite.Sprite(
#             game_board_img,
#             x=self.game_window.width / 2,
#             y=self.game_window.height / 2,
#             batch=self.batch,
#             group=pyglet.graphics.OrderedGroup(0),
#         )
#         self.game_board_sprite.scale = board_scale

#     def define_board_spaces(self):
#         # Game board is made up of n x n spaces that we'll treat as a cartesion plane
#         # Space coord of Bottom-est space is 0, 0
#         # Space coord of right-est space is 0, n
#         # Space coord or left-ist space is n, 0

#         # height, width, and center point of gameboard
#         h = self.game_board_sprite.height
#         w = self.game_board_sprite.width
#         x_center = self.game_board_sprite.x
#         y_center = self.game_board_sprite.y

#         # Bounds of game board
#         board_bottom_coord = [x_center, y_center - h / 2]

#         # Divide the board into 2 n divisions to define spaces tiles can go on isometric board
#         # see GameBoardMath.png
#         s_w = round(w / (2 * self.tiles_per_row))
#         s_h = round(h / (2 * self.tiles_per_row))

#         # start at 0,0
#         # Loop through each square on the board
#         for y_space_coord in range(self.tiles_per_row):
#             # Define a color for debugging convencience
#             # self.color = (self.color[0] + 1, self.color[1], self.color[2])
#             for x_space_coord in range(self.tiles_per_row):
#                 # Place bottom coordinate depending on which space were on
#                 s_b = [
#                     board_bottom_coord[0] + s_w * (x_space_coord + y_space_coord * -1),
#                     board_bottom_coord[1] + s_h * (y_space_coord + x_space_coord),
#                 ]
#                 # Define a color for debugging convencience
#                 # self.color = (self.color[0] + 1, self.color[1], self.color[2] + 1)

#                 # Create board space as interactable object
#                 self.board_spaces[x_space_coord, y_space_coord] = BoardSpace(
#                     s_b, s_w, s_h, color=self.color, batch=self.batch, visible=False
#             )

# def get_game_objects(self):
#     """
#     Returns a list of all sprites on the board right now
#     """
#     return [self.game_board_sprite] + self.player_hand

# def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
#     """
#     Checks if player is dragging tile over board space and then snaps tile to spaces
#     """
#     game.game_actions.snap_tile_to_board_space(self.player_hand, self.board_spaces)

# # TODO: Convert to it's own function and write a test for it, also think a little on how to test grouping mechanism
# def on_mouse_release(self, x, y, button, modifier):
#     """
#     When you let go of the mouse, the tiles should no longer be active
#     """
#     # TODO: Assign ordered group numbers somehowwww???
#     draw_group = None
#     spaces_selected = 0
#     for idx, spaces_row in enumerate(self.board_spaces):
#         for jdx, space in enumerate(spaces_row):
#             if space.space_status == SpaceStatus.Selected:
#                 draw_group = 48 - (idx + jdx + 2) * 2
#                 spaces_selected += 1
#     if spaces_selected > 1:
#         raise Exception("More than one selected board space space was found")

#     for tile in self.player_hand:
#         if tile.active:
#             game.game_actions.deactivate_tiles(tile, draw_group)


class GamePieceSprite(pyglet.sprite.Sprite):
    """
    Empty sprite that includes both gem and block sprites as attributes,
    should be created only when spawned on the board.
    "active" is a boolean describing whether this is an active file.
    """

    def __init__(
        self,
        game_piece_info: GamePiece,
        draw_batch: pyglet.graphics.Batch,
        active: bool = False,
    ):
        self.block = pyglet.sprite.Sprite(
            game_piece_info.block,
            batch=draw_batch,
            group=pyglet.graphics.OrderedGroup(49),
        )
        self.block_color_str = game_piece_info.block_color
        self.gem = pyglet.sprite.Sprite(
            game_piece_info.gem,
            batch=draw_batch,
            group=pyglet.graphics.OrderedGroup(50),
        )
        self.gem_color_str = game_piece_info.gem_color

        # Tile status
        self.active = active  # Is player holding tile right now
        self.tile_status = game_piece_info.tile_status  # Is tile in bag, hand, or board

        super().__init__(pyglet.resource.image("None.png"), batch=draw_batch)

    def outline_tile(self, draw_batch):
        outlines = Outlines()
        group = self.gem.group.order + 1
        if self.tile_status == TileStatus.Selected:
            self.outline = pyglet.sprite.Sprite(
                img=outlines.active_outline,
                x=self.block.x,
                y=self.block.y + self.block.height / 2,
                batch=draw_batch,
                group=pyglet.graphics.OrderedGroup(group),
            )
        elif self.tile_status == TileStatus.PotentialSelection:
            self.outline = pyglet.sprite.Sprite(
                img=outlines.option_outline,
                x=self.block.x,
                y=self.block.y + self.block.height / 2,
                batch=draw_batch,
                group=pyglet.graphics.OrderedGroup(group),
            )
        else:
            if hasattr(self, "outline"):
                self.outline.delete()
                delattr(self, "outline")
            Warning(
                f"cannout use outline_tile() when status is '{self.tile_status.name}'"
            )

    def remove_outline(self):
        self.outline.delete()

    def on_mouse_press(self, x, y, button, modifier):
        """
        If a Tile gets clicked, define it as active
        """
        game.game_actions.click_tile_make_active(x, y, self)

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        """
        Click and Drag tiles around weeee
        """
        # Only drag if sprite is active
        if self.active:
            self.update(x=self.x + dx, y=y + dy)

    # TODO: Move this to game actions
    def update(
        self, x=None, y=None, rotation=None, scale=None, scale_x=None, scale_y=None
    ):
        """
        In addition to updating any parameters we want to update, also force gem and block sprites to move together
        adapted from pyglet.sprite.Sprite()
        """
        game.game_actions.update_game_piece(
            game_piece=self,
            x=x,
            y=y,
            rotation=rotation,
            scale=scale,
            scale_x=scale_x,
            scale_y=scale_y,
        )


class TilePool(GameAssets):
    """
    Describes the status of each tile in the tile pool
    """

    def __init__(
        self,
        no_sets: int = 3,
    ):
        # Game Pieces contains assets
        GameAssets.__init__(self)

        # Number of each tile present in a new pool
        self.no_sets = no_sets

        # Initialize the pool: Build a list of all tiles
        self.tiles = []
        # Dict of tuples key is index # and each tuple describes unique gem/block pair
        for set in range(no_sets):
            for block in self.block_list:
                for gem in self.gem_list:
                    self.tiles.append(
                        GamePiece(
                            gem=gem,
                            block=block,
                            tile_status=TileStatus.Bag,
                        )
                    )
        return

    def draw_tiles(self, no_tiles: int, status: TileStatus) -> list[GamePiece]:
        """
        Draw an initial hand
        """
        # Select six random tiles
        tiles_drawn = list(np.random.choice(self.tiles, no_tiles, replace=False))
        # Remove those tiles from the bag & place in hand
        for tile in tiles_drawn:
            self.tiles.remove(tile)
            tile.tile_status = status

        return tiles_drawn

    def report_tile_pool_size(self):
        return len(self.tiles)


class PlayerHand:
    """
    Describes the status of a player's hand
    """

    def __init__(
        self,
        hand_size: int,
        hand_scale: float,
        tile_pool: TilePool,
        window: pyglet.window.Window,
        draw_batch: pyglet.graphics.Batch,
    ):
        """
        Create sprites for a game window and return as a single batch
        """
        self.hand_size = hand_size
        self.hand_scale = hand_scale  # how big to make tiles in hand
        self.draw_batch = draw_batch
        self.window = window
        # draw first tiles (draw like cards)
        drawn_tiles = tile_pool.draw_tiles(hand_size, TileStatus.Hand)

        # TODO: programatically calculated spacer size
        self.spacer = 50 * self.hand_scale  # distance between tiles in hand
        hand_x = window.width / 2 - self.spacer  # Center your hand on x
        hand_y = 25  # hand's distance from bottom of window

        self.player_hand = []
        for idx, tile in enumerate(drawn_tiles):
            # X position and Y position of each tile, 2 x 3
            x = (idx % 3 * self.spacer) + hand_x
            y = (idx % 2 * self.spacer) + hand_y
            # Place block and gem for one tile in two sprites with some coordinates
            game_piece_sprite = GamePieceSprite(
                tile, draw_batch=draw_batch, active=False
            )
            # Scale accordingly
            game_piece_sprite.update(x=x, y=y, scale=self.hand_scale)

            # Update Gamepiece status
            tile.tile_status = TileStatus.Hand

            # Add both block and gem to sprite batch
            self.player_hand.append(game_piece_sprite)

    def __iter__(self):
        return iter(self.player_hand)

    def __getitem__(self, key):
        return self.player_hand[key]

    def on_mouse_press(self, x, y, button, modifiers):
        # Get selected tile
        for tile in self.player_hand:
            if game.game_actions.was_tile_clicked(x, y, tile):
                tile.tile_status = TileStatus.Selected
            else:
                tile.tile_status = TileStatus.Hand

    def on_mouse_release(self, x, y, button, modifiers):
        for tile in self.player_hand:
            tile.outline_tile(self.draw_batch)


class Game:
    def __init__(
        self,
        board_size: int = 6,
        no_sets: int = 3,
        hand_size: int = 6,
        game_window: pyglet.window.Window = pyglet.window.Window(800, 600),
        draw_batch: pyglet.graphics.Batch = pyglet.graphics.Batch(),
        game_scale: float = 1,
        # game_board: GameBoard = GameBoard(),
    ):
        self.draw_batch = draw_batch
        self.board_size = board_size
        self.game_window = game_window
        self.game_scale = game_scale
        self.tile_pool = TilePool(no_sets)
        self.player_hand = PlayerHand(
            hand_size, game_scale, self.tile_pool, game_window, draw_batch
        )
        # self.game_board = game_board

    def _get_game_objects(self):
        return self.player_hand

    def add_event_handlers(self):
        """
        Add player hand sprites, board spaces, to event handlers
        """
        self.game_window.push_handlers(self)
        self.game_window.push_handlers(self.player_hand)
        for tile in self.player_hand:
            self.game_window.push_handlers(tile)

        # for col in self.board_spaces:
        #     for space in col:
        #         self.game_window.push_handlers(space)

    def update(self, dt):
        """
        Runs all sprites update() function
        """
        objs = self._get_game_objects()
        for obj in objs:
            obj.update()
