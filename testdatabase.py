import unittest
from unittest.mock import Mock
from usecase import *
from infrastructure import UserRepositoryImpl, User

class RegistrationUseCaseTests(unittest.TestCase):

    def test_register_success(self):
        mock_user_repository = Mock(spec=UserRepositoryImpl)
        use_case = RegistrationUseCase(mock_user_repository)

        name = "Test User"
        password = "testpassword"
        tetris = 0
        spaceinvader = 0
        snake = 0
        flappy = 0

        user = User(name, password, tetris, spaceinvader, snake, flappy)

        use_case.register(name, password, tetris, spaceinvader, snake, flappy)
        mock_user_repository.save.assert_called_once()
        saved_user = mock_user_repository.save.call_args[0][0]

        self.assertEqual(saved_user.name, user.name)
        self.assertEqual(saved_user.password, user.password)
        self.assertEqual(saved_user.tetris, user.tetris)
        self.assertEqual(saved_user.spaceinvader, user.spaceinvader)
        self.assertEqual(saved_user.snake, user.snake)
        self.assertEqual(saved_user.flappy, user.flappy)

    def test_register_with_empty_name(self):
        mock_user_repository = Mock(spec=UserRepositoryImpl)
        use_case = RegistrationUseCase(mock_user_repository)

        name = ""
        password = "testpassword"
        tetris = 0
        spaceinvader = 0
        snake = 0
        flappy = 0

        with self.assertRaises(ValueError):
            use_case.register(name, password, tetris, spaceinvader, snake, flappy)

    def test_register_with_empty_password(self):
        mock_user_repository = UserRepositoryImpl()
        use_case = RegistrationUseCase(mock_user_repository)

        name = "Test User"
        password = ""
        tetris = 0
        spaceinvader = 0
        snake = 0
        flappy = 0

        with self.assertRaises(ValueError):
            use_case.register(name, password, tetris, spaceinvader, snake, flappy)


class LoginUseCaseTests(unittest.TestCase):

    def test_execute_success(self):
        mock_user_repository = Mock(spec=UserRepositoryImpl)
        use_case = LoginUseCase(mock_user_repository)

        name = "Test User"
        password = "testpassword"

        user = User(name, password, 0, 0, 0, 0)
        mock_user_repository.find_by_name.return_value = user
        result = use_case.execute(name, password)

        self.assertTrue(result)

    def test_execute_wrong_password(self):
        mock_user_repository = Mock(spec=UserRepositoryImpl)
        use_case = LoginUseCase(mock_user_repository)

        name = "Test User"
        password = "testpassword"

        user = User(name, password, 0, 0, 0, 0)
        mock_user_repository.find_by_name.return_value = user
        result = use_case.execute(name, "wrongpassword")

        self.assertFalse(result)

    def test_execute_user_not_found(self):
        mock_user_repository = Mock(spec=UserRepositoryImpl)
        use_case = LoginUseCase(mock_user_repository)

        name = "Test User"
        password = "testpassword"

        mock_user_repository.find_by_name.return_value = None
        result = use_case.execute(name, password)

        self.assertFalse(result)


class DeleteUseCaseTests(unittest.TestCase):

    def test_execute_success(self):
        mock_user_repository = Mock(spec=UserRepositoryImpl)
        use_case = DeleteUseCase(mock_user_repository)

        name = "Test User"
        password = "testpassword"

        user = User(name, password, 0, 0, 0, 0)
        mock_user_repository.find_by_name.return_value = user
        result = use_case.execute(name, password)

        self.assertTrue(result)
        mock_user_repository.delete_by_name.assert_called_once_with

if __name__ == '__main__':
    unittest.main()