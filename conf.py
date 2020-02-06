# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys, os


#dal conf.py di tansignari #
import recommonmark
from recommonmark.transform import AutoStructify


on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

sys.path.append(os.path.abspath(os.pardir))

__version__ = '1.0'

# -- General configuration -----------------------------------------------------

# source_suffix = '.rst' eliminato dal conf.py di tansignari #
master_doc = 'index'
project = 'schema tipo Read the Docs'
copyright = 'change-me'

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

extlinks = {}

# -- Options for HTML output ---------------------------------------------------

html_theme = 'default'

html_static_path = ['static']

def setup(app):
    # overrides for wide tables in RTD theme
    app.add_stylesheet('theme_overrides.css') # path relative to static
  

#dal conf.py di tansignari #
from recommonmark.parser import CommonMarkParser

source_parsers = {
    '.md': 'recommonmark.parser.CommonMarkParser',
}

source_suffix = ['.rst', '.md']

extensions = ['sphinx.ext.ifconfig','sphinx_markdown_tables']

    
"""
  You might want to uncomment the “latex_documents = []” if you use CKJ characters in your document.
  Because the pdflatex raises exception when generate Latex documents with CKJ characters.
"""
#latex_documents = []

latex_logo = "static/help.jpg"
html_logo = "static/help.jpg"


# Adding Custom CSS or JavaScript to a Sphinx Project: al seguente link ci sono esempi
# https://docs.readthedocs.io/en/latest/guides/adding-custom-css.html

templates_path = ['_templates']
