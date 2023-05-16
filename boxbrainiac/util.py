# file: boxbrainiac/util.py
import os
from boxbrainiac.debug import logger

def find_box_index(cfg, data, box_id):
    for index, box in enumerate(data[cfg['ns']]):
        if box['id'] == box_id:
            logger.debug(" - Found last used index: {}".format(str(index)))
            return index
    logger.debug(" - Found no last used index")
    return None

