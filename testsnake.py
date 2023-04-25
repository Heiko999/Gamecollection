import unittest
from unittest.mock import Mock
import pygame as pg
from snake import SnakeGame


class TestGame(unittest.TestCase):

    def test_snake_moveright(self):
        game = SnakeGame()
        initial_position = game.snake.rect.center
        event = Mock(type=pg.KEYDOWN, key=pg.K_RIGHT)
        game.snake.control(event)
        game.snake.update()
        updated_position = game.snake.rect.center
        updated_direction = game.snake.direction
        self.assertNotEqual(initial_position, updated_position)
        self.assertEqual(updated_direction, (50, 0))  # Check if direction changed to right    

    def test_snake_moverleft(self):
        game = SnakeGame()
        initial_position = game.snake.rect.center
        event = Mock(type=pg.KEYDOWN, key=pg.K_LEFT)
        game.snake.control(event)
        game.snake.update()
        updated_position = game.snake.rect.center
        updated_direction = game.snake.direction
        self.assertNotEqual(initial_position, updated_position)
        self.assertEqual(updated_direction, (-50, 0))  # Check if direction changed to left

    def test_snake_moveup(self):
        game = SnakeGame()
        initial_position = game.snake.rect.center
        event = Mock(type=pg.KEYDOWN, key=pg.K_UP)
        game.snake.control(event)
        game.snake.update()
        updated_position = game.snake.rect.center
        updated_direction = game.snake.direction
        self.assertNotEqual(initial_position, updated_position)
        self.assertEqual(updated_direction, (0, -50))  # Check if direction changed to up

    def test_snake_movedown(self):
        game = SnakeGame()
        initial_position = game.snake.rect.center
        event = Mock(type=pg.KEYDOWN, key=pg.K_DOWN)
        game.snake.control(event)
        game.snake.update()
        updated_position = game.snake.rect.center
        updated_direction = game.snake.direction
        self.assertNotEqual(initial_position, updated_position)
        self.assertEqual(updated_direction, (0, 50))  # Check if direction changed to down

        

if __name__ == '__main__':
    unittest.main()
