
from menu import *
from spaceinvader import *
from tetris import *
from logger import *
from snake import *
from flappy import *
from skyfallgame import *
from usecase import *

#TO-DO: Pygame Dependency entfernen, damit diese Klasse für Clean Code auf Framework Abhängigkeiten verzichtet.

class Game():
    def __init__(self):
        self.player = ''
        self.highscoreplayer = ''
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 600, 400
        self.backgroundcolor, self.textcolor = (0, 0, 0), (255, 255, 255)
        self.main_menu = ''
        self.options = ''
        self.credits = ''
        self.highscores = ''
        self.gamescores = ''
        self.playerscores = ''
        self.playerhighscore = ''
        self.spacescoremenu = ''
        self.tetrisscoremenu = ''
        self.snakescoremenu = ''
        self.flappyscoremenu = ''
        self.game_collection = ''
        self.curr_menu = ''
        self.closedcounter = 0
    
    #Wird für das Gamemenu verwendet. Solange man im GameMenu ist wird der State erfasst, um zu sehen, welches spiel gerade gespielt wird
    #dann wird ein Objekt des Spiels erzeugt und somit dieses Spiel gestartet
    def game_loop(self):
        if self.playing:
            if self.game_collection.state == 'SpaceInvaders':
                game = skyfallGame()
                game.run()
                user_repository = UserRepositoryImpl()
                high_score_use_case = HighScoreUseCase(user_repository)
                high_score_use_case.update_high_score(self.player, 'spaceinvader', skyfallGame.highscore)
                print("Skyfallhighscore = " + str(skyfallGame.highscore))
                skyfallGame.highscore = 0
                self.closedcounter = 1
            if self.game_collection.state == 'Tetris':
                game = Tetris(20,10)
                game.run()
                user_repository = UserRepositoryImpl()
                high_score_use_case = HighScoreUseCase(user_repository)
                high_score_use_case.update_high_score(self.player, 'tetris', game.score_tetris)
                print (game.score_tetris)
                self.closedcounter = 1
            if self.game_collection.state == 'Snake':
                game = SnakeGame()
                game.run()
                user_repository = UserRepositoryImpl()
                high_score_use_case = HighScoreUseCase(user_repository)
                high_score_use_case.update_high_score(self.player, 'snake', SnakeGame.highscore)
                print("Highscore is: " + str(SnakeGame.highscore))
                SnakeGame.highscore = 0
                self.closedcounter = 1
            if self.game_collection.state == 'Flappy':
                game = flappy()
                game.run()
                user_repository = UserRepositoryImpl()
                high_score_use_case = HighScoreUseCase(user_repository)
                high_score_use_case.update_high_score(self.player, 'flappy', game.score_flappy)
                print(game.score_flappy)
                self.closedcounter = 1 
            self.playing = False
            self.reset_keys()


    #Wird in den Menuklassen benutzt um am ende eines Displayloop die gedrückten Tasten zu resetten, damit nach einem Klick nach
    #z.B. Unten nicht durchgehend nach unten gescrollt wird
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
    
    def main_menu_set(self):
        self.main_menu = MainMenu(self)
        self.curr_menu = self.main_menu

    def options_set(self):
        self.options = OptionsMenu(self)
        self.curr_menu = self.options
    
    def credits_set(self):
        self.credits = CreditsMenu(self)
        self.curr_menu = self.credits

    def highscores_set(self):
        self.highscores = HighscoreMenu(self)
        self.curr_menu  = self.highscores
    
    def gamescores_set(self):
        self.gamescores = GamescoreMenu(self)
        self.curr_menu = self.gamescores

    def playerscores_set(self):
        self.playerscores = PlayerscoreMenu(self)
        self.curr_menu = self.playerscores

    def playerhighscores_set(self):
        self.playerhighscore = PlayerhighscoreMenu(self)
        self.curr_menu = self.playerhighscore

    def spacescoremenu_set(self):
        self.spacescoremenu = SpaceMenu(self)
        self.curr_menu = self.spacescoremenu

    def tetrisscoremenu_set(self):
        self.tetrisscoremenu = TetrisMenu(self)
        self.curr_menu = self.tetrisscoremenu

    def snakescoremenu_set(self):
        self.snakescoremenu = SnakeMenu(self)
        self.curr_menu = self.snakescoremenu

    def flappyscoremenu_set(self):
        self.flappyscoremenu = FlappyMenu(self)
        self.curr_menu = self.flappyscoremenu

    def game_collection_set(self):
        self.game_collection = GameMenu(self)
        self.curr_menu = self.game_collection

    def login_set(self):
        self.login = LoginMenu(self)
        self.curr_menu = self.login



