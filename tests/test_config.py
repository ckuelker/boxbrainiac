# file: tests/test_config.py
import os
import unittest
from config import cfg

class TestConfig(unittest.TestCase):

    ns = 'boxbrainiac'

    def test_config_keys(self):
        expected_keys = ['ns', 'host', 'port', 'yaml_file', 'repo_dir', 'tpl', 'copyright']
        self.assertCountEqual(cfg.keys(), expected_keys)

    def test_config_values(self):
        ns = 'boxbrainiac'
        repo_dir = os.path.join(os.path.expanduser('~'), '.' + ns, 'data')
        self.assertEqual(cfg['ns'], ns)
        self.assertEqual(cfg['host'], 'localhost')
        self.assertEqual(cfg['port'], 5000)
        self.assertEqual(cfg['yaml_file'], 'boxbrainiac.yaml')
        self.assertEqual(cfg['repo_dir'], repo_dir)
        self.assertEqual(cfg['tpl'], 'templates')
        self.assertEqual(cfg['copyright'], {
            'year': '2023',
            'url': 'https://github.com/ckuelker/boxbrainiac',
            'license': 'GPLv3',
            'target': ns,
            'license': 'GPLv3'
        })

if __name__ == '__main__':
    unittest.main()

