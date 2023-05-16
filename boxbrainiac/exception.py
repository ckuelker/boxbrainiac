# file: boxbrainiac/exception.py
from boxbrainiac.debug import logger
from boxbrainiac.error import error_message

class MainApplicationError(Exception):
    def __init__(self, number, info):
        message = error_message[number] + info
        super().__init__(message) # Pass the message to the base Exception class
        self.number  = number
        self.message = message
        logger.error("Error "+ number + ": " + message)

class DataProcessingError(Exception):
    def __init__(self, number, info):
        message = error_message[number] + info
        super().__init__(message) # Pass the message to the base Exception class
        self.number  = number
        self.message = message
        logger.error("Error "+ number + ": " + message)

class GitOperationError(Exception):
    def __init__(self, number, info):
        message = error_message[number] + info
        super().__init__(message) # Pass the message to the base Exception class
        self.number  = number
        self.message = message
        logger.error("Error "+ number + ": " + message)

class StoreOperationError(Exception):
    def __init__(self, number, filename, info):
        message = error_message[number].format(filename) + info
        super().__init__(message) # Pass the message to the base Exception class
        self.number  = number
        self.message = message
        logger.error("Error "+ number + ": " + message)

