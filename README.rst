..
    This file is part of COUNTER-Robots.
    Copyright (C) 2018 CERN.

    COUNTER-Robots is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.

================
 COUNTER-Robots
================

.. image:: https://img.shields.io/github/license/inveniosoftware/counter-robots.svg
        :target: https://github.com/inveniosoftware/counter-robots/blob/master/LICENSE

.. image:: https://img.shields.io/travis/inveniosoftware/counter-robots.svg
        :target: https://travis-ci.org/inveniosoftware/counter-robots

.. image:: https://img.shields.io/coveralls/inveniosoftware/counter-robots.svg
        :target: https://coveralls.io/r/inveniosoftware/counter-robots

.. image:: https://img.shields.io/pypi/v/counter-robots.svg
        :target: https://pypi.org/pypi/counter-robots


Library for COUNTER-compliant detection of machines and robots.


Update user agent pattern lists
===============================
The user agent pattern lists used to detect robots and machines come from
`Make-Data-Count <https://github.com/CDLUC3/Make-Data-Count>`_.
In order to update the lists, run the
`update-lists <https://github.com/inveniosoftware/counter-robots/blob/master/scripts/update-lists.py>`_ script.
Then commit the changes to the following files:

* `machine.txt`
* `robot.txt`

Further documentation is available on
https://counter-robots.readthedocs.io/
