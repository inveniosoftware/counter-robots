# -*- coding: utf-8 -*-
#
# This file is part of COUNTER-Robots.
# Copyright (C) 2018 CERN.
#
# COUNTER-Robots is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test counter robots."""

import pytest

from counter_robots import is_machine, is_robot, is_robot_or_machine


def test_version():
    """Test version string."""
    from counter_robots import __version__
    assert __version__


def test_is_robot():
    machine_ua = 'Wget/1.14 (linux-gnu)'
    robot_ua = 'AdsBot-Google (+http://www.google.com/adsbot.html)'
    assert is_robot(machine_ua) is not True
    assert is_robot(robot_ua) is True


def test_is_machine():
    machine_ua = 'Wget/1.14 (linux-gnu)'
    robot_ua = 'AdsBot-Google (+http://www.google.com/adsbot.html)'
    assert is_machine(machine_ua) is True
    assert is_machine(robot_ua) is not True


def test_is_robot_or_machine():
    machine_ua = 'Wget/1.14 (linux-gnu)'
    robot_ua = 'AdsBot-Google (+http://www.google.com/adsbot.html)'
    assert is_robot_or_machine(machine_ua) is True
    assert is_robot_or_machine(robot_ua) is True
