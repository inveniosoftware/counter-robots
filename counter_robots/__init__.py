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

from .version import __version__


def _get_resource_content(filename):
    """Retrieve content from a file in this Python package."""
    return pkg_resources.resource_string(__name__, join('data', filename))


__all__ = ('__version__', )
