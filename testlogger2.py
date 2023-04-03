import unittest
from unittest.mock import Mock
from logger import Log
from tinydb import Query

class LogTests(unittest.TestCase):

    def setUp(self):
        self.db = Mock()
        self.db2 = Mock()
        self.log = Log(self.db, self.db2)

    def test_signIn(self):
        self.log.signIn("John Doe", "password")
        self.db.insert.assert_called_with({
            'Name': "John Doe",
            'Passwort': "password",
            'Tetris' : "0",
            'Mastermind' : "0",
            'SpaceInvaders' : "0",
            'Snake' : "0",
            'Flappy' : "0"
        })

    def test_login_with_correct_credentials(self):
        self.db.search.return_value = [{'Name': 'John Doe', 'Passwort': 'password'}]
        success = self.log.login("John Doe", "password")
        self.assertTrue(success)

    def test_login_with_incorrect_credentials(self):
        self.db.search.return_value = []
        success = self.log.login("John Doe", "password")
        self.assertFalse(success)

    def test_delete_with_correct_credentials(self):
        self.db.search.return_value = [{'Name': 'John Doe', 'Passwort': 'password'}]
        success = self.log.delete("John Doe", "password")
        #self.db.remove.assert_called_with((self.db.Name == "John Doe") & (self.db.Passwort == "password"))
        self.assertTrue(success)

    def test_delete_with_incorrect_credentials(self):
        self.db.search.return_value = []
        success = self.log.delete("John Doe", "password")
        self.assertFalse(success)
        #self.assertEqual(self.log.last_delete_error, 'Anmeldedaten nicht korrekt')

    def test_highscore_entry(self):
        # define test parameters
        game = 'Tetris'
        highscore = 100
        player = 'Alice'

        # set up mock database search and update methods
        self.db2.search.return_value = [{'Game': 'Tetris', 'THighscore': 50}]
        self.db.search.return_value = [{'Name': 'Alice', 'Tetris': '80', 'Mastermind': '20', 'SpaceInvaders': '30', 'Snake': '40', 'Flappy': '50'}]

        # call highscore method
        self.log.highscore(game, highscore, player)
        user = Query()

        # assert that the mock database update methods were called with the expected arguments
        self.db2.update.assert_called_once_with({'THighscore': 100, 'Player': 'Alice'}, user.Game == 'Tetris')
        self.db.update.assert_called_once_with({'Tetris': '100'}, user.Name == 'Alice')


    
        

if __name__ == '__main__':
    unittest.main()