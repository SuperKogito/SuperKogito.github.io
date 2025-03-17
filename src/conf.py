# Configuration file for the Sphinx documentation builder.
#
# For a full list of options see:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------
from datetime import datetime

# -- Project information -----------------------------------------------------
project = "🧠 SuperKogito"
copyright = f"2019-{datetime.now() .year}, Ayoub Malek"
author = "Ayoub Malek"
html_short_title = "Ayoub Malek's Blog"
html_favicon = "_static/favicon_io/favicon.ico"

# -- General configuration ---------------------------------------------------
# Add Sphinx extension modules
extensions = [
    "ablog",
    "sphinx.ext.intersphinx",
    "sphinxext.opengraph",
    "sphinx_copybutton",
    "sphinxcontrib.bibtex",
    "sphinxcontrib.tikz",
    "sphinxcontrib.pdfembed",
    "sphinxemoji.sphinxemoji",
]

# Template paths
templates_path = ['_templates', 'ablog']

# Patterns to ignore when looking for source files
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
# Emoji style
sphinxemoji_style = "twemoji"

# Theme configuration
html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "github_url": "https://github.com/superkogito/",
    "search_bar_text": "Search this site...",
    "google_analytics_id": "UA-133660046-1",
    "primary_sidebar_end": ["sidebar-ethical-ads"],
      "footer": ["footer.html"],
    "back_to_top_button": True,
}

# Sidebar configuration
html_sidebars = {
    "403": ["hello.html"],
    "404": ["hello.html"],
    "index": ["hello.html"],
    "about": ["hello.html"],
    "publications": ["hello.html"],
    "projects": ["hello.html"],
    "projects/**": ["hello.html"],
    "policy/**": ["hello.html"],
    "blog": ["tagcloud.html", "archives.html"],
    "blog/**": ["ablog/postcard.html", "ablog/recentposts.html", "ablog/archives.html"]
}

# ABlog configuration
blog_baseurl = "https://superkogito.github.io"
blog_title = "SuperKogito"
blog_path = "blog"
fontawesome_included = True
blog_post_pattern = "blog/*/*"
post_redirect_refresh = 1
post_auto_image = 0
post_auto_excerpt = 1

# Static files
html_static_path = ["_static"]
html_css_files = [
    "css/custom.css",
    "css/tree_graph.css",
    "css/social_media_sharing.css",
]

# Bibliography and citations
bibtex_bibfiles = ["refs.bib"]
suppress_warnings = ["bibtex.duplicate_label"]
bibtex_default_style = 'unsrt'

# TikZ configuration
tikz_proc_suite = 'ImageMagick'
tikz_tikzlibraries = 'arrows.meta,arrows,shapes,positioning,decorations.pathreplacing,chains,backgrounds,fit,shadows,shapes.geometric'

# OpenGraph configuration
ogp_site_url = "https://superkogito.github.io/"
ogp_image = "_static/meta_images/meta_ws_img_old.png"
ogp_description_length = 300
ogp_type = "article"
ogp_custom_meta_tags = [
    '<meta property="og:ignore_canonical" content="true" />',
]

# Language configuration
language = "english"

# Base URL for sitemap
html_baseurl = "https://superkogito.github.io/"
