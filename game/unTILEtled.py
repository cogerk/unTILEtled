import pyglet
import game.game_setup

### Define resources directory ###
pyglet.resource.reindex()

### Define Scaling Style as Neartest Neighbors ###
# MUST BE FIRST to work
pyglet.font.base.Font.texture_min_filter = pyglet.gl.GL_NEAREST  # type: ignore
pyglet.font.base.Font.texture_mag_filter = pyglet.gl.GL_NEAREST  # type: ignore
pyglet.image.Texture.default_min_filter = pyglet.gl.GL_NEAREST
pyglet.image.Texture.default_mag_filter = pyglet.gl.GL_NEAREST

# # TODO: Make this its own class if necessary
# ### Initialize game ###
# game_board = game.game_setup.GameBoard()
# game_tiles = game.game_setup.TilePool()

# ## Add Gameboard ##
# game_board.add_game_board_sprite()
# game_board.define_board_spaces()

# ### Initialize Hand And Draw First Tiles ###
# player_hand = game.game_setup.PlayerHand()
# player_hand = game_tiles.pull_new_hand(
#     player_hand
# )  # Draw hand from the available game_tiles
# game_board = player_hand.build_hand_tiles_sprites(game_board)

# TODO: Turn these labels into prettier images and put labels in their own module that GameBoard() accesses


new_game = game.game_setup.Game()


# ### Load Font ###
# pyglet.resource.add_font("BAUHS93.TTF")

### Set BG color: ###
pyglet.gl.glClearColor(9 / 255, 4 / 255, 10 / 255, 255)

# Labels, when using a custom font, you have to use it's full name (dbl click ttf file)
title = pyglet.text.Label(
    text="UnTILEtled",
    font_name="Bauhaus 93",
    y=new_game.game_window.height,
    x=10,
    anchor_x="left",
    anchor_y="top",
    font_size=72,
)

your_hand_text = pyglet.text.Label(
    text="Your Hand:",
    font_name="Bauhaus 93",
    y=new_game.player_hand[3].y + 50 * new_game.game_scale,
    x=new_game.player_hand[3].x,
    anchor_x="right",
    anchor_y="baseline",
    font_size=24,
)

### Draw it ###
@new_game.game_window.event
def on_draw():
    # draw things here
    new_game.game_window.clear()
    title.draw()
    your_hand_text.draw()
    new_game.draw_batch.draw()


# # Print events executed in the window (for debugging)
# event_logger = pyglet.window.event.WindowEventLogger().on_mouse_press
# new_game.game_window.push_handlers(event_logger)
new_game.add_event_handlers()

### Run it ###
if __name__ == "__main__":
    pyglet.clock.schedule_interval(new_game.update, 1 / 60)
    pyglet.app.run()
