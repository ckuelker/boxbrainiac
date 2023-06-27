# file: boxbrainiac/config.py
import os

ns = 'boxbrainiac'
store_yaml_file =  ns + '.yaml'
store_repo_dir = str(os.path.join(os.path.expanduser('~'), '.' + ns, 'data'))
store_yaml_path = os.path.join(store_repo_dir,store_yaml_file)

cfg  = {
    # Namespace: boxbrainiac
    'ns': ns,
    # IP address or hostname or 0.0.0.0 (not recommended)
    'host': 'localhost',
    # Port of Flask web server
    'port': 5000,
    # Database file: boxbrainiac.yaml
    'yaml_file': store_yaml_file,
    # Repository: $HOME/.boxbrainiac/data
    'repo_dir': store_repo_dir,
    # Fully qualified file name
    'yaml_path': store_yaml_path,
    # Template directory of boxbrainiac
    'tpl': 'templates',
    # Copyright
    'copyright': {
        'year': '2023',
        'url': 'https://github.com/ckuelker/boxbrainiac',
        'target': ns,
        'license': 'GPLv3',
    },
}

