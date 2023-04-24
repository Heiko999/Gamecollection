import unittest
from menu import MainMenu
from game import Game
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'

class TestMainMenu(unittest.TestCase):
        
    def test_move_cursor_down(self):
        self.game = Game()
        self.main_menu = MainMenu(self.game)
        self.game.DOWN_KEY = True
        self.main_menu.move_cursor()
        self.assertEqual(self.main_menu.state, 'Highscores')
        self.main_menu.move_cursor()
        self.assertEqual(self.main_menu.state, 'Options')
        self.game.reset_keys()
    
    def test_move_cursor_up(self):
        self.game = Game()
        self.main_menu = MainMenu(self.game)
        self.game.UP_KEY = True
        self.main_menu.move_cursor()
        self.assertEqual(self.main_menu.state, 'Credits')
        self.main_menu.move_cursor()
        self.assertEqual(self.main_menu.state, 'Options')


if __name__ == '__main__':
    unittest.main()

