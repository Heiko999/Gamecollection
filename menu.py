from input import InputBox
from button import Button
from usecase import *

signin_img = pygame.image.load('files/signin_btn.png').convert_alpha()
login_img = pygame.image.load('files/login_btn.png').convert_alpha()
delete_img = pygame.image.load('files/delete_btn.png').convert_alpha()
search_img = pygame.image.load('files/search_btn.png').convert_alpha()
FONT = pygame.font.Font(None, 32)

#Main class; other classes inherit from this class
class Menu():
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

    #sets the "*" cursor to the currently chosen option
    def draw_cursor(self):
        self.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)
    #refreshes the UI after an action
    def blit_screen(self):
        self.window.blit(self.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

    #saves the pressed keys
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
    #this function is called when the corresponding menu is active and looped
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            clock = pygame.time.Clock()
            self.check_events()
            self.display.fill(self.game.backgroundcolor)
            
            self.done = False
            while not self.done:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        exit()
                    for box in self.input_boxes:
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
    
    #creates a new user and saves the username & password to the database after the button has been pressed
    def new_check_signin(self):
        self.signin_button.draw(self.screen)
        if self.signin_button.click():
            user_repo = UserRepositoryImpl()
            registration_use_case = RegistrationUseCase(user_repo)
            registration_use_case.register(self.input_box1.text, self.input_box2.text, 0, 0, 0, 0)
            self.reset_boxes()

    
    #checks if a uuser with the same username & password exists
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
    
    #this function is called when the corresponding menu is active and looped
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            self.draw_display()

    def draw_display(self):
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
            exit()

    #calls the function that belongs to the input
    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.game_collection_set()
            elif self.state == 'Highscores':
                self.game.highscores_set()
            elif self.state == 'Options':
                self.game.options_set()
            elif self.state == 'Credits':
                self.game.credits_set()
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

    #this function is called when the corresponding menu is active and looped
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            self.draw_display()

    def draw_display(self):
        self.display.fill(self.game.backgroundcolor)
        self.draw_text('GameCollection', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
        self.draw_text("SpaceInvaders", 15, self.spacex, self.spacey)
        self.draw_text("Tetris", 15, self.tetrisx, self.tetrisy)
        self.draw_text("Snake", 15, self.snakex, self.snakey)
        self.draw_text("Flappy Bird", 15, self.flapx, self.flapy)
        self.draw_cursor()
        self.blit_screen()



    #calls the function that belongs to the input
    def check_input(self):
        if self.game.BACK_KEY:
            self.game.main_menu_set()
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

    #this function is called when the corresponding menu is active and looped
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            self.draw_display()

    def draw_display(self):
        self.display.fill(self.game.backgroundcolor)
        self.draw_text('Highscores', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
        self.draw_text("Playerscore", 15, self.phighscorex, self.phighscorey)
        self.draw_text("Gamescore", 15, self.ghighscorex, self.ghighscorey)
        self.draw_cursor()
        self.blit_screen()
            


    #calls the function that belongs to the input
    def check_input(self):
        if self.game.BACK_KEY:
            self.game.main_menu_set()
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
                self.run_display = False
            elif self.state == 'Playerscore':
                self.game.playerscores_set()
                self.run_display = False
                

class PlayerscoreMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Playerscore"
        self.screen = pygame.display.set_mode((self.game.DISPLAY_W,self.game.DISPLAY_H))
    #this function is called when the corresponding menu is active and looped
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            clock = pygame.time.Clock()
            self.display.fill(self.game.backgroundcolor)
            user_repository = UserRepositoryImpl()
            Playercheck = FindPlayerUseCase(user_repository)
            #creates textboxes and buttons for the login menu
            input_box1 = InputBox(self.game.DISPLAY_W / 2 - 100,  50, 140, 32)  
            input_button = Button(self.game.DISPLAY_W / 2 -50, 200, search_img, 0.4)
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
                input_button.draw(self.screen)
                if input_button.click():
                
                    if Playercheck.execute(input_box1.text):
                        self.game.highscoreplayer = input_box1.text
                        self.done = True
                        self.run_display = False
                        self.game.playerhighscores_set()
                    input_box1.text = ''
                    input_box1.txt_surface = FONT.render(input_box1.text, True, input_box1.color)
                pygame.display.flip()
                clock.tick(20)
                self.blit_screen()

    # calls the function that belongs to the input
    def check_input(self):
        if self.game.BACK_KEY:
            self.game.highscores_set()
            self.done = True
            self.run_display = False

class PlayerhighscoreMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        
        
    #this function is called when the corresponding menu is active and looped
    def display_menu(self):
        user_repository = UserRepositoryImpl()
        playerhigh_score_use_case = PlayerHighscoreUseCase(user_repository)
        self.gamerscore = playerhigh_score_use_case.execute(self.game.highscoreplayer)
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            self.draw_display()

    def draw_display(self):
        self.display.fill(self.game.backgroundcolor)
        self.draw_text('Highscores Player ' + self.game.highscoreplayer + ':', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
        for i in range(4):
            gamescore_formatted = str(self.gamerscore[i]).replace("(", "").replace("'", "").replace(",", " -").replace(")", "")
            self.draw_text(gamescore_formatted, 15, self.mid_w, self.mid_h + 20 + (i * 20))
        self.blit_screen()


    #calls the function that belongs to the input
    def check_input(self):
        if self.game.BACK_KEY:
            self.game.highscores_set()
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

    #this function is called when the corresponding menu is active and looped
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            self.draw_display()

    def draw_display(self):
        self.display.fill(self.game.backgroundcolor)
        self.draw_text('GameCollection', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
        self.draw_text("SpaceInvaders", 15, self.spacex, self.spacey)
        self.draw_text("Tetris", 15, self.tetrisx, self.tetrisy)
        self.draw_text("Snake", 15, self.snakex, self.snakey)
        self.draw_text("Flappy Bird", 15, self.flapx, self.flapy)
        self.draw_cursor()
        self.blit_screen()


    #calls the function that belongs to the input
    def check_input(self):
        if self.game.BACK_KEY:
            self.game.main_menu_set()
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
            elif self.state == 'Tetris':
                self.game.tetrisscoremenu_set()
            elif self.state == 'Snake':
                self.game.snakescoremenu_set()
            elif self.state == 'Flappy':
                self.game.flappyscoremenu_set()
        self.run_display = False

class SpaceMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.n = 0
        user_repository = UserRepositoryImpl()
        gamehigh_score_use_case = GamesHighscoreUseCase(user_repository)
        self.spacescore = gamehigh_score_use_case.execute('spaceinvader')
        self.leng = len(self.spacescore)
        
    #this function is called when the corresponding menu is active and looped
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            self.draw_display()

    def draw_display(self):
        self.display.fill(self.game.backgroundcolor)
        self.draw_text('Highscores Spaceinvader:', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
        #shows the highscore list in increments of 5 players
        for i in range(5):
            if i + 1 + self.n <= self.leng:
                spacescore_formatted = str(self.spacescore[i + self.n]).replace("(", "").replace("'", "").replace(",", " -").replace(")", "")
                self.draw_text(spacescore_formatted, 15, self.mid_w, self.mid_h + 20 + (i * 20))
        self.blit_screen()




    #calls the function that belongs to the input
    def check_input(self):
        if self.game.BACK_KEY:
            self.game.gamescores_set()
            self.run_display = False
        elif self.game.UP_KEY:
            if self.n >0:
                self.n = self.n - 5
        elif self.game.DOWN_KEY:
            if 5+self.n < self.leng:
                self.n =self.n + 5

class TetrisMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.n = 0
        user_repository = UserRepositoryImpl()
        gamehigh_score_use_case = GamesHighscoreUseCase(user_repository)
        self.tetscore = gamehigh_score_use_case.execute('tetris')
        self.leng = len(self.tetscore)

    #this function is called when the corresponding menu is active and looped
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            self.draw_display()

    def draw_display(self):
        self.display.fill(self.game.backgroundcolor)
        self.draw_text('Highscores Tetris:', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
        #shows the highscore list in increments of 5 players
        for i in range(5):
            if i + 1 + self.n <= self.leng:
                tetscore_formatted = str(self.tetscore[i + self.n]).replace("(", "").replace("'", "").replace(",", " -").replace(")", "")
                self.draw_text(tetscore_formatted, 15, self.mid_w, self.mid_h + 20 + (i * 20))
        self.blit_screen()


    #calls the function that belongs to the input
    def check_input(self):
        if self.game.BACK_KEY:
            self.game.gamescores_set()
            self.run_display = False
        elif self.game.UP_KEY:
            if self.n >0:
                self.n = self.n - 5
        elif self.game.DOWN_KEY:
            if 5+self.n < self.leng:
                self.n =self.n + 5

class SnakeMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.n = 0
        user_repository = UserRepositoryImpl()
        gamehigh_score_use_case = GamesHighscoreUseCase(user_repository)
        self.snakescore = gamehigh_score_use_case.execute('snake')
        self.leng = len(self.snakescore)

    #this function is called when the corresponding menu is active and looped
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            self.draw_display()

    def draw_display(self):
        self.display.fill(self.game.backgroundcolor)
        self.draw_text('Highscores Snake:', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
        #shows the highscore list in increments of 5 players
        for i in range(5):
            if i + 1 + self.n <= self.leng:
                snakescore_formatted = str(self.snakescore[i + self.n]).replace("(", "").replace("'", "").replace(",", " -").replace(")", "")
                self.draw_text(snakescore_formatted, 15, self.mid_w, self.mid_h + 20 + (i * 20))
        self.blit_screen()

            

    #calls the function that belongs to the input
    def check_input(self):
        if self.game.BACK_KEY:
            self.game.gamescores_set()
            self.run_display = False
        elif self.game.UP_KEY:
            if self.n >0:
                self.n = self.n - 5
        elif self.game.DOWN_KEY:
            if 5+self.n < self.leng:
                self.n =self.n + 5

class FlappyMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.n = 0
        user_repository = UserRepositoryImpl()
        gamehigh_score_use_case = GamesHighscoreUseCase(user_repository)
        self.flapscore = gamehigh_score_use_case.execute('flappy')
        self.leng = len(self.flapscore)

    #this function is called when the corresponding menu is active and looped
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            self.draw_display()

    def draw_display(self):
        self.display.fill(self.game.backgroundcolor)
        self.draw_text('Highscores FlappyBird:', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
        #shows the highscore list in increments of 5 players
        for i in range(5):
            if i + 1 + self.n <= self.leng:
                flapscore_formatted = str(self.flapscore[i + self.n]).replace("(", "").replace("'", "").replace(",", " -").replace(")", "")
                self.draw_text(flapscore_formatted, 15, self.mid_w, self.mid_h + 20 + (i * 20))
        self.blit_screen()


    #calls the function that belongs to the input
    def check_input(self):
        if self.game.BACK_KEY:
            self.game.gamescores_set()
            self.run_display = False
        elif self.game.UP_KEY:
            if self.n >0:
                self.n = self.n - 5
        elif self.game.DOWN_KEY:
            if 5+self.n < self.leng:
                self.n =self.n + 5
            


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.volume = ""
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.modex, self.modey = self.mid_w, self.mid_h + 40
        self.voltextx, self.voltexty = self.mid_w, self.mid_h + 60
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    #this function is called when the corresponding menu is active and looped
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            self.draw_display()

    def draw_display(self):
        self.display.fill(self.game.backgroundcolor)
        self.draw_text('Options', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
        self.draw_text("Volume", 15, self.volx, self.voly)
        self.draw_text("Mode", 15, self.modex, self.modey)
        self.draw_text(f"""{self.volume}""", 15, self.voltextx, self.voltexty)
        self.draw_cursor()
        self.blit_screen()


    #calls the function that belongs to the input
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
                    return
                elif self.game.backgroundcolor == (57, 57, 57):
                    self.game.backgroundcolor = (2, 56, 5)
                    self.game.textcolor = (57, 57, 57)
                    return
                elif self.game.backgroundcolor == (2, 56, 5):
                    self.game.backgroundcolor = (0, 0, 0)
                    self.game.textcolor = (255, 255, 255)
                    return
            if self.state == 'Volume':
                self.volume = 'volume - (doesn´t change anything currently)'
            

class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
    
    #this function is called when the corresponding menu is active and looped; no check_input() since it only shows the credits
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.main_menu_set()
                self.run_display = False
            self.draw_display()

    def draw_display(self):
        self.display.fill(self.game.backgroundcolor)
        self.draw_text('Credits', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
        self.draw_text('Made by ', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10)
        self.draw_text('Heiko Herrmann', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 30)
        self.draw_text('&', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 50)
        self.draw_text('Tom Witzel', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 70)
        self.blit_screen()
