import enum
import numpy as np
import pyglet
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

COLORS = ["Pink", "Purple", "Indigo", "Blue", "Aqua", "Green"]
pyglet.resource.path = ["../../resources"]
pyglet.resource.reindex()


# Load all block and gem images into a matrix of images 2 x 6 in size
class GameAssets:
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

        # Is space selected
        self.space_selected = False

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        # Is mouse dragging over space?
        # Use Shapely to determine if polygon contains the point

        point = Point(x, y)
        polygon = Polygon(self.vertex_list)
        if polygon.contains(point):
            self.space_selected = True
        else:
            self.space_selected = False

    def on_mouse_release(self, x, y, button, modifiers):
        self.space_selected = False


class GameBoard:
    """
    Describes window and sprites in that window
    """

    def __init__(
        self,
        game_window: pyglet.window = pyglet.window.Window(800, 600),
        player_hand_sprites: list["pyglet.sprite.Sprite"] = [],
        batch: pyglet.graphics.Batch = pyglet.graphics.Batch(),
        color: tuple = (9, 4, 10),
        tiles_per_row: int = 6,
    ):
        self.game_window = game_window
        self.batch = batch
        self.player_hand_sprites = player_hand_sprites
        self.color = color
        self.tiles_per_row = tiles_per_row

    def add_game_board_sprite(self, board_scale: float = 2):
        """
        Adds Game Board sprite to window
        """
        # Get Game Board Img
        game_board_img = pyglet.resource.image("GameBoard.png")
        # Place Anchor at image center
        game_board_img.anchor_x = game_board_img.width / 2
        game_board_img.anchor_y = game_board_img.height / 2

        # Put in Sprite
        self.game_board_sprite = pyglet.sprite.Sprite(
            game_board_img,
            x=self.game_window.width / 2,
            y=self.game_window.height / 2,
            batch=self.batch,
        )
        self.game_board_sprite.scale = board_scale

    # TODO: Maybe combine this and above function into a "gameboard class" and make this class a "game" class
    def define_board_spaces(self):
        # Game board is made up of n x n spaces that we'll treat as a cartesion plane
        # Space coord of Bottom-est space is 0, 0
        # Space coord of right-est space is 0, n
        # Space coord left-ist space is n, 0

        # height, width, and center point of gameboard
        h = self.game_board_sprite.height
        w = self.game_board_sprite.width
        x_center = self.game_board_sprite.x
        y_center = self.game_board_sprite.y

        # Bounds of game board
        board_bottom_coord = [x_center, y_center - h / 2]

        # Divide the board into 2 n divisions to define spaces tiles can go on isometric board
        # see GameBoardMath.png
        s_w = w / (2 * self.tiles_per_row)
        s_h = h / (2 * self.tiles_per_row)

        # start at 0,0
        # Loop through each square on the board
        self.board_spaces = np.empty((6, 6), dtype=object)
        for y_space_coord in range(6):
            self.color = (self.color[0] + 1, self.color[1], self.color[2])
            for x_space_coord in range(6):
                # Place bottom coordinate depending on which space were on
                x_space_coord = 0
                y_space_coord = 0
                s_b = [
                    board_bottom_coord[0] + s_w * (x_space_coord + y_space_coord * -1),
                    board_bottom_coord[1] + s_h * (y_space_coord + x_space_coord),
                ]
                self.color = (self.color[0] + 1, self.color[1], self.color[2] + 1)
                self.board_spaces[x_space_coord, y_space_coord] = BoardSpace(
                    s_b, s_w, s_h, color=self.color, batch=self.batch, visible=False
                )

    def get_game_objects(self):
        """
        Returns a list of all sprites on the board right now
        """
        return [self.game_board_sprite] + self.player_hand_sprites

    def add_event_handlers(self):
        """
        Add player hand sprites, board spaces, to event handlers
        """
        for tile in self.player_hand_sprites:
            self.game_window.push_handlers(tile)
        for col in self.board_spaces:
            for space in col:
                self.game_window.push_handlers(space)

    def update(self, dt):
        """
        Runs all sprites update() function
        """
        objs = self.get_game_objects()
        for obj in objs:
            obj.update()


class TileStatus(enum.Enum):
    Bag = 0
    Hand = 1
    Board = 2


