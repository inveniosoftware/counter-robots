..
    This file is part of COUNTER-Robots.
    Copyright (C) 2018 CERN.

    COUNTER-Robots is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


.. include:: ../README.rst

.. include:: ../INSTALL.rst

Usage
=====

The usage of the library is pretty simple. Import the library, and provide
one of the API functions with a user agent string:

>>> from counter_robots import is_machine, is_robot, is_robot_or_machine
>>> is_machine('Wget/1.14 (linux-gnu)')
True
>>> is_robot('AdsBot-Google (+http://www.google.com/adsbot.html)')
True
>>> is_robot_or_machine('Mozilla/5.0')
False

API
===

.. automodule:: counter_robots
    :members:

Additional Notes
----------------

Notes on how to contribute, legal information and changes are here for the
interested.

.. toctree::
   :maxdepth: 1

   developer
   contributing
   changes
   license
   authors
