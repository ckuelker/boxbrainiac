# file: test_util.py
import unittest
from unittest.mock import patch
from util import find_box_index, get_expected_new_id

class TestUtilFunctions(unittest.TestCase):

    @patch('util.logger')
    def test_find_box_index(self, mock_logger):
        cfg = {'ns': 'namespace'}
        data = {'namespace': [{'id': 1}, {'id': 2}, {'id': 3}]}
        box_id = 2
        result = find_box_index(cfg, data, box_id)
        self.assertEqual(result, 1)  # because the box with id=2 is at index 1

    @patch('util.logger')
    def test_find_box_index_not_found(self, mock_logger):
        cfg = {'ns': 'namespace'}

        # Test case 1: available_ids is not empty
        data1 = {'namespace': [{'id': 1}, {'id': 2}, {'id': 3}], 'available_ids': [5, 6, 7]}
        result1 = get_expected_new_id(cfg, data1)
        self.assertEqual(result1, 5) # because the smallest available id is 5
        self.assertEqual(data1['available_ids'], [6, 7])  # because 4 was removed from available_ids

        # Test case 2: available_ids is empty
        data2 = {'namespace': [{'id': 1}, {'id': 2}, {'id': 3}], 'available_ids': []}
        result2 = get_expected_new_id(cfg, data2)
        self.assertEqual(result2, 4)  # because the length of data['namespace'] is 4

if __name__ == '__main__':
    unittest.main()

