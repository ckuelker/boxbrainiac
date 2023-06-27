# file: tests/test_store.py
import unittest
from unittest.mock import patch, mock_open, MagicMock, call
from unittest import TestCase
from boxbrainiac.store import read_yaml, write_yaml, ensure_yaml_exists
from boxbrainiac.exception import StoreOperationError
import boxbrainiac.vcs as vcs
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

    @patch('os.makedirs')
    @patch('os.path.exists', return_value=False)
    @patch('boxbrainiac.store.yaml.safe_load', return_value={'ns': [], 'available_ids': []})
    @patch('boxbrainiac.store.write_yaml')
    @patch('boxbrainiac.vcs.is_git_repo', return_value=True)
    @patch('boxbrainiac.vcs.git_commit_and_push')
    def test_ensure_yaml_exists_when_file_does_not_exist(self, mock_git_commit_and_push, mock_is_git_repo, mock_write_yaml, mock_safe_load, mock_exists, mock_makedirs):
        cfg = { 'repo_dir': '/tmp', 'ns': 'namespace', 'yaml_file': 'file.yaml', 'yaml_path': '/tmp/file.yaml' }
        ensure_yaml_exists(cfg)
        # Python 3.6
        #mock_makedirs.assert_called_once_with('/fake/path/to')
        #mock_write_yaml.assert_called_once_with(cfg, mock_safe_load.return_value)
        #mock_git_commit_and_push.assert_called_once_with(cfg, "Initialize file.yaml")
        # Python 3.5
        self.assertEqual(mock_makedirs.call_count, 1)
        self.assertEqual(mock_exists.call_count, 2)
        self.assertEqual(mock_safe_load.call_count, 1)
        self.assertEqual(mock_write_yaml.call_count, 1)
        self.assertEqual(mock_is_git_repo.call_count, 1)
        self.assertEqual(mock_git_commit_and_push.call_count, 1)

    @patch('os.makedirs')
    @patch('os.path.exists', side_effect=[False, False]) # Directory doesn't exist, file doesn't exist
    @patch('boxbrainiac.store.yaml.safe_load', return_value={'ns': [], 'available_ids': []})
    @patch('boxbrainiac.store.write_yaml')
    @patch('boxbrainiac.vcs.is_git_repo', return_value=True)
    @patch('boxbrainiac.vcs.git_commit_and_push')
    def test_ensure_yaml_exists_when_file_does_not_exist(self, mock_git_commit_and_push, mock_is_git_repo, mock_write_yaml, mock_safe_load, mock_exists, mock_makedirs):
        cfg = {'repo_dir': '/tmp', 'ns': 'namespace', 'yaml_file': 'file.yaml', 'yaml_path': '/tmp/file.yaml'}
        ensure_yaml_exists(cfg)
        # Python 3.6
        #mock_makedirs.assert_called_once_with(os.path.dirname(cfg['yaml_path']))
        #mock_exists.assert_has_calls([call(os.path.dirname(cfg['yaml_path'])),call(cfg['yaml_path'])])
        #mock_safe_load.assert_called_once()
        #mock_write_yaml.assert_called_once_with(cfg, {'ns': [], 'available_ids': []})
        #mock_is_git_repo.assert_called_once_with(cfg)
        #mock_git_commit_and_push.assert_called_once_with(cfg, "Initialize file.yaml")
        # Python 3.5
        self.assertEqual(mock_makedirs.call_count, 1)
        self.assertEqual(mock_exists.call_count, 2)
        self.assertEqual(mock_safe_load.call_count, 1)
        self.assertEqual(mock_write_yaml.call_count, 1)
        self.assertEqual(mock_is_git_repo.call_count, 1)
        self.assertEqual(mock_git_commit_and_push.call_count, 1)

if __name__ == '__main__':
    unittest.main()

