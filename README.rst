..
    This file is part of COUNTER-Robots.
    Copyright (C) 2018 CERN.

    COUNTER-Robots is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.

================
 COUNTER-Robots
================

.. image:: https://img.shields.io/github/license/inveniosoftware/counter-robots.svg
        :target: https://github.com/inveniosoftware/counter-robots/blob/master/LICENSE

.. image:: https://img.shields.io/travis/inveniosoftware/counter-robots.svg
        :target: https://travis-ci.org/inveniosoftware/counter-robots

.. image:: https://img.shields.io/coveralls/inveniosoftware/counter-robots.svg
        :target: https://coveralls.io/r/inveniosoftware/counter-robots

.. image:: https://img.shields.io/pypi/v/counter-robots.svg
        :target: https://pypi.org/pypi/counter-robots


Library for COUNTER-compliant detection of machines and robots.

The purpose behind COUNTER is to enable comparable usage statistics by only
reporting genuine user-driven usage for repositories. The purpose behind Code
of Practice for Research Data is to split genuine COUNTER user-driven usage
into human- and machine-based access.

This Python library implements a tiny API to check if a given user agent
string from a browser is considered a robot/crawler/spider or a machine
according to the `Code of Practice for Research Data
<https://doi.org/10.7287/peerj.preprints.26505v1>`_ [1]  as well as the
`COUNTER Code of Practice
<https://www.projectcounter.org/code-of-practice-five-sections/abstract/>`_.

The library depends on official lists published by both projects. You can see
the lists on:

- `Making Data Count
  <https://github.com/CDLUC3/Make-Data-Count/tree/master/user-agents>`_
- `COUNTER <https://github.com/atmire/COUNTER-Robots/>`_
