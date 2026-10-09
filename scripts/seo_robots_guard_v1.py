#!/usr/bin/env python3
"""Shared, fail-closed SEO robots checks for source and final HTTP responses.

Unknown/unsupported header directives are rejected by this project's approved
indexing policy; this is not a general-purpose robots standard interpreter.
"""
from __future__ import annotations

import re
import sys
from email.message import Message
from io import BytesIO
from html.parser import HTMLParser
from typing import Sequence

PUBLIC_ROBOTS = "index, follow, max-image-preview:large"
PRIVATE_ROBOTS = "noindex, follow"
ROBOT_NAMES = frozenset({"robots", "googlebot", "googlebot-news"})
DIRECTIVE_PARAMETERS = frozenset({
    "max-image-preview", "max-snippet", "max-video-preview", "unavailable_after",
})


def normalized_policy(content: str) -> tuple[str, ...]:
    """Normalize semantically equivalent approved directives, never extra rules."""
    return tuple(
        re.sub(r"\s*:\s*", ":", part.strip().casefold())
        for part in content.split(",")
    )


def read_complete_response(response, *, limit: int) -> bytes:
    """Read at most limit+1 bytes, refuse oversized/truncated HTTP bodies."""
    if limit < 1:
        raise ValueError("invalid HTTP body limit")
    sizes = response.headers.get_all("Content-Length", [])
    if len(sizes) > 1:
        raise ValueError("duplicate Content-Length headers; complete body cannot be verified")
    declared = None
    if sizes:
        raw_size = sizes[0].strip()
        if not raw_size.isdecimal():
            raise ValueError(f"invalid Content-Length: {raw_size!r}")
        declared = int(raw_size)
        if declared > limit:
            raise ValueError(f"HTTP body exceeds {limit}-byte audit limit (Content-Length={declared})")
    data = response.read(limit + 1)
    if len(data) > limit:
        raise ValueError(f"HTTP body exceeds {limit}-byte audit limit")
    if declared is not None and len(data) != declared:
        raise ValueError(f"incomplete HTTP body: read {len(data)} bytes of declared {declared}")
    return data


class CanonicalLinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.found = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "link" and any(
            "canonical" in (value or "").strip().casefold().split()
            for key, value in attrs if key == "rel"
        ):
            self.found = True


def has_canonical_link(html: str) -> bool:
    parser = CanonicalLinkParser()
    parser.feed(html)
    parser.close()
    return parser.found


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
    required_directives = normalized_policy(expected)
    for names, contents in parser.entries:
        normalized = [(name or "").strip().casefold() for name in names]
        if len(names) != 1 or len(contents) != 1 or contents[0] is None:
            violations.append(f"robots meta has missing/duplicate name or content attributes: {normalized!r}")
        if "robots" in normalized:
            general += 1
            if len(names) == 1 and len(contents) == 1:
                actual = normalized_policy(contents[0] or "")
                if len(actual) != len(required_directives) or set(actual) != set(required_directives):
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
        ("public uppercase", '<meta name="robots" content="INDEX, FOLLOW, MAX-IMAGE-PREVIEW:LARGE">', True, [], True),
        ("public reordered", '<meta name="robots" content="follow, max-image-preview:large, index">', True, [], True),
        ("public mixed case reordered", '<meta name="robots" content="FOLLOW, index, MAX-IMAGE-PREVIEW:LaRgE">', True, [], True),
        ("privacy uppercase", '<meta name="robots" content="NOINDEX, FOLLOW">', False, [], True),
        ("privacy reordered", '<meta name="robots" content="FOLLOW, NoIndex">', False, [], True),
        ("colon padded", '<meta name="robots" content=" index , follow , max-image-preview : large ">', True, [], True),
        ("uppercase spaced", '<meta name="robots" content=" MAX-IMAGE-PREVIEW : LARGE , INDEX , FOLLOW ">', True, [], True),
        ("directive repeated", '<meta name="robots" content="index, follow, follow, max-image-preview:large">', True, [], False),
        ("directive extra", '<meta name="robots" content="index, follow, max-image-preview:large, noindex">', True, [], False),
        ("directive missing", '<meta name="robots" content="index, follow">', True, [], False),
        ("empty directive", '<meta name="robots" content="index,, follow, max-image-preview:large">', True, [], False),
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
    class FakeResponse(BytesIO):
        def __init__(self, data: bytes, content_lengths: tuple[str, ...] = ()) -> None:
            super().__init__(data)
            self.headers = Message()
            for length in content_lengths:
                self.headers.add_header("Content-Length", length)

    http_reads = [
        ("complete with length", b"abcd", ("4",), 4, True),
        ("complete without length", b"abcd", (), 4, True),
        ("shorter than header", b"abc", ("4",), 4, False),
        ("declared oversized", b"abcde", ("5",), 4, False),
        ("undeclared oversized", b"abcde", (), 4, False),
        ("bad length", b"abcd", ("abc",), 4, False),
        ("negative length", b"abcd", ("-1",), 4, False),
        ("duplicate lengths", b"abcd", ("4", "4"), 4, False),
        ("exact declared under limit", b"abc", ("3",), 4, True),
    ]
    for name, data, lengths, limit, should_pass in http_reads:
        try:
            result = read_complete_response(FakeResponse(data, lengths), limit=limit)
            actual_pass = result == data
        except ValueError:
            actual_pass = False
        if actual_pass == should_pass:
            passed += 1
        else:
            print(f"FAIL HTTP read: {name}: actual_pass={actual_pass}")

    canonical_cases = [
        ('<link rel="canonical" href="https://alinahorb.com/">', True),
        ('<LINK HREF="https://alinahorb.com/" REL=canonical>', True),
        ("<link rel='alternate canonical' href='https://alinahorb.com/'>", True),
        ('<link rel="alternate" href="https://alinahorb.com/">', False),
        ('<meta name="robots" content="noindex, follow">', False),
    ]
    for html, should_find in canonical_cases:
        if has_canonical_link(html) == should_find:
            passed += 1
        else:
            print(f"FAIL canonical parser: {html!r}")

    total = len(samples) + 1 + len(http_reads) + len(canonical_cases)
    print(f"Robots guard self-test: {passed}/{total} PASS, {total-passed} FAIL")
    return 0 if passed == total else 1


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        sys.exit(self_test())
    print("Usage: python3 scripts/seo_robots_guard_v1.py --self-test", file=sys.stderr)
    sys.exit(2)
