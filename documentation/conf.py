import sys
import os

sys.path.append(os.path.abspath('..'))

project = 'hw_14_FastAPI_test'
copyright = '2023, Artem Danilov'
author = 'Artem Danilov'

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'alabaster'
html_static_path = ['_static']
