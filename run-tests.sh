#!/usr/bin/env sh
# -*- coding: utf-8 -*-
#
# This file is part of COUNTER-Robots.
# Copyright (C) 2018 CERN.
#
# COUNTER-Robots is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

# Quit on errors
set -o errexit

# Quit on unbound symbols
set -o nounset

pydocstyle counter_robots tests docs
isort counter_robots tests --check-only --diff
check-manifest --ignore ".*-requirements.txt"
sphinx-build -qnNW docs docs/_build/html
python setup.py test
