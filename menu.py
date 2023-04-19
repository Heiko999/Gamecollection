import pygame
#from main import *
from input import InputBox
from button import Button
from logger import *
from usecase import *




signin_img = pygame.image.load('signin_btn.png').convert_alpha()
login_img = pygame.image.load('login_btn.png').convert_alpha()
delete_img = pygame.image.load('delete_btn.png').convert_alpha()
search_img = pygame.image.load('search_btn.png').convert_alpha()
FONT = pygame.font.Font(None, 32)

#Hauptklasse von welcher die anderen Klassen erben.
class Menu():
    #currentPlayer=''
    def __init__(self, game):
        pygame.init()
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100
        self.display = pygame.Surface((self.game.DISPLAY_W,self.game.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.game.DISPLAY_W,self.game.DISPLAY_H)))
        self.font_name = pygame.font.get_default_font()

    #Wird verwendet um den * Cursor an den ensprechenden Menupunkt zu setzen
    def draw_cursor(self):
        self.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)
    #Wird verwendet, um nach Ende einer Aktion in einem Menu das Bild zu aktualisieren
    def blit_screen(self):
        self.window.blit(self.display, (0, 0))
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
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                    self.game.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.game.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.game.UP_KEY = True

    def draw_text(self, text, size, x, y ):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, self.game.textcolor)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)

class LoginMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Login"
        self.screen = pygame.display.set_mode((self.game.DISPLAY_W,self.game.DISPLAY_H))
        self.input_box1 = InputBox(self.game.DISPLAY_W / 2 - 100,  50, 140, 32)
        self.input_box2 = InputBox(self.game.DISPLAY_W / 2 - 100, 100, 140, 32)
        self.input_boxes = [self.input_box1, self.input_box2]
        self.signin_button = Button(self.game.DISPLAY_W / 2 - 250, 200, signin_img, 0.4)
        self.login_button = Button(self.game.DISPLAY_W / 2 -50, 200, login_img, 0.4)
        self.delete_button = Button(self.game.DISPLAY_W / 2 + 150, 200, delete_img, 0.4)
        self.log = Log(DatabaseConnection1().getDB(), DatabaseConnection2().getDB())
    #Funktion welche aufgerufen wird, wenn das entsprechende Menu aktiv ist und einen Loop für das anzuzeigende Menu ausführt,
    #welcher auf Eingaben wartet
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            clock = pygame.time.Clock()
            self.check_events()
            self.display.fill(self.game.backgroundcolor)
            
            self.done = False
            while not self.done:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.done = True
                    for box in self.input_boxes:
                        #if event.type == pygame.K_RETURN:
                            #print(box.text + "test")
                        box.handle_event(event)
                for box in self.input_boxes:
                    box.update()
                
                self.display.fill((30, 30, 30))
                self.draw_text('Login Screen', 20, self.game.DISPLAY_W / 2, 30)
                for box in self.input_boxes:
                    box.draw(self.display)
                self.new_check_signin()
                self.new_check_login()
                self.new_check_delete()
                pygame.display.flip()
                clock.tick(20)
                self.blit_screen()
    
    def reset_boxes(self):
        self.input_box1.text = ''
        self.input_box2.text = ''
        self.input_box1.txt_surface = FONT.render(self.input_box1.text, True, self.input_box1.color)
        self.input_box2.txt_surface = FONT.render(self.input_box2.text, True, self.input_box2.color)

    #Legt bei Klick auf SignIn Button nach eingabe eines Usernamen und Passworts einen neuen Benutzer
    #in der Datenbank 
    def check_signin(self):
        self.signin_button.draw(self.screen)
        if self.signin_button.click():
            self.log.signIn(self.input_box1.text,self.input_box2.text)
            self.reset_boxes()

    def new_check_signin(self):
        self.signin_button.draw(self.screen)
        if self.signin_button.click():
            user_repo = UserRepositoryImpl()
            registration_use_case = RegistrationUseCase(user_repo)
            registration_use_case.register(self.input_box1.text, self.input_box2.text, 0, 0, 0, 0)
            high_score_use_case = HighScoreUseCase(user_repo)

            # Update the high score for Tetris game
            high_score_use_case.update_high_score(self.input_box1.text, 'Tetris', 100)
            self.reset_boxes()

    
    
    #Checkt nach auswahl des LoginButton, Ob Username und Passwort mit eintrag in Datenbank übereinstimmen
    #Stimmt es wird das Menu auf das Main Menu geändert 
    def check_login(self):
        self.login_button.draw(self.screen)
        if self.login_button.click():
            if self.log.login(self.input_box1.text, self.input_box2.text) == True:
                self.game.player = self.input_box1.text
                self.done = True
                self.run_display = False
                self.game.main_menu_set()
            self.reset_boxes()

    def new_check_login(self):
        self.login_button.draw(self.screen)
        if self.login_button.click():
            user_repo = UserRepositoryImpl()
            login_use_case = LoginUseCase(user_repo)
            if login_use_case.execute(self.input_box1.text, self.input_box2.text):
                self.game.player = self.input_box1.text
                self.done = True
                self.run_display = False
                self.game.main_menu_set()
            self.reset_boxes()

    #Checkt nach Klick auf den Deletebutton ob User und Passwort mit eintrag in Datenbank übereinstimmen.
    #Tun sie das, wird der Spieler gelöscht 
    def check_delete(self):
        self.delete_button.draw(self.screen)
        if self.delete_button.click():
            self.log.delete(self.input_box1.text,self.input_box2.text)
            self.reset_boxes()

    def new_check_delete(self):
        self.delete_button.draw(self.screen)
        if self.delete_button.click():
            user_repo = UserRepositoryImpl()
            delete_use_case = DeleteUseCase(user_repo)
            if delete_use_case.execute(self.input_box1.text,self.input_box2.text):
                self.reset_boxes()

                

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
            #draw the MenuText on the screen
            self.display.fill(self.game.backgroundcolor)
            mainM = "Main Menu" + "      Hello Player: " + str(self.game.player)
            self.draw_text(mainM, 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.draw_text("Start Game", 20, self.startx, self.starty)
            self.draw_text("Highscores", 20, self.highscorex, self.highscorey)
            self.draw_text("Options", 20, self.optionsx, self.optionsy)
            self.draw_text("Credits", 20, self.creditsx, self.creditsy)
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
                self.game.game_collection_set()
                #self.game.curr_menu = self.game.game_collection
            elif self.state == 'Highscores':
                self.game.highscores_set()
                #self.game.curr_menu = self.game.highscores
            elif self.state == 'Options':
                self.game.options_set()
                #self.game.curr_menu = self.game.options
            elif self.state == 'Credits':
                self.game.credits_set()
                #self.game.curr_menu = self.game.credits
            self.run_display = False

class GameMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'SpaceInvaders'
        self.spacex, self.spacey = self.mid_w, self.mid_h + 20
        self.tetrisx, self.tetrisy = self.mid_w, self.mid_h + 40
        self.snakex, self.snakey = self.mid_w, self.mid_h + 60
        self.flapx, self.flapy = self.mid_w, self.mid_h + 80
        self.cursor_rect.midtop = (self.spacex + self.offset, self.spacey)

    #Funktion welche aufgerufen wird, wenn das entsprechende Menu aktiv ist und einen Loop für das anzuzeigende Menu ausführt,
    #welcher auf Eingaben wartet
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            #draw the MenuText on the screen
            self.display.fill(self.game.backgroundcolor)
            self.draw_text('GameCollection', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            self.draw_text("SpaceInvaders", 15, self.spacex, self.spacey)
            self.draw_text("Tetris", 15, self.tetrisx, self.tetrisy)
            self.draw_text("Snake", 15, self.snakex, self.snakey)
            self.draw_text("Flappy Bird", 15, self.flapx, self.flapy)
            self.draw_cursor()
            self.blit_screen()



    #Reagiert auf gedrückte Tasten mit entsprechender Funktion
    def check_input(self):
        if self.game.BACK_KEY:
            self.game.main_menu_set()
            #self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.DOWN_KEY:
            if self.state == 'SpaceInvaders':
                self.state = 'Tetris'
                self.cursor_rect.midtop = (self.tetrisx + self.offset, self.tetrisy)
            elif self.state == 'Tetris':
                self.state = 'Snake'
                self.cursor_rect.midtop = (self.snakex + self.offset, self.snakey)
            elif self.state == 'Snake':
                self.state = 'Flappy'
                self.cursor_rect.midtop = (self.flapx + self.offset, self.flapy)
            elif self.state == 'Flappy':
                self.state = 'SpaceInvaders'
                self.cursor_rect.midtop = (self.spacex + self.offset, self.spacey)
        elif self.game.UP_KEY:
            if self.state == 'Tetris':
                self.state = 'SpaceInvaders'
                self.cursor_rect.midtop = (self.spacex + self.offset, self.spacey)
            elif self.state == 'SpaceInvaders':
                self.state = 'Flappy'
                self.cursor_rect.midtop = (self.flapx + self.offset, self.flapy)
            elif self.state == 'Flappy':
                self.state = 'Snake'
                self.cursor_rect.midtop = (self.snakex + self.offset, self.snakey)
            elif self.state == 'Snake':
                self.state = 'Tetris'
                self.cursor_rect.midtop = (self.tetrisx + self.offset, self.tetrisy)
        elif self.game.START_KEY:
            if self.state == 'SpaceInvaders':
                self.game.playing = True
            if self.state == 'Tetris':
                self.game.playing = True
            if self.state == 'Snake':
                self.game.playing = True
            if self.state == 'Flappy':
                self.game.playing = True
        self.run_display = False
        if self.game.closedcounter == 1:
            self.game.closedcounter = 0
            self.window = pygame.display.set_mode(((self.game.DISPLAY_W,self.game.DISPLAY_H)))

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
            #draw the MenuText on the screen
            self.display.fill(self.game.backgroundcolor)
            self.draw_text('Highscores', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            self.draw_text("Playerscore", 15, self.phighscorex, self.phighscorey)
            self.draw_text("Gamescore", 15, self.ghighscorex, self.ghighscorey)
            self.draw_cursor()
            self.blit_screen()
            


    #Reagiert auf gedrückte Tasten mit entsprechender Funktion
    def check_input(self):
        if self.game.BACK_KEY:
            self.game.main_menu_set()
            #self.game.curr_menu = self.game.main_menu
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
                self.game.gamescores_set()
                #self.game.curr_menu = self.game.gamescores
                self.run_display = False
            elif self.state == 'Playerscore':
                self.game.playerscores_set()
                #self.game.curr_menu = self.game.playerscores
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
            self.display.fill(self.game.backgroundcolor)
            #log = Log(DatabaseConnection1().getDB(), DatabaseConnection2().getDB())
            user_repository = UserRepositoryImpl()
            Playercheck = FindPlayerUseCase(user_repository)
            #Erzeugt TextBoxen und Buttons für das LoginMenu
            input_box1 = InputBox(self.game.DISPLAY_W / 2 - 100,  50, 140, 32)  
            input_button = Button(self.game.DISPLAY_W / 2 -50, 200, search_img, 0.4)
            #buttons =[start_button, exit_button]
            self.done = False

            while not self.done:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.done = True
                    input_box1.handle_event(event)
                    input_box1.update()
                
                self.display.fill((30, 30, 30))
                self.draw_text('Highscores for which Player?', 20, self.game.DISPLAY_W / 2, 30)
                input_box1.draw(self.display)
                #Legt bei Klick auf SignIn Button nach eingabe eines Usernamen und Passworts einen neuen Benutzer
                #in der Datenbank an

                input_button.draw(self.screen) 
                if input_button.click():
                    print('input')
                    print(input_box1.text)
                
                    if Playercheck.execute(input_box1.text):
                        self.game.highscoreplayer = input_box1.text
                        self.done = True
                        self.run_display = False
                        self.game.playerhighscores_set()
                        #self.game.curr_menu = self.game.playerhighscore
                    input_box1.text = ''
                    input_box1.txt_surface = FONT.render(input_box1.text, True, input_box1.color)
                pygame.display.flip()
                clock.tick(20)
                self.blit_screen()
    
    def check_input(self):
        if self.game.BACK_KEY:
            print("jo geht")
            self.game.highscores_set()
            #self.game.curr_menu = self.game.highscores
            self.done = True
            self.run_display = False

class PlayerhighscoreMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        
        
    #Funktion welche aufgerufen wird, wenn das entsprechende Menu aktiv ist und einen Loop für das anzuzeigende Menu ausführt,
    #welcher auf Eingaben wartet
    def display_menu(self):
        #self.log = Log(DatabaseConnection1().getDB(), DatabaseConnection2().getDB())
        user_repository = UserRepositoryImpl()
        playerhigh_score_use_case = PlayerHighscoreUseCase(user_repository)
        self.gamerscore = playerhigh_score_use_case.execute(self.game.highscoreplayer)
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            #draw the MenuText on the screen
            self.display.fill(self.game.backgroundcolor)
            self.draw_text('Highscores Player ' + self.game.highscoreplayer + ':', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            self.draw_text(str(self.gamerscore[0]).replace("(", "").replace("'", "").replace(",", " -").replace(")", ""), 15, self.mid_w, self.mid_h + 20)
            self.draw_text(str(self.gamerscore[1]).replace("(", "").replace("'", "").replace(",", " -").replace(")", ""), 15, self.mid_w, self.mid_h + 40)
            self.draw_text(str(self.gamerscore[2]).replace("(", "").replace("'", "").replace(",", " -").replace(")", ""), 15, self.mid_w, self.mid_h + 60)
            self.draw_text(str(self.gamerscore[3]).replace("(", "").replace("'", "").replace(",", " -").replace(")", ""), 15, self.mid_w, self.mid_h + 80)
            self.blit_screen()


    #Reagiert auf gedrückte Tasten mit entsprechender Funktion
    def check_input(self):
        if self.game.BACK_KEY:
            self.game.highscores_set()
            #self.game.curr_menu = self.game.highscores
            self.run_display = False

class GamescoreMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'SpaceInvaders'
        self.spacex, self.spacey = self.mid_w, self.mid_h + 20
        self.tetrisx, self.tetrisy = self.mid_w, self.mid_h + 40
        self.snakex, self.snakey = self.mid_w, self.mid_h + 60
        self.flapx, self.flapy = self.mid_w, self.mid_h + 80
        self.cursor_rect.midtop = (self.spacex + self.offset, self.spacey)

    #Funktion welche aufgerufen wird, wenn das entsprechende Menu aktiv ist und einen Loop für das anzuzeigende Menu ausführt,
    #welcher auf Eingaben wartet
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            #draw the MenuText on the screen
            self.display.fill(self.game.backgroundcolor)
            self.draw_text('GameCollection', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            self.draw_text("SpaceInvaders", 15, self.spacex, self.spacey)
            self.draw_text("Tetris", 15, self.tetrisx, self.tetrisy)
            self.draw_text("Snake", 15, self.snakex, self.snakey)
            self.draw_text("Flappy Bird", 15, self.flapx, self.flapy)
            self.draw_cursor()
            self.blit_screen()


    #Reagiert auf gedrückte Tasten mit entsprechender Funktion
    def check_input(self):
        if self.game.BACK_KEY:
            self.game.main_menu_set()
            #self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.DOWN_KEY:
            if self.state == 'SpaceInvaders':
                self.state = 'Tetris'
                self.cursor_rect.midtop = (self.tetrisx + self.offset, self.tetrisy)
            elif self.state == 'Tetris':
                self.state = 'Snake'
                self.cursor_rect.midtop = (self.snakex + self.offset, self.snakey)
            elif self.state == 'Snake':
                self.state = 'Flappy'
                self.cursor_rect.midtop = (self.flapx + self.offset, self.flapy)
            elif self.state == 'Flappy':
                self.state = 'SpaceInvaders'
                self.cursor_rect.midtop = (self.spacex + self.offset, self.spacey)
        elif self.game.UP_KEY:
            if self.state == 'Tetris':
                self.state = 'SpaceInvaders'
                self.cursor_rect.midtop = (self.spacex + self.offset, self.spacey)
            elif self.state == 'SpaceInvaders':
                self.state = 'Flappy'
                self.cursor_rect.midtop = (self.flapx + self.offset, self.flapy)
            elif self.state == 'Flappy':
                self.state = 'Snake'
                self.cursor_rect.midtop = (self.snakex + self.offset, self.snakey)
            elif self.state == 'Snake':
                self.state = 'Tetris'
                self.cursor_rect.midtop = (self.tetrisx + self.offset, self.tetrisy)
        elif self.game.START_KEY:
            if self.state == 'SpaceInvaders':
                self.game.spacescoremenu_set()
                #self.game.curr_menu = self.game.spacescoremenu
            elif self.state == 'Tetris':
                self.game.tetrisscoremenu_set()
                #self.game.curr_menu = self.game.tetrisscoremenu
            elif self.state == 'Snake':
                self.game.snakescoremenu_set()
                #self.game.curr_menu = self.game.snakescoremenu
            elif self.state == 'Flappy':
                self.game.flappyscoremenu_set()
                #self.game.curr_menu = self.game.flappyscoremenu
        self.run_display = False

class SpaceMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.n = 0
        #log = Log(DatabaseConnection1().getDB(), DatabaseConnection2().getDB())
        user_repository = UserRepositoryImpl()
        gamehigh_score_use_case = GamesHighscoreUseCase(user_repository)
        self.spacescore = gamehigh_score_use_case.execute('spaceinvader')
        #self.spacescore = log.gamesscores('spaceinvader')
        self.leng = len(self.spacescore)
        print("leng ist : " + str(self.leng))
        
    #Funktion welche aufgerufen wird, wenn das entsprechende Menu aktiv ist und einen Loop für das anzuzeigende Menu ausführt,
    #welcher auf Eingaben wartet
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            #draw the MenuText on the screen:
            self.display.fill(self.game.backgroundcolor)
            self.draw_text('Highscores Spaceinvader:', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            #Zeichnet die aktuellen Highscores. Self.leng ist die länge der Liste welche die Highscores enthält self n kann immer 
            # um 5 erhöht werden und somit soll in 5er inkrementen durch die komplette highscoreliste gescrollt werden und 
            #immer 5 Scores auf einmal angeschaut werden
            if 1+ self.n <= self.leng:
                self.draw_text(str(self.spacescore[0 + self.n]).replace("(", "").replace("'", "").replace(",", " -").replace(")", ""), 15, self.mid_w, self.mid_h + 20)
            if 2+ self.n <= self.leng:
                self.draw_text(str(self.spacescore[1 + self.n]).replace("(", "").replace("'", "").replace(",", " -").replace(")", ""), 15, self.mid_w, self.mid_h + 40)
            if 3+ self.n <= self.leng:
                self.draw_text(str(self.spacescore[2 + self.n]).replace("(", "").replace("'", "").replace(",", " -").replace(")", ""), 15, self.mid_w, self.mid_h + 60)
            if 4+ self.n <= self.leng:
                self.draw_text(str(self.spacescore[3 + self.n]).replace("(", "").replace("'", "").replace(",", " -").replace(")", ""), 15, self.mid_w, self.mid_h + 80)
            if 5+ self.n <= self.leng:
                self.draw_text(str(self.spacescore[4 + self.n]).replace("(", "").replace("'", "").replace(",", " -").replace(")", ""), 15, self.mid_w, self.mid_h + 100)
            self.blit_screen()




    #Reagiert auf gedrückte Tasten mit entsprechender Funktion
    def check_input(self):
        if self.game.BACK_KEY:
            self.game.gamescores_set()
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
        #log = Log(DatabaseConnection1().getDB(), DatabaseConnection2().getDB())
        #self.tetscore = log.gamesscores('tetris')
        user_repository = UserRepositoryImpl()
        gamehigh_score_use_case = GamesHighscoreUseCase(user_repository)
        self.tetscore = gamehigh_score_use_case.execute('tetris')
        self.leng = len(self.tetscore)
        print("leng ist : " + str(self.leng))

    #Funktion welche aufgerufen wird, wenn das entsprechende Menu aktiv ist und einen Loop für das anzuzeigende Menu ausführt,
    #welcher auf Eingaben wartet    
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            #draw the MenuText on the screen
            self.display.fill(self.game.backgroundcolor)
            self.draw_text('Highscores Tetris:', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            #Zeichnet die aktuellen Highscores. Self.leng ist die länge der Liste welche die Highscores enthält self n kann immer 
            # um 5 erhöht werden und somit soll in 5er inkrementen durch die komplette highscoreliste gescrollt werden und 
            #immer 5 Scores auf einmal angeschaut werden
            if 1+ self.n <= self.leng:
                self.draw_text(str(self.tetscore[0 + self.n]).replace("(", "").replace("'", "").replace(",", " -").replace(")", ""), 15, self.mid_w, self.mid_h + 20)
            if 2+ self.n <= self.leng:
                self.draw_text(str(self.tetscore[1 + self.n]).replace("(", "").replace("'", "").replace(",", " -").replace(")", ""), 15, self.mid_w, self.mid_h + 40)
            if 3+ self.n <= self.leng:
                self.draw_text(str(self.tetscore[2 + self.n]).replace("(", "").replace("'", "").replace(",", " -").replace(")", ""), 15, self.mid_w, self.mid_h + 60)
            if 4+ self.n <= self.leng:
                self.draw_text(str(self.tetscore[3 + self.n]).replace("(", "").replace("'", "").replace(",", " -").replace(")", ""), 15, self.mid_w, self.mid_h + 80)
            if 5+ self.n <= self.leng:
                self.draw_text(str(self.tetscore[4 + self.n]).replace("(", "").replace("'", "").replace(",", " -").replace(")", ""), 15, self.mid_w, self.mid_h + 100)
            self.blit_screen()


    #Reagiert auf gedrückte Tasten mit entsprechender Funktion
    def check_input(self):
        if self.game.BACK_KEY:
            self.game.gamescores_set()
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
        #log = Log(DatabaseConnection1().getDB(), DatabaseConnection2().getDB())
        #print("snakescore=")
        #self.snakescore = log.gamesscores('snake')
        user_repository = UserRepositoryImpl()
        gamehigh_score_use_case = GamesHighscoreUseCase(user_repository)
        self.snakescore = gamehigh_score_use_case.execute('snake')
        print(self.snakescore)
        self.leng = len(self.snakescore)
        print("leng ist : " + str(self.leng))

    #Funktion welche aufgerufen wird, wenn das entsprechende Menu aktiv ist und einen Loop für das anzuzeigende Menu ausführt,
    #welcher auf Eingaben wartet    
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            #draw the MenuText on the screen 
            self.display.fill(self.game.backgroundcolor)
            self.draw_text('Highscores Snake:', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            #Zeichnet die aktuellen Highscores. Self.leng ist die länge der Liste welche die Highscores enthält self n kann immer 
            # um 5 erhöht werden und somit soll in 5er inkrementen durch die komplette highscoreliste gescrollt werden und 
            #immer 5 Scores auf einmal angeschaut werden
            if 1+ self.n <= self.leng:
                self.draw_text(str(self.snakescore[0 + self.n]).replace("(", "").replace("'", "").replace(",", " -").replace(")", ""), 15, self.mid_w, self.mid_h + 20)
            if 2+ self.n <= self.leng:
                self.draw_text(str(self.snakescore[1 + self.n]).replace("(", "").replace("'", "").replace(",", " -").replace(")", ""), 15, self.mid_w, self.mid_h + 40)
            if 3+ self.n <= self.leng:
                self.draw_text(str(self.snakescore[2 + self.n]).replace("(", "").replace("'", "").replace(",", " -").replace(")", ""), 15, self.mid_w, self.mid_h + 60)
            if 4+ self.n <= self.leng:
                self.draw_text(str(self.snakescore[3 + self.n]).replace("(", "").replace("'", "").replace(",", " -").replace(")", ""), 15, self.mid_w, self.mid_h + 80)
            if 5+ self.n <= self.leng:
                self.draw_text(str(self.snakescore[4 + self.n]).replace("(", "").replace("'", "").replace(",", " -").replace(")", ""), 15, self.mid_w, self.mid_h + 100)
            self.blit_screen()

            

    #Reagiert auf gedrückte Tasten mit entsprechender Funktion
    def check_input(self):
        if self.game.BACK_KEY:
            self.game.gamescores_set()
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
        user_repository = UserRepositoryImpl()
        gamehigh_score_use_case = GamesHighscoreUseCase(user_repository)
        self.flapscore = gamehigh_score_use_case.execute('flappy')
        self.leng = len(self.flapscore)
        print("leng ist : " + str(self.leng))

    #Funktion welche aufgerufen wird, wenn das entsprechende Menu aktiv ist und einen Loop für das anzuzeigende Menu ausführt,
    #welcher auf Eingaben wartet    
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            #draw the MenuText on the screen 
            self.display.fill(self.game.backgroundcolor)
            self.draw_text('Highscores FlappyBird:', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            #Zeichnet die aktuellen Highscores. Self.leng ist die länge der Liste welche die Highscores enthält self n kann immer 
            # um 5 erhöht werden und somit soll in 5er inkrementen durch die komplette highscoreliste gescrollt werden und 
            #immer 5 Scores auf einmal angeschaut werden
            if 1+ self.n <= self.leng:
                self.draw_text(str(self.flapscore[0 + self.n]).replace("(", "").replace("'", "").replace(",", " -").replace(")", ""), 15, self.mid_w, self.mid_h + 20)
            if 2+ self.n <= self.leng:
                self.draw_text(str(self.flapscore[1 + self.n]).replace("(", "").replace("'", "").replace(",", " -").replace(")", ""), 15, self.mid_w, self.mid_h + 40)
            if 3+ self.n <= self.leng:
                self.draw_text(str(self.flapscore[2 + self.n]).replace("(", "").replace("'", "").replace(",", " -").replace(")", ""), 15, self.mid_w, self.mid_h + 60)
            if 4+ self.n <= self.leng:
                self.draw_text(str(self.flapscore[3 + self.n]).replace("(", "").replace("'", "").replace(",", " -").replace(")", ""), 15, self.mid_w, self.mid_h + 80)
            if 5+ self.n <= self.leng:
                self.draw_text(str(self.flapscore[4 + self.n]).replace("(", "").replace("'", "").replace(",", " -").replace(")", ""), 15, self.mid_w, self.mid_h + 100)
            self.blit_screen()


    #Reagiert auf gedrückte Tasten mit entsprechender Funktion
    def check_input(self):
        if self.game.BACK_KEY:
            self.game.gamescores_set()
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
        self.volume = ""
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.modex, self.modey = self.mid_w, self.mid_h + 40
        self.voltextx, self.voltexty = self.mid_w, self.mid_h + 60
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    #Funktion welche aufgerufen wird, wenn das entsprechende Menu aktiv ist und einen Loop für das anzuzeigende Menu ausführt,
    #welcher auf Eingaben wartet
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            #draw the MenuText on the screen 
            self.display.fill(self.game.backgroundcolor)
            self.draw_text('Options', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            self.draw_text("Volume", 15, self.volx, self.voly)
            self.draw_text("Mode", 15, self.modex, self.modey)
            self.draw_text(f"""{self.volume}""", 15, self.voltextx, self.voltexty)
            self.draw_cursor()
            self.blit_screen()


    #Reagiert auf gedrückte Tasten mit entsprechender Funktion
    def check_input(self):
        if self.game.BACK_KEY:
            self.volume = ""
            self.game.main_menu_set()
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
                if self.game.backgroundcolor == (0, 0, 0):
                    self.game.backgroundcolor = (57, 57, 57)
                    self.game.textcolor = (0, 0, 0)
                    print(self.game.backgroundcolor)
                    print(self.game.textcolor)
                    return
                elif self.game.backgroundcolor == (57, 57, 57):
                    self.game.backgroundcolor = (2, 56, 5)
                    self.game.textcolor = (57, 57, 57)
                    print(self.game.backgroundcolor)
                    print(self.game.textcolor)
                    return
                elif self.game.backgroundcolor == (2, 56, 5):
                    self.game.backgroundcolor = (0, 0, 0)
                    self.game.textcolor = (255, 255, 255)
                    return
            if self.state == 'Volume':
                print("Volume activated / deactivated")
                self.volume = 'volume - (doesn´t change anything currently)'
                self.draw_display()
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
                self.game.main_menu_set()
                self.run_display = False
            #draw the MenuText on the screen    
            self.display.fill(self.game.backgroundcolor)
            self.draw_text('Credits', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.draw_text('Made by ', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10)
            self.draw_text('Heiko Herrmann', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 30)
            self.draw_text('&', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 50)
            self.draw_text('Tom Witzel', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 70)
            self.blit_screen()
