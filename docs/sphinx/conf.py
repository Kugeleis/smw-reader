import os
import sys

from sphinx.application import Sphinx
from sphinx.config import Config
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
myst_enable_extensions = ["deflist", "html_admonition", "html_image", "colon_fence", "substitution"]


# -- Event handler for config-inited ----------------------------------------
def setup_myst_substitutions(app: Sphinx, config: Config) -> None:
    """
    Set up myst_substitutions after the configuration is initialized.
    This ensures that the `version` and `release` values are correctly
    populated by sphinx_pyproject before being used.
    """
    config.myst_substitutions = {
        "version": config.version,
        "release": config.release,
    }


def setup(app: Sphinx) -> None:
    """
    Connect the event handler to the `config-inited` event.
    """
    app.connect("config-inited", setup_myst_substitutions)
