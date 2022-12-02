from tinydb import TinyDB, Query
from menu import *

db  = TinyDB('db.json')
db2 = TinyDB('db2.json')

class Log:
    def signIn(self,x,y):
        db.insert({'Name': x, 'Passwort': y, 'Tetris' : 0})
        print(x + 'ist registriert')
        

    def login(self,x,y):
        sucess = False
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
        user = Query()
        ergebnis = db2.search((user.Game == game) & (user.Highscore < highscore))
        print(ergebnis)
        if ergebnis != []:
            db2.update({'Highscore': highscore}, user.Game == game)
            db2.update({'Player': player}, user.Game == game)
        #player = Query()
        ergebnis = db.search((user.Name == player) & (user.Tetris < highscore))
        if ergebnis != []:
            db.update({'Tetris': highscore}, user.Name == player)



        

    