..
    SPDX-FileCopyrightText: 2018-2025 CERN.
    SPDX-FileCopyrightText: 2025 Graz University of Technology.
    SPDX-License-Identifier: MIT

Changes
=======

Version 2026.6 (unreleased)

- fix: keep consumer ISPs and universities out of the datacenter list. open-bot-list
  files some ASNs under both a datacenter and the isp/education category; those are
  now subtracted from its contribution. A handful of bad-asn-list false positives that
  PeeringDB confirms are eyeball or academic networks are added to the allow list.

- feat: ``extended_preset`` also flags the AI crawlers from the ai-robots-txt list,
  refreshed into ``ai_robots.txt`` by ``scripts/update-lists.py`` and matched
  case-insensitively as robots.

- fix: machine takes precedence over robot. The COUNTER robot and Make-Data-Count
  machine lists overlap heavily (wget, curl, python, ...); a user agent matched by
  both is now classified as a machine, not a robot, so machine access is counted
  and reported separately instead of being excluded with the robots (issue #15).

- refactor: composable, class-based API. ``Classifier`` (built by
  ``ClassifierBuilder``) exposes ``is_robot`` / ``is_machine`` /
  ``is_robot_or_machine``. Lists are added as presets, callables that add sources
  to the builder and are applied with ``builder.use(...)``; ``counter_preset`` is
  the generic COUNTER baseline. The module-level ``is_robot`` / ``is_machine`` /
  ``is_robot_or_machine`` remain as a backwards-compatible default classifier built
  from ``counter_preset``.

- feat: ``extended_preset`` adds detection from the maintained
  ``crawler-user-agents`` dataset (a new dependency), split by tag so HTTP
  libraries and browser-automation tools are machines and every other tag is a
  robot (case-sensitive, as that dataset intends), plus a curated
  ``machine_extra.txt`` of non-browser tools and CLIs it does not cover, matched
  case-insensitively.

- feat: datacenter/hosting ASN classification. ``is_datacenter(asn)`` classifies
  an ASN against a generated list (union of brianhama/bad-asn-list, PeeringDB
  ``Content`` networks, and O-X-L/open-bot-list hosting/cloud/cdn ASNs, refreshed by
  ``scripts/update-asn-list.py``) minus an allow
  list (Apple iCloud Private Relay). ``is_browser(ua)`` exposes a conservative
  browser-UA heuristic. ``is_datacenter_ip(ip)`` resolves IP to ASN through a
  resolver supplied to the builder; ``maxminddb_resolver(path)`` (the ``asn`` extra)
  builds one over a GeoLite2-ASN mmdb with an in-memory cache. The library reads no
  config and ships no geo database.

Version 2025.11 (released on 2025-11-04)

- chore(setup): update dependencies
- fix: pkg_resources DeprecationWarning

Version 2025.2 (released on 2025-02-13)

- User agents lists update.

Version 2018.6 (released on 2018-06-15)

- Initial public release.
