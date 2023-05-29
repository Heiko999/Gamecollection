import unittest
from tetris import Tetris

class TestTetris(unittest.TestCase):

    def test_new_figure(self):
        #Check that a new figure is created and the figure variable is set
        game = Tetris(20, 10)
        self.assertIsNone(game.figure)
        game.new_figure()
        self.assertIsNotNone(game.figure)


if __name__ == '__main__':
    unittest.main()