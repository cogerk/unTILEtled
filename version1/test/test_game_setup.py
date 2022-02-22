import unittest
import pyglet


class TestGameSetup(unittest.TestCase):
    def setUp(self):
        print(pyglet.resource.path)
        ### Initialize Hand ###
        self.tiles = game.setup.AvailableTiles()
        #self.my_hand = game.setup.PlayerHand()
        #self.tile_to_draw = self.my_hand.pull_first_hand()
    def test_no_of_assets(self):
        self.assertEqual(len(self.tiles.tiles), len(game.setup.COLORS)**2*self.tiles.no_sets)
    # def test_no_of_tiles_in_game(self):
    #     self.assertEqual('foo'.upper(), 'FOO')

    # def test_isupper(self):
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())

    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

if __name__ == '__main__':
    unittest.main()