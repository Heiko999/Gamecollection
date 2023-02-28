import unittest
from unittest.mock import patch, Mock
from tinydb import TinyDB
from logger import Log



class TestLog(unittest.TestCase):
    
    def setUp(self):
        # create a mock database and patch the TinyDB calls in the Log class to use it
        self.mock_db = Mock(TinyDB)
        self.patcher = patch.multiple(Log, db=self.mock_db)
        self.patcher.start()
        
    def tearDown(self):
        self.patcher.stop()

    def test_signIn(self):
        # create mock data to be inserted into the database
        mock_data = {'Name': 'test50000', 'Passwort': 'test', 'Tetris': "0", 'Mastermind': "0", 'SpaceInvaders': "0",
                     'Snake': "0", 'Flappy': "0"}

        # create a mock insert function that returns the mock data
        insert_mock = Mock(return_value=mock_data)
        self.mock_db.insert = insert_mock
        
        # create a Log instance and call signIn with mock data
        log = Log()
        log.signIn('test50000', 'test')
        
        # assert that the mock insert function was called with the expected data
        insert_mock.assert_called_once_with(mock_data)
'''
    def test_login(self):
        # create mock data to be searched in the database
        mock_data = {'Name': 'test', 'Passwort': 'test'}

        # create a mock search function that returns the mock data if it is found in the database
        search_mock = Mock(return_value=[mock_data])
        self.mock_db.search = search_mock
        
        # create a Log instance and call login with mock data
        log = Log()
        success = log.login('test', 'test')
        
        # assert that the mock search function was called with the expected data
        search_mock.assert_called_once_with((log.user.Name == 'test') & (log.user.Passwort == 'test'))
        # assert that success is True, indicating the login was successful
        self.assertTrue(success)

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
        log = Log()
        log.delete('test', 'test')
        
        # assert that the mock search function was called with the expected data
        search_mock.assert_called_once_with((log.user.Name == 'test') & (log.user.Passwort == 'test'))
        # assert that the mock remove function was called with the expected data
        remove_mock.assert_called_once_with((log.user.Name == 'test') & (log.user.Passwort == 'test'))
    '''

if __name__ == '__main__':
    unittest.main()
