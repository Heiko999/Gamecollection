import unittest
from unittest.mock import patch, Mock
from tinydb import TinyDB, Query
from logger import Log



class TestLog(unittest.TestCase):
    
    def setUp(self):
        # Erstellt ein Mock Datenbank Objekt
        self.mock_db = Mock(TinyDB)
        

    def test_signIn(self):
        # Erstellt ein Mock Dataset welches in die Datenbank eingefügt werden soll
        mock_data = {'Name': 'test50', 'Passwort': 'test', 'Tetris': "0", 'Mastermind': "0", 'SpaceInvaders': "0",
                     'Snake': "0", 'Flappy': "0"}

        # Erstellt eine Mock Instert Funktion, welche das Mock Dataset zurückgibt
        insert_mock = Mock(return_value=mock_data)
        self.mock_db.insert = insert_mock
        
        # Erstellt eine Neue Instanz der Log Klasse und ruft die signIn Funktion mit den Mock Daten auf
        log = Log(self.mock_db,self.mock_db)
        log.signIn('test50', 'test')
        
        # Assert prüft, ob die mock insert Funktion mit den erwarteten Daten aufgerufen wurde.
        insert_mock.assert_called_once_with(mock_data)
        print("hier war der signing test")

    def test_login(self):
        # create mock data to be searched in the database
        mock_data = {'Name': 'test', 'Passwort': 'test'}

        # create a mock search function that returns the mock data if it is found in the database
        search_mock = Mock(return_value=[mock_data])
        self.mock_db.search = search_mock
        
        # create a Log instance and call login with mock data
        log = Log(self.mock_db,self.mock_db)
        success = log.login('test', 'test')
        user= Query()
        # assert that the mock search function was called with the expected data
        search_mock.assert_called_once_with((user.Name == 'test') & (user.Passwort == 'test'))
        # assert that success is True, indicating the login was successful
        self.assertTrue(success)
        print("hier war der login Test")

    def test_delete(self):
        # create mock data to be searched and deleted in the database
        mock_data = {'Name': 'test', 'Passwort': 'test'}

        # create a mock search function that returns the mock data if it is found in the database
        search_mock = Mock(return_value=[mock_data])
        self.mock_db.search = search_mock
        
        # create a mock remove function that returns None
        remove_mock = Mock(return_value=None)
        self.mock_db.remove = remove_mock
        
        # create a Log instance and call delete with mock data
        log = Log(self.mock_db,self.mock_db)
        user = Query()
        log.delete('test', 'test')
        
        # assert that the mock search function was called with the expected data
        search_mock.assert_called_once_with((user.Name == 'test') & (user.Passwort == 'test'))
        # assert that the mock remove function was called with the expected data
        remove_mock.assert_called_once_with((user.Name == 'test') & (user.Passwort == 'test'))
        print("hier war der delete Test")
    

    #def tearDown(self):
        #self.patcher.stop()

if __name__ == '__main__':
    unittest.main()
