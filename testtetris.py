import unittest
from tetris import Tetris

class TestTetris(unittest.TestCase):

    def test_new_figure(self):
        # Check that a new figure is created and the figure variable is set
        game =Tetris(20, 10)
        print("Check if FIgure Variable is not Set")
        self.assertIsNone(game.figure)
        print("Not Set")
        print("Creating new Figure")
        game.new_figure()
        print("Check if new Figure is Created")
        self.assertIsNotNone(game.figure)
        print("new Figure is created")


if __name__ == '__main__':
    unittest.main()