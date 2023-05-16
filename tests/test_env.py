# file: tests/test_env.py
from boxbrainiac.env import get
import logging
import tempfile
import unittest
from unittest.mock import patch

class TestEnv(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def test_get(self):
        with patch('sys.argv', ['env.py', '--host', '127.0.0.1','--port', '6000', '--yaml_file', 'newboxbrainiac.yaml' ,'--repo_dir', self.temp_dir.name, '-v']):
            cfg = {
                'ns' : 'boxbrainiac',
                'host': 'localhost',
                'port': 5000,
                'yaml_file': 'boxbrainiac.yaml',
                'repo_dir': self.temp_dir.name,
                'tpl': 'templates',
            }
            args, is_debug = get(cfg)

            self.assertEqual(args.host, '127.0.0.1')
            self.assertEqual(args.port, 6000)
            self.assertEqual(args.repo_dir, self.temp_dir.name)
            self.assertEqual(args.yaml_file, 'newboxbrainiac.yaml')
            self.assertEqual(args.loglevel, logging.INFO)
            self.assertFalse(is_debug)

    def tearDown(self):
        self.temp_dir.cleanup()

if __name__ == '__main__':
    unittest.main()

