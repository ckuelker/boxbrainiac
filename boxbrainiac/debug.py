# file: boxbrainiac/debug.py
import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(filename)9s,%(lineno)s;%(funcName)20s: %(message)s"))
logger.addHandler(handler)

