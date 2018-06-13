# -*- coding: utf-8 -*-
#
# This file is part of COUNTER-Robots.
# Copyright (C) 2018 CERN.
#
# COUNTER-Robots is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test counter robots."""

import pytest

from counter_robots import _get_resource_content


def test_version():
    """Test version string."""
    from counter_robots import __version__
    assert __version__


def test_get_resource_content():
    """Test version string."""
    data = _get_resource_content('machine.txt')
    assert data
