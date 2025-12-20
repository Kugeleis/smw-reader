import datetime
import os
import sys

from sphinx_pyproject import SphinxConfig

sys.path.insert(0, os.path.abspath("../../src"))


config = SphinxConfig("../../pyproject.toml", globalns=globals())

# -- Project information -----------------------------------------------------
project = config.name
copyright = f"{datetime.date.today().year}, Kugeleis"
version = config.version
release = config.version

# -- General configuration ---------------------------------------------------
extensions = [
    "myst_parser",
    "sphinx_pyproject",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "**.ipynb_checkpoints"]

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_favicon = "_static/favicon.svg"

html_context = {
    "display_github": True,
    "github_user": "Kugeleis",
    "github_repo": "smw-reader",
    "github_version": "main",
    "conf_py_path": "/docs/sphinx/",
}

html_theme_options = {
    "navigation_depth": 4,
    "logo_only": False,
    "prev_next_buttons_location": "bottom",
    "style_external_links": False,
    "style_nav_header_background": "#2980B9",
}

# MyST settings
myst_enable_extensions = ["deflist", "html_admonition", "html_image", "colon_fence", "substitution"]

# -- MyST substitutions ---------------------------------------------------
# This needs to be at the end of the file, so that the `version` and `release`
# variables are defined by sphinx_pyproject before they are used.
myst_substitutions = {
    "version": version,  # noqa: F821
    "release": version,  # noqa: F821
}
