# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import sphinx_rtd_theme

module_path = os.path.abspath('../..')
sys.path.insert(0, module_path)

import pyenvbuilder

def setup(app):
    app.add_css_file(os.path.abspath('_static/theme.css'))
# -- Project information -----------------------------------------------------

project = 'PyEnvBuilder'
copyright = '2020, SLAC National Accelerator Laboratory'
author = 'SLAC National Accelerator Laboratory'

# The short X.Y version.
version = pyenvbuilder.__version__
# The full version, including alpha/beta/rc tags
release = pyenvbuilder.__version__

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinxarg.ext'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Output file base name for HTML help builder.
htmlhelp_basename = 'PyEnvBuilderdoc'

# -- Ouptions for LateX output -----------------------------------------------
# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
# author, documentclass [howto, manual, or own class]).
latex_documents = [
    ('index', 'PyEnvBuilder.tex', u'PyEnvBuilder Documentation', 
    u'SLAC National Accelerator Laboratory', 'manual'),
]

# -- Options for manual page output ------------------------------------------

# One entry per manyal page. List of tuples
# (source start file, name description, authors, manual section).
man_pages = [
    ('index', 'PyEnvBuilder', u'PyEnvBuilder Documentation', 
    [u'SLAC National Accelerator Laboratory'], 1)
]

# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author, 
# dir meny entry, description, category)
textinfo_documents = [
    ('index', 'PyEnvBuilder', u'PyEnvBuilder Documentation',
    u'SLAC National Accelerator Laboratory', 'One line description of project.',
    'Miscellaneous'),
]
