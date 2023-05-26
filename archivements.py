from abc import ABC, abstractmethod
import pygame

class archivement(ABC):
    @abstractmethod
    def __init__(self,points):
        pass

    @abstractmethod
    def congrats(self):
        pass

class bigger_archivement(archivement):
    @abstractmethod
    def music_play(self):
        pass

class points_reached(archivement):
    def __init__(self, points):
        self.points = points

    def congrats(self):
        print("congrats you got %d points and broke your own Highscore!" % self.points)

class highscore_reached(bigger_archivement):
    def __init__(self, points):
        self.points = points

    def congrats(self):
        print("congrats you got %d points and broke the Games Highscore!" % self.points)

    def music_play(self):
        print("playing music")
        pygame.init()
        sound = pygame.mixer.Sound("gamedump/highscoresound.mp3")
        sound.play()
        pygame.time.wait(int(sound.get_length() * 1000))