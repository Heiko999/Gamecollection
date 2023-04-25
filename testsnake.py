import unittest
import pygame as pg
from snake import SnakeGame


class TestGame(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        pg.display.init()
        pg.display.set_mode((1, 1), pg.NOFRAME)
    
    def test_snake_moveright(self):
        game = SnakeGame()
        initial_position = game.snake.rect.center
        pg.event.post(pg.event.Event(pg.KEYDOWN, {"key": pg.K_RIGHT}))  # move right
        game.check_event()
        game.update()
        updated_position = game.snake.rect.center
        updated_direction = game.snake.direction
        self.assertNotEqual(initial_position, updated_position)
        self.assertEqual(updated_direction, (50, 0))  # Check if direction changed to right
    
    def test_snake_moverleft(self):
        game = SnakeGame()
        initial_position = game.snake.rect.center
        pg.event.post(pg.event.Event(pg.KEYDOWN, {"key": pg.K_LEFT}))  # move right
        game.check_event()
        game.update()
        updated_position = game.snake.rect.center
        updated_direction = game.snake.direction
        self.assertNotEqual(initial_position, updated_position)
        self.assertEqual(updated_direction, (-50, 0))  # Check if direction changed to right

    def test_snake_moveup(self):
        game = SnakeGame()
        initial_position = game.snake.rect.center
        pg.event.post(pg.event.Event(pg.KEYDOWN, {"key": pg.K_UP}))  # move right
        game.check_event()
        game.update()
        updated_position = game.snake.rect.center
        updated_direction = game.snake.direction
        self.assertNotEqual(initial_position, updated_position)
        self.assertEqual(updated_direction, (0, -50))  # Check if direction changed to right

    def test_snake_movedown(self):
        game = SnakeGame()
        initial_position = game.snake.rect.center
        pg.event.post(pg.event.Event(pg.KEYDOWN, {"key": pg.K_DOWN}))  # move right
        game.check_event()
        game.update()
        updated_position = game.snake.rect.center
        updated_direction = game.snake.direction
        self.assertNotEqual(initial_position, updated_position)
        self.assertEqual(updated_direction, (0, 50))  # Check if direction changed to right

        

if __name__ == '__main__':
    unittest.main()
