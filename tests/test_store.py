# file: tests/test_store.py
import unittest
from unittest.mock import patch, mock_open
from boxbrainiac.store import read_yaml, write_yaml, ensure_yaml_exists
from boxbrainiac.exception import StoreOperationError
import boxbrainiac.git as git
import tempfile
import os

class TestStore(unittest.TestCase):
    @patch('boxbrainiac.store.os.path.exists', return_value=True)
    @patch('boxbrainiac.store.yaml.safe_load')
    @patch('builtins.open', new_callable=mock_open, read_data="yaml_data")
    def test_read_yaml(self, mock_open, mock_safe_load, mock_exists):
        cfg = {'yaml_path': '/path/to/yaml'}
        read_yaml(cfg)
        mock_open.assert_called_once_with(cfg['yaml_path'], 'r')
        self.assertEqual(mock_safe_load.call_count, 1)

    @patch('boxbrainiac.store.yaml.safe_dump')
    @patch('builtins.open', new_callable=mock_open)
    def test_write_yaml(self, mock_open, mock_safe_dump):
        cfg = {'yaml_path': '/path/to/yaml'}
        data = {'data': 'value'}
        write_yaml(cfg, data)
        mock_open.assert_called_once_with(cfg['yaml_path'], 'wb')
        self.assertEqual(mock_safe_dump.call_count, 1)

    @patch('boxbrainiac.git.is_git_repo', return_value=True)
    @patch('boxbrainiac.git.git_commit_and_push')
    @patch('boxbrainiac.store.write_yaml')
    @patch('boxbrainiac.store.yaml.safe_load', return_value={'ns': [], 'available_ids': []})
    @patch('boxbrainiac.store.os.path.exists', return_value=True)
    def test_ensure_yaml_exists(self, mock_exists, mock_safe_load, mock_write_yaml, mock_git_commit_and_push, mock_is_git_repo):
        with tempfile.TemporaryDirectory() as temp_dir:
            cfg = { 'repo_dir':  temp_dir, 'ns': 'namespace', 'yaml_file': 'file.yaml', 'yaml_path': os.path.join(temp_dir,'file.yaml') }
            ensure_yaml_exists(cfg)
            self.assertEqual(mock_write_yaml.call_count, 0)
            self.assertEqual(mock_git_commit_and_push.call_count, 0)

    @patch('boxbrainiac.git.is_git_repo', return_value=True)
    @patch('boxbrainiac.git.git_commit_and_push')
    @patch('boxbrainiac.store.write_yaml')
    @patch('boxbrainiac.store.yaml.safe_load', return_value={'ns': [], 'available_ids': []})
    @patch('boxbrainiac.store.os.path.exists', return_value=False)
    def test_ensure_yaml_exists_when_file_does_not_exist(self, mock_exists, mock_safe_load, mock_write_yaml, mock_git_commit_and_push, mock_is_git_repo):
        with tempfile.TemporaryDirectory() as temp_dir:
            cfg = { 'repo_dir':  temp_dir, 'ns': 'namespace', 'yaml_file': 'file.yaml', 'yaml_path': os.path.join(temp_dir,'file.yaml') }
            ensure_yaml_exists(cfg)
            self.assertEqual(mock_write_yaml.call_count, 1)
            self.assertEqual(mock_git_commit_and_push.call_count, 1)

if __name__ == '__main__':
    unittest.main()

