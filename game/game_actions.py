from __future__ import annotations
from typing import TYPE_CHECKING
from dataclasses import dataclass
import numpy as np

if TYPE_CHECKING:
    import game_setup
    import numpy as np

import pyglet
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from game.game_utils import TileStatus, SpaceStatus

### Defines how board reacts to user actions


def is_board_space_selected(
    mouse_x: int,
    mouse_y: int,
    board_space_vertices: list[tuple[int]],
    space_status: SpaceStatus,
):
    """Detemines in X & Y coordinates are within a given board space

    Args:
        mouse_x (int): X coordinate of mouse cursor
        mouse_y (int): Y coordinate of mouse cursor
        board_space_vertices (list[list[int]]): list of vertices describing a board space

    Returns:
        bool: True only if mouse cursor is inside of board space
    """
    if space_status is not SpaceStatus.Occupied:
        # Use Shapely to determine if polygon contains the point
        point = Point(mouse_x, mouse_y)
        polygon = Polygon(board_space_vertices)

        # If it does, space is selected
        if polygon.contains(point):
            return SpaceStatus.Selected
        else:
            return SpaceStatus.Free


def snap_tile_to_board_space(
    player_hand: list[game_setup.GamePieceSprite],
    board_spaces: np.ndarray,
):
    """_summary_

    Args:
        player_hand (game_setup.PlayerHand): Tiles in a players hand
        board_spaces (game_setup.GameBoard): Current state of game board
    """
    for tile in player_hand:
        # If Tile is current active (held by player cursor)
        if tile.active:
            tile.tile_status = TileStatus.Hand
            # And dragging tile over a board space
            for y_space_coord in range(board_spaces.shape[0]):
                for x_space_coord in range(board_spaces.shape[1]):
                    current_space = board_spaces[x_space_coord][y_space_coord]
                    # Snap to actively selected space
                    if current_space.space_status == SpaceStatus.Selected:
                        draw_group = 40 - (y_space_coord + x_space_coord + 2) * 2
                        tile.block.group = pyglet.graphics.OrderedGroup(draw_group - 1)
                        tile.gem.group = pyglet.graphics.OrderedGroup(draw_group)
                        # Align tile to bottom corner so it snaps to board space
                        tile.update(
                            x=current_space.vertex_list[0][0],
                            y=current_space.vertex_list[0][1],
                        )
                        tile.tile_status = TileStatus.BoardThinking


# TODO: Test
def was_tile_clicked(
    mouse_x: int, mouse_y: int, tile: game_setup.GamePieceSprite
) -> bool:
    """
    Determine if a tile was clicked

    Args:
        mouse_x (int): mouse x position
        mouse_y (int): mouse y position
        tile (game_setup.GamePieceSprite): tile sprite current in the game window

    Returns:
        bool: whether or not tile was clicked
    """
    current_sprite_x_bounds = (
        tile.x - tile.block.width / 2,
        tile.x + tile.block.width / 2,
    )  # have to use block width bc parent sprite is 1x1
    current_sprite_y_bounds = (tile.y, tile.y + tile.block.height)
    # Did the mouse click the sprite?
    tile_was_clicked = (
        current_sprite_x_bounds[0] < mouse_x < current_sprite_x_bounds[1]
    ) and (current_sprite_y_bounds[0] < mouse_y < current_sprite_y_bounds[1])
    return tile_was_clicked


# TODO: Test
def find_shared_feature_tiles(
    tile: game_setup.GamePieceSprite, player_hand: list[game_setup.GamePieceSprite]
):
    """
    Call a given tile(s) "selected" and highlight other tiles with shared features

    Args:
        tile (game_setup.GamePieceSprite): Selected tile
        player_hand (list[game_setup.GamePieceSprite]): Player hand of tiles to highlight shared features in
    """
    tile.tile_status = TileStatus.Selected  # make tile selected
    # Get the clicked tiles features
    gem_color = tile.gem_color
    block_color = tile.block_color

    # Go through the other tiles and note tiles that share a feature as a potential
    temp_hand = player_hand.copy()
    temp_hand.remove(tile)
    for other_tiles in temp_hand:
        share_gem_color = other_tiles.gem_color == gem_color
        share_block_color = other_tiles.block_color == block_color
        if share_gem_color or share_block_color:
            other_tiles.tile_status = TileStatus.PotentialSelection
    # The clicked tile should be selected


