from tinydb import TinyDB, Query
#from menu import *
import threading

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print('Creating the database connection')
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.db = TinyDB('db.json')
        return cls._instance

    def getDB(self):
        return self.db
    
#db = DatabaseConnection().getDB()

#db = TinyDB('db.json')
db2 = TinyDB('db2.json')

class Log:
    db = DatabaseConnection().getDB()
    #db = TinyDB('db.json')
    #Erstellt neuen Spieler
    def signIn(self,x,y):
        self.db.insert({'Name': x, 'Passwort': y, 'Tetris' : "0", 'Mastermind' : "0", 'SpaceInvaders' : "0" , 'Snake' : "0", 'Flappy' : "0"})
        print(x + ' ist registriert')
        
    #Meldet Spieler an
    def login(self,x,y):
        success = False #notwendig?
        user = Query()
        ergebnis = self.db.search((user.Name == x) & (user.Passwort == y))
        if len(ergebnis) == 0:
            print('Anmeldedaten nicht korrekt')
        elif ergebnis != False:
            print('Hallo User ' + x)
            success = True
            return success
    
    #Löscht einen Spieler
    def delete(self,x,y):
        user = Query()
        ergebnis = self.db.search((user.Name == x) & (user.Passwort == y))
        if len(ergebnis) == 0:
            print('Anmeldedaten nicht korrekt')
        elif ergebnis != False:
            self.db.remove((user.Name == x) & (user.Passwort == y))
            print('User ' + x + ' wurde gelöscht')

    def playername(self,x):
        user = Query()
        ergebnis = self.db.search(user.Name == x)
        if len(ergebnis) ==0:
            print("User nicht registriert")
        elif ergebnis != False:
            return True

    #aktualisiert die Highscore Einträge
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

        ergebnis = self.db.search((dbEntry.Name == player) & (dbEntry.Tetris < str(highscore)))
        if ergebnis != [] and game == 'Tetris':
            print(f"""Game: {game} Score: {highscore}""")
            self.db.update({'Tetris': str(highscore)}, dbEntry.Name == player)
        ergebnis = self.db.search((dbEntry.Name == player) & (dbEntry.Mastermind < str(highscore)))
        if ergebnis != [] and game == 'Mastermind':
            print(f"""Game: {game} Score: {highscore}""")
            self.db.update({'Mastermind': str(highscore)}, dbEntry.Name == player)
        ergebnis = self.db.search((dbEntry.Name == player) & (dbEntry.SpaceInvaders < str(highscore)))
        if ergebnis != [] and game == 'SpaceInvaders':
            print(f"""Game: {game} Score: {highscore}""")
            self.db.update({'SpaceInvaders': str(highscore)}, dbEntry.Name == player)
        ergebnis = self.db.search((dbEntry.Name == player) & (dbEntry.Snake < str(highscore)))
        if ergebnis != [] and game == 'Snake':
            print(f"""Game: {game} Score: {highscore}""")
            self.db.update({'Snake': str(highscore)}, dbEntry.Name == player)
        ergebnis = self.db.search((dbEntry.Name == player) & (dbEntry.Flappy < str(highscore)))
        if ergebnis != [] and game == 'Flappy':
            print(f"""Game: {game} Score: {highscore}""")
            self.db.update({'Flappy': str(highscore)}, dbEntry.Name == player)

    

#TODO: Funktionen um Highscore des entsprechenden spiels aus der Datenbank auszulesen
    #Werte werden in einem Dictionaryder Form {Spieler: Punkte} gespeichert und anschließend
    #in ein Array umgewandelt welches weiter verwendet werden kann

    def playerscores(self,player):
        User = Query()
        dicture = {}
        ergebnis = self.db.search(User.Name == player)
        print("x ist gleich: " + player)
        ergebnisStr =str(ergebnis)
        ergebnisSplit = ergebnisStr.split("'")
        dicture[ergebnisSplit[9]] = int(ergebnisSplit[11])
        dicture[ergebnisSplit[13]] = int(ergebnisSplit[15])
        dicture[ergebnisSplit[17]] = int(ergebnisSplit[19])
        dicture[ergebnisSplit[21]] = int(ergebnisSplit[23])
        dicture[ergebnisSplit[25]] = int(ergebnisSplit[27])
        sorted_dict = sorted(dicture.items(),key=lambda x:x[1], reverse=True)
        converted_dict=dict(sorted_dict)
        result = converted_dict.items()
        data=list(result)
        return data
    
    def tetrisscore(self):
        ergebnis = self.db.all()
        self.len = len(self.db)
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
        ergebnis = self.db.all()
        self.len = len(self.db)
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
        ergebnis = self.db.all()
        self.len = len(self.db)
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
        ergebnis = self.db.all()
        self.len = len(self.db)
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
        ergebnis = self.db.all()
        self.len = len(self.db)
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
    
    def gamesscores(self, game):
        ergebnis = self.db.all()
        print("ergebnis = ")
        print(ergebnis)
        self.len = len(self.db)
        dicture = {}
        game_positions = {'tetris': 11, 'mastermind': 15, 'spaceinvader': 19, 'snake': 23, 'flappy' : 27}
        game_position = game_positions[game]
        for i in range(self.len): 
            score = ergebnis[i]
            scoreStr = str(score)
            scoreSplit = scoreStr.split("'")
            dicture[scoreSplit[3]] = int(scoreSplit[game_position])

        sorted_dict = sorted(dicture.items(),key=lambda x:x[1], reverse=True)
        converted_dict=dict(sorted_dict)
        print(converted_dict)
        result = converted_dict.items()
        data=list(result)
        return data

    #Zu einer Funktion refactoren
    #scoreSplit[i] kann einfach je nach spiel angepasst werden
    





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
        

    