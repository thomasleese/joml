"""A markup language for describing journeys."""

from .parser import Journey, Leg, Stop, parse
from .tokeniser import tokenise


def loads(string):
    """Parse journeys from a Waymark document.

    :param string: A Waymark document.
    :return: The journeys described by the document, in the order they
        appear.
    """
    return parse(tokenise(string))


__all__ = ["Journey", "Leg", "Stop"]
