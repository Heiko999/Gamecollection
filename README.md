# Gamecollection
Repository für software engineering
Das Spiel wird durch das Starten der main.py gestartet. Es läd den Loginscreen.
An diesem kann man sich nun entweder einen neuen Spieler anlegen, einen vorhandenen Spieler löschen oder mit einem vorhandenen Spieler anmelden.
Die Spieler sind in einer TinyDB Datenbank gespeichert
![loginscreen](https://github.com/Heiko999/Gamecollection/assets/84904473/19ec0996-a737-4750-9c23-445f40edd1f7)

Nach dem Anmelden kommt man zum Loginscreen, auf welchem man ins Spiel Menü oder die HighscoreTabelle wechseln kann.
Im Spiel Menu gibt es 4 verschiedene Spiele: Skyfallgame, Snake, Tetris, Flappy. Diese können alle gespielte werden und der Highscore aus dem jeweiligen Spiel wird in die Datenbank geschrieben.![collection menu](https://github.com/Heiko999/Gamecollection/assets/84904473/04b2528c-4424-4bb6-b9a9-a811d9611e5d)

Im Highscore Menu kann man sich schließlich entweder die Highscores aller Spieler in einem bestimmten Spiel ansehen, oder den Highscore, welchen ein bestimmter Spieler in allen Spielen hat.
![Playerscore](https://github.com/Heiko999/Gamecollection/assets/84904473/88a1c5af-f420-4c46-88c0-ef8def845e30)



# Die Verschiedenen Spiele:
![flappygame](https://github.com/Heiko999/Gamecollection/assets/84904473/2f6eb6e1-fe10-4a75-870a-a897db4141da)
![tetrisgame](https://github.com/Heiko999/Gamecollection/assets/84904473/d3207641-1480-4535-b79e-321ff05bfd65)
![snakegame](https://github.com/Heiko999/Gamecollection/assets/84904473/c7e02d24-000e-4123-b8e7-3fd91e045c1b)
![Skyfallgame](https://github.com/Heiko999/Gamecollection/assets/84904473/df097b3f-a3e0-4f29-a7a1-7ecc92ec4cc9)


# Installation:
Nach dem man das Repo heruntergeladen hat, kann man es mit einem beliebigen Texteditor oder IDE welche Python unterstützt öffnen.
Es müssen die beiden Libraries Pygame und TinyDB installiert werden. Die geschieht mit folgenden Kommands
$ pip install pygame

$ pip install tinydb
Anschließend kann die main.py ausgeführt werden und die Spielesammlung genutzt werden.
