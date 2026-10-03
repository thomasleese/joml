"""Sphinx configuration for the joml documentation."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

project = "joml"
copyright = "Thomas Leese"
author = "Thomas Leese <thomas@leese.io>"

release = "0.1.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

autodoc_member_order = "bysource"

html_theme = "alabaster"

htmlhelp_basename = "jomldoc"
