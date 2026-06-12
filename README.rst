..
    SPDX-FileCopyrightText: 2018 CERN.
    SPDX-License-Identifier: MIT

================
 COUNTER-Robots
================

.. image:: https://img.shields.io/github/license/inveniosoftware/counter-robots.svg
        :target: https://github.com/inveniosoftware/counter-robots/blob/master/LICENSE

.. image:: https://github.com/inveniosoftware/counter-robots/workflows/CI/badge.svg
        :target: https://github.com/inveniosoftware/counter-robots/actions

.. image:: https://img.shields.io/coveralls/inveniosoftware/counter-robots.svg
        :target: https://coveralls.io/r/inveniosoftware/counter-robots

.. image:: https://img.shields.io/pypi/v/counter-robots.svg
        :target: https://pypi.org/pypi/counter-robots


Library for COUNTER-compliant detection of machines and robots.

The purpose behind COUNTER is to enable comparable usage statistics by only
reporting genuine user-driven usage for repositories. The purpose behind Code
of Practice for Research Data is to split genuine COUNTER user-driven usage
into human- and machine-based access.

This Python library checks whether a given user agent is a robot/crawler/spider
or a machine (script, library, tool), following the `Code of Practice for
Research Data <https://doi.org/10.7287/peerj.preprints.26505v1>`_ and the
`COUNTER Code of Practice
<https://www.projectcounter.org/code-of-practice-five-sections/abstract/>`_. It
has a module-level API for the generic COUNTER baseline and a composable
``Classifier`` you can extend with your own lists and with datacenter/hosting
network detection.


Installation
============

.. code-block:: console

    $ pip install counter-robots

The optional ``asn`` extra adds IP-to-ASN resolution (via ``maxminddb``) for
datacenter detection:

.. code-block:: console

    $ pip install counter-robots[asn]


Usage
=====

The module-level functions use a default classifier built from the generic
COUNTER baseline (the Atmire robot list and the Make-Data-Count machine list):

.. code-block:: python

    from counter_robots import is_robot, is_machine, is_robot_or_machine, is_browser

    is_robot("Googlebot/2.1 (+http://www.google.com/bot.html)")  # True
    is_machine("Wget/1.14 (linux-gnu)")                          # True
    is_robot_or_machine("python-requests/2.31")                  # True
    is_browser(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
    )                                                            # True

The two lists overlap (``wget``, ``curl``, ``python``, ...). A user agent matched
by both is a machine, not a robot, so it is counted and reported separately rather
than excluded with the robots.

Composable classifier
----------------------

Build a classifier from presets with ``ClassifierBuilder``. A preset is a
callable that adds sources to the builder, applied with ``use``:

.. code-block:: python

    from counter_robots import ClassifierBuilder, counter_preset, extended_preset

    classifier = (
        ClassifierBuilder().use(counter_preset).use(extended_preset).build()
    )
    classifier.is_robot("LinkedInBot/1.0")         # True
    classifier.is_machine("python-requests/2.31")  # True

The library ships two presets:

- ``counter_preset``: the generic COUNTER baseline (the Atmire robot list and the
  Make-Data-Count machine list), matched case-sensitively.
- ``extended_preset``: adds the maintained `crawler-user-agents
  <https://github.com/monperrus/crawler-user-agents>`_ dataset (an install
  dependency), split by its tags into robots and machines; a curated
  ``machine_extra`` list of non-browser tools and CLIs the dataset does not cover;
  and a datacenter ASN list. It catches the modern crawlers (CamelCase bots, AI
  crawlers, link-preview bots) that the frozen, case-sensitive baseline misses.

The module-level ``is_robot`` / ``is_machine`` / ``is_robot_or_machine`` /
``is_browser`` remain as a backwards-compatible default built from
``counter_preset``.

Adding your own lists
---------------------

A deployment can add instance-specific patterns through the builder. User-agent
patterns can be matched case-insensitively; ASN lists are plain numbers:

.. code-block:: python

    from counter_robots import (
        ClassifierBuilder,
        counter_preset,
        file_asns,
        file_patterns,
    )

    classifier = (
        ClassifierBuilder()
        .use(counter_preset)
        .robots(file_patterns("/etc/myrepo/robots.txt"), ignore_case=True)
        .machines(file_patterns("/etc/myrepo/machines.txt"), ignore_case=True)
        .datacenter_asns(file_asns("/etc/myrepo/datacenter_asns.txt"))
        .build()
    )

Datacenter detection
--------------------

A request that claims to be a browser but originates from a datacenter/hosting
network is likely automation faking a browser. ``is_datacenter`` classifies an ASN
number; ``is_datacenter_ip`` resolves an IP first, using a resolver you supply.
``maxminddb_resolver`` (the ``asn`` extra) builds one over a GeoLite2-ASN database,
which you provide; no geo database is shipped with this package:

.. code-block:: python

    from counter_robots import (
        ClassifierBuilder,
        counter_preset,
        extended_preset,
        maxminddb_resolver,
    )

    classifier = (
        ClassifierBuilder()
        .use(counter_preset)
        .use(extended_preset)
        .asn_resolver(maxminddb_resolver("/path/to/GeoLite2-ASN.mmdb"))
        .build()
    )
    classifier.is_datacenter(16509)             # True (AWS)
    classifier.is_datacenter_ip("203.0.113.7")  # resolves the IP, then checks

Without an ASN resolver, ``is_datacenter_ip`` returns ``False``.


Data sources
============

The lists live under ``counter_robots/data`` and are refreshed by the scripts in
``scripts/``:

- ``robot.txt`` — the `COUNTER <https://github.com/atmire/COUNTER-Robots/>`_ robot
  list; synced by ``scripts/update-lists.py``.
- ``machine.txt`` — the `Make Data Count
  <https://github.com/CDLUC3/Make-Data-Count/tree/master/user-agents>`_ machine
  list; synced by ``scripts/update-lists.py``.
- ``machine_extra.txt`` — a curated list of non-browser tools and CLIs not covered
  by the above or by crawler-user-agents; matched case-insensitively.
- ``datacenter_asn.txt`` — datacenter/hosting ASNs, the union of `bad-asn-list
  <https://github.com/brianhama/bad-asn-list>`_ and `PeeringDB
  <https://www.peeringdb.com>`_ networks of type ``Content``; generated by
  ``scripts/update-asn-list.py``.
- ``datacenter_asn_allow.txt`` — ASNs never treated as datacenter even when a
  source lists them (e.g. Apple iCloud Private Relay).

``extended_preset`` additionally reads the crawler-user-agents dataset from the
installed dependency, so it updates with the package.
