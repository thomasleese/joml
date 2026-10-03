"""Parse JOML tokens into journeys."""

import datetime
from dataclasses import dataclass
from enum import Enum

from .tokeniser import Token, TokenType


@dataclass(frozen=True)
class Stop:
    """A place at a point in time.

    :attr place_name: The name of the place.
    :attr date: The date the stop is reached.
    """

    place_name: str
    date: datetime.date

    def __str__(self):
        return f"{self.place_name} ({self.date})"

    def __lt__(self, other):
        if not isinstance(other, Stop):
            return NotImplemented
        return self.date < other.date


@dataclass(frozen=True)
class Leg:
    """A single mode of transport between two stops.

    :attr origin: The stop the leg starts from.
    :attr destination: The stop the leg ends at.
    :attr mode_of_transport: How the leg is travelled.
    """

    origin: Stop
    destination: Stop
    mode_of_transport: str

    def __str__(self):
        return f"{self.origin} to {self.destination} by {self.mode_of_transport}"


@dataclass(frozen=True)
class Journey:
    """A sequence of legs, travelled in order.

    :attr legs: The legs of the journey, in the order they are travelled.
    """

    legs: list[Leg]

    def __lt__(self, other):
        if not isinstance(other, Journey):
            return NotImplemented
        return self.origin < other.origin

    @property
    def origin(self) -> Stop:
        """The first stop of the journey."""
        return self.legs[0].origin

    @property
    def destination(self) -> Stop:
        """The final stop of the journey."""
        return self.legs[-1].destination


class CurrentAction(Enum):
    EXPECTING_DATE = 0
    EXPECTING_DESCRIPTOR = 1
    EXPECTING_DESTINATION = 2
    EXPECTING_MODE_OF_TRANSPORT = 3
    EXPECTING_SOURCE = 4


def parse(tokens: list[Token]) -> list[Journey]:
    """Parse a list of JOML tokens into a list of journeys.

    :param tokens: The tokens to parse.
    :return: The journeys described by the tokens.
    :raises ValueError: If the tokens do not describe valid journeys.
    """
    journeys = []

    current_action = CurrentAction.EXPECTING_DESCRIPTOR

    is_first_from = True
    is_first_to = True

    current_legs: list[Leg] = []
    current_origin_place_name: str | None = None
    current_origin_date: datetime.date | None = None
    current_destination_place_name: str | None = None
    current_destination_date: datetime.date | None = None
    current_mode_of_transport: str | None = None

    def append_current_leg():
        nonlocal \
            current_legs, \
            current_origin_place_name, \
            current_origin_date, \
            current_destination_place_name, \
            current_destination_date

        if current_origin_place_name is None:
            raise ValueError("No origin stop is defined yet")
        elif current_destination_place_name is None:
            raise ValueError("No destination stop is defined yet")
        elif current_origin_date is None:
            raise ValueError("No origin date is defined yet")
        elif current_destination_date is None:
            raise ValueError("No destination date is defined yet")
        elif current_mode_of_transport is None:
            raise ValueError("No mode of transport is defined yet")

        origin = Stop(place_name=current_origin_place_name, date=current_origin_date)
        destination = Stop(
            place_name=current_destination_place_name, date=current_destination_date
        )

        current_legs.append(
            Leg(
                origin=origin,
                destination=destination,
                mode_of_transport=current_mode_of_transport,
            )
        )

        current_origin_place_name = current_destination_place_name
        current_origin_date = current_destination_date
        current_destination_place_name = None

    def append_current_journey():
        nonlocal \
            journeys, \
            is_first_to, \
            current_legs, \
            current_origin_place_name, \
            current_origin_date, \
            current_destination_place_name, \
            current_destination_date, \
            current_mode_of_transport

        append_current_leg()

        journeys.append(Journey(legs=current_legs))

        is_first_to = True
        current_legs = []
        current_origin_place_name = None
        current_origin_date = None
        current_destination_place_name = None
        current_destination_date = None
        current_mode_of_transport = None

    def handle_date(token):
        nonlocal current_action, current_origin_date, current_destination_date

        if current_action == CurrentAction.EXPECTING_DATE:
            date = datetime.date.fromisoformat(token.value)
            if current_origin_date is None:
                current_origin_date = date

            current_destination_date = date
            current_action = CurrentAction.EXPECTING_DESCRIPTOR
        else:
            raise ValueError("Unexpected date")

    def handle_keyword(token):
        nonlocal current_action, current_mode_of_transport, is_first_from, is_first_to

        if not current_action == CurrentAction.EXPECTING_DESCRIPTOR:
            raise ValueError(f"Unexpected keyword '{token.value}'")

        match token.value:
            case "by":
                current_action = CurrentAction.EXPECTING_MODE_OF_TRANSPORT
            case "from":
                if not is_first_from:
                    append_current_journey()

                current_action = CurrentAction.EXPECTING_SOURCE
                is_first_from = False
            case "on":
                current_action = CurrentAction.EXPECTING_DATE
            case "to":
                if not is_first_to:
                    append_current_leg()

                current_action = CurrentAction.EXPECTING_DESTINATION
                is_first_to = False
            case _:
                raise ValueError(f"Unexpected keyword '{token.value}'")

    def handle_string(token):
        nonlocal \
            current_action, \
            current_origin_place_name, \
            current_destination_place_name, \
            current_mode_of_transport

        match current_action:
            case CurrentAction.EXPECTING_SOURCE:
                current_origin_place_name = token.value
                current_action = CurrentAction.EXPECTING_DESCRIPTOR
            case CurrentAction.EXPECTING_DESTINATION:
                current_destination_place_name = token.value
                current_action = CurrentAction.EXPECTING_DESCRIPTOR
            case CurrentAction.EXPECTING_MODE_OF_TRANSPORT:
                current_mode_of_transport = token.value
                current_action = CurrentAction.EXPECTING_DESCRIPTOR

    for token in tokens:
        match token.type:
            case TokenType.DATE:
                handle_date(token)
            case TokenType.KEYWORD:
                handle_keyword(token)
            case TokenType.STRING:
                handle_string(token)

    append_current_journey()

    return journeys
