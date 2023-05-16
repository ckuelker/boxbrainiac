# file: tests/test_debug.py
import unittest
import logging
from boxbrainiac.debug import logger, handler

class TestDebug(unittest.TestCase):
    def test_logger_name(self):
        self.assertEqual(logger.name, 'boxbrainiac.debug')

    def test_logger_handler(self):
        self.assertIsInstance(logger.handlers[0], logging.StreamHandler)

    def test_handler_formatter(self):
        self.assertIsInstance(handler.formatter, logging.Formatter)

if __name__ == '__main__':
    unittest.main()

