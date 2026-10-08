#!/usr/bin/env python3
"""Shared, fail-closed SEO robots checks for source and final HTTP responses.

Unknown/unsupported header directives are rejected by this project's approved
indexing policy; this is not a general-purpose robots standard interpreter.
"""
from __future__ import annotations

import re
import sys
from email.message import Message
from html.parser import HTMLParser
from typing import Sequence

PUBLIC_ROBOTS = "index, follow, max-image-preview:large"
PRIVATE_ROBOTS = "noindex, follow"
ROBOT_NAMES = frozenset({"robots", "googlebot", "googlebot-news"})
DIRECTIVE_PARAMETERS = frozenset({
    "max-image-preview", "max-snippet", "max-video-preview", "unavailable_after",
})


class RobotsMetaParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.entries: list[tuple[list[str | None], list[str | None]]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "meta":
            return
        names = [value for key, value in attrs if key == "name"]
        if any((value or "").strip().casefold() in ROBOT_NAMES for value in names):
            contents = [value for key, value in attrs if key == "content"]
            self.entries.append((names, contents))


def check_html_robots(html: str, *, indexable: bool) -> list[str]:
    """Return violations of the 18-route robots-meta contract."""
    parser = RobotsMetaParser()
    try:
        parser.feed(html)
        parser.close()
    except Exception as error:  # Defensive: malformed/invalid inputs must not pass.
        return [f"robots HTML could not be parsed: {error}"]
    violations: list[str] = []
    general = 0
    expected = PUBLIC_ROBOTS if indexable else PRIVATE_ROBOTS
    for names, contents in parser.entries:
        normalized = [(name or "").strip().casefold() for name in names]
        if len(names) != 1 or len(contents) != 1 or contents[0] is None:
            violations.append(f"robots meta has missing/duplicate name or content attributes: {normalized!r}")
        if "robots" in normalized:
            general += 1
            if len(names) == 1 and len(contents) == 1 and (contents[0] or "").strip() != expected:
                violations.append(f"robots meta policy mismatch: found {(contents[0] or '').strip()!r}, expected {expected!r}")
        if any(name in {"googlebot", "googlebot-news"} for name in normalized):
            violations.append(f"unapproved crawler-specific robots meta: {normalized!r}")
    if general != 1:
        violations.append(f"expected exactly one general robots meta, found {general}")
    return violations


def get_x_robots_tags(headers: Message | None) -> list[str] | None:
    """Preserve repeated HTTP header fields; None signals unavailable response."""
    return list(headers.get_all("X-Robots-Tag", [])) if headers is not None else None


def check_x_robots_headers(values: Sequence[str] | None, *, indexable: bool) -> list[str]:
    """Check all X-Robots-Tag lines, including comma groups and scoped rules.

    A crawler prefix applies to the comma-separated rules following it until a
    new crawler prefix. News-only directives are reported as *news scoped*, not
    as global Google web-search indexing rules.
    """
    if values is None:
        return ["X-Robots-Tag response headers unavailable (HTTP verification incomplete)"]
    violations: list[str] = []
    allowed = {"index", "follow", "all", "max-image-preview:large"} if indexable else {"noindex", "follow"}
    for header_number, raw in enumerate(values, start=1):
        if not isinstance(raw, str) or not raw.strip():
            violations.append(f"X-Robots-Tag #{header_number}: empty/invalid header")
            continue
        agent: str | None = None
        for raw_part in raw.split(","):
            part = raw_part.strip().casefold()
            if not part:
                violations.append(f"X-Robots-Tag #{header_number}: empty directive")
                continue
            prefix = re.match(r"^([a-z][a-z0-9_-]*)\s*:\s*(.*)$", part)
            if prefix and prefix.group(1) not in DIRECTIVE_PARAMETERS:
                agent = prefix.group(1)
                part = prefix.group(2).strip()
            if not part:
                violations.append(f"X-Robots-Tag #{header_number}: missing directive after crawler prefix")
                continue
            part = re.sub(r"\s*:\s*", ":", part)
            scope = f"{agent} scoped" if agent else "all crawlers"
            if agent is not None:
                violations.append(f"X-Robots-Tag #{header_number}: unapproved {scope} directive {part!r}")
            elif part not in allowed:
                violations.append(f"X-Robots-Tag #{header_number}: {scope} directive {part!r} conflicts with approved {'public' if indexable else 'privacy'} policy")
    return violations


def audit_robots(html: str, *, indexable: bool, headers: Sequence[str] | None = ()) -> list[str]:
    return check_html_robots(html, indexable=indexable) + check_x_robots_headers(headers, indexable=indexable)


def self_test() -> int:
    public = '<meta name="robots" content="index, follow, max-image-preview:large">'
    private = '<meta name="robots" content="noindex, follow">'
    samples: list[tuple[str, str, bool, Sequence[str] | None, bool]] = [
        ("public approved", public, True, [], True),
        ("privacy approved", private, False, [], True),
        ("ordinary meta", public + '<meta name="description" content="Hi"><meta name="viewport" content="width=device-width"><meta property="og:title" content="ok">', True, [], True),
        ("reordered attributes", "<META CONTENT='index, follow, max-image-preview:large' NAME='ROBOTS'>", True, [], True),
        ("padded name", '<META NAME = " robots " CONTENT = "index, follow, max-image-preview:large">', True, [], True),
        ("privacy matching header", private, False, ["noindex", "follow"], True),
        ("public positive header", public, True, ["index, follow, max-image-preview:large"], True),
        ("missing", "<html><head></head></html>", True, [], False),
        ("public noindex", '<meta name="robots" content="noindex">', True, [], False),
        ("public nofollow", '<meta name="robots" content="nofollow">', True, [], False),
        ("duplicate", public + public, True, [], False),
        ("conflict", public + private, True, [], False),
        ("googlebot none", public + '<meta name="googlebot" content="none">', True, [], False),
        ("googlebot noindex", public + '<meta name="googlebot" content="noindex">', True, [], False),
        ("googlebot news", public + '<meta name="googlebot-news" content="noindex">', True, [], False),
        ("news none", public + '<meta name="googlebot-news" content="none">', True, [], False),
        ("case and quotes", public + "<META CONTENT='NONE' NAME='GOOGLEBOT'>", True, [], False),
        ("reordered crawler", public + '<meta content="none" name="googlebot-news">', True, [], False),
        ("duplicate name", '<meta name="robots" name="description" content="index, follow, max-image-preview:large">', True, [], False),
        ("duplicate content", '<meta name="robots" content="index, follow, max-image-preview:large" content="noindex">', True, [], False),
        ("privacy misclassified", private, True, [], False),
        ("public header noindex", public, True, ["noindex"], False),
        ("public header nofollow", public, True, ["nofollow"], False),
        ("public header none", public, True, ["none"], False),
        ("googlebot header", public, True, ["googlebot: noindex"], False),
        ("googlebot news header", public, True, ["googlebot-news: noindex"], False),
        ("multiple same-name headers", public, True, ["index", "noindex"], False),
        ("multiple directives", public, True, ["index, nofollow"], False),
        ("scoped multi", public, True, ["googlebot: index, nofollow"], False),
        ("scoped followed by different scoped", public, True, ["otherbot: noindex, googlebot: follow"], False),
        ("privacy conflict", private, False, ["noindex", "nofollow"], False),
        ("privacy none", private, False, ["none"], False),
        ("unavailable response", public, True, None, False),
        ("empty header", public, True, [""], False),
        ("unknown directive", public, True, ["unavailable_after: 25 Jun 2010 15:00:00 PST"], False),
        ("restrict thumbnail", public, True, ["max-image-preview:standard"], False),
    ]
    passed = 0
    for name, html, indexable, headers, expected in samples:
        errors = audit_robots(html, indexable=indexable, headers=headers)
        if (not errors) == expected:
            passed += 1
        else:
            print(f"FAIL: {name}: {errors}")
    duplicated = Message()
    duplicated.add_header("X-Robots-Tag", "index")
    duplicated.add_header("X-Robots-Tag", "noindex")
    if get_x_robots_tags(duplicated) == ["index", "noindex"] and check_x_robots_headers(get_x_robots_tags(duplicated), indexable=True):
        passed += 1
    else:
        print("FAIL: repeated HTTPMessage headers")
    total = len(samples) + 1
    print(f"Robots guard self-test: {passed}/{total} PASS, {total-passed} FAIL")
    return 0 if passed == total else 1


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        sys.exit(self_test())
    print("Usage: python3 scripts/seo_robots_guard_v1.py --self-test", file=sys.stderr)
    sys.exit(2)
