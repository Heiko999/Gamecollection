from tinydb import TinyDB, Query
from menu import *

db = TinyDB('db.json')
db2 = TinyDB('db2.json')

class Log:
    def signIn(self,x,y):
        db.insert({'Name': x, 'Passwort': y, 'Tetris' : "0", 'Mastermind' : "0", 'SpaceInvaders' : "0" , 'Snake' : "0", 'Flappy' : "0"})
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

        ergebnis = db.search((dbEntry.Name == player) & (dbEntry.Tetris < str(highscore)))
        if ergebnis != [] and game == 'Tetris':
            print(f"""Game: {game} Score: {highscore}""")
            db.update({'Tetris': str(highscore)}, dbEntry.Name == player)
        ergebnis = db.search((dbEntry.Name == player) & (dbEntry.Mastermind < str(highscore)))
        if ergebnis != [] and game == 'Mastermind':
            print(f"""Game: {game} Score: {highscore}""")
            db.update({'Mastermind': str(highscore)}, dbEntry.Name == player)
        ergebnis = db.search((dbEntry.Name == player) & (dbEntry.SpaceInvaders < str(highscore)))
        if ergebnis != [] and game == 'SpaceInvaders':
            print(f"""Game: {game} Score: {highscore}""")
            db.update({'SpaceInvaders': str(highscore)}, dbEntry.Name == player)
        ergebnis = db.search((dbEntry.Name == player) & (dbEntry.Snake < str(highscore)))
        if ergebnis != [] and game == 'Snake':
            print(f"""Game: {game} Score: {highscore}""")
            db.update({'Snake': str(highscore)}, dbEntry.Name == player)
        ergebnis = db.search((dbEntry.Name == player) & (dbEntry.Flappy < str(highscore)))
        if ergebnis != [] and game == 'Flappy':
            print(f"""Game: {game} Score: {highscore}""")
            db.update({'Flappy': str(highscore)}, dbEntry.Name == player)
    

    

    def tetrisscore(self):
        ergebnis = db.all()
        self.len = len(db)
        dicture = {}
        for i in range(self.len): 
            score = ergebnis[i]
            scoreStr =str(score)
            scoreSplit = scoreStr.split("'")
            #print(TetrisSplit)
            print(scoreSplit[3])
            print(scoreSplit[11])
            dicture[scoreSplit[3]] = int(scoreSplit[11])

        sorted_dict = sorted(dicture.items(),key=lambda x:x[1], reverse=True)
        converted_dict=dict(sorted_dict)
        print(converted_dict)
        result = converted_dict.items()
        data=list(result)
        return data

    def mastermindscore(self):
        ergebnis = db.all()
        self.len = len(db)
        dicture = {}
        for i in range(self.len): 
            score = ergebnis[i]
            scoreStr =str(score)
            scoreSplit = scoreStr.split("'")
            #print(TetrisSplit)
            print(scoreSplit[3])
            print(scoreSplit[15])
            dicture[scoreSplit[3]] = int(scoreSplit[15])

        sorted_dict = sorted(dicture.items(),key=lambda x:x[1], reverse=True)
        converted_dict=dict(sorted_dict)
        print(converted_dict)
        result = converted_dict.items()
        data=list(result)
        return data

    def spaceinvaderscore(self):
        ergebnis = db.all()
        self.len = len(db)
        dicture = {}
        for i in range(self.len): 
            score = ergebnis[i]
            scoreStr =str(score)
            scoreSplit = scoreStr.split("'")
            #print(TetrisSplit)
            dicture[scoreSplit[3]] = int(scoreSplit[19])

        sorted_dict = sorted(dicture.items(),key=lambda x:x[1], reverse=True)
        converted_dict=dict(sorted_dict)
        print(converted_dict)
        result = converted_dict.items()
        data=list(result)
        return data

    def snakescore(self):
        ergebnis = db.all()
        self.len = len(db)
        dicture = {}
        for i in range(self.len): 
            score = ergebnis[i]
            scoreStr =str(score)
            scoreSplit = scoreStr.split("'")
            #print(TetrisSplit)
            print(scoreSplit[3])
            print(scoreSplit[23])
            dicture[scoreSplit[3]] = int(scoreSplit[23])

        sorted_dict = sorted(dicture.items(),key=lambda x:x[1], reverse=True)
        converted_dict=dict(sorted_dict)
        print(converted_dict)
        result = converted_dict.items()
        data=list(result)
        return data

    def flappyscore(self):
        ergebnis = db.all()
        self.len = len(db)
        dicture = {}
        for i in range(self.len): 
            score = ergebnis[i]
            scoreStr =str(score)
            scoreSplit = scoreStr.split("'")
            #print(TetrisSplit)
            print(scoreSplit[3])
            print(scoreSplit[27])
            dicture[scoreSplit[3]] = int(scoreSplit[27])

        sorted_dict = sorted(dicture.items(),key=lambda x:x[1], reverse=True)
        converted_dict=dict(sorted_dict)
        print(converted_dict)
        result = converted_dict.items()
        data=list(result)
        return data




"""
def spaceinvaderscore():
        ergebnis = db.all()
        len = len(db)
        dicture = {}
        for i in range(len): 
            score = ergebnis[i]
            scoreStr =str(score)
            scoreSplit = scoreStr.split("'")
            #print(TetrisSplit)
            print(scoreSplit[3])
            print(scoreSplit[19])
            dicture[scoreSplit[3]] = int(scoreSplit[19])

        sorted_dict = sorted(dicture.items(),key=lambda x:x[1], reverse=True)
        converted_dict=dict(sorted_dict)
        print(converted_dict)
        result = converted_dict.items()
        data=list(result)
        for i in range(len):
            print(data[i])
"""
        

    