# file: tests/test_exception.py
import unittest
from unittest.mock import patch
from exception import MainApplicationError, DataProcessingError, GitOperationError, StoreOperationError
from error import error_message

class TestExceptions(unittest.TestCase):
    @patch('exception.logger')
    def test_main_application_error(self, mock_logger):
        error_number = "MAI-000"
        error_info = "Test Info"
        expected_message = error_message[error_number] + error_info  # from error.py

        try:
            raise MainApplicationError(error_number, error_info)
        except MainApplicationError as e:
            self.assertEqual(e.number, error_number)
            self.assertEqual(e.message, expected_message)
            mock_logger.error.assert_called_once_with("Error " + error_number + ": " + expected_message)

    @patch('exception.logger')
    def test_data_processing_error(self, mock_logger):
        error_number = "DAT-006"
        error_info = "Test Info"
        expected_message = error_message[error_number] + error_info  # from error.py

        try:
            raise DataProcessingError(error_number, error_info)
        except DataProcessingError as e:
            self.assertEqual(e.number, error_number)
            self.assertEqual(e.message, expected_message)
            mock_logger.error.assert_called_once_with("Error " + error_number + ": " + expected_message)

    @patch('exception.logger')
    def test_git_operation_error(self, mock_logger):
        error_number = "GIT-004"
        error_info = "Test Info"
        expected_message = error_message[error_number] + error_info  # from error.py

        try:
            raise GitOperationError(error_number, error_info)
        except GitOperationError as e:
            self.assertEqual(e.number, error_number)
            self.assertEqual(e.message, expected_message)
            mock_logger.error.assert_called_once_with("Error " + error_number + ": " + expected_message)

    @patch('exception.logger')
    def test_store_operation_error(self, mock_logger):
        error_number = "STO-001"
        filename = "test_file"
        error_info = "Test Info"
        expected_message = error_message[error_number].format(filename) + error_info  # from error.py

        try:
            raise StoreOperationError(error_number, filename, error_info)
        except StoreOperationError as e:
            self.assertEqual(e.number, error_number)
            self.assertEqual(e.message, expected_message)
            mock_logger.error.assert_called_once_with("Error " + error_number + ": " + expected_message)

if __name__ == '__main__':
    unittest.main()

