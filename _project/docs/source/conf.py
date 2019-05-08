#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../../'))
#sys.path.append(os.path.abspath("_extensions"))

# print(sys.path)
#
def setup(app):
    app.add_stylesheet('css/ls.css')
    app.add_stylesheet('css/new.css')
    app.add_stylesheet('css/custom_pygments.css')


# # Activate the theme.
# sys.path.append(os.path.abspath('_themes'))
# html_theme_path = ['_themes']
# html_theme = 'bootstrap'

# Optional. Use a shorter name to conserve nav. bar space.
html_short_title = 'Ayoub Malek\'s Blog'

# -- Project information -----------------------------------------------------

project = 'Ayoub Malek'
copyright = '2018, SuperKogito'
author = 'SuperKogito'
html_favicon = '_static/favicon.ico'
# The short X.Y version
version = ''
# The full version, including alpha/beta/rc tags
release = ''


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.todo',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinxcontrib.napoleon',
    'sphinxjp.themes.basicstrap',
#    'sphinxcontrib.googleanalytics',
    'sphinxcontrib.bibtex',
    'sphinxcontrib.spelling',
#    'sphinxcontrib.email',
    'sphinx_sitemap',
    'ablog',
    'sphinx.ext.intersphinx',
    'sphinxcontrib.pdfembed',
]
     #'sphinxprettysearchresults',
    #'sphinxcontrib.disqus',
# 2. Add ablog templates path
import ablog
#disqus_shortname = 'https-superkogito-github-io'
# 2a. if `templates_path` is not defined
templates_path = [ablog.get_html_templates_path()]
googleanalytics_id = 'UA-133660046-1'
spelling_lang='en_US'
spelling_show_suggestions=True
# Add any paths that contain templates here, relative to this directory.
# templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
#source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'
#html_sidebars = {
#   '**': [...,
#          'postcard.html', 'recentposts.html',
#          'tagcloud.html', 'categories.html',
#          'archives.html', ]
#}
# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# -- Options for HTML output ----------------------------------------	both modified:   ../../searchindex.js

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#html_logo =  '../Alogo_dark.png'
#html_logo =  'me.gif'


# html_theme = 'sphinxbootstrap4theme'
# import sphinx_readable_theme
# import sphinxbootstrap4theme
# html_theme = 'basicstrap'
# import sphinxbootstrap4theme
# html_theme = 'sphinxbootstrap4theme'
# html_theme_path = [sphinxbootstrap4theme.get_path()]



# import sphinxbootstrap4theme
# html_theme = 'basicstrap'
# html_theme_options = {
#                       'nosidebar': False,
#                       'sidebar_span': 4, # 1(min) - 12(max)
#                       'content_fixed': True,
#                       'content_width': '1000px',
#                       'nav_fixed': True,
#                       'googlewebfont': True,
#                       'googlewebfont_url': 'http://fonts.googleapis.com/css?family=Text+Me+One',
#                       'googlewebfont_style': "font-family: 'Text Me One', sans-serif",
#                       'inner_theme': True,
#                       'inner_theme_name': 'bootswatch-slate', #'bootswatch-readable',
#                       #'theme_preview': True,
# }
#
#import sphinxbootstrap4theme
html_theme = 'basicstrap'
html_theme_options = {
                      #'rightsidebar': True,
                      'nosidebar': True,
                      'sidebar_span': 2, # 1(min) - 12(max)
                      'content_fixed': True,
                      'content_width': '800px',
                      'nav_fixed': False,
                      'googlewebfont': True,
                      'googlewebfont_url': 'https://fonts.googleapis.com/css?family=Text+Me+One',
                      'googlewebfont_style': "font-family: 'Text Me One', sans-serif",
                      'inner_theme': True,
                      'inner_theme_name': 'bootswatch-yeti', #'bootswatch-readable',
 #                     'theme_preview': True,
                      #'noresponsive': False,


}



source_suffix = '.rst'
master_doc    = 'index'
exclude_patterns = ['_build', 'README.rst']
pygments_style   = 'tango'
html_show_copyright = True

# html_favicon = "favicon.ico"
project = "Ayoub Malek's blog"
html_title = project
suppress_warnings = ["image.nonlocal_uri"]

# import sphinx_rtb_theme
# html_theme = 'sphinx_rtb_theme'
# html_theme_path = [sphinx_rtb_theme.get_html_theme_path()]
# html_theme_options = {
#                         'navigation_depth': 4,
#                         'canonical_url': 'https://superkogito.github.io/',
#                         'blog_url': 'https://superkogito.github.io/blog',
#                         'disqus_comments': False,
#                         #'disqus_username': 'SuperKogito',
#                         'collapse_navigation': False,
#                         'display_version': False,
# }


html_sidebars = { '**': ['relations.html', 'sourcelink.html', 'searchbox.html'] }


# Html logo in navbar.
# Fit in the navbar at the height of image is 37 px.
#html_logo = '../html_logo.png'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'SphinxTutorialdoc'


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'SphinxTutorial.tex', 'SphinxTutorial Documentation',
     'SuperKogito', 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'sphinxtutorial', 'SphinxTutorial Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'SphinxTutorial', 'SphinxTutorial Documentation',
     author, 'SphinxTutorial', 'One line description of project.',
     'Miscellaneous'),
]


# -- Extension configuration -------------------------------------------------
# -- Options for todo extension ----------------------------------------------
# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True
site_url = 'https://superkogito.github.io/'
