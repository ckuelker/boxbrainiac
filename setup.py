# file: setup.py
import os
from setuptools import setup

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

setup(
    name='boxbrainiac',
    version='0.1.1', # Semantic versioning MAJOR.MINOR.PATCH
    description='Web application to manage box content, realm and location',
    long_description=(read('README.md') + '\n\n'),
    license="GPLv3+",
    author='Christian Külker',
    author_email='c@c8i.org',
    url="https://github.com/ckuelker/boxbrainiac",
    packages=['boxbrainiac'],
    include_package_data=True,
    package_data={'boxbrainiac': ['templates/*', 'static/css/*']},
    python_requires='>=3.5',
    # html, os, argparse, logging, subprocess, sys are standard
    install_requires=[
        'flask', # python3-flask
        'pyyaml', # python3-yaml
        'fuzzywuzzy', # python3-fuzzywuzzy
        'python-Levenshtein', # python3-levenshtein
        'dulwich', # python3-dulwich for git
    ],
    extras_require={
        'build': [
            'setuptools',
            'wheel',
        ],
        'test': [
            'html5lib', # python3-html5lib
            'flask', # python3-flask
            'lxml', # python3-lxml
        ],
    },
    entry_points={
        'console_scripts': [
            'boxbrainiac = boxbrainiac.main:run_app',
        ]
    },
    classifiers=[
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
    ],
)

