#file: tests/test_git.py
import unittest
from unittest.mock import patch, MagicMock
from vcs import is_git_repo, git_pull, git_commit_and_push
from exception import GitOperationError
from git import InvalidGitRepositoryError

class TestGit(unittest.TestCase):
    @patch('vcs.Repo')
    @patch('vcs.logger')
    def test_is_git_repo_true(self, mock_logger, mock_Repo):
        mock_Repo.return_value = MagicMock()
        cfg = {'repo_dir': '/path/to/repo'}
        self.assertTrue(is_git_repo(cfg))
        mock_logger.debug.assert_called_with(" - Directory is a git repository: /path/to/repo")

    @patch('vcs.Repo')
    @patch('vcs.logger')
    def test_is_git_repo_false(self, mock_logger, mock_Repo):
        mock_Repo.side_effect = InvalidGitRepositoryError('dummy command')
        cfg = {'repo_dir': '/path/to/repo'}
        self.assertFalse(is_git_repo(cfg))
        mock_logger.debug.assert_called_with(" - Directory is NOT a git repository: /path/to/repo")

    @patch('vcs.Repo')
    @patch('vcs.is_git_repo', return_value=True)
    @patch('vcs.logger')
    def test_git_pull(self, mock_logger, mock_is_git_repo, mock_repo):
        cfg = {'repo_dir': '/path/to/repo'}
        mock_pull = MagicMock()
        mock_origin = MagicMock()
        mock_origin.pull = mock_pull
        mock_repo.return_value.remotes.origin = mock_origin
        git_pull(cfg)
        self.assertEqual(mock_pull.call_count, 1)

    @patch('vcs.Repo')
    @patch('vcs.is_git_repo', return_value=True)
    @patch('vcs.os.path.join', return_value='/path/to/repo/yaml_file')
    @patch('vcs.logger')
    def test_git_commit_and_push(self, mock_logger, mock_join, mock_is_git_repo, mock_repo):
        mock_index = MagicMock()
        mock_origin = MagicMock()
        mock_repo.return_value.remotes.origin = mock_origin
        mock_repo.return_value.index = mock_index
        mock_repo.return_value.is_dirty.return_value = False
        mock_repo.return_value.untracked_files = ['file1', 'file2']
        cfg = {
             'repo_dir': '/path/to/repo', 
            'yaml_file': 'file1'
        }
        commit_message = 'Test commit'
        git_commit_and_push(cfg, commit_message)
        self.assertEqual(mock_index.add.call_count, 1)
        self.assertEqual(mock_index.add.call_args[0][0], [cfg['yaml_file']])
        self.assertEqual(mock_index.commit.call_count, 1)
        self.assertEqual(mock_index.commit.call_args[0][0], "Added %s" % cfg['yaml_file'])
        self.assertEqual(mock_origin.push.call_count, 1)

if __name__ == '__main__':
    unittest.main()

