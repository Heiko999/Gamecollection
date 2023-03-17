from abc import ABC, abstractmethod


class archivement(ABC):
    @abstractmethod
    def __init__(self,points):
        pass

    @abstractmethod
    def congrats():
        pass

class bigger_archivement(archivement):
    @abstractmethod
    def music_play():
        pass

class points_reached(archivement):
    def __init__(self, points):
        self.points = points

    def congrats(self):
        print("congrats you got %d points!" % self.points)

class highscore_reached(bigger_archivement):
    def __init__(self, points):
        self.points = points

    def congrats(self):
        print("congrats you got %d points and broke the Highscore!" % self.points)

    def music_play(self):
        print("play musik") 



h = highscore_reached(30)

h.congrats()
h.music_play()