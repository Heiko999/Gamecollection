import pygame
#from main import *
from input import InputBox
from button import Button
from logger import Log

signin_img = pygame.image.load('signin_btn.png').convert_alpha()
login_img = pygame.image.load('login_btn.png').convert_alpha()
delete_img = pygame.image.load('delete_btn.png').convert_alpha()
FONT = pygame.font.Font(None, 32)
class Menu():
    #currentPlayer=''
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100

    def draw_cursor(self):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

class LoginMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Login"
        self.screen = pygame.display.set_mode((self.game.DISPLAY_W,self.game.DISPLAY_H))

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            clock = pygame.time.Clock()
            self.game.check_events()
            self.game.display.fill(self.game.BLACK)
            
            log = Log()

            input_box1 = InputBox(self.game.DISPLAY_W / 2 - 100,  50, 140, 32)
            input_box2 = InputBox(self.game.DISPLAY_W / 2 - 100, 100, 140, 32)
            input_boxes = [input_box1, input_box2]
            signin_button = Button(self.game.DISPLAY_W / 2 - 250, 200, signin_img, 0.4)
            login_button = Button(self.game.DISPLAY_W / 2 -50, 200, login_img, 0.4)
            delete_button = Button(self.game.DISPLAY_W / 2 + 150, 200, delete_img, 0.4)
            #buttons =[start_button, exit_button]
            done = False

            while not done:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                    for box in input_boxes:
                        if event.type == pygame.K_RETURN:
                            print(box.text + "test")
                        box.handle_event(event)

                for box in input_boxes:
                    box.update()
                
                self.game.display.fill((30, 30, 30))
                self.game.draw_text('Login Screen', 20, self.game.DISPLAY_W / 2, 30)
                for box in input_boxes:
                    box.draw(self.game.display)
                if signin_button.draw(self.screen):
                    print('START')
                    print(input_box1.text)
                    print(input_box2.text)
                    log.signIn(input_box1.text,input_box2.text)
                    input_box1.text = ''
                    input_box2.text = ''
                    input_box1.txt_surface = FONT.render(input_box1.text, True, input_box1.color)
                    input_box2.txt_surface = FONT.render(input_box2.text, True, input_box2.color)
                    
                if login_button.draw(self.screen):
                    print('EXIT')
                    print(input_box1.text)
                    print(input_box2.text)
                    if log.login(input_box1.text, input_box2.text) == True:
                        self.game.player = input_box1.text
                        done = True
                        self.run_display = False
                        self.game.curr_menu = self.game.main_menu
                    input_box1.text = ''
                    input_box2.text = ''
                    input_box1.txt_surface = FONT.render(input_box1.text, True, input_box1.color)
                    input_box2.txt_surface = FONT.render(input_box2.text, True, input_box2.color)

                if delete_button.draw(self.screen):
                    print('delete')
                    print(input_box1.text)
                    print(input_box2.text)
                    log.delete(input_box1.text,input_box2.text)
                    input_box1.text = ''
                    input_box2.text = ''
                    input_box1.txt_surface = FONT.render(input_box1.text, True, input_box1.color)
                    input_box2.txt_surface = FONT.render(input_box2.text, True, input_box2.color)
                pygame.display.flip()
                clock.tick(20)
                self.blit_screen()

                
                
    

    

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.highscorex, self.highscorey = self.mid_w, self.mid_h + 50
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 70
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 90
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            mainM = "Main Menu" + "      Hallo Player: " + str(self.game.player)
            self.game.draw_text(mainM, 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text("Start Game", 20, self.startx, self.starty)
            self.game.draw_text("Highscores", 20, self.highscorex, self.highscorey)
            self.game.draw_text("Options", 20, self.optionsx, self.optionsy)
            self.game.draw_text("Credits", 20, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.blit_screen()


    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.highscorex + self.offset, self.highscorey)
                self.state = 'Highscores'
            elif self.state == 'Highscores':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Highscores':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.highscorex + self.offset, self.highscorey)
                self.state = 'Highscores'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.login
            self.run_display = False

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.curr_menu = self.game.game_collection
            elif self.state == 'Highscores':
                self.game.curr_menu = self.game.highscores
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            self.run_display = False

class GameMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'SpaceInvaders'
        self.spacex, self.spacey = self.mid_w, self.mid_h + 20
        self.tetrisx, self.tetrisy = self.mid_w, self.mid_h + 40
        self.mindx, self.mindy = self.mid_w, self.mid_h + 60
        self.snakex, self.snakey = self.mid_w, self.mid_h + 80
        self.flapx, self.flapy = self.mid_w, self.mid_h + 100
        self.cursor_rect.midtop = (self.spacex + self.offset, self.spacey)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('GameCollection', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            self.game.draw_text("SpaceInvaders", 15, self.spacex, self.spacey)
            self.game.draw_text("Tetris", 15, self.tetrisx, self.tetrisy)
            self.game.draw_text("Mastermind", 15, self.mindx, self.mindy)
            self.game.draw_text("Snake", 15, self.snakex, self.snakey)
            self.game.draw_text("Flappy Bird", 15, self.flapx, self.flapy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.DOWN_KEY:
            if self.state == 'SpaceInvaders':
                self.state = 'Tetris'
                self.cursor_rect.midtop = (self.tetrisx + self.offset, self.tetrisy)
            elif self.state == 'Tetris':
                self.state = 'Mastermind'
                self.cursor_rect.midtop = (self.mindx + self.offset, self.mindy)
            elif self.state == 'Mastermind':
                self.state = 'Snake'
                self.cursor_rect.midtop = (self.snakex + self.offset, self.snakey)
            elif self.state == 'Snake':
                self.state = 'Flappy'
                self.cursor_rect.midtop = (self.flapx + self.offset, self.flapy)
            elif self.state == 'Flappy':
                self.state = 'SpaceInvaders'
                self.cursor_rect.midtop = (self.spacex + self.offset, self.spacey)
        elif self.game.UP_KEY:
            if self.state == 'Mastermind':
                self.state = 'Tetris'
                self.cursor_rect.midtop = (self.tetrisx + self.offset, self.tetrisy)
            elif self.state == 'Tetris':
                self.state = 'SpaceInvaders'
                self.cursor_rect.midtop = (self.spacex + self.offset, self.spacey)
            elif self.state == 'SpaceInvaders':
                self.state = 'Flappy'
                self.cursor_rect.midtop = (self.flapx + self.offset, self.flapy)
            elif self.state == 'Flappy':
                self.state = 'Snake'
                self.cursor_rect.midtop = (self.snakex + self.offset, self.snakey)
            elif self.state == 'Snake':
                self.state = 'Mastermind'
                self.cursor_rect.midtop = (self.mindx + self.offset, self.mindy)
        elif self.game.START_KEY:
            if self.state == 'SpaceInvaders':
                self.game.playing = True
            if self.state == 'Tetris':
                self.game.playing = True
            if self.state == 'Mastermind':
                self.game.playing = True
            if self.state == 'Snake':
                self.game.playing = True
            if self.state == 'Flappy':
                self.game.playing = True
        self.run_display = False

class HighscoreMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Playerscore'
        self.phighscorex, self.phighscorey = self.mid_w, self.mid_h + 20
        self.ghighscorex, self.ghighscorey = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.phighscorex + self.offset, self.phighscorey)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Highscores', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            self.game.draw_text("Playerscore", 15, self.phighscorex, self.phighscorey)
            self.game.draw_text("Gamescore", 15, self.ghighscorex, self.ghighscorey)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Playerscore':
                self.state = 'Gamescore'
                self.cursor_rect.midtop = (self.ghighscorex + self.offset, self.ghighscorey)
            elif self.state == 'Gamescore':
                self.state = 'Playerscore'
                self.cursor_rect.midtop = (self.phighscorex + self.offset, self.phighscorey)
        elif self.game.START_KEY:
            if self.state == '':
                if self.game.BLACK == (0, 0, 0):
                    self.game.BLACK = (255, 255, 255)  
                    self.game.WHITE = (0, 0, 0)
                    print(self.game.BLACK)
                    print(self.game.WHITE)
                    return
                

class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.modex, self.modey = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Options', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            self.game.draw_text("Volume", 15, self.volx, self.voly)
            self.game.draw_text("Mode", 15, self.modex, self.modey)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Volume':
                self.state = 'Mode'
                self.cursor_rect.midtop = (self.modex + self.offset, self.modey)
            elif self.state == 'Mode':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.START_KEY:
            if self.state == 'Mode':
                if self.game.BLACK == (0, 0, 0):
                    self.game.BLACK = (255, 255, 255)  
                    self.game.WHITE = (0, 0, 0)
                    print(self.game.BLACK)
                    print(self.game.WHITE)
                    return
                elif self.game.BLACK == (255, 255, 255):
                    self.game.BLACK = (0, 0, 0)  
                    self.game.WHITE = (255, 255, 255)
                    print(self.game.BLACK)
                    print(self.game.WHITE)
                    return
            if self.state == 'Volume':
                print('volume')
                self.game.curr_menu = self.game.main_menu
            

class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Credits', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text('Made by ', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10)
            self.game.draw_text('Heiko Herrmann', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 30)
            self.game.draw_text('&', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 50)
            self.game.draw_text('Tom Witzel', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 70)
            self.blit_screen()







