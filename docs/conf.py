# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys, os

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

sys.path.append(os.path.abspath(os.pardir))

__version__ = '1.0'

# -- General configuration -----------------------------------------------------

source_suffix = '.rst'
master_doc = 'index'
project = 'cirospat'
copyright = '= licenza CC BY cirospat'

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

extlinks = {}

# -- Options for HTML output ---------------------------------------------------

html_theme = 'default'

html_static_path = ['static']

def setup(app):
    # overrides for wide tables in RTD theme
    app.add_stylesheet('theme_overrides.css') # path relative to static

"""
  You might want to uncomment the “latex_documents = []” if you use CKJ characters in your document.
  Because the pdflatex raises exception when generate Latex documents with CKJ characters.
"""
#latex_documents = []
latex_logo = "static/cirospat.jpg"
html_logo = "static/cirospat.jpg"

setup(
packages=['newproject'],
package_data={'top': [
'*.html',
'*.css',
'*.js',	
	'/img/*.png',
'/img/*.db',
	]},
include_package_data=True,
],
)
