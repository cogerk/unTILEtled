import pyglet
from game.game_setup import PlayerHand

### Define Scaling Style as Neartest Neighbors ###
# MUST BE FIRST to work
pyglet.font.base.Font.texture_min_filter = pyglet.gl.GL_NEAREST
pyglet.font.base.Font.texture_mag_filter = pyglet.gl.GL_NEAREST
pyglet.image.Texture.default_min_filter = pyglet.gl.GL_NEAREST
pyglet.image.Texture.default_mag_filter = pyglet.gl.GL_NEAREST

### Initialize Window ###
game_window = pyglet.window.Window(800, 600)

### Load Font ###
pyglet.resource.add_font("BAUHS93.TTF")

### Set BG color: ###
pyglet.gl.glClearColor(9 / 255, 4 / 255, 10 / 255, 255)

### Set Scales ###
hand_scale = 1
board_scale = 2

### Place Gameboard ###
game_board_img = pyglet.resource.image("GameBoard.png")
# Place Anchor at image center
game_board_img.anchor_x = game_board_img.width / 2
game_board_img.anchor_y = game_board_img.height / 2
# Put in Sprite
game_board_sprite = pyglet.sprite.Sprite(
    game_board_img, x=game_window.width / 2, y=game_window.height / 2
)
# Set Scale
game_board_sprite.scale = board_scale

### Initialize Hand ###
my_hand = PlayerHand()
tile_to_draw = my_hand.pull_first_hand()

### Build Hand ###
# TODO: Why do you need the list my_hands_sprites pyglet? you don't appear to access it again?
batch, my_hands_sprites = my_hand.build_hand_tiles_sprites(game_window, hand_scale)
# Happens whenever the window needs to be re-drawn
# Labels, when using a custom font, you have to use it's full name (dbl click ttf file)
title = pyglet.text.Label(
    text="Cool Name Here",
    font_name="Bauhaus 93",
    y=game_window.height,
    x=10,
    anchor_x="left",
    anchor_y="top",
    font_size=72,
)
your_hand_text = pyglet.text.Label(
    text="Your Hand:",
    font_name="Bauhaus 93",
    y=my_hands_sprites[3].y + 50 * hand_scale,
    x=my_hands_sprites[3].x,
    anchor_x="right",
    anchor_y="baseline",
    font_size=24,
)

### Draw it ###
@game_window.event
def on_draw():
    # draw things here
    game_window.clear()
    title.draw()
    your_hand_text.draw()
    batch.draw()
    game_board_sprite.draw()


### Run it ###
if __name__ == "__main__":
    pyglet.app.run()
