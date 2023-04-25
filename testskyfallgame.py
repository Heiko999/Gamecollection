import unittest
from skyfallgame import *

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.game = skyfallGame()
        
    def test_collision_detection(self):
        self.assertFalse(self.game.game_over)
        self.game.player.rect.centerx = self.game.enemy_sprites.sprites()[0].rect.centerx
        self.game.player.rect.centery = self.game.enemy_sprites.sprites()[0].rect.centery
        self.game.collision_score_update()
        self.assertTrue(self.game.game_over)
 

if __name__ == '__main__':
    unittest.main()