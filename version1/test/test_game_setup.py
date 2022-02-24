import unittest
import pyglet
import game
import game.game_setup
import os
import __main__
from pathlib import Path


# Find and Set Resources path relative to module (necessary for running tests in VSC)
module_dir = Path(game.__file__)
repo_dir = str(module_dir.parent.absolute().parent.absolute().parent.absolute())
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
        self.game_board = game.game_setup.GameBoard()
        self.game_tiles = game.game_setup.TilePool(self.game_board)

        ## Add Gameboard ##
        # TODO: set this function
        self.game_board.add_game_board_sprite()

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
        self.assertEqual(len(self.game_tiles.gem_list), len(game.game_setup.COLORS))
        self.assertEqual(len(self.game_tiles.block_list), len(game.game_setup.COLORS))

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


class TestGameSetup(unittest.TestCase):
    def setUp(self):
        ### Initialize game ###
        self.game_board = game.game_setup.GameBoard()
        self.game_tiles = game.game_setup.TilePool(self.game_board)

        ### Initialize Hand ###
        self.player_hand = game.game_setup.PlayerHand()
        self.player_hand = self.game_tiles.pull_new_hand(
            self.player_hand
        )  # Draw hand from the available game_tiles
        # TODO: test that sprites don't overlap
        self.game_board = self.player_hand.build_hand_tiles_sprites(
            self.game_board
        )  # Build the hand's sprites on the game board

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
        self.assertIsInstance(
            self.game_board.player_hand_sprites[0], pyglet.sprite.Sprite
        )

    def test_game_piece_sprites_x(self):
        """
        tests if all the sprites in the game_piece_sprite object are together on the board
        """

        for idx, sprite in enumerate(self.game_board.player_hand_sprites):
            parent_sprite_x = sprite.x
            gem_sprite_x = sprite.gem.x
            block_sprite_x = sprite.block.x
            # TODO: Add resource name to message
            self.assertEqual(parent_sprite_x, block_sprite_x, f"{idx} Block failed")
            self.assertEqual(parent_sprite_x, gem_sprite_x, f"{idx} Gem failed")

    def test_game_piece_sprites_y(self):
        """
        tests if all the sprites in the game_piece_sprite object are together on the board
        """

        for idx, sprite in enumerate(self.game_board.player_hand_sprites):
            parent_sprite_y = sprite.y
            gem_sprite_y = sprite.gem.y
            block_sprite_y = sprite.block.y
            # TODO: Add resource name to message,
            self.assertEqual(parent_sprite_y, block_sprite_y, f"{idx} Block failed")
            self.assertEqual(parent_sprite_y, gem_sprite_y, f"{idx} Gem failed")

    def test_player_game_piece_correctly_placed(self):
        """
        tests if all the player's game piece sprite is correctly placed on board.
        """
        x = self.game_board.game_window.width / 2 - self.player_hand.spacer

        self.assertEqual(self.game_board.player_hand_sprites[0].x, x, f"x failed")
        self.assertEqual(self.game_board.player_hand_sprites[0].y, 25, f"y failed")


if __name__ == "__main__":
    unittest.main()
