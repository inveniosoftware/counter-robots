import datetime

current_year = datetime.datetime.now().year
version_file = 'version.py'

with open(version_file, 'r') as file:
    try:
        content = file.read()
        current_version = content.split('__version__ = ')[1][1:-1]
    except FileNotFoundError:
        current_version = '2018.6'

major, minor = map(int, current_version.split('.'))
new_version = f'{major}.{minor + 1}\n'

with open(version_file, 'w') as file:
    file.write(f"""# -*- coding: utf-8 -*-
#
# This file is part of COUNTER-Robots.
# Copyright (C) {current_year} CERN.
#
# COUNTER-Robots is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

\"\"\"Version information for COUNTER-Robots.

This file is imported by ``counter_robots.__init__``,
and parsed by ``setup.py``.
\"\"\"

from __future__ import absolute_import, print_function

__version__ = '{new_version}'
""")

print(new_version)
