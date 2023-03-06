import unittest
import pygame as pg
from snake import SnakeGame


class TestGame(unittest.TestCase):
    def test_snake_moveright(self):
        game = SnakeGame()
        initial_position = game.snake.rect.center
        pg.event.post(pg.event.Event(pg.KEYDOWN, {"key": pg.K_d}))  # move right
        game.check_event()
        game.update()
        updated_position = game.snake.rect.center
        print(initial_position)
        print(updated_position)
        self.assertNotEqual(initial_position, updated_position)
        print("Snake moved right")

    def test_snake_moveleft(self):
        game = SnakeGame()
        initial_position = game.snake.rect.center
        pg.event.post(pg.event.Event(pg.KEYDOWN, {"key": pg.K_a}))  # move left
        game.check_event()
        game.update()
        updated_position = game.snake.rect.center
        print(initial_position)
        print(updated_position)
        self.assertNotEqual(initial_position, updated_position)
        print("Snake moved left")

    def test_snake_moveup(self):
        game = SnakeGame()
        initial_position = game.snake.rect.center
        pg.event.post(pg.event.Event(pg.KEYDOWN, {"key": pg.K_w}))  # move up
        game.check_event()
        game.update()
        updated_position = game.snake.rect.center
        print(initial_position)
        print(updated_position)
        self.assertNotEqual(initial_position, updated_position)
        print("Snake moved up")

    def test_snake_movedown(self):
        game = SnakeGame()
        initial_position = game.snake.rect.center
        pg.event.post(pg.event.Event(pg.KEYDOWN, {"key": pg.K_s}))  # move down
        game.check_event()
        game.update()
        updated_position = game.snake.rect.center
        print(initial_position)
        print(updated_position)
        self.assertNotEqual(initial_position, updated_position)
        print("Snake moved down")
        

if __name__ == '__main__':
    unittest.main()