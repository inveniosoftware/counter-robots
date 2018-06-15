# -*- coding: utf-8 -*-
#
# This file is part of COUNTER-Robots.
# Copyright (C) 2018 CERN.
#
# COUNTER-Robots is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Library for COUNTER-compliant detection of machines and robots."""

from __future__ import absolute_import, print_function

import re
from functools import wraps
from os.path import join

import pkg_resources

from .version import __version__


def _get_resource_content(filename):
    """Retrieve content from a file in this Python package."""
    return pkg_resources.resource_string(__name__, join('data', filename))


def memoize(func):
    """Cache result of function call."""
    cache = {}

    @wraps(func)
    def inner(filename):
        if filename not in cache:
            cache[filename] = func(filename)
        return cache[filename]
    return inner


@memoize
def _regexp(filename):
    """Get a list of patterns from a file and make a regular expression."""
    lines = _get_resource_content(filename).decode('utf-8').splitlines()
    return re.compile('|'.join(lines))


def _match_useragent(user_agent, filename):
    return bool(_regexp(filename).search(user_agent))


def is_robot(user_agent):
    """Determine if user agent is a robot/crawler/spider.

    Determined according to the *Code of Practice for Research Data*.
    """
    return _match_useragent(user_agent, 'robot.txt')


def is_machine(user_agent):
    """Determine if user agent is a machine (e.g. script).

    Determined according to the *Code of Practice for Research Data*.
    """
    return _match_useragent(user_agent, 'machine.txt')


def is_robot_or_machine(user_agent):
    """Determine if a user agent is a machine/robot or human.

    Determined according to the *COUNTER Code of Practice*.
    """
    return is_robot(user_agent) or is_machine(user_agent)


__all__ = (
    '__version__',
    'is_machine',
    'is_robot',
    'is_robot_or_machine',
)
