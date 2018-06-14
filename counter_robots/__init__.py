# -*- coding: utf-8 -*-
#
# This file is part of COUNTER-Robots.
# Copyright (C) 2018 CERN.
#
# COUNTER-Robots is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Library for COUNTER-compliant detection of machines and robots."""

from __future__ import absolute_import, print_function

from os.path import join
import pkg_resources
import re

from .version import __version__


config = dict(
    ROBOTS_URL='https://raw.githubusercontent.com/CDLUC3/Make-Data-Count/'
               'master/user-agents/lists/robot.txt',
    MACHINE_URL='https://raw.githubusercontent.com/CDLUC3/Make-Data-Count/'
                'master/user-agents/lists/machine.txt',
    ROBOTS_FILE='robot.txt',
    MACHINES_FILE='machine.txt'
)


def _get_resource_content(filename):
    """Retrieve content from a file in this Python package."""
    return pkg_resources.resource_string(__name__, join('data', filename))


def _get_resource_path(filename):
    """Retrieve path of a file in this Python package."""
    return pkg_resources.resource_filename(__name__, join('data', filename))


def _regexp(filename):
    """Get a list of patterns from a file and make a regular expression."""
    lines = _get_resource_content(filename).decode('utf-8').splitlines()
    return re.compile('|'.join(lines))


robots_regexp = _regexp(config['ROBOTS_FILE'])
machines_regexp = _regexp(config['MACHINES_FILE'])


def is_robot(user_agent):
    """Detect if the user agent belongs to a robot."""
    if user_agent is None:
        return False
    return bool(robots_regexp.search(user_agent))


def is_machine(user_agent):
    """Detect if a user agent belongs to a machine."""
    if user_agent is None:
        return True
    return bool(machines_regexp.search(user_agent))


__all__ = ('__version__', )
