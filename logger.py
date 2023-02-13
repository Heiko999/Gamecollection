from tinydb import TinyDB, Query
from menu import *

db = TinyDB('db.json')
db2 = TinyDB('db2.json')

class Log:
    def signIn(self,x,y):
        db.insert({'Name': x, 'Passwort': y, 'Tetris' : 0, 'Mastermind' : 0, 'SpaceInvaders' : 0 , 'Snake' : 0, 'Flappy' : 0})
        print(x + ' ist registriert')
        

    def login(self,x,y):
        success = False #notwendig?
        user = Query()
        ergebnis = db.search((user.Name == x) & (user.Passwort == y))
        if len(ergebnis) == 0:
            print('Anmeldedaten nicht korrekt')
        elif ergebnis != False:
            print('Hallo User ' + x)
            success = True
            return success
    
    def delete(self,x,y):
        user = Query()
        ergebnis = db.search((user.Name == x) & (user.Passwort == y))
        if len(ergebnis) == 0:
            print('Anmeldedaten nicht korrekt')
        elif ergebnis != False:
            db.remove((user.Name == x) & (user.Passwort == y))
            print('User ' + x + ' wurde gelöscht')

    def highscore(self,game,highscore,player):
        dbEntry = Query()
        ergebnis = db2.search((dbEntry.Game == 'Tetris') & (dbEntry.THighscore < highscore))
        if ergebnis != [] and game == 'Tetris':
            print(f"""Game: {game} Score: {highscore}""")
            db2.update({'THighscore': highscore, 'Player': player}, dbEntry.Game == 'Tetris')
        ergebnis = db2.search((dbEntry.Game == 'Mastermind') & (dbEntry.MHighscore < highscore))
        if ergebnis != [] and game == 'Mastermind':
            print(f"""Game: {game} Score: {highscore}""")
            db2.update({'MHighscore': highscore, 'Player': player}, dbEntry.Game == 'Mastermind')
        ergebnis = db2.search((dbEntry.Game == 'SpaceInvaders') & (dbEntry.SHighscore < highscore))
        if ergebnis != [] and game == 'SpaceInvaders':
            print(f"""Game: {game} Score: {highscore}""")
            db2.update({'SHighscore': highscore, 'Player': player}, dbEntry.Game == 'SpaceInvaders')
        ergebnis = db2.search((dbEntry.Game == 'Snake') & (dbEntry.SNHighscore < highscore))
        if ergebnis != [] and game == 'Snake':
            print(f"""Game: {game} Score: {highscore}""")
            db2.update({'SNHighscore': highscore, 'Player': player}, dbEntry.Game == 'Snake')
        ergebnis = db2.search((dbEntry.Game == 'Flappy') & (dbEntry.FHighscore < highscore))
        if ergebnis != [] and game == 'Flappy':
            print(f"""Game: {game} Score: {highscore}""")
            db2.update({'FHighscore': highscore, 'Player': player}, dbEntry.Game == 'Flappy')

        ergebnis = db.search((dbEntry.Name == player) & (dbEntry.Tetris < highscore))
        if ergebnis != [] and game == 'Tetris':
            print(f"""Game: {game} Score: {highscore}""")
            db.update({'Tetris': highscore}, dbEntry.Name == player)
        ergebnis = db.search((dbEntry.Name == player) & (dbEntry.Mastermind < highscore))
        if ergebnis != [] and game == 'Mastermind':
            print(f"""Game: {game} Score: {highscore}""")
            db.update({'Mastermind': highscore}, dbEntry.Name == player)
        ergebnis = db.search((dbEntry.Name == player) & (dbEntry.SpaceInvaders < highscore))
        if ergebnis != [] and game == 'SpaceInvaders':
            print(f"""Game: {game} Score: {highscore}""")
            db.update({'SpaceInvaders': highscore}, dbEntry.Name == player)
        ergebnis = db.search((dbEntry.Name == player) & (dbEntry.Snake < highscore))
        if ergebnis != [] and game == 'Snake':
            print(f"""Game: {game} Score: {highscore}""")
            db.update({'Snake': highscore}, dbEntry.Name == player)
        ergebnis = db.search((dbEntry.Name == player) & (dbEntry.Flappy < highscore))
        if ergebnis != [] and game == 'Flappy':
            print(f"""Game: {game} Score: {highscore}""")
            db.update({'Flappy': highscore}, dbEntry.Name == player)



        

    