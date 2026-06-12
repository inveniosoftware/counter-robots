# SPDX-FileCopyrightText: 2018-2025 CERN.
# SPDX-FileCopyrightText: 2025 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Library for COUNTER-compliant detection of machines and robots.

The classifier is composed from one or more presets and used directly::

    from counter_robots import ClassifierBuilder, counter_preset, extended_preset

    classifier = ClassifierBuilder().use(counter_preset).use(extended_preset).build()
    classifier.is_robot(user_agent)

The module-level :func:`is_robot`, :func:`is_machine`, :func:`is_robot_or_machine`
and :func:`is_browser` keep working as before, backed by a default classifier built
from the generic COUNTER preset.
"""

import re
from functools import lru_cache
from importlib.resources import files

__version__ = "2026.6"

# User-agent tokens that mark a request as claiming to be an interactive browser.
_BROWSER_TOKENS = (
    "Chrome/",
    "Safari/",
    "Firefox/",
    "Gecko/",
    "Edg/",
    "OPR/",
    "AppleWebKit/",
    "Trident/",
    "Version/",
    "Presto/",
)

# Default size of the in-memory ip -> ASN cache. Bounds memory (each entry is an
# IP string and an int) while covering the working set of frequently-seen client
# IPs; override per resolver with the ``cache_size`` argument.
_ASN_CACHE_SIZE = 100_000


#
# Loading helpers
#


def patterns_from(text):
    """Read regex patterns from list text (drop blank lines and ``#`` comments)."""
    return [line for line in text.splitlines() if line and not line.startswith("#")]


def asns_from(text):
    """Read ASN numbers from list text (first token per line, ``#`` comments dropped)."""
    out = set()
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        token = line.split()[0]
        if token.isdigit():
            out.add(int(token))
    return out


def _read_package(filename):
    return (files(__package__) / "data" / filename).read_text()


def package_patterns(filename):
    """Read regex patterns from a file packaged under ``counter_robots/data``."""
    return patterns_from(_read_package(filename))


def package_asns(filename):
    """Read ASN numbers from a file packaged under ``counter_robots/data``."""
    return asns_from(_read_package(filename))


def file_patterns(path):
    """Read regex patterns from an external file."""
    with open(path, encoding="utf-8") as fp:
        return patterns_from(fp.read())


def file_asns(path):
    """Read ASN numbers from an external file."""
    with open(path, encoding="utf-8") as fp:
        return asns_from(fp.read())


def is_browser(user_agent):
    """Determine if a user agent claims to be an interactive web browser.

    It does not validate the browser, only whether the request presents itself as
    one, so it also matches automation faking a browser user agent. Unrecognised
    clients read as non-browsers.
    """
    # Require ``Mozilla/`` and an engine token together, so a bare engine token on
    # a non-browser client (e.g. a stray ``Version/1.0``) does not match.
    if not user_agent or "Mozilla/" not in user_agent:
        return False
    return any(token in user_agent for token in _BROWSER_TOKENS)


#
# Core
#


class _PatternSet:
    """Compiled matcher for one category, supporting mixed case sensitivity.

    Patterns can be added case-sensitively or case-insensitively, stored as at
    most two compiled regexes and OR-matched.
    """

    def __init__(self, cs_patterns, ci_patterns):
        self._cs = re.compile("|".join(cs_patterns)) if cs_patterns else None
        self._ci = (
            re.compile("|".join(ci_patterns), re.IGNORECASE) if ci_patterns else None
        )

    def matches(self, value):
        if not value:
            return False
        return bool(
            (self._cs and self._cs.search(value))
            or (self._ci and self._ci.search(value))
        )


class Classifier:
    """Immutable classifier of user agents and client networks.

    Build one with :class:`ClassifierBuilder`. ``is_datacenter_ip`` is only
    meaningful when an ASN resolver was supplied; otherwise it returns ``False``.
    """

    def __init__(
        self, robots, machines, datacenter_asns, allow_asns, asn_resolver=None
    ):
        """Initialize from compiled pattern sets and ASN sets (use the builder)."""
        self._robots = robots
        self._machines = machines
        self._datacenter_asns = datacenter_asns
        self._allow_asns = allow_asns
        self._asn_resolver = asn_resolver

    def is_robot(self, user_agent):
        """Determine if a user agent is a robot/crawler/spider.

        Machine takes precedence: the COUNTER robot and Make-Data-Count machine
        lists overlap (wget, curl, python, ...), but machine access is counted and
        reported separately while robots are excluded, so a user agent in both is
        a machine, not a robot.
        """
        return self._robots.matches(user_agent) and not self._machines.matches(
            user_agent
        )

    def is_machine(self, user_agent):
        """Determine if a user agent is a machine (script, library, tool)."""
        return self._machines.matches(user_agent)

    def is_robot_or_machine(self, user_agent):
        """Determine if a user agent is a robot or a machine."""
        return self.is_robot(user_agent) or self.is_machine(user_agent)

    def is_browser(self, user_agent):
        """Determine if a user agent claims to be an interactive web browser."""
        return is_browser(user_agent)

    def is_datacenter(self, asn):
        """Determine if an ASN is a datacenter/hosting network (and not allow-listed)."""
        if asn is None:
            return False
        asn = int(asn)
        return asn in self._datacenter_asns and asn not in self._allow_asns

    def is_datacenter_ip(self, ip):
        """Determine if an IP belongs to a datacenter/hosting network.

        Resolves the IP to an ASN with the configured resolver and applies
        :meth:`is_datacenter`. Returns ``False`` when no resolver was supplied.
        """
        if not ip or self._asn_resolver is None:
            return False
        return self.is_datacenter(self._asn_resolver(ip))


class ClassifierBuilder:
    """Fluent builder for a :class:`Classifier`.

    Every method returns ``self``; :meth:`build` freezes an immutable classifier.
    A preset is any callable taking the builder, applied with :meth:`use`.
    """

    def __init__(self):
        """Initialize an empty builder."""
        self._cs_robots, self._ci_robots = [], []
        self._cs_machines, self._ci_machines = [], []
        self._datacenter_asns, self._allow_asns = set(), set()
        self._asn_resolver = None

    def robots(self, patterns, ignore_case=False):
        """Add robot patterns (case-sensitive unless ``ignore_case``)."""
        (self._ci_robots if ignore_case else self._cs_robots).extend(patterns)
        return self

    def machines(self, patterns, ignore_case=False):
        """Add machine patterns (case-sensitive unless ``ignore_case``)."""
        (self._ci_machines if ignore_case else self._cs_machines).extend(patterns)
        return self

    def datacenter_asns(self, asns):
        """Add ASN numbers treated as datacenter/hosting networks."""
        self._datacenter_asns.update(asns)
        return self

    def allow_asns(self, asns):
        """Add ASN numbers exempt from datacenter classification."""
        self._allow_asns.update(asns)
        return self

    def asn_resolver(self, resolver):
        """Set the ``ip -> ASN`` resolver used by ``is_datacenter_ip``."""
        self._asn_resolver = resolver
        return self

    def use(self, preset):
        """Apply a preset, any callable that adds sources to this builder."""
        preset(self)
        return self

    def build(self):
        """Freeze and return the :class:`Classifier`."""
        return Classifier(
            _PatternSet(self._cs_robots, self._ci_robots),
            _PatternSet(self._cs_machines, self._ci_machines),
            frozenset(self._datacenter_asns),
            frozenset(self._allow_asns),
            self._asn_resolver,
        )


#
# Presets
#

# crawler-user-agents tags that denote a machine (script/library) rather than a
# crawler; every other tag is treated as a robot.
_MACHINE_TAGS = frozenset({"http-library", "browser-automation"})


def counter_preset(builder):
    """Generic COUNTER baseline: atmire robots and Make-Data-Count machines."""
    builder.robots(package_patterns("robot.txt"))
    builder.machines(package_patterns("machine.txt"))


def extended_preset(builder):
    """Extended detection beyond the COUNTER baseline.

    Adds the crawler-user-agents patterns split by tag (HTTP libraries and
    browser-automation tools as machines, every other tag as robots), matched
    case-sensitively as that dataset intends; the ai-robots-txt AI-crawler names as
    robots, matched case-insensitively; a curated list of non-browser tools and CLIs
    the datasets do not cover, also case-insensitive; and the packaged datacenter ASN
    list with its allow list.
    """
    import crawleruseragents

    robots, machines = [], []
    for entry in crawleruseragents.CRAWLER_USER_AGENTS_DATA:
        bucket = machines if _MACHINE_TAGS.intersection(entry["tags"]) else robots
        bucket.append(entry["pattern"])
    builder.robots(robots)
    builder.robots(package_patterns("ai_robots.txt"), ignore_case=True)
    builder.machines(machines)
    builder.machines(package_patterns("machine_extra.txt"), ignore_case=True)
    builder.datacenter_asns(package_asns("datacenter_asn.txt"))
    builder.allow_asns(package_asns("datacenter_asn_allow.txt"))


def maxminddb_resolver(path, cache_size=_ASN_CACHE_SIZE):
    """Build an ``ip -> ASN`` resolver backed by a GeoLite2-ASN mmdb, cached.

    Requires the ``asn`` extra (``maxminddb``). The mmdb is supplied by the
    caller; it is never shipped with this package.
    """
    import maxminddb

    reader = maxminddb.open_database(path)

    @lru_cache(maxsize=cache_size)
    def resolve(ip):
        record = reader.get(ip) or {}
        return record.get("autonomous_system_number")

    return resolve


#
# Default classifier and backwards-compatible module-level API
#


def default_classifier():
    """Build the default classifier (the generic COUNTER baseline)."""
    return ClassifierBuilder().use(counter_preset).build()


_default = None


def _get_default():
    global _default
    if _default is None:
        _default = default_classifier()
    return _default


def is_robot(user_agent):
    """Determine if a user agent is a robot/crawler/spider (default classifier)."""
    return _get_default().is_robot(user_agent)


def is_machine(user_agent):
    """Determine if a user agent is a machine (default classifier)."""
    return _get_default().is_machine(user_agent)


def is_robot_or_machine(user_agent):
    """Determine if a user agent is a robot or a machine (default classifier)."""
    return _get_default().is_robot_or_machine(user_agent)


__all__ = (
    "__version__",
    "Classifier",
    "ClassifierBuilder",
    "counter_preset",
    "extended_preset",
    "maxminddb_resolver",
    "default_classifier",
    "package_patterns",
    "package_asns",
    "file_patterns",
    "file_asns",
    "patterns_from",
    "asns_from",
    "is_browser",
    "is_machine",
    "is_robot",
    "is_robot_or_machine",
)
