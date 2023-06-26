# file: tests/test_git.py
import unittest
from unittest.mock import patch, MagicMock
from vcs import is_git_repo, git_pull, git_commit_and_push
from exception import GitOperationError

class TestGit(unittest.TestCase):
    @patch('vcs.Repo')
    @patch('vcs.logger')
    def test_is_git_repo_true(self, mock_logger, mock_Repo):
        mock_Repo.return_value = MagicMock()
        cfg = {'repo_dir': '/path/to/repo'}
        self.assertTrue(is_git_repo(cfg))
        mock_logger.debug.assert_called_with(" - Directory is a git repository")

    @patch('vcs.Repo')
    @patch('vcs.logger')
    def test_is_git_repo_false(self, mock_logger, mock_Repo):
        mock_Repo.side_effect = Exception()
        cfg = {'repo_dir': '/path/to/repo'}
        self.assertFalse(is_git_repo(cfg))
        mock_logger.debug.assert_called_with(" - Directory is NOT a git repository")

    @patch('vcs.pull')
    @patch('vcs.is_git_repo', return_value=True)
    def test_git_pull(self, mock_is_git_repo, mock_pull):
        cfg = {'repo_dir': '/path/to/repo'}
        git_pull(cfg)
        mock_pull.assert_called_with(cfg['repo_dir'])

    @patch('vcs.push')
    @patch('vcs.commit')
    @patch('vcs.add')
    @patch('vcs.Repo')
    @patch('vcs.is_git_repo', return_value=True)
    def test_git_commit_and_push(self, mock_is_git_repo, mock_Repo, mock_add, mock_commit, mock_push):
        mock_Repo.return_value = MagicMock()
        cfg = {'repo_dir': '/path/to/repo', 'yaml_file': 'file.yaml'}
        commit_message = "Test commit"
        git_commit_and_push(cfg, commit_message)
        mock_add.assert_called_with(mock_Repo.return_value, cfg['yaml_file'])
        mock_commit.assert_called_with(mock_Repo.return_value, message=commit_message)
        mock_push.assert_called_with(mock_Repo.return_value, "origin", refspecs="master")

if __name__ == '__main__':
    unittest.main()

