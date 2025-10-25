import os
import sys

from sphinx_pyproject import SphinxConfig

sys.path.insert(0, os.path.abspath("../../src"))


config = SphinxConfig("../../pyproject.toml", globalns=globals())


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

# MyST settings
myst_enable_extensions = ["deflist", "html_admonition", "html_image", "colon_fence","substitution"]
myst_substitutions = {
    "version": version,
    "release": release,
}
