from tinydb import TinyDB, Query
#from menu import *


class DatabaseConnection1:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print('Creating the database connection')
            cls._instance = super(DatabaseConnection1, cls).__new__(cls)
            cls._instance.db = TinyDB('db.json')
        return cls._instance

    def getDB(self):
        return self.db
    
class DatabaseConnection2:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print('Creating the database connection')
            cls._instance = super(DatabaseConnection2, cls).__new__(cls)
            cls._instance.db2 = TinyDB('db2.json')
        return cls._instance

    def getDB(self):
        return self.db2
    
class Log:
    
    def __init__(self,database,database2):
        self.db=database
        self.db2=database2
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
        success = False #notwendig?
        user = Query()
        ergebnis = self.db.search((user.Name == x) & (user.Passwort == y))
        if len(ergebnis) == 0:
            print('Anmeldedaten nicht korrekt')
        elif ergebnis != False:
            self.db.remove((user.Name == x) & (user.Passwort == y))
            print('User ' + x + ' wurde gelöscht')
            success = True
            return success

    def playername(self,x):
        user = Query()
        ergebnis = self.db.search(user.Name == x)
        if len(ergebnis) ==0:
            print("User nicht registriert")
        elif ergebnis != False:
            return True

    #aktualisiert die Highscore Einträge
    def highscore(self, game, highscore, player):
        dbEntry = Query()

        # Mapping of game name to highscore field
        game_fields = {
            'Tetris': 'THighscore',
            'Mastermind': 'MHighscore',
            'SpaceInvaders': 'SHighscore',
            'Snake': 'SNHighscore',
            'Flappy': 'FHighscore'
        }

        # Loop through each game and check for a new high score
        for game_name, highscore_field in game_fields.items():
            if game == game_name:
                ergebnis = self.db2.search((dbEntry.Game == game_name) & (getattr(dbEntry, highscore_field) < highscore))
                if ergebnis:
                    print(f"Game: {game} Score: {highscore}")
                    self.db2.update({highscore_field: highscore, 'Player': player}, dbEntry.Game == game_name)

                ergebnis = self.db.search((dbEntry.Name == player) & (getattr(dbEntry, game_name) < str(highscore)))
                if ergebnis:
                    print(f"Game: {game} Score: {highscore}")
                    self.db.update({game_name: str(highscore)}, dbEntry.Name == player)

    

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