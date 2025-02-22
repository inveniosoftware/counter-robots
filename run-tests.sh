#!/usr/bin/env sh
# -*- coding: utf-8 -*-
#
# This file is part of COUNTER-Robots.
# Copyright (C) 2018-2025 CERN.
#
# COUNTER-Robots is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

# Quit on errors
set -o errexit

# Quit on unbound symbols
set -o nounset


python -m check_manifest
python -m sphinx.cmd.build -qnNW docs docs/_build/html
python -m pytest
python -m sphinx.cmd.build -qnNW -b doctest docs docs/_build/doctest
