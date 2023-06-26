# file: boxbrainiac/store.py
import yaml
import boxbrainiac.vcs as vcs
from boxbrainiac.debug import logger
from boxbrainiac.exception import StoreOperationError
import os

def read_yaml(cfg):
    if os.path.exists(cfg['yaml_path']):
        logger.debug(" - Read YAML file [{}]".format(cfg['yaml_path']))
        try:
            with open(cfg['yaml_path'], 'r') as f:
                data = yaml.safe_load(f)
            return data
        except (IOError, yaml.YAMLError) as e:
            raise StoreOperationError('STO-001', cfg['yaml_path'], str(e))
    else:
        logger.debug(" - Create Data")
        data = {ns: [], 'available_ids': []}
    return data

def write_yaml(cfg, data):
    try:
        with open(cfg['yaml_path'], 'wb') as f:
            logger.debug(" - Write YAML file [%s]".format(cfg['yaml_path']))
            yaml.safe_dump(data, f, encoding='utf-8', allow_unicode=True)
    except (IOError, yaml.YAMLError) as e:
        raise StoreOperationError('STO-002', cfg['yaml_path'], str(e))

def ensure_yaml_exists(cfg):
    if not os.path.exists(cfg['yaml_path']):

        init = "available_ids: []\n" + cfg['ns'] + ": []\n"
        data = yaml.safe_load(init)
        write_yaml(cfg, data) # 'w' (but as 'wb')

        if vcs.is_git_repo(cfg):
           vcs.git_commit_and_push(cfg,"Initialize " + cfg['yaml_file'])

