..
    This file is part of COUNTER-Robots.
    Copyright (C) 2018 CERN.

    COUNTER-Robots is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


Developer notes
===============

.. note::

    This part is intended for the developers of this package.

New lists of robots are released regularly, and needs to be propagated to this
package. The procedure is as follows:

1) Fetch new lists:

.. code-block:: console

    $ python scripts/update-lists.py

2) Commit lists

.. code-block:: console

    $ git add counter_robots/data/*.txt
    $ git commit -m "Update machine and robots lists"

3) Bump version in ``counter_robots/version.py`` and ``CHANGES.rst``. The new
   version number is made using the pattern ``YYYY.MM`` (note, without leading
   zeros - e.g. ``2018.6``)

4) Commit release

.. code-block:: console

    $ git add counter_robots/version.py CHANGES.rst
    $ git commit -m "release: YYYY.MM"
