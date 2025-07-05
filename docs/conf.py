import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'easy-slam'
copyright = '2024, Your Name'
author = 'Your Name'
release = '0.1.0'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
html_theme = 'alabaster' 