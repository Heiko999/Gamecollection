from infrastructure import *
from achievements import *

#Registration-Use-Case
class RegistrationUseCase:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def register(self, name, password, tetris, spaceinvader, snake, flappy):
        if name == "" or password == "":
            return False

        #Calls Domain Layer to create a User object
        user = User(name, password, tetris, spaceinvader, snake, flappy)

        #Calls User Repository in the Infrastructure Layer to save the data
        self.user_repository.save(user)

class LoginUseCase:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def execute(self, name, password):
        user = self.user_repository.find_by_name(name)
        if user and user.password == password:
            return True
        return False
    
#Deletes the User; in the Application Layer
class DeleteUseCase:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def execute(self, name, password):
        user = self.user_repository.find_by_name(name)
        if user and user.password == password:
            self.user_repository.delete_by_name(name)
            return True
        return False
    
class HighScoreUseCase:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def update_high_score(self, name, game_name, score):
        user = self.user_repository.find_by_name(name)
        if user:
            if game_name == 'tetris' and user.get_tetris() < score:
                user.set_tetris(score)
                h = points_reached(score)
                h.congrats()
            elif game_name == 'spaceinvader' and user.get_spaceinvader() < score:
                user.set_spaceinvader(score)
                user.set_tetris(score)
                h = points_reached(score)
                h.congrats()
            elif game_name == 'snake' and user.get_snake() < score:
                user.set_snake(score)
                user.set_tetris(score)
                h = points_reached(score)
                h.congrats()
            elif game_name == 'flappy' and user.get_flappy() < score:
                user.set_flappy(score)
                user.set_tetris(score)
                h = points_reached(score)
                h.congrats()

            max_score = self.user_repository.get_highest_score(game_name)
            if score > max_score:
                h = highscore_reached(score)
                h.music_play()
                h.congrats()
            self.user_repository.update(user)

class PlayerHighscoreUseCase:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def execute(self, name):
        user = self.user_repository.find_by_name(name)
        if not user:
            return None
        
        highscores = {}
        highscores['Tetris'] = user.get_tetris()
        highscores['SpaceInvaders'] = user.get_spaceinvader()
        highscores['Snake'] = user.get_snake()
        highscores['Flappy'] = user.get_flappy()
        
        sorted_highscores = sorted(highscores.items(), key=lambda x: x[1], reverse=True)
        return sorted_highscores


class GamesHighscoreUseCase:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def execute(self, game_name):
        highscores = []
        for user in self.user_repository.find_all():
            if game_name == 'tetris':
                highscore = user.get_tetris()
            elif game_name == 'spaceinvader':
                highscore = user.get_spaceinvader()
            elif game_name == 'snake':
                highscore = user.get_snake()
            elif game_name == 'flappy':
                highscore = user.get_flappy()

            if highscore is not None:
                highscores.append((user.get_name(), highscore))

        sorted_highscores = sorted(highscores, key=lambda x: x[1], reverse=True)
        return sorted_highscores
    

class FindPlayerUseCase:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def execute(self, name):
        user = self.user_repository.find_by_name(name)
        if user:
            return True
        return False