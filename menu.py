import pygame
#from main import *
from input import InputBox
from button import Button
from logger import Log




signin_img = pygame.image.load('signin_btn.png').convert_alpha()
login_img = pygame.image.load('login_btn.png').convert_alpha()
delete_img = pygame.image.load('delete_btn.png').convert_alpha()
search_img = pygame.image.load('search_btn.png').convert_alpha()
FONT = pygame.font.Font(None, 32)

#Hauptklasse von welcher die anderen Klassen erben.
class Menu():
    #currentPlayer=''
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100

    #Wird verwendet um den * Cursor an den ensprechenden Menupunkt zu setzen
    def draw_cursor(self):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)
    #Wird verwendet, um nach Ende einer Aktion in einem Menu das Bild zu aktualisieren
    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

    #Funktion um die gedrückten Tasten zu erfassen und in einem Boolean zu speichern
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running, self.game.playing = False, False
                self.game.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.game.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.game.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.game.UP_KEY = True

class LoginMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Login"
        self.screen = pygame.display.set_mode((self.game.DISPLAY_W,self.game.DISPLAY_H))
    #Funktion welche aufgerufen wird, wenn das entsprechende Menu aktiv ist und einen Loop für das anzuzeigende Menu ausführt,
    #welcher auf Eingaben wartet
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            clock = pygame.time.Clock()
            self.check_events()
            self.game.display.fill(self.game.BLACK)
            
            log = Log()

            #Erzeugt TextBoxen und Buttons für das LoginMenu
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
##TODO: Inputbox.text und txt_surface in Methode, für DRY damit Code mehr Lightweight                
                #Legt bei Klick auf SignIn Button nach eingabe eines Usernamen und Passworts einen neuen Benutzer
                #in der Datenbank 
                signin_button.draw(self.screen)
                if signin_button.click():
                    print('START')
                    print(input_box1.text)
                    print(input_box2.text)
                    log.signIn(input_box1.text,input_box2.text)
                    input_box1.text = ''
                    input_box2.text = ''
                    input_box1.txt_surface = FONT.render(input_box1.text, True, input_box1.color)
                    input_box2.txt_surface = FONT.render(input_box2.text, True, input_box2.color)

                #Checkt nach auswahl des LoginButton, Ob Username und Passwort mit eintrag in Datenbank übereinstimmen
                #Stimmt es wird das Menu auf das Main Menu geändert    
                login_button.draw(self.screen)
                if login_button.click():
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

                #Checkt nach Klick auf den Deletebutton ob User und Passwort mit eintrag in Datenbank übereinstimmen.
                #Tun sie das, wird der Spieler gelöscht 
                delete_button.draw(self.screen)
                if delete_button.click():
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
    
    #Funktion welche aufgerufen wird, wenn das entsprechende Menu aktiv ist und einen Loop für das anzuzeigende Menu ausführt,
    #welcher auf Eingaben wartet
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
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
    #Reagiert auf gedrückte Tasten mit entsprechender Funktion
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

    #Funktion welche aufgerufen wird, wenn das entsprechende Menu aktiv ist und einen Loop für das anzuzeigende Menu ausführt,
    #welcher auf Eingaben wartet
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
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

    #Reagiert auf gedrückte Tasten mit entsprechender Funktion
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

    #Funktion welche aufgerufen wird, wenn das entsprechende Menu aktiv ist und einen Loop für das anzuzeigende Menu ausführt,
    #welcher auf Eingaben wartet
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Highscores', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            self.game.draw_text("Playerscore", 15, self.phighscorex, self.phighscorey)
            self.game.draw_text("Gamescore", 15, self.ghighscorex, self.ghighscorey)
            self.draw_cursor()
            self.blit_screen()
    #Reagiert auf gedrückte Tasten mit entsprechender Funktion
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
            if self.state == 'Gamescore':
                self.game.curr_menu = self.game.gamescores
                self.run_display = False
            elif self.state == 'Playerscore':
                self.game.curr_menu = self.game.playerscores
                self.run_display = False
                

class PlayerscoreMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Playerscore"
        self.screen = pygame.display.set_mode((self.game.DISPLAY_W,self.game.DISPLAY_H))
    #Funktion welche aufgerufen wird, wenn das entsprechende Menu aktiv ist und einen Loop für das anzuzeigende Menu ausführt,
    #welcher auf Eingaben wartet
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            clock = pygame.time.Clock()
            self.check_events()
            self.game.display.fill(self.game.BLACK)
            
            log = Log()

            #Erzeugt TextBoxen und Buttons für das LoginMenu
            input_box1 = InputBox(self.game.DISPLAY_W / 2 - 100,  50, 140, 32)  
            input_button = Button(self.game.DISPLAY_W / 2 -50, 200, search_img, 0.4)
            #buttons =[start_button, exit_button]
            done = False

            while not done:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                    input_box1.handle_event(event)
                    input_box1.update()
                
                self.game.display.fill((30, 30, 30))
                self.game.draw_text('Highscores for which Player?', 20, self.game.DISPLAY_W / 2, 30)
                input_box1.draw(self.game.display)
                
                #Legt bei Klick auf SignIn Button nach eingabe eines Usernamen und Passworts einen neuen Benutzer
                #in der Datenbank an

                input_button.draw(self.screen) 
                if input_button.click():
                    print('input')
                    print(input_box1.text)
                    if log.playername(input_box1.text):
                        self.game.highscoreplayer = input_box1.text
                        done = True
                        self.run_display = False
                        self.game.curr_menu = self.game.playerhighscore
                    input_box1.text = ''
                    input_box1.txt_surface = FONT.render(input_box1.text, True, input_box1.color)
                pygame.display.flip()
                clock.tick(20)
                self.blit_screen()

class PlayerhighscoreMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        log = Log()
        self.gamerscore = log.playerscores(self.game.highscoreplayer)
        
    #Funktion welche aufgerufen wird, wenn das entsprechende Menu aktiv ist und einen Loop für das anzuzeigende Menu ausführt,
    #welcher auf Eingaben wartet
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Highscores Player ' + self.game.highscoreplayer + ':', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            self.game.draw_text(str(self.gamerscore[0]), 15, self.mid_w, self.mid_h + 20)
            self.game.draw_text(str(self.gamerscore[1]), 15, self.mid_w, self.mid_h + 40)
            self.game.draw_text(str(self.gamerscore[2]), 15, self.mid_w, self.mid_h + 60)
            self.game.draw_text(str(self.gamerscore[3]), 15, self.mid_w, self.mid_h + 80)
            self.game.draw_text(str(self.gamerscore[4]), 15, self.mid_w, self.mid_h + 100)
            self.blit_screen()

    #Reagiert auf gedrückte Tasten mit entsprechender Funktion
    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.playerscores
            self.run_display = False

class GamescoreMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'SpaceInvaders'
        self.spacex, self.spacey = self.mid_w, self.mid_h + 20
        self.tetrisx, self.tetrisy = self.mid_w, self.mid_h + 40
        self.mindx, self.mindy = self.mid_w, self.mid_h + 60
        self.snakex, self.snakey = self.mid_w, self.mid_h + 80
        self.flapx, self.flapy = self.mid_w, self.mid_h + 100
        self.cursor_rect.midtop = (self.spacex + self.offset, self.spacey)

    #Funktion welche aufgerufen wird, wenn das entsprechende Menu aktiv ist und einen Loop für das anzuzeigende Menu ausführt,
    #welcher auf Eingaben wartet
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
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

    #Reagiert auf gedrückte Tasten mit entsprechender Funktion
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
                self.game.curr_menu = self.game.spacescoremenu
            elif self.state == 'Tetris':
                self.game.curr_menu = self.game.tetrisscoremenu
            elif self.state == 'Mastermind':
                self.game.curr_menu = self.game.masterscoremenu
            elif self.state == 'Snake':
                self.game.curr_menu = self.game.snakescoremenu
            elif self.state == 'Flappy':
                self.game.curr_menu = self.game.flappyscoremenu
        self.run_display = False

class SpaceMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.n = 0
        log = Log()
        self.spacescore = log.spaceinvaderscore()
        self.leng = len(self.spacescore)
        print("leng ist : " + str(self.leng))
        
    #Funktion welche aufgerufen wird, wenn das entsprechende Menu aktiv ist und einen Loop für das anzuzeigende Menu ausführt,
    #welcher auf Eingaben wartet
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Highscores Spaceinvader:', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            #if self.spacescore[0 + self.n] != []:
            if 1+ self.n <= self.leng:
                self.game.draw_text(str(self.spacescore[0 + self.n]), 15, self.mid_w, self.mid_h + 20)
            if 2+ self.n <= self.leng:
                self.game.draw_text(str(self.spacescore[1 + self.n]), 15, self.mid_w, self.mid_h + 40)
            if 3+ self.n <= self.leng:
                self.game.draw_text(str(self.spacescore[2 + self.n]), 15, self.mid_w, self.mid_h + 60)
            if 4+ self.n <= self.leng:
                self.game.draw_text(str(self.spacescore[3 + self.n]), 15, self.mid_w, self.mid_h + 80)
            if 5+ self.n <= self.leng:
                self.game.draw_text(str(self.spacescore[4 + self.n]), 15, self.mid_w, self.mid_h + 100)
            self.blit_screen()

    #Reagiert auf gedrückte Tasten mit entsprechender Funktion
    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.gamescores
            self.run_display = False
        elif self.game.UP_KEY:
            if self.n >0:
                self.n = self.n - 5
                print("N ist jetzt:" + str(self.n))              
        elif self.game.DOWN_KEY:
            if 5+self.n < self.leng:
                self.n =self.n + 5
                print("N ist jetzt:" + str(self.n))

class TetrisMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.n = 0
        log = Log()
        self.tetscore = log.tetrisscore()
        self.leng = len(self.tetscore)
        print("leng ist : " + str(self.leng))

    #Funktion welche aufgerufen wird, wenn das entsprechende Menu aktiv ist und einen Loop für das anzuzeigende Menu ausführt,
    #welcher auf Eingaben wartet    
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Highscores Tetris:', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            #if self.spacescore[0 + self.n] != []:
            if 1+ self.n <= self.leng:
                self.game.draw_text(str(self.tetscore[0 + self.n]), 15, self.mid_w, self.mid_h + 20)
            if 2+ self.n <= self.leng:
                self.game.draw_text(str(self.tetscore[1 + self.n]), 15, self.mid_w, self.mid_h + 40)
            if 3+ self.n <= self.leng:
                self.game.draw_text(str(self.tetscore[2 + self.n]), 15, self.mid_w, self.mid_h + 60)
            if 4+ self.n <= self.leng:
                self.game.draw_text(str(self.tetscore[3 + self.n]), 15, self.mid_w, self.mid_h + 80)
            if 5+ self.n <= self.leng:
                self.game.draw_text(str(self.tetscore[4 + self.n]), 15, self.mid_w, self.mid_h + 100)
            self.blit_screen()

    #Reagiert auf gedrückte Tasten mit entsprechender Funktion
    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.gamescores
            self.run_display = False
        elif self.game.UP_KEY:
            if self.n >0:
                self.n = self.n - 5
                print("N ist jetzt:" + str(self.n))              
        elif self.game.DOWN_KEY:
            if 5+self.n < self.leng:
                self.n =self.n + 5
                print("N ist jetzt:" + str(self.n))

class MastermindMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.n = 0
        log = Log()
        self.masterscore = log.mastermindscore()
        self.leng = len(self.masterscore)
        print("leng ist : " + str(self.leng))
    
    #Funktion welche aufgerufen wird, wenn das entsprechende Menu aktiv ist und einen Loop für das anzuzeigende Menu ausführt,
    #welcher auf Eingaben wartet    
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Highscores Mastermind:', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            #if self.spacescore[0 + self.n] != []:
            if 1+ self.n <= self.leng:
                self.game.draw_text(str(self.masterscore[0 + self.n]), 15, self.mid_w, self.mid_h + 20)
            if 2+ self.n <= self.leng:
                self.game.draw_text(str(self.masterscore[1 + self.n]), 15, self.mid_w, self.mid_h + 40)
            if 3+ self.n <= self.leng:
                self.game.draw_text(str(self.masterscore[2 + self.n]), 15, self.mid_w, self.mid_h + 60)
            if 4+ self.n <= self.leng:
                self.game.draw_text(str(self.masterscore[3 + self.n]), 15, self.mid_w, self.mid_h + 80)
            if 5+ self.n <= self.leng:
                self.game.draw_text(str(self.masterscore[4 + self.n]), 15, self.mid_w, self.mid_h + 100)
            self.blit_screen()

    #Reagiert auf gedrückte Tasten mit entsprechender Funktion
    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.gamescores
            self.run_display = False
        elif self.game.UP_KEY:
            if self.n >0:
                self.n = self.n - 5
                print("N ist jetzt:" + str(self.n))              
        elif self.game.DOWN_KEY:
            if 5+self.n < self.leng:
                self.n =self.n + 5
                print("N ist jetzt:" + str(self.n))


class SnakeMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.n = 0
        log = Log()
        print("snekscore=")
        self.snekscore = log.snakescore()
        print(self.snekscore)
        self.leng = len(self.snekscore)
        print("leng ist : " + str(self.leng))

    #Funktion welche aufgerufen wird, wenn das entsprechende Menu aktiv ist und einen Loop für das anzuzeigende Menu ausführt,
    #welcher auf Eingaben wartet    
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Highscores Snake:', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            #if self.spacescore[0 + self.n] != []:
            if 1+ self.n <= self.leng:
                self.game.draw_text(str(self.snekscore[0 + self.n]), 15, self.mid_w, self.mid_h + 20)
            if 2+ self.n <= self.leng:
                self.game.draw_text(str(self.snekscore[1 + self.n]), 15, self.mid_w, self.mid_h + 40)
            if 3+ self.n <= self.leng:
                self.game.draw_text(str(self.snekscore[2 + self.n]), 15, self.mid_w, self.mid_h + 60)
            if 4+ self.n <= self.leng:
                self.game.draw_text(str(self.snekscore[3 + self.n]), 15, self.mid_w, self.mid_h + 80)
            if 5+ self.n <= self.leng:
                self.game.draw_text(str(self.snekscore[4 + self.n]), 15, self.mid_w, self.mid_h + 100)
            self.blit_screen()

    #Reagiert auf gedrückte Tasten mit entsprechender Funktion
    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.gamescores
            self.run_display = False
        elif self.game.UP_KEY:
            if self.n >0:
                self.n = self.n - 5
                print("N ist jetzt:" + str(self.n))              
        elif self.game.DOWN_KEY:
            if 5+self.n < self.leng:
                self.n =self.n + 5
                print("N ist jetzt:" + str(self.n))

class FlappyMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.n = 0
        log = Log()
        self.flapscore = log.flappyscore()
        self.leng = len(self.flapscore)
        print("leng ist : " + str(self.leng))

    #Funktion welche aufgerufen wird, wenn das entsprechende Menu aktiv ist und einen Loop für das anzuzeigende Menu ausführt,
    #welcher auf Eingaben wartet    
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Highscores FlappyBird:', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            #if self.spacescore[0 + self.n] != []:
            if 1+ self.n <= self.leng:
                self.game.draw_text(str(self.flapscore[0 + self.n]), 15, self.mid_w, self.mid_h + 20)
            if 2+ self.n <= self.leng:
                self.game.draw_text(str(self.flapscore[1 + self.n]), 15, self.mid_w, self.mid_h + 40)
            if 3+ self.n <= self.leng:
                self.game.draw_text(str(self.flapscore[2 + self.n]), 15, self.mid_w, self.mid_h + 60)
            if 4+ self.n <= self.leng:
                self.game.draw_text(str(self.flapscore[3 + self.n]), 15, self.mid_w, self.mid_h + 80)
            if 5+ self.n <= self.leng:
                self.game.draw_text(str(self.flapscore[4 + self.n]), 15, self.mid_w, self.mid_h + 100)
            self.blit_screen()

    #Reagiert auf gedrückte Tasten mit entsprechender Funktion
    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.gamescores
            self.run_display = False
        elif self.game.UP_KEY:
            if self.n >0:
                self.n = self.n - 5
                print("N ist jetzt:" + str(self.n))              
        elif self.game.DOWN_KEY:
            if 5+self.n < self.leng:
                self.n =self.n + 5
                print("N ist jetzt:" + str(self.n))
            


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.modex, self.modey = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    #Funktion welche aufgerufen wird, wenn das entsprechende Menu aktiv ist und einen Loop für das anzuzeigende Menu ausführt,
    #welcher auf Eingaben wartet
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Options', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            self.game.draw_text("Volume", 15, self.volx, self.voly)
            self.game.draw_text("Mode", 15, self.modex, self.modey)
            self.draw_cursor()
            self.blit_screen()

    #Reagiert auf gedrückte Tasten mit entsprechender Funktion
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
    
    #Funktion welche aufgerufen wird, wenn das entsprechende Menu aktiv ist und einen Loop für das anzuzeigende Menu ausführt,
    #welcher auf Eingaben wartet, benötigt kein Check_input() da es nur ein Bild der Credits anzeigt
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
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







