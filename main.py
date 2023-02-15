#"Start-Funktion" 
#Initialisiert das komplette Spiel, indem ein Objet der GameKlasse erzeugt wird
#Switcht durch die verschiedenen Menus, indem die Variable curr_Menu auf das aktuelle Menu geändert wird und in diesem Menu
#die display_Menu Funktion ausgeführt wird, welche dafür sorgt, dass das Bild für dieses Menu generiert wird
#Sobald ein Spiel im GameMenu aufgerufen wird, wird der Gameloop gestartet welcher ein Objekt des zu spielenden Spiels generiert 
from game import Game
g = Game()
while g.running:
    g.curr_menu.display_menu()
    g.game_loop()
    