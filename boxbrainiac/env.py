# file: boxbrainiac/env.py
import argparse
import logging # To get constants
from boxbrainiac.debug import logger # To set log level
from boxbrainiac.version import version
import os
import sys


def get(cfg):
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=cfg['port'], help='The port number to use (default: {})'.format(cfg['port']))
    parser.add_argument('--host', type=str, default=cfg['host'], help='The host to use (default: {})'.format(cfg['host']))
    parser.add_argument('-y', '--yaml_file', type=str, default=cfg['yaml_file'], help='The datafile to use (default: {})'.format(cfg['yaml_file']))
    parser.add_argument('-r', '--repo_dir', type=str, default=cfg['repo_dir'], help='The repository directory to use (default: {})'.format(cfg['repo_dir']))
    parser.add_argument('-v', '--verbose', action="store_const",dest="loglevel", const=logging.INFO, default=logging.WARNING, help="Enable verbose logging")
    parser.add_argument('-d', '--debug', action="store_const",dest="loglevel", const=logging.DEBUG, default=logging.WARNING, help="Enable debug logging")
    parser.add_argument('-q', '--quiet', action="store_const",dest="loglevel", const=logging.ERROR, default=logging.WARNING, help="Enable only error logging")
    parser.add_argument('--version', action="store_true", default=False, help="Print version")
    parser.add_argument('--dump', action="store_true", default=False, help="Print configuration default values")

    args = parser.parse_args()

    if args.version:
        print("{}: {}".format(cfg['ns'], version))
        sys.exit()

    if args.dump:
        max_key_length = max(len(key) for key in cfg.keys())
        for key, value in sorted(cfg.items()):
            print('{0:<{width}} {1}'.format(key + ":", value, width=max_key_length + 1))
        sys.exit()

    os.makedirs(args.repo_dir, exist_ok=True)

    if args.loglevel == logging.DEBUG: # debug if --debug
        is_debug = True
        logger.setLevel(logging.DEBUG)
    else:
        is_debug = os.environ.get(cfg['ns'].upper() + '_WEB_DEBUG', 'false').lower() == 'true'
        if is_debug:
            logger.setLevel(logging.DEBUG) # debug if export BOXES_WEB_DEBUG=true
        else:
            logger.setLevel(args.loglevel) # otherise --verbose or --quiet
            if args.loglevel == logging.ERROR:
                logging.basicConfig(level=logging.ERROR) # no verbose for --quiet

    return args, is_debug