# TODO: Test
def create_game_board_sprite(
    x: int, y: int, batch: pyglet.graphics.Batch, board_scale: float = 2
) -> pyglet.sprite.Sprite:
    """Create the game board sprite

    Args:
        x (int): center image on this x
        y (int): center image on this y
        batch (pyglet.graphics.Batch): batch to draw sprite with
        board_scale (float, optional): size of board scale Defaults to 2.

    Returns:
        pyglet.sprite.Sprite: game board sprite
    """
    # Get Game Board Img
    game_board_img = pyglet.resource.image("GameBoard.png")
    # Place Anchor at image center
    game_board_img.anchor_x = game_board_img.width / 2
    game_board_img.anchor_y = game_board_img.height / 2

    # Put in Sprite
    game_board_sprite = pyglet.sprite.Sprite(
        game_board_img,
        x=x,
        y=y,
        batch=batch,
        group=pyglet.graphics.OrderedGroup(0),
    )
    game_board_sprite.scale = board_scale
    return game_board_sprite


@dataclass
class BoardSpaceGenerator:
    """Describe a board space for the BoardSpace class"""

    bottom_coord: Point
    width_divider: int
    height_divider: int = 0
    color: tuple[int, int, int] = (9, 4, 10)


# TODO: Test
def create_game_board_spaces(
    h: int,
    w: int,
    x_center: int,
    y_center: int,
    n: int,
    color: tuple[int, int, int] = (9, 4, 10),
):
    # Bounds of game board
    board_bottom_coord = [x_center, y_center - h / 2]

    # Divide the board into 2 n divisions to define spaces tiles can go on isometric board
    # see GameBoardMath.png
    s_w = round(w / (2 * n))
    s_h = round(h / (2 * n))

    # start at 0,0
    # Loop through each square on the board
    board_spaces = np.empty([n, n], dtype=BoardSpaceGenerator)
    for y_space_coord in range(n):
        # Define a color for debugging convencience
        color = (color[0] + 1, color[1], color[2])
        for x_space_coord in range(n):
            # Place bottom coordinate depending on which space were on
            s_b = Point(
                board_bottom_coord[0] + s_w * (x_space_coord + y_space_coord * -1),
                board_bottom_coord[1] + s_h * (y_space_coord + x_space_coord),
            )
            # Define a color for debugging convencience
            color = (color[0] + 1, color[1], color[2] + 1)

            # Create board space as interactable object
            board_spaces[x_space_coord, y_space_coord] = BoardSpaceGenerator(
                s_b, s_w, s_h
            )
    return board_spaces


def click_tile_make_active(
    mouse_x: int, mouse_y: int, game_piece: game_setup.GamePieceSprite
):
    """
    If a tile from hand is clicked, it becomes active

    Args:
        mouse_x (int): mouse x coord
        mouse_y (int): mouse y coord
        game_piece (game.game_setup.GamePieceSprite): game piece to check
    """
    # Only react if Tile is in hand
    if game_piece.tile_status == TileStatus.Hand:
        # Get coordinates bounding the sprite

        if game_piece.active:
            game_piece.update(scale=game_piece.scale * 2)


# TODO Move this function to on_release for game board and then use the sum of board space indices to determine draw group
def deactivate_tiles(game_piece: game_setup.GamePieceSprite, draw_group: int | None):
    trigger_tile_update = False
    # Once you let go of mouse, tile is no longer active
    if game_piece.active:
        game_piece.active = False
        # If tile was over a board space, it is now officially placed
        if game_piece.tile_status is TileStatus.BoardThinking:
            game_piece.tile_status = TileStatus.BoardPlaced
            # TODO: replace this with a function that draws new tiles and removes them from the tile pool
            trigger_tile_update = True  # If a tile is placed we need to update the playerhand and tile pool
        # If tile isn't on a board spot, return it to scale
        else:
            game_piece.block.group = pyglet.graphics.OrderedGroup(49)
            game_piece.gem.group = pyglet.graphics.OrderedGroup(50)
            game_piece.update(scale=game_piece.scale / 2)
    return trigger_tile_update


def update_game_piece(
    game_piece: game_setup.GamePieceSprite,
    x: int | None = None,
    y: int | None = None,
    rotation: int | None = None,
    scale: int | None = None,
    scale_x: int | None = None,
    scale_y: int | None = None,
):
    spirtes_to_update = [game_piece, game_piece.gem, game_piece.block]

    spirtes_to_update.append(game_piece.outline) if hasattr(
        game_piece, "outline"
    ) else None

    for sprite in spirtes_to_update:
        if y is not None:
            sprite.y = y
        if x is not None:
            sprite.x = x
        if rotation is not None:
            sprite.rotation = rotation
        if scale is not None:
            sprite.scale = scale
        if scale_x is not None:
            sprite.scale_x = scale_x
        if scale_y is not None:
            sprite.scale_y = scale_y

    if hasattr(game_piece, "outline") and y is not None:
        game_piece.outline.y = y + game_piece.block.height / 2
