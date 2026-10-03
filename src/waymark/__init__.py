from .parser import Journey, Leg, Stop, parse
from .tokeniser import tokenise


def loads(string):
    return parse(tokenise(string))


__all__ = ["Journey", "Leg", "Stop"]