class GamePiece:
    """
    Contains gem and block images (not sprites!)
    Used to create a game piece sprite
    Also describes status of each tile.
    """

    def __init__(
        self,
        gem: pyglet.resource.image,
        block: pyglet.resource.image,
        tile_status: TileStatus,
    ):
        self.gem = gem
        self.block = block
        self.tile_status = tile_status


class GamePieceSprite(pyglet.sprite.Sprite):
    """
    Empty sprite that includes both gem and block sprites as attributes,
    should be created only when spawned on the board.
    "active" is a boolean describing whether this is an active file.
    """

    def __init__(
        self,
        game_piece_info: GamePiece,
        batch: pyglet.graphics.Batch(),
        active: bool = False,
    ):
        self.block = pyglet.sprite.Sprite(game_piece_info.block, batch=batch)
        self.gem = pyglet.sprite.Sprite(game_piece_info.gem, batch=batch)
        self.tile_status = game_piece_info.tile_status
        self.active = active
        super().__init__(pyglet.resource.image("None.png"), batch=batch)

    def on_mouse_press(self, x, y, button, modifier):
        # Get coordinates bounding the sprite
        current_sprite_x_bounds = (
            self.x,
            self.x + self.block.width,
        )  # have to use block width bc parent sprite is 1x1
        current_sprite_y_bounds = (self.y, self.y + self.block.height)
        # Did the mouse click the sprite?
        self.active = (
            current_sprite_x_bounds[0] < x < current_sprite_x_bounds[1]
        ) and (current_sprite_y_bounds[0] < y < current_sprite_y_bounds[1])
        if self.active:
            self.update(scale=self.scale * 2)

    def on_mouse_release(self, x, y, button, modifier):
        if self.active:
            self.active = False
            self.update(scale=self.scale / 2)

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        """
        Click and Drag tiles around weeee
        """
        # Only drag if sprite is active
        if self.active:
            self.update(x=self.x + dx, y=y + dy)

    def update(
        self, x=None, y=None, rotation=None, scale=None, scale_x=None, scale_y=None
    ):
        """
        In addition to updating any parameters we want to update, also force gem and block sprites to move together
        adapted from pyglet.sprite.Sprite()
        """
        for sprite in [self, self.gem, self.block]:
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


class PlayerHand:
    """
    Describes the status of a player's hand
    """

    def __init__(self, hand_size: int = 6, hand_scale: int = 1):
        self.hand_size = hand_size
        self.player_hand = []  # Player hasn't drawn tiles
        self.hand_scale = hand_scale  # how big to make tiles in hand

    def build_hand_tiles_sprites(
        self,
        game_board: GameBoard,
    ):
        """
        Create sprites for a game window and return as a single batch
        """
        # Coordinates of tiles in hand
        # TODO: programatically calculated spacer size
        self.spacer = 50 * self.hand_scale  # distance between tiles in hand
        hand_x = game_board.game_window.width / 2 - self.spacer  # Center your hand on x
        hand_y = 25  # hand's distance from bottom of window

        # Put all resources for hand in a batch of sprites
        game_board.player_hand_sprites = []
        for idx, tile in enumerate(self.player_hand):
            # X position and Y position of each tile, 2 x 3
            x = (idx % 3 * self.spacer) + hand_x
            y = (idx % 2 * self.spacer) + hand_y
            # Place block and gem for one tile in two sprites with some coordinates
            game_piece_sprite = GamePieceSprite(
                tile, batch=game_board.batch, active=True
            )
            # Scale accordingly
            game_piece_sprite.update(x=x, y=y, scale=self.hand_scale)

            # Update Gamepiece status
            tile.status = TileStatus.Hand
            # Add both block and gem to sprite batch
            game_board.player_hand_sprites.append(game_piece_sprite)
        return game_board


class TilePool(GameAssets):
    """
    Describes the status of each tile in the tile pool
    """

    def __init__(
        self,
        game_board: GameBoard,
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

    def pull_new_hand(
        self, player_hand: PlayerHand = PlayerHand()
    ) -> list["GamePiece"]:
        """
        Draw an initial hand
        """
        # Select six random tiles
        player_hand.player_hand = np.random.choice(
            self.tiles, player_hand.hand_size, replace=False
        )
        # Remove those tiles from the pool
        [self.tiles.remove(tile) for tile in player_hand.player_hand]
        return player_hand
