# file: boxbrainiac/config.py
import os

ns = 'boxbrainiac'

cfg  = {
    # Namespace: boxbrainiac
    'ns': ns,
    # IP address or hostname or 0.0.0.0 (not recommended)
    'host': 'localhost',
    # Port of Flask web server
    'port': 5000,
    # Database file: boxbrainiac.yaml
    'yaml_file': ns + '.yaml',
    # Repository: $HOME/.boxbrainiac/data
    'repo_dir': str(os.path.join(os.path.expanduser('~'), '.' + ns, 'data')),
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

