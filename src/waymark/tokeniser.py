"""Tokenise Waymark documents into low-level tokens."""

import re
from enum import Enum, StrEnum
from typing import NamedTuple


class TokenType(Enum):
    """The type of a token."""

    DATE = 1
    KEYWORD = 2
    STRING = 3


class Keyword(StrEnum):
    """A keyword that delimits parts of a Waymark document."""

    BY = "by"
    FROM = "from"
    ON = "on"
    TO = "to"


class Token(NamedTuple):
    """A low-level token from a Waymark document.

    :attr type: The type of the token.
    :attr value: The value of the token.
    """

    type: TokenType
    value: str


KEYWORDS = [keyword.value for keyword in Keyword]
DATE_PATTERN = r"\d{4}-\d{2}-\d{2}"


def tokenise(s: str) -> list[Token]:
    """Split a Waymark document into a list of tokens.

    Comments, which begin with ``#`` and continue to the end of the line,
    are discarded.

    :param s: A Waymark document.
    :return: The tokens in the document, in the order they appear.
    """
    tokens = []
    i = 0
    n = len(s)

    while i < n:
        if s[i].isspace():
            i += 1
            continue

        if s[i] == "#":
            while i < n and s[i] != "\n":
                i += 1
            continue

        if i + 9 < n and re.match(DATE_PATTERN, s[i : i + 10]):
            tokens.append(Token(TokenType.DATE, s[i : i + 10]))
            i += 10
            continue

        for keyword in KEYWORDS:
            if s[i : i + len(keyword)].lower() == keyword and (
                i + len(keyword) == n or not s[i + len(keyword)].isalpha()
            ):
                tokens.append(Token(TokenType.KEYWORD, keyword))
                i += len(keyword)
                continue

        j = i
        while j < n and not s[j].isspace() and s[j] not in ["#"]:
            j += 1
        if j > i:
            tokens.append(Token(TokenType.STRING, s[i:j]))
        i = j

    return tokens
