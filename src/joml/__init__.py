"""A markup language for describing journeys."""

from .parser import Journey, Leg, Stop, parse
from .tokeniser import tokenise


def loads(string):
    """Parse journeys from a JOML document.

    :param string: A JOML document.
    :return: The journeys described by the document, in the order they
        appear.
    """
    return parse(tokenise(string))


__all__ = ["Journey", "Leg", "Stop"]
