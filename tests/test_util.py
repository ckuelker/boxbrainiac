# file: test_util.py
import unittest
from unittest.mock import patch
from util import find_box_index

class TestUtilFunctions(unittest.TestCase):

    @patch('util.logger')
    def test_find_box_index(self, mock_logger):
        cfg = {'ns': 'namespace'}
        data = {'namespace': [{'id': 1}, {'id': 2}, {'id': 3}]}
        box_id = 2
        result = find_box_index(cfg, data, box_id)
        self.assertEqual(result, 1)  # because the box with id=2 is at index 1

if __name__ == '__main__':
    unittest.main()

