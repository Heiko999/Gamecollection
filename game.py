
from menu import *
from spaceinvader import *
from tetris import *
from mastermind import *
from logger import *
from snake import *
from flappy import *
from skyfallgame import *

#TO-DO: Pygame Dependency entfernen, damit diese Klasse für Clean Code auf Framework Abhängigkeiten verzichtet.

class Game():
    def __init__(self):
        #pygame.init()
        self.player = ''
        self.highscoreplayer = 'test'
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 600, 400
        #self.font_name = '8-BIT WONDER.TTF'
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.highscores = HighscoreMenu(self)
        self.gamescores = GamescoreMenu(self)
        self.playerscores = PlayerscoreMenu(self)
        self.playerhighscore = PlayerhighscoreMenu(self)
        self.spacescoremenu = SpaceMenu(self)
        self.tetrisscoremenu = TetrisMenu(self)
        self.masterscoremenu = MastermindMenu(self)
        self.snakescoremenu = SnakeMenu(self)
        self.flappyscoremenu = FlappyMenu(self)
        self.game_collection = GameMenu(self)
        self.login = LoginMenu(self)
        self.curr_menu = self.login
        self.closedcounter = 0
    
    #Wird für das Gamemenu verwendet. Solange man im GameMenu ist wird der State erfasst, um zu sehen, welches spiel gerade gespielt wird
    #dann wird ein Objekt des Spiels erzeugt und somit dieses Spiel gestartet
    def game_loop(self):
        if self.playing:
            if self.game_collection.state == 'SpaceInvaders':
                game = skyfallGame()
                game.run()
                log = Log(DatabaseConnection1().getDB(), DatabaseConnection2().getDB())
                log.highscore('SpaceInvaders', skyfallGame.highscore, self.player)
                print("Skyfallhighscore = " + str(skyfallGame.highscore))
                skyfallGame.highscore = 0
                self.closedcounter = 1
            if self.game_collection.state == 'Tetris':
                game = Tetris(20,10)
                game.run()
                log = Log(DatabaseConnection1().getDB(), DatabaseConnection2().getDB())
                log.highscore('Tetris', game.score_tetris, self.player)
                print (game.score_tetris)
                self.closedcounter = 1
            if self.game_collection.state == 'Mastermind':
                game = Mastermind()
                log = Log(DatabaseConnection1().getDB(), DatabaseConnection2().getDB())
                log.highscore('Mastermind', game.score_mm, self.player)
                print(game.score_mm)
                self.closedcounter = 1
            if self.game_collection.state == 'Snake':
                game = SnakeGame()
                game.run()
                log = Log(DatabaseConnection1().getDB(), DatabaseConnection2().getDB())
                scoresnake= SnakeGame.highscore
                log.highscore('Snake', scoresnake, self.player)
                print("Highscore is: " + str(SnakeGame.highscore))
                SnakeGame.highscore = 0
                self.closedcounter = 1
            if self.game_collection.state == 'Flappy':
                game = flappy()
                game.run()
                log = Log(DatabaseConnection1().getDB(), DatabaseConnection2().getDB())
                log.highscore('Flappy', game.score_flappy, self.player)
                print(game.score_flappy)
                self.closedcounter = 1
            #TO-DO: Wenn man einen Highscore erreicht, aber das spiel dann nicht schließt sondern eine neue Runde anfängt
            #wird der Highscore nicht gespeichert 
            self.playing = False
            self.reset_keys()

    #Wird in den Menuklassen benutzt um am ende eines Displayloop die gedrückten Tasten zu resetten, damit nach einem Klick nach
    #z.B. Unten nicht durchgehend nach unten gescrollt wird
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
    
    #Führt alle Schritte aus, um Text auf die Oberfläche zu zeichnen
    



#Ist glaube ich ein überbleibsel und wird nicht benötigt aber not sure
class gamescore:
    def __init__(self, game, score ):
        self.game = game
        self.score = score

