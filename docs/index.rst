JOML
=======

A markup language for describing journeys.

Usage
-----

.. code-block:: python

   import joml

   journeys = joml.loads("""
   From heathrow on 2020-01-01 to gatwick by plane
   To stansted on 2020-01-02 by train
   """)

   for journey in journeys:
       for leg in journey.legs:
           print(leg)

Documentation
-------------

.. toctree::
   :maxdepth: 2

   api
