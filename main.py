#"Start-Function"
#Initializes the game by creating a game class object
#responsible for switching menus through calling display_menu
#starts a gameloop if a game is called via the game Menu

from game import Game
g = Game()
g.login_set()
while g.running:
    g.curr_menu.display_menu()
    g.game_loop()
    