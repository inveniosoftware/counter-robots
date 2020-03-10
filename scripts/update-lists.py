# -*- coding: utf-8 -*-
#
# This file is part of COUNTER-Robots.
# Copyright (C) 2018-2019 CERN.
#
# COUNTER-Robots is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""
Small script to update the list of robots and machines.

Usage:

.. code-block:: console

    $ cd scripts
    $ python update-lists.py
"""

from __future__ import absolute_import, print_function

from os.path import dirname, join

try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen


files = {
    'machine.txt':
        'https://raw.githubusercontent.com/CDLUC3/Make-Data-Count/'
        'master/user-agents/lists/machine.txt',
    'robot.txt':
        'https://raw.githubusercontent.com/atmire/COUNTER-Robots/'
        'master/generated/COUNTER_Robots_list.txt',
    'unclassified.txt':
        'https://raw.githubusercontent.com/CDLUC3/Make-Data-Count/'
        'master/user-agents/lists/unclassified.txt'
}

def _create_set(filename):
    """Create a set containing all lines in the file."""
    with open(_get_package_path(filename), 'r') as fp:
        return set(fp.readlines())

def _get_package_path(filename):
    """Retrieve path of a file in this Python package."""
    return join(dirname(__file__), '../counter_robots/data/', filename)


def _update_file(url, filename):
    """Update the content of a single file."""
    response = urlopen(url)
    if response.code != 200:
        raise Exception('{0} GET {1} failed.'.format(response.code, url))

    user_agents = [agent.decode('utf-8')
                   for agent in response if not agent.startswith(b'w')]

    with open(_get_package_path(filename), 'wb') as fp:
        for agent in user_agents:
            fp.write(agent.encode('utf-8'))

    print('Updated {}'.format(filename))


def _filter_machines_from_robots(files):
    """Filter Machines from robots.

    The Counter-Robots repository keeps a list of all user-agents that are
    regarded robots/spyders. The Make-Data-Count repository uses manually
    curated lists to seperate machine user-agents from robot user-agents.

    Unfortunately Make-Data-Count is on a less frequent update schedule than the
    COUNTER-Robots repository. To make sure that we have the latest user agents
    available to use we fetch the latest Counter-Robots data and diff it with
    the latest machine/unclassified user-agents known from Make-Data-Count.
    """
    machine_set = _create_set('machine.txt')
    unclassified_set = _create_set('unclassified.txt')
    robot_set = _create_set('robot.txt')

    robot_set = robot_set.difference(machine_set, unclassified_set)
    robot_set = sorted(robot_set, key=str.lower)

    with open(_get_package_path('robot.txt'), 'w') as fp:
        fp.writelines(robot_set)

    print('Filtered robot.txt')


def main():
    """Update the files containing the list of robots and machines."""
    for filename, url in files.items():
        _update_file(url, filename)

    _filter_machines_from_robots(files)


if __name__ == '__main__':
    main()
