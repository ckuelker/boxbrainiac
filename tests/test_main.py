# file: tests/test_main.py
import unittest
from unittest.mock import patch, MagicMock
from main import run_app
from config import cfg
import tempfile

class TestMain(unittest.TestCase):

    @patch('main.Flask.run')
    @patch('main.env.get')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('main.vcs.git_pull')
    @patch('main.store.read_yaml')
    @patch('main.store.write_yaml')
    @patch('main.vcs.git_commit_and_push')
    @patch('os.makedirs')  # Mock os.makedirs
    def test_manage_boxes(self, mock_makedirs, mock_git_commit_and_push, mock_write_yaml, mock_read_yaml, mock_git_pull, mock_parse_args, mock_env_get,mock_flask_run):
        with tempfile.TemporaryDirectory() as temp_dir:
            mock_read_yaml.return_value = {'available_ids': [1], 'boxbrainiac': []}
            mock_parse_args.return_value = MagicMock(repo_dir=temp_dir, yaml_file='boxbrainiac.yaml', loglevel='INFO')
            mock_env_get.return_value = (mock_parse_args.return_value, False)
            with run_app().test_client() as client:
                response = client.post('/boxbrainiac', data={'realm': 'realm', 'content': 'content', 'location': 'location'})
            self.assertEqual(response.status_code, 302)
            self.assertTrue(mock_git_pull.called)
            self.assertEqual(mock_git_pull.call_count, 1)
            self.assertTrue(mock_read_yaml.called)
            self.assertEqual(mock_read_yaml.call_count, 1)
            self.assertTrue(mock_write_yaml.called)
            self.assertEqual(mock_write_yaml.call_count, 2)
            self.assertTrue(mock_git_commit_and_push.called)
            self.assertEqual(mock_git_commit_and_push.call_count, 1)

    @patch('main.Flask.run')
    @patch('main.env.get')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('main.vcs.git_pull')
    @patch('main.store.read_yaml')
    @patch('os.makedirs')  # Mock os.makedirs
    def test_list_view(self, mock_makedirs, mock_read_yaml, mock_git_pull, mock_parse_args, mock_env_get, mock_flask_run):
        with tempfile.TemporaryDirectory() as temp_dir:
            mock_read_yaml.return_value = {'available_ids': [], 'boxbrainiac': [{'id': 1, 'realm': 'realm', 'content': 'content', 'location': 'location'}]}
            mock_parse_args.return_value = MagicMock(repo_dir=temp_dir, yaml_file='boxbrainiac.yaml', loglevel='INFO')
            mock_env_get.return_value = (mock_parse_args.return_value, False)
            with run_app().test_client() as client:
                response = client.get('/list')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(mock_git_pull.call_count, 1)
            self.assertEqual(mock_read_yaml.call_count, 1)

    @patch('main.Flask.run')
    @patch('main.env.get')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('main.vcs.git_pull')
    @patch('main.store.read_yaml')
    @patch('main.store.write_yaml')
    @patch('main.vcs.git_commit_and_push')
    @patch('os.makedirs')  # Mock os.makedirs
    def test_edit_box(self, mock_makedirs, mock_git_commit_and_push, mock_write_yaml, mock_read_yaml, mock_git_pull, mock_parse_args, mock_env_get, mock_flask_run):
        with tempfile.TemporaryDirectory() as temp_dir:
            mock_read_yaml.return_value = {'available_ids': [1], 'boxbrainiac': [{'id': 1, 'realm': 'realm', 'content': 'content', 'location': 'location'}]}
            mock_parse_args.return_value = MagicMock(repo_dir=temp_dir, yaml_file='boxbrainiac.yaml', loglevel='INFO')
            mock_env_get.return_value = (mock_parse_args.return_value, False)

            # Testing GET method
            with run_app().test_client() as client:
                response = client.get('/edit/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(mock_git_pull.call_count, 1)
            self.assertEqual(mock_read_yaml.call_count, 1)

            # Testing POST method
            with run_app().test_client() as client:
                response = client.post('/edit/1', data={'realm': 'new_realm', 'content': 'new_content', 'location': 'new_location'})
            self.assertEqual(response.status_code, 302)
            self.assertEqual(mock_git_pull.call_count, 2)
            self.assertEqual(mock_read_yaml.call_count, 2)
            self.assertEqual(mock_write_yaml.call_count, 3)
            self.assertEqual(mock_git_commit_and_push.call_count, 1)

    @patch('main.Flask.run')
    @patch('main.env.get')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('main.vcs.git_pull')
    @patch('main.store.read_yaml')
    @patch('main.store.write_yaml')
    @patch('main.vcs.git_commit_and_push')
    @patch('main.util.find_box_index')
    @patch('os.makedirs')  # Mock os.makedirs
    def test_delete_box(self, mock_makedirs, mock_find_box_index, mock_git_commit_and_push, mock_write_yaml, mock_read_yaml, mock_git_pull, mock_parse_args, mock_env_get, mock_flask_run):
        with tempfile.TemporaryDirectory() as temp_dir:
            mock_read_yaml.return_value = {'available_ids': [1], 'boxbrainiac': [{'id': 1, 'realm': 'realm', 'content': 'content', 'location': 'location'}]}
            mock_find_box_index.return_value = 0
            mock_parse_args.return_value = MagicMock(repo_dir=temp_dir, yaml_file='boxbrainiac.yaml', loglevel='INFO')
            mock_env_get.return_value = (mock_parse_args.return_value, False)
            with run_app().test_client() as client:
                response = client.post('/delete/1')
            self.assertEqual(response.status_code, 302)
            self.assertEqual(mock_git_pull.call_count, 1)
            self.assertEqual(mock_read_yaml.call_count, 1)
            self.assertEqual(mock_write_yaml.call_count, 2) # 1 route detete_box, 1 store.ensure_yaml_exists
            self.assertEqual(mock_git_commit_and_push.call_count, 1)
            self.assertEqual(mock_find_box_index.call_count, 1)

    @patch('main.Flask.run')
    @patch('main.env.get')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('main.vcs.git_pull')
    @patch('main.store.read_yaml')
    @patch('os.makedirs')  # Mock os.makedirs
    def test_search_view(self, mock_makedirs, mock_read_yaml, mock_git_pull, mock_parse_args, mock_env_get, mock_flask_run):
        with tempfile.TemporaryDirectory() as temp_dir:
            mock_read_yaml.return_value = {'available_ids': [1], 'boxbrainiac': [{'id': 1, 'realm': 'realm', 'content': 'content', 'location': 'location'}]}
            mock_parse_args.return_value = MagicMock(repo_dir=temp_dir, yaml_file='boxbrainiac.yaml', loglevel='INFO')
            mock_env_get.return_value = (mock_parse_args.return_value, False)
            with run_app().test_client() as client:
                # Testing with a search_query that matches the content
                response = client.get('/search', query_string={'search_query': 'content'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(mock_read_yaml.call_count, 1)

            mock_read_yaml.reset_mock()

            with run_app().test_client() as client:
                # Testing with a search_query that doesn't match the content
                response = client.get('/search', query_string={'search_query': 'nonexistent'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(mock_read_yaml.call_count, 1)

            mock_read_yaml.reset_mock()

            with run_app().test_client() as client:
                # Testing without a search_query
                response = client.get('/search')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(mock_read_yaml.call_count, 0)

  
if __name__ == '__main__':
    unittest.main()

