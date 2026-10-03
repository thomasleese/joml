# JOML

A markup language for describing journeys (**Journey Markup Language**).

## Installation

```shell
$ pip install joml
```

## Usage

```python
import joml

journeys = joml.loads("""
From heathrow on 2020-01-01 to gatwick by plane
To stansted on 2020-01-02 by train
""")

for journey in journeys:
    for leg in journey.legs:
        print(leg)
```

For more examples, including multiple journeys, comments, and parsing
low-level tokens, see the [documentation].

[documentation]: https://thomas.leese.io/joml/

## Development

### Tests

```shell
$ uv run pytest
```

### Linting

```shell
$ uv run ruff format
$ uv run ruff check
$ uv run ty check
```
