# SPDX-FileCopyrightText: 2018 CERN.
# SPDX-License-Identifier: MIT

"""Test counter robots."""

import pytest

from counter_robots import (
    ClassifierBuilder,
    counter_preset,
    extended_preset,
    file_patterns,
    is_browser,
    is_machine,
    is_robot,
    is_robot_or_machine,
)


def test_version():
    """Test version string."""
    from counter_robots import __version__

    assert __version__


def test_is_robot():
    # Wget is in both lists; machine wins, so it is not a robot (issue #15).
    machine_ua = "Wget/1.14 (linux-gnu)"
    robot_ua = "AdsBot-Google (+http://www.google.com/adsbot.html)"
    assert is_robot(machine_ua) is not True
    assert is_robot(robot_ua) is True


@pytest.mark.parametrize(
    "ua",
    [
        "Wget/1.14 (linux-gnu)",
        "curl/8.5.0",
        "python-requests/2.31.0",
        "urllib/3.10",
        "aria2/1.36.0",
        "PycURL/7.45.2",
    ],
)
def test_machine_takes_precedence_over_robot(ua):
    """User agents in both the robot and machine lists are machines (issue #15)."""
    assert is_machine(ua) is True
    assert is_robot(ua) is False
    assert is_robot_or_machine(ua) is True  # still non-human, just not a robot


def test_is_machine():
    machine_ua = "Wget/1.14 (linux-gnu)"
    robot_ua = "AdsBot-Google (+http://www.google.com/adsbot.html)"
    assert is_machine(machine_ua) is True
    assert is_machine(robot_ua) is not True


def test_is_robot_or_machine():
    machine_ua = "Wget/1.14 (linux-gnu)"
    robot_ua = "AdsBot-Google (+http://www.google.com/adsbot.html)"
    assert is_robot_or_machine(machine_ua) is True
    assert is_robot_or_machine(robot_ua) is True


def test_baseline_is_case_sensitive():
    """The COUNTER baseline matches case-sensitively, so CamelCase bots evade it."""
    assert is_robot("YisouSpider") is False


@pytest.mark.parametrize(
    "ua",
    [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0",
        # bare WebKit (older Safari) and Internet Explorer (Trident)
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko)",
        "Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko",
    ],
)
def test_is_browser_true(ua):
    assert is_browser(ua) is True


@pytest.mark.parametrize("ua", ["python-requests/2.31", "GDAL/3.12", ""])
def test_is_browser_false(ua):
    assert is_browser(ua) is False


@pytest.fixture
def extended_classifier():
    return ClassifierBuilder().use(counter_preset).use(extended_preset).build()


@pytest.mark.parametrize(
    "ua",
    [
        "YisouSpider",
        "LinkedInBot/1.0 (compatible; Mozilla/5.0)",
        "Googlebot/2.1 (+http://www.google.com/bot.html)",
        "Screaming Frog SEO Spider/23.2",
        "Google-NotebookLM",
    ],
)
def test_extended_preset_robots(extended_classifier, ua):
    """The extended preset catches crawlers the case-sensitive baseline misses."""
    assert extended_classifier.is_robot(ua) is True


@pytest.mark.parametrize(
    "ua",
    [
        "Crawlspace/1.0",
        "QuillBot/2.0",
        "Andibot",
        "bedrockbot/1.0",
    ],
)
def test_extended_preset_ai_crawlers(extended_classifier, ua):
    """ai-robots-txt AI crawlers, beyond what crawler-user-agents covers."""
    assert extended_classifier.is_robot(ua) is True


@pytest.mark.parametrize(
    "ua",
    [
        "python-requests/2.31",  # crawler-user-agents http-library
        "Python/3.10 aiohttp/3.10.5",
        "GDAL/3.12.1",  # curated tool list
        "siril/1.4",
    ],
)
def test_extended_preset_machines(extended_classifier, ua):
    """The extended preset tags HTTP libraries and research tools as machines."""
    assert extended_classifier.is_machine(ua) is True


def test_extended_preset_tools_case_insensitive(extended_classifier):
    """The curated tools list is matched case-insensitively."""
    assert extended_classifier.is_machine("gdal/3.12.1") is True


def test_extended_preset_keeps_browsers(extended_classifier):
    chrome = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
    )
    assert extended_classifier.is_robot(chrome) is False
    assert extended_classifier.is_machine(chrome) is False


def test_is_datacenter(extended_classifier):
    assert extended_classifier.is_datacenter(16509) is True  # AWS, generated list
    assert extended_classifier.is_datacenter(714) is False  # Apple, allow-listed
    assert extended_classifier.is_datacenter(3320) is False  # eyeball ISP, not listed
    assert extended_classifier.is_datacenter(None) is False


def test_is_datacenter_ip_with_resolver():
    asn_by_ip = {"1.1.1.1": 16509, "2.2.2.2": 714, "3.3.3.3": 3320}
    classifier = (
        ClassifierBuilder()
        .use(counter_preset)
        .use(extended_preset)
        .asn_resolver(lambda ip: asn_by_ip.get(ip))
        .build()
    )
    assert classifier.is_datacenter_ip("1.1.1.1") is True  # AWS
    assert classifier.is_datacenter_ip("2.2.2.2") is False  # Apple, allow-listed
    assert classifier.is_datacenter_ip("3.3.3.3") is False  # eyeball ISP
    assert classifier.is_datacenter_ip("9.9.9.9") is False  # unknown -> no ASN


def test_is_datacenter_ip_without_resolver(extended_classifier):
    """Without a resolver, ip-based datacenter detection is a no-op."""
    assert extended_classifier.is_datacenter_ip("1.1.1.1") is False


def test_external_file_via_builder(tmp_path):
    """A deployment can add its own list file through the builder."""
    f = tmp_path / "instance_robots.txt"
    f.write_text("# my instance\nMyCustomScraper\n")
    classifier = (
        ClassifierBuilder()
        .use(counter_preset)
        .robots(file_patterns(str(f)), ignore_case=True)
        .build()
    )
    assert classifier.is_robot("MyCustomScraper/1.0") is True
    assert classifier.is_robot("PostmanRuntime/7.30.0") is not True
