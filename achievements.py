from abc import ABC, abstractmethod
import pygame

class achievement(ABC):
    @abstractmethod
    def __init__(self,points):
        pass

    @abstractmethod
    def congrats(self):
        pass

class bigger_achievement(achievement):
    @abstractmethod
    def music_play(self):
        pass

class points_reached(achievement):
    def __init__(self, points):
        self.points = points

    def congrats(self):
        print("congrats you got %d points and broke your own Highscore!" % self.points)

class highscore_reached(bigger_achievement):
    def __init__(self, points):
        self.points = points

    def congrats(self):
        print("congrats you got %d points and broke the Games Highscore!" % self.points)

    def music_play(self):
        print("playing music")
        pygame.init()
        sound = pygame.mixer.Sound("files/highscoresound.mp3")
        sound.play()
        pygame.time.wait(int(sound.get_length() * 1000))