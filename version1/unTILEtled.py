import pyglet
from pyglet.window import mouse
import game.game_setup

### Define resources directory ###
pyglet.resource.path = ["../resources"]
pyglet.resource.reindex()

### Define Scaling Style as Neartest Neighbors ###
# MUST BE FIRST to work
pyglet.font.base.Font.texture_min_filter = pyglet.gl.GL_NEAREST
pyglet.font.base.Font.texture_mag_filter = pyglet.gl.GL_NEAREST
pyglet.image.Texture.default_min_filter = pyglet.gl.GL_NEAREST
pyglet.image.Texture.default_mag_filter = pyglet.gl.GL_NEAREST

# TODO: Make this its own class if necessary
### Initialize game ###
game_board = game.game_setup.GameBoard()
game_tiles = game.game_setup.TilePool(game_board)

## Add Gameboard ##
game_board.add_game_board_sprite()

### Initialize Hand And Draw First Tiles ###
player_hand = game.game_setup.PlayerHand()
player_hand = game_tiles.pull_new_hand(
    player_hand
)  # Draw hand from the available game_tiles
game_board = player_hand.build_hand_tiles_sprites(game_board)

### Load Font ###
print(pyglet.resource.path)
pyglet.resource.add_font("BAUHS93.TTF")

### Set BG color: ###
pyglet.gl.glClearColor(9 / 255, 4 / 255, 10 / 255, 255)

# Labels, when using a custom font, you have to use it's full name (dbl click ttf file)
title = pyglet.text.Label(
    text="UnTILEtled",
    font_name="Bauhaus 93",
    y=game_board.game_window.height,
    x=10,
    anchor_x="left",
    anchor_y="top",
    font_size=72,
)

your_hand_text = pyglet.text.Label(
    text="Your Hand:",
    font_name="Bauhaus 93",
    y=game_board.player_hand_sprites[3].y + 50 * player_hand.hand_scale,
    x=game_board.player_hand_sprites[3].x,
    anchor_x="right",
    anchor_y="baseline",
    font_size=24,
)

### Draw it ###
@game_board.game_window.event
def on_draw():
    # draw things here
    game_board.game_window.clear()
    title.draw()
    your_hand_text.draw()
    game_board.batch.draw()


# @game_board.game_window.event
# def on_mouse_drag(x, y, dx, dy, button, modifiers):
#     sprite_x = (
#         game_board.player_hand_sprites[0].x,
#         game_board.player_hand_sprites[0].x + game_board.player_hand_sprites[0].width,
#     )
#     sprite_y = (
#         game_board.player_hand_sprites[0].y,
#         game_board.player_hand_sprites[0].y + game_board.player_hand_sprites[0].height,
#     )
#     if (sprite_x[0] < x < sprite_x[1]) and (sprite_y[0] < y < sprite_y[1]):
#         game_board.player_hand_sprites[0].update(
#             x=game_board.player_hand_sprites[0].x + dx,
#             y=game_board.player_hand_sprites[0].y + dy,
#         )
#         game_board.player_hand_sprites[1].x = game_board.player_hand_sprites[1].x + dx
#         game_board.player_hand_sprites[1].y = game_board.player_hand_sprites[1].y + dy

# printing some message


# Print events executed in the window (for debugging)
# event_logger = pyglet.window.event.WindowEventLogger()
# game_board.game_window.push_handlers(event_logger)

### Run it ###
if __name__ == "__main__":
    pyglet.clock.schedule_interval(game_board.update, 1 / 120.0)
    pyglet.app.run()