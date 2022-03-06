import unittest
import pyglet
import os
import __main__
from pathlib import Path
import game
import game.game_setup
import game.game_utils


# Find and Set Resources path relative to module (necessary for running tests in VSC)
module_dir = Path(game.__file__)
repo_dir = str(module_dir.parent.absolute().parent.absolute())

pyglet.resource.path = [f"{repo_dir}/resources"]
pyglet.resource.reindex()


class TestAssets(unittest.TestCase):
    """
    Integrational Tests: Test game assets are accesible and named as expected
    """

    def setUp(self):
        """
        Get a hand and game tiles
        """
        ### Initialize game ###
        self.game = game.game_setup.Game()
        self.game_assets = game.game_setup.GameAssets()

    def test_detect_resources(self):
        """
        Test that example png is in resources directory and there are at least 2 *
        colors assets in the resources folder
        """
        self.assertIn("Block_Pink.png", os.listdir(pyglet.resource.path[0]))

    def test_block_gem_assets(self):
        """
        Test that example png is in resources directory and there are at least 2 *
        colors assets in the resources folder
        """
        self.assertEqual(
            len(self.game_assets.gem_list), len(game.game_utils.TileColors)
        )
        self.assertEqual(
            len(self.game_assets.block_list), len(game.game_utils.TileColors)
        )

    def test_no_of_assets(self):
        """
        Test that the right number of game blocks and gems are loaded
        """
        self.assertEqual(
            len(self.game_tiles.tiles),
            len(game.game_setup.COLORS) ** 2 * self.game_tiles.no_sets,
        )

    def test_game_init_no_tiles(self):
        """
        Test that the right number game tiles are present at the beginning of the game
        """
        self.assertEqual(
            len(self.game_tiles.tiles),
            len(game.game_setup.COLORS) ** 2 * self.game_tiles.no_sets,
        )

    def test_game_board_sprite(self):
        """
        Confirm game board exists
        """
        self.assertIsInstance(self.game_board.game_board_sprite, pyglet.sprite.Sprite)


class TestGameSetup(unittest.TestCase):
    """
    Unit tests to make sure assets are placed correctly during setup
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
        # TODO: test that sprites don't overlap
        self.game_board = self.player_hand.build_hand_tiles_sprites(
            self.game_board
        )  # Build the hand's sprites on the game board

    def test_game_board_sprite(self):
        """
        Confirm game board gets placed in center of board
        """
        self.assertEqual(
            self.game_board.game_board_sprite.x, self.game_board.game_window.width / 2
        )
        self.assertEqual(
            self.game_board.game_board_sprite.y, self.game_board.game_window.height / 2
        )

    def test_player_hand_size(self):
        """
        Confirm that the correct # of assets were drawn
        """
        self.assertEqual(len(self.player_hand.player_hand), self.player_hand.hand_size)

    def test_tiles_removed_after_draw(self):
        """
        Confirm the tile pool gets smaller after drawing a hand
        """
        self.assertEqual(
            len(self.game_tiles.tiles),
            len(game.game_setup.COLORS) ** 2 * self.game_tiles.no_sets
            - self.player_hand.hand_size,
        )

    def test_player_tiles_are_sprites(self):
        self.assertIsInstance(self.game_board.player_hand[0], pyglet.sprite.Sprite)

    def test_game_piece_sprites_x(self):
        """
        tests if all the sprites in the game_piece_sprite object are together on the board
        """

        for idx, sprite in enumerate(self.game_board.player_hand):
            parent_sprite_x = sprite.x
            gem_sprite_x = sprite.gem.x
            block_sprite_x = sprite.block.x
            self.assertEqual(
                parent_sprite_x,
                block_sprite_x,
                f"{sprite.block_color_str} Block failed, index:{idx}",
            )
            self.assertEqual(
                parent_sprite_x, gem_sprite_x, f"{sprite.gem_color_str} Gem failed"
            )

    def test_game_piece_sprites_y(self):
        """
        tests if images of gems and block get put together to make a single sprite
        """

        for idx, sprite in enumerate(self.game_board.player_hand):
            parent_sprite_y = sprite.y
            gem_sprite_y = sprite.gem.y
            block_sprite_y = sprite.block.y
            self.assertEqual(
                parent_sprite_y,
                block_sprite_y,
                f"{sprite.block_color_str} Block failed, index:{idx}",
            )
            self.assertEqual(
                parent_sprite_y, gem_sprite_y, f"{sprite.gem_color_str} Gem failed"
            )

    def test_player_game_piece_correctly_placed(self):
        """
        tests if all the player's game piece sprite is correctly placed in hand.
        """
        x = self.game_board.game_window.width / 2 - self.player_hand.spacer

        self.assertEqual(self.game_board.player_hand[0].x, x, f"x failed")
        self.assertEqual(self.game_board.player_hand[0].y, 25, f"y failed")

    def test_board_spaces_placed_correct(self):
        """
        Check that board spaces are placed by seeing if last space is in expected spot (top middle of board)
        """
        self.game_board.board_spaces

        # Top space
        last_space = self.game_board.board_spaces[
            self.game_board.tiles_per_row - 1, self.game_board.tiles_per_row - 1
        ]

        x = self.game_board.game_window.width / 2
        y = (
            self.game_board.game_window.height / 2
            + self.game_board.game_board_sprite.height / 2
        ) - last_space.height_divisions * 2
        self.assertEqual(last_space.x, x, "Last tile space misaligned on X axis")
        self.assertAlmostEqual(
            last_space.y, y, delta=5, msg="Last tile space misaligned on Y axis"
        )

    def test_no_board_spaces(self):

        # Count elements in list-matrix of board spaces
        no_space = 0
        for x in self.game_board.board_spaces:
            for y in self.game_board.board_spaces:
                no_space += 1

        # No of spaces should be tiles per row squared
        self.assertEqual(no_space, self.game_board.tiles_per_row**2)


if __name__ == "__main__":
    unittest.main()
