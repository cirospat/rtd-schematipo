# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys, os

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

sys.path.append(os.path.abspath(os.pardir))

__version__ = '1.0'

# -- General configuration -----------------------------------------------------

source_suffix = '.rst'
master_doc = 'index'
project = 'Ciro Spataro'
copyright = '= licenza CC BY Cirospat'

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

extlinks = {}

# -- Options for HTML output ---------------------------------------------------

html_theme = 'default'

html_static_path = ['static']

def setup(app):
    # overrides for wide tables in RTD theme
    app.add_stylesheet('theme_overrides.css') # path relative to static

html_static_path = ['js']

def setup(app):
    # overrides for backtop
    app.add_javascript('arrow.js')

html_static_path = ['top']

def setup(app):
    # overrides for backtop
    app.add_stylesheet('backTop.css')
    app.add_stylesheet('jquerysctipttop.css')
    app.add_javascript('jquery-1.11.1.min.js')
    app.add_javascript('jquery.backTop.js')
    app.add_javascript('jquery.backTop.min.js')
    

"""
  You might want to uncomment the “latex_documents = []” if you use CKJ characters in your document.
  Because the pdflatex raises exception when generate Latex documents with CKJ characters.
"""
#latex_documents = []


latex_logo = "static/cirospat.jpg"
html_logo = "static/cirospat.jpg"



# -- note---- estensioni per lo script 'top' per abilitare la freccia che porta in alto (sono solo prove) --------------------

# extensions = ['top']

# setup(
# packages=['top'],
# package_data={'top': [
# '*.css',
# '*.js',	
# '/img/*.png',
# '/img/*.db',
# ]},
# include_package_data=True,
# )
