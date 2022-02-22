import numpy as np
from operator import itemgetter
import pyglet


COLORS = ['Pink', 'Purple', 'Indigo', 'Blue', 'Aqua', 'Green']


# Set Resources Directory
pyglet.resource.path = ['../resources']
pyglet.resource.reindex()


# Load all block and gem images into a matrix of images 2 x 6 in size
class GamePieces:
    def __init__(self):
    # Create list of block and gem resources, respectively
        self.block_list = []
        self.gem_list = []
        for color_idx in range(len(COLORS)):
            # Build File Names
            block_file_name = f"Block_{COLORS[color_idx]}.png"
            gem_file_name = f"Gem_{COLORS[color_idx]}.png"
            # Populate Lists
            self.block_list.append(pyglet.resource.image(block_file_name))
            self.gem_list.append(pyglet.resource.image(gem_file_name))
        return

class AvailableTiles(GamePieces):
    def __init__(self, no_sets: int=3):
        # List of all assets
        GamePieces.__init__(self)
        self.no_sets = no_sets
        self.tiles = {}
        # Dict of tuples key is index # and each tuple describes unique gem/block pair
        i=0
        for set in range(no_sets):
            for block in self.block_list:
                for gem in self.gem_list:
                    self.tiles[i] = (block, gem)
                    i += 1
        return


class PlayerHand(AvailableTiles): 
    def __init__(self):
        # Get Available Tiles
        AvailableTiles.__init__(self)

    def pull_first_hand(self, no_tiles: int=6):
        """
        Draw an initial hand
        """
        # Select six random tiles using index keys in the available_tiles dict
        hand_idxs = np.random.choice(list(self.tiles.keys()), no_tiles, replace=False)
        self.hand = itemgetter(*tuple(hand_idxs))(self.tiles)
        
        [self.tiles.pop(idx) for idx, tile in enumerate(self.hand)]
        return self.hand
    
    def build_hand_tiles_sprites(self, game_window: pyglet.window, sprite_scale):
        """
        Create sprites for a game window and return as a single batch
        """
        # Coordinates of tiles in hand
        spacer = 50 * sprite_scale # distance between tiles in hand
        hand_x=game_window.width/2-spacer # Center your hand on x 
        hand_y=25 # hand's distance from bottom of window

        # Put all resources for hand in a batch of sprites
        batch = pyglet.graphics.Batch()
        my_hands_sprites = []
        for idx, tiles in enumerate(self.hand):
            # X position and Y position of each tile, 2 x 3
            x = (idx % 3 * spacer) + hand_x
            y = (idx % 2 * spacer) + hand_y
            # Place block and gem for one tile in two sprites with some coordinates
            block_sprite = pyglet.sprite.Sprite(tiles[0], x, y, batch=batch)
            gem_sprite = pyglet.sprite.Sprite(tiles[1], x, y, batch=batch)
            # Scale accordingly
            block_sprite.scale = sprite_scale
            gem_sprite.scale = sprite_scale
            # Add both block and gem to sprite batch
            my_hands_sprites.append(block_sprite)
            my_hands_sprites.append(gem_sprite)
        return batch, my_hands_sprites