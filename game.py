import pygame
from menu import *
from spaceinvader import *
from tetris import *
from mastermind import *
from logger import Log
from snake import *
from flappy import *


class Game():
    def __init__(self):
        pygame.init()
        self.player = ''
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 600, 400
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)))
        #self.font_name = '8-BIT WONDER.TTF'
        self.font_name = pygame.font.get_default_font()
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.highscores = HighscoreMenu(self)
        self.game_collection = GameMenu(self)
        self.login = LoginMenu(self)
        self.curr_menu = self.login

    def game_loop(self):
        while self.playing:
            if self.game_collection.state == 'SpaceInvaders':
                game = SpaceGame(600,400)
                log = Log()
                log.highscore('SpaceInvaders', game.score_si, self.player)
                print(game.score_si)
            if self.game_collection.state == 'Tetris':
                game = Tetris(20,10)
                log = Log()
                log.highscore('Tetris', game.score_tetris, self.player)
                print (game.score_tetris)
            if self.game_collection.state == 'Mastermind':
                game = Mastermind()
                log = Log()
                log.highscore('Mastermind', game.score_mm, self.player)
                print(game.score_mm)
            if self.game_collection.state == 'Snake':
                game = Snake()
                log = Log()
                log.highscore('Snake', game.score_snake, self.player)
                print(game.score_snake)
            if self.game_collection.state == 'Flappy':
                game = flappy()
                log = Log()
                log.highscore('Flappy', game.score_flappy, self.player)
                print(game.score_flappy)
            #TO-DO: Wenn man einen Highscore erreicht, aber das spiel dann nicht schließt sondern eine neue Runde anfängt
            #wird der Highscore nicht gespeichert 

            self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)))
            self.playing = False
            #self.check_events()
            #if self.START_KEY:
                #self.playing= False
            self.display.fill(self.BLACK)
            self.draw_text('Thanks for Playing', 20, self.DISPLAY_W/2, self.DISPLAY_H/2)
            self.window.blit(self.display, (0,0))
            pygame.display.update()
            self.reset_keys()



    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y ):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)




class gamescore:
    def __init__(self, game, score ):
        self.game = game
        self.score = score

