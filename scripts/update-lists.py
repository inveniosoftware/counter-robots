# -*- coding: utf-8 -*-
#
# This file is part of COUNTER-Robots.
# Copyright (C) 2018-2025 CERN.
#
# COUNTER-Robots is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Small script to update the list of robots and machines.

Usage:

.. code-block:: console

    $ cd scripts
    $ python update-lists.py
"""

from os.path import dirname, join

try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen


files = [
    (
        "machine.txt",
        "https://raw.githubusercontent.com/CDLUC3/Make-Data-Count/"
        "master/user-agents/lists/machine.txt",
    ),
    (
        "robot.txt",
        "https://raw.githubusercontent.com/atmire/COUNTER-Robots/"
        "master/generated/COUNTER_Robots_list.txt",
    ),
]


def _get_package_path(filename):
    """Retrieve path of a file in this Python package."""
    return join(dirname(__file__), "../counter_robots/data/", filename)


def update_file(url, filename):
    """Update the content of a single file."""
    resp = urlopen(url)
    if resp.code != 200:
        raise Exception("GET {} failed.".format(url))
    with open(_get_package_path(filename), "w") as fp:
        for l in resp:
            if not l.startswith(b"#"):
                fp.write(l.decode("utf8"))
    print("Updated {}".format(filename))


def main():
    """Update the files containing the list of robots and machines."""
    for filename, url in files:
        update_file(url, filename)


if __name__ == "__main__":
    main()
