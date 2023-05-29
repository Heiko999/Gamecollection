#User-Object
from abc import ABC, abstractmethod
class User:
    def __init__(self, name, password, tetris, spaceinvader, snake, flappy):
        self.name = name
        self.password = password
        self.tetris = tetris
        self.spaceinvader = spaceinvader
        self.snake = snake
        self.flappy = flappy

    def get_name(self):
        return self.name

    def get_password(self):
        return self.password
    
    def get_tetris(self):
        return self.tetris
    
    def get_spaceinvader(self):
        return self.spaceinvader
    
    def get_snake(self):
        return self.snake
    
    def get_flappy(self):
        return self.flappy
    
    def set_tetris(self, score):
        self.tetris = score
    
    def set_spaceinvader(self,score):
        self.spaceinvader = score
    
    def set_snake(self,score):
        self.snake = score
    
    def set_flappy(self,score):
        self.flappy = score

#User-Repository-Interface
class UserRepository(ABC):
    @abstractmethod
    def save(self, user):
        pass

    @abstractmethod
    def find_by_name(self, name):
        pass

    @abstractmethod
    def check_password(self,name, password):
        pass

    @abstractmethod
    def delete_by_name(self, name):
        pass
    
    @abstractmethod
    def update(self, user):
        pass

    @abstractmethod
    def find_all(self):
        pass

    @abstractmethod
    def get_highest_score(self, game_name):
        pass
