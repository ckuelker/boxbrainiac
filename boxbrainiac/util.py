# file: boxbrainiac/util.py
import os
from boxbrainiac.debug import logger

# find_box_index: 
#   Find the index of the box with the given id
#   If no box with the given id is found, return None
def find_box_index(cfg, data, box_id):
    for index, box in enumerate(data[cfg['ns']]):
        if box['id'] == box_id:
            logger.debug(" - Found last used index: {}".format(str(index)))
            return index
    logger.debug(" - Found no last used index")
    return None

# get_expected_new_id:
#   Get the expected new id for the next box
#   If there are available ids, use the first one
#   Otherwise, use the next integer
def get_expected_new_id(cfg, data):
    logger.debug(" - Get expected new id")
    if data['available_ids']:
        new_id = data['available_ids'].pop(0)
    else:
        new_id = len(data[cfg['ns']]) + 1
    logger.debug(" - Expected new id: {}".format(str(new_id)))
    return new_id

