"""Sphinx configuration for the joml documentation."""

import sys
from pathlib import Path

from pygments.lexer import RegexLexer
from pygments.token import Comment, Keyword, Name, String, Text
from sphinx.highlighting import lexers

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class JomlLexer(RegexLexer):
    """A Pygments lexer for the JOML file format."""

    name = "joml"
    aliases = ["joml"]  # noqa: RUF012
    filenames = ["*.joml"]  # noqa: RUF012

    tokens = {  # noqa: RUF012
        "root": [
            (r"#.*", Comment),
            (r"(?i)\b(?:at|by|from|on|to)\b", Keyword),
            (r"\d{4}-\d{2}-\d{2}", Name.Decorator),
            (r"\d{2}:\d{2}", Name.Decorator),
            (r"\S+", String),
            (r"\s+", Text),
        ]
    }


lexers["joml"] = JomlLexer()

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
