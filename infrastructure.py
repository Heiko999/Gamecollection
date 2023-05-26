from tinydb import TinyDB, Query
from user import *

class DatabaseConnection:
    __instance = None
    db = None

    @staticmethod
    def get_instance():
        if DatabaseConnection.__instance is None:
            DatabaseConnection()
        return DatabaseConnection.__instance

    def __init__(self):
        if DatabaseConnection.__instance is not None:
            raise Exception("DatabaseConnection ist ein Singleton!")
        else:
            DatabaseConnection.__instance = self
            self.db = TinyDB('users.json')

    def close(self):
        self.db.close()

# User-Repository-Implementierung in der Infrastrukturschicht
class UserRepositoryImpl(UserRepository):
    def __init__(self):
        self.db = DatabaseConnection.get_instance().db
        self.table = self.db.table('users')

    def save(self, user):
        user_data = {'name': user.get_name(), 
                     'password': user.get_password(), 
                     'Tetris' : user.get_tetris(), 
                     'SpaceInvaders' : user.get_spaceinvader() , 
                     'Snake' : user.get_snake(), 
                     'Flappy' : user.get_snake()}
        self.table.insert(user_data)

    def find_by_name(self, name):
        UserQuery = Query()
        result = self.table.search(UserQuery.name == name)
        if result:
            user_data = result[0]
            print(user_data)
            return User(user_data['name'], 
                        user_data['password'], 
                        user_data['Tetris'], 
                        user_data['SpaceInvaders'], 
                        user_data['Snake'], 
                        user_data['Flappy'])
        return None
    
    def check_password(self, name, password):
        user = self.find_by_name(name)
        if user and user.password == password:
            return True
        else:
            return False
        
    def delete_by_name(self, name):
        UserQuery = Query()
        self.table.remove(UserQuery.name == name)

    def update(self, user):
        UserQuery = Query()
        result = self.table.update({'Tetris': user.get_tetris(), 'SpaceInvaders': user.get_spaceinvader(), 'Snake': user.get_snake(), 'Flappy': user.get_flappy()},UserQuery.name == user.get_name() )
        if result == []:
            return False
        else:
            return True
        
    def find_all(self):
        result = self.table.all()
        users = []
        for user_data in result:
            user = User(user_data['name'], user_data['password'], user_data['Tetris'], user_data['SpaceInvaders'], user_data['Snake'], user_data['Flappy'])
            users.append(user)
        return users
    
    def get_highest_score(self, game_name):
        #game_name = game_name.lower()
        users = self.find_all()
        highest_score = 0
        for user in users:
            if getattr(user, f"get_{game_name}")() > highest_score:
                highest_score = getattr(user, f"get_{game_name}")()
        return highest_score
