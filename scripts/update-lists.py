# -*- coding: utf-8 -*-
#
# This file is part of COUNTER-Robots.
# Copyright (C) 2018 CERN.
#
# COUNTER-Robots is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Small script to update the list of robots and machines."""

from __future__ import absolute_import, print_function

import requests

from counter_robots import _get_resource_path
from counter_robots.config import config


def update_lists():
    """Update the files containing the list of robots and machines."""
    update_file(config['ROBOTS_URL'], config['ROBOTS_FILE'])
    update_file(config['MACHINE_URL'], config['ROBOTS_FILE'])


def update_file(url, filename):
    """Update the content of a single file."""
    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception('GET {} failed.'.format(url))
    lines = resp.text.splitlines()
    lines = [s for s in lines if not s.startswith('#')]
    with open(_get_resource_path(filename), "w+") as f:
        for line in lines:
            f.write(line+'\n')
