import unittest
import pyglet
import __main__
from pathlib import Path
import game.game_setup
import game.game_actions
from game.game_utils import TileStatus, SpaceStatus
from game.game.game_actions import deactivate_tiles

# Find and Set Resources path relative to module (necessary for running tests in VSC)
module_dir = Path(game.__file__)  # type: ignore
repo_dir = str(module_dir.parent.absolute().parent.absolute().parent.absolute())
pyglet.resource.path = [f"{repo_dir}/resources"]
pyglet.resource.reindex()


class TestGameActions(unittest.TestCase):
    """
    Unit tests to make sure game actions are handled correctly
    """

    def setUp(self):
        ### Initialize game ###
        self.game_board = game.game_setup.GameBoard()
        self.game_tiles = game.game_setup.TilePool()

        ### Place Gameboard ###
        self.game_board.add_game_board_sprite()
        self.game_board.define_board_spaces()

        ### Initialize Hand ###
        self.player_hand = game.game_setup.PlayerHand()
        self.player_hand = self.game_tiles.pull_new_hand(
            self.player_hand
        )  # Draw hand from the available game_tiles
        self.game_board = self.player_hand.build_hand_tiles_sprites(
            self.game_board
        )  # Build the hand's sprites on the game board

    def test_board_space_selected(self):
        # Test when mouse inside board space, space is selected

        # Use 0,0 space to test with
        space = self.game_board.board_spaces[0][0]

        # Place "mouse cursor" in center of space
        mouse_x = (space.vertex_list[1][0] + space.vertex_list[3][0]) / 2
        mouse_y = (space.vertex_list[0][1] + space.vertex_list[2][1]) / 2

        self.assertEqual(
            game.game_actions.is_board_space_selected(
                mouse_x, mouse_y, space.vertex_list, space.space_status
            ),
            SpaceStatus.Selected,
        )

    def test_board_space_not_selected(self):
        """
        Test when mouse isn't in board space, a space is deselected
        """

        # Use 0,0 space to test with
        space = self.game_board.board_spaces[0][0]

        space.space_status = SpaceStatus.Selected
        # Place "mouse cursor" in center of space
        mouse_x = -1
        mouse_y = -1

        self.assertEqual(
            game.game_actions.is_board_space_selected(
                mouse_x, mouse_y, space.vertex_list, space.space_status
            ),
            SpaceStatus.Free,
        )

    def test_space_gets_deselected_after_tile_leaves(self):
        """
        Test that selected space gets deselected (integrational I think?)
        """
        self.game_board.player_hand[0].active = True
        test_space = self.game_board.board_spaces[0][0]
        test_space.space_status = SpaceStatus.Selected
        game.game_actions.snap_tile_to_board_space(
            self.game_board.player_hand, self.game_board.board_spaces
        )

    def test_click_tile_make_active(self):
        tile = self.game_board.player_hand[0]
        x = tile.x + tile.width / 2
        y = tile.y + tile.height / 2
        game.game_actions.click_tile_make_active(x, y, tile)

        self.assertTrue(tile.active)

    def test_active_tile_scale(self):
        tile = self.game_board.player_hand[0]
        x = tile.x + tile.width / 2
        y = tile.y + tile.height / 2
        game.game_actions.click_tile_make_active(x, y, tile)

        self.assertEqual(tile.scale, self.player_hand.hand_scale * 2)

    def test_deactivate_tile(self):
        # Make tile active first
        tile = self.game_board.player_hand[0]
        x = tile.x + tile.width / 2
        y = tile.y + tile.height / 2
        game.game_actions.click_tile_make_active(x, y, tile)
        game.game_actions.deactivate_tiles(tile, 0)
        self.assertFalse(tile.active)
        # Tile status is in hand, so it should return to normal scale
        self.assertEqual(tile.scale, self.player_hand.hand_scale)

    def test_update_game_piece(self):
        tile = self.game_board.player_hand[0]
        x = 0
        y = 0
        rotation = 90
        scale = 3
        game.game_actions.update_game_piece(tile, x, y, rotation, scale)
        self.assertEqual(self.game_board.player_hand[0].x, 0, "X postion failed")
        self.assertEqual(self.game_board.player_hand[0].y, 0, "Y postion failed")
        self.assertEqual(
            self.game_board.player_hand[0].rotation, 90, "rotation postion failed"
        )
        self.assertEqual(
            self.game_board.player_hand[0].scale, 3, "scale postion failed"
        )
