Examples
========

A JOML document describes one or more journeys. Each journey is made up
of one or more legs, and each leg is made up of an origin stop, a
destination stop, and a mode of transport.

Stops are described using the keywords ``from`` (the origin of the
journey), ``to`` (the destination of a leg), ``on`` (the date a stop is
reached) and ``at`` (the time a stop is reached). The keyword ``by``
describes the mode of transport for a leg.

Keywords are case-insensitive, and one document can describe many
journeys.

Single leg
----------

The simplest journey has a single leg:

.. code-block:: joml

   From heathrow on 2020-01-01 to gatwick by plane

The origin and destination dates are independent, so a leg can span
more than one day:

.. code-block:: joml

   From london on 2020-01-01 to paris on 2020-01-02 by train

Multiple legs
-------------

A leg ends when the mode of transport is given. Starting another leg
with ``to`` continues the same journey, with the destination of the
previous leg becoming the origin of the next:

.. code-block:: joml

   From heathrow on 2020-01-01 to gatwick by plane
   To stansted on 2020-01-02 by train

This describes one journey with two legs, travelling from heathrow to
gatwick by plane, then from gatwick to stansted by train.

Times
-----

The ``at`` keyword describes the time a stop is reached. Before the
destination is named, it gives the departure time; after the
destination, it gives the arrival time:

.. code-block:: joml

   From heathrow at 09:30 on 2020-01-01 to gatwick at 10:30 by plane

Times, like the departure time above, do not carry over to the next leg:

.. code-block:: joml

   From heathrow at 09:30 on 2020-01-01 to gatwick by plane
   To stansted on 2020-01-02 by train

Here only the first leg has a departure time.

Multiple journeys
------------------

Starting a new journey with ``from`` finishes the previous one:

.. code-block:: joml

   From heathrow to gatwick on 2020-01-01 by plane
   From stansted to luton on 2020-01-02 by bicycle

This describes two separate journeys.

Whitespace
----------

Whitespace and newlines are not significant. Keywords delimit the parts
of a document, so a journey can be laid out however you like:

.. code-block:: joml

   From heathrow at 09:30 on 2020-01-01 to gatwick by plane
       to stansted on 2020-01-02 by train
