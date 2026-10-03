from datetime import date, time

from joml.parser import parse
from joml.tokeniser import tokenise


def parse_and_tokenise(string):
    return parse(tokenise(string))


def test_simple():
    string = "From heathrow on 2020-01-01 to gatwick by plane"

    journeys = parse_and_tokenise(string)

    assert len(journeys) == 1

    journey = journeys[0]
    assert len(journey.legs) == 1

    leg = journey.legs[0]
    assert leg.origin.place_name == "heathrow"
    assert leg.origin.date == date(2020, 1, 1)
    assert leg.destination.place_name == "gatwick"
    assert leg.destination.date == date(2020, 1, 1)
    assert leg.mode_of_transport == "plane"


def test_newline():
    string = "From heathrow on 2020-01-01\nTo gatwick by plane"

    journeys = parse_and_tokenise(string)

    assert len(journeys) == 1

    journey = journeys[0]
    assert len(journey.legs) == 1

    leg = journey.legs[0]
    assert leg.origin.place_name == "heathrow"
    assert leg.origin.date == date(2020, 1, 1)
    assert leg.destination.place_name == "gatwick"
    assert leg.destination.date == date(2020, 1, 1)
    assert leg.mode_of_transport == "plane"


def test_comments():
    string = "From heathrow on 2020-01-01 # a comment\nTo gatwick by plane"

    journeys = parse_and_tokenise(string)

    assert len(journeys) == 1

    journey = journeys[0]
    assert len(journey.legs) == 1

    leg = journey.legs[0]
    assert leg.origin.place_name == "heathrow"
    assert leg.origin.date == date(2020, 1, 1)
    assert leg.destination.place_name == "gatwick"
    assert leg.destination.date == date(2020, 1, 1)
    assert leg.mode_of_transport == "plane"


def test_multiple_journeys():
    string = """
    From heathrow to gatwick on 2020-01-01 by plane
    From stansted to luton on 2020-01-02 by bicycle
    """

    journeys = parse_and_tokenise(string)
    assert len(journeys) == 2

    journey = journeys[0]
    assert len(journey.legs) == 1

    leg = journey.legs[0]
    assert leg.origin.place_name == "heathrow"
    assert leg.origin.date == date(2020, 1, 1)
    assert leg.destination.place_name == "gatwick"
    assert leg.destination.date == date(2020, 1, 1)
    assert leg.mode_of_transport == "plane"

    journey = journeys[1]
    assert len(journey.legs) == 1

    leg = journey.legs[0]
    assert leg.origin.place_name == "stansted"
    assert leg.origin.date == date(2020, 1, 2)
    assert leg.destination.place_name == "luton"
    assert leg.destination.date == date(2020, 1, 2)
    assert leg.mode_of_transport == "bicycle"


def test_multiple_legs():
    string = """
    From heathrow on 2020-01-01 to gatwick by plane
    To stansted on 2020-01-02 by train
    """

    journeys = parse_and_tokenise(string)
    assert len(journeys) == 1

    journey = journeys[0]
    assert len(journey.legs) == 2

    leg = journey.legs[0]
    assert leg.origin.place_name == "heathrow"
    assert leg.origin.date == date(2020, 1, 1)
    assert leg.destination.place_name == "gatwick"
    assert leg.destination.date == date(2020, 1, 1)
    assert leg.mode_of_transport == "plane"

    leg = journey.legs[1]
    assert leg.origin.place_name == "gatwick"
    assert leg.origin.date == date(2020, 1, 1)
    assert leg.destination.place_name == "stansted"
    assert leg.destination.date == date(2020, 1, 2)
    assert leg.mode_of_transport == "train"


def test_departure_time():
    string = "From heathrow at 09:30 on 2020-01-01 to gatwick by plane"

    journeys = parse_and_tokenise(string)

    assert len(journeys) == 1

    journey = journeys[0]
    assert len(journey.legs) == 1

    leg = journey.legs[0]
    assert leg.origin.place_name == "heathrow"
    assert leg.origin.date == date(2020, 1, 1)
    assert leg.origin.time == time(9, 30)
    assert leg.destination.place_name == "gatwick"
    assert leg.destination.date == date(2020, 1, 1)
    assert leg.destination.time is None
    assert leg.mode_of_transport == "plane"


def test_arrival_time():
    string = "From heathrow on 2020-01-01 to gatwick at 10:30 by plane"

    journeys = parse_and_tokenise(string)

    assert len(journeys) == 1

    journey = journeys[0]
    assert len(journey.legs) == 1

    leg = journey.legs[0]
    assert leg.origin.place_name == "heathrow"
    assert leg.origin.date == date(2020, 1, 1)
    assert leg.origin.time is None
    assert leg.destination.place_name == "gatwick"
    assert leg.destination.date == date(2020, 1, 1)
    assert leg.destination.time == time(10, 30)
    assert leg.mode_of_transport == "plane"


def test_time_resets_between_legs():
    string = """
    From heathrow at 09:30 on 2020-01-01 to gatwick by plane
    To stansted on 2020-01-02 by train
    """

    journeys = parse_and_tokenise(string)

    assert len(journeys) == 1

    journey = journeys[0]
    assert len(journey.legs) == 2

    leg = journey.legs[0]
    assert leg.origin.time == time(9, 30)
    assert leg.destination.time is None

    leg = journey.legs[1]
    assert leg.origin.time is None
    assert leg.destination.time is None
