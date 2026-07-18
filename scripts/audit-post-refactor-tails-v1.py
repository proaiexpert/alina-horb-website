#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict, deque
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "qa" / "post-refactor-tails"
STRICT = os.environ.get("AUDIT_STRICT") == "1"
LIVE_ORIGIN = "https://alinahorb.com"

ROUTES = [
    "/", "/ru/", "/about/", "/ru/about/", "/consultations/", "/ru/consultations/",
    "/notes/", "/ru/notes/", "/notes/first-consultation/", "/ru/notes/first-consultation/",
    "/notes/how-to-start-the-conversation/", "/ru/notes/how-to-start-the-conversation/",
    "/notes/when-coping-stops-helping/", "/ru/notes/when-coping-stops-helping/",
    "/notes/stress-relocation-and-lost-support/", "/ru/notes/stress-relocation-and-lost-support/",
    "/privacy/", "/ru/privacy/",
]

STALE_ASSET_CANDIDATES = [
    "assets/js/site.global-chrome.v1.js",
    "assets/js/site.chrome.v3.js",
    "assets/js/site.notes-images.v3-1.js",
    "assets/css/site.footer.v3-2.css",
    "assets/css/site.chrome.v3.css",
    "assets/images/notes/alina-horb-notes-editorial-v2.webp",
    "assets/images/portrait/alina-horb-portrait-hero-v3.jpg",
    "assets/images/portrait/alina-horb-portrait-v4-desktop.jpg",
    "assets/images/portrait/alina-horb-portrait-v4-desktop.webp",
    "assets/images/portrait/alina-horb-portrait-v4-mobile.jpg",
    "assets/images/portrait/alina-horb-portrait-v4-mobile.webp",
]

FORBIDDEN_PRODUCTION_PATTERNS = {
    "localhost": re.compile(r"localhost", re.I),
    "loopback": re.compile(r"127\.0\.0\.1"),
    "lorem": re.compile(r"lorem\s+ipsum", re.I),
    "todo": re.compile(r"\bTODO\b", re.I),
    "fixme": re.compile(r"\bFIXME\b", re.I),
    "old Financial Stream email": re.compile(r"financialstreamllc@gmail\.com", re.I),
    "old Alina Gmail": re.compile(r"alinahorb1991@gmail\.com", re.I),
    "example domain": re.compile(r"https?://(?:www\.)?example\.com", re.I),
}

ROUTE_FILES = {
    route: ROOT / ("index.html" if route == "/" else route.strip("/") + "/index.html")
    for route in ROUTES
}


def git_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, text=True, capture_output=True, check=True
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


TRACKED = git_files()
TRACKED_SET = set(TRACKED)


def add_issue(bucket: list[dict], category: str, message: str, path: str | None = None) -> None:
    item = {"category": category, "message": message}
    if path:
        item["path"] = path
    bucket.append(item)


def route_for_file(path: Path) -> str | None:
    try:
        relative = path.relative_to(ROOT).as_posix()
    except ValueError:
        return None
    for route, candidate in ROUTE_FILES.items():
        if candidate.relative_to(ROOT).as_posix() == relative:
            return route
    return None


def local_file_for_url(url: str, base_route: str) -> tuple[Path | None, str | None, str | None]:
    absolute = urllib.parse.urljoin(f"{LIVE_ORIGIN}{base_route}", url)
    parsed = urllib.parse.urlparse(absolute)
    if parsed.scheme not in {"http", "https", ""}:
        return None, None, None
    if parsed.netloc and parsed.netloc not in {"alinahorb.com", "www.alinahorb.com"}:
        return None, None, None
    path = urllib.parse.unquote(parsed.path)
    if path == "/":
        target = ROOT / "index.html"
    elif path.endswith("/"):
        target = ROOT / path.strip("/") / "index.html"
    else:
        target = ROOT / path.lstrip("/")
    return target, path, parsed.fragment or None


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.h1_count = 0
        self.title_count = 0
        self.title_text = ""
        self._in_title = False
        self.html_lang: str | None = None
        self.refs: list[tuple[str, str, str]] = []
        self.images: list[dict[str, str]] = []
        self.buttons: list[dict[str, str]] = []
        self.inputs: list[dict[str, str]] = []
        self.labels_for: set[str] = set()
        self.anchors: list[dict[str, str]] = []
        self.meta_robots: str | None = None
        self.canonical: str | None = None
        self.hreflangs: dict[str, str] = {}
        self.forms: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value or "" for key, value in attrs}
        tag = tag.lower()
        if tag == "html":
            self.html_lang = values.get("lang")
        if tag == "h1":
            self.h1_count += 1
        if tag == "title":
            self.title_count += 1
            self._in_title = True
        if values.get("id"):
            self.ids.append(values["id"])
        if tag == "meta" and values.get("name", "").lower() == "robots":
            self.meta_robots = values.get("content")
        if tag == "link" and values.get("rel", "").lower() == "canonical":
            self.canonical = values.get("href")
        if tag == "link" and values.get("rel", "").lower() == "alternate" and values.get("hreflang"):
            self.hreflangs[values["hreflang"].lower()] = values.get("href", "")

        for attr in ("href", "src", "action", "poster"):
            if values.get(attr):
                self.refs.append((tag, attr, values[attr]))
        if values.get("srcset"):
            for part in values["srcset"].split(","):
                candidate = part.strip().split()[0] if part.strip() else ""
                if candidate:
                    self.refs.append((tag, "srcset", candidate))

        if tag == "img":
            self.images.append(values)
        if tag == "button":
            self.buttons.append(values)
        if tag in {"input", "select", "textarea"}:
            self.inputs.append({"tag": tag, **values})
        if tag == "label" and values.get("for"):
            self.labels_for.add(values["for"])
        if tag == "a":
            self.anchors.append(values)
        if tag == "form":
            self.forms.append(values)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_text += data


def parse_page(path: Path) -> PageParser:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def fetch(url: str, timeout: int = 30) -> tuple[dict, str]:
    last: tuple[dict, str] | None = None
    for attempt in range(3):
        request = urllib.request.Request(url, headers={"User-Agent": "AlinaHorbTailAudit/1.1"})
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                body = response.read(2_000_000)
                text = body.decode("utf-8", errors="replace")
                return ({
                    "ok": 200 <= response.status < 400,
                    "status": response.status,
                    "final_url": response.geturl(),
                    "content_type": response.headers.get("content-type", ""),
                    "bytes": len(body),
                }, text)
        except urllib.error.HTTPError as error:
            last = ({"ok": False, "status": error.code, "final_url": error.geturl(), "error": str(error)}, "")
            if error.code not in {429, 500, 502, 503, 504}:
                return last
        except Exception as error:  # noqa: BLE001
            last = ({"ok": False, "status": None, "final_url": None, "error": str(error)}, "")
        if attempt < 2:
            time.sleep(1.5 * (attempt + 1))
    return last or ({"ok": False, "status": None, "final_url": None, "error": "unknown fetch failure"}, "")


def grep_references(path: str) -> list[str]:
    basename = Path(path).name
    result = subprocess.run(
        ["git", "grep", "-n", "-F", basename, "--", ":!qa/**"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    return [line for line in result.stdout.splitlines() if not line.startswith(f"{path}:")]


def main() -> int:
    critical: list[dict] = []
    warnings: list[dict] = []
    info: list[dict] = []
    page_data: dict[str, PageParser] = {}
    graph: dict[str, set[str]] = defaultdict(set)
    referenced_local_files: set[str] = set()

    # Repository hygiene.
    junk = [
        path for path in TRACKED
        if path.endswith((".tmp", ".bak", ".orig", ".rej", "~", ".DS_Store"))
        or "/__pycache__/" in f"/{path}/"
        or path.startswith(("node_modules/", "_site/"))
    ]
    for path in junk:
        add_issue(critical, "repository-hygiene", "Generated or temporary file is tracked", path)

    for route, path in ROUTE_FILES.items():
        relative = path.relative_to(ROOT).as_posix()
        if not path.is_file():
            add_issue(critical, "route", "Production route file is missing", relative)
            continue
        parser = parse_page(path)
        page_data[route] = parser
        expected_lang = "ru" if route.startswith("/ru/") or route == "/ru/" else "uk"
        if parser.html_lang != expected_lang:
            add_issue(critical, "localization", f"Expected html lang={expected_lang!r}, found {parser.html_lang!r}", relative)
        if parser.h1_count != 1:
            add_issue(critical, "semantics", f"Expected exactly one H1, found {parser.h1_count}", relative)
        if parser.title_count != 1 or not parser.title_text.strip():
            add_issue(critical, "seo", "Missing or duplicate document title", relative)
        duplicate_ids = sorted({value for value in parser.ids if parser.ids.count(value) > 1})
        if duplicate_ids:
            add_issue(critical, "semantics", f"Duplicate IDs: {', '.join(duplicate_ids)}", relative)
        if parser.canonical != f"{LIVE_ORIGIN}{route}":
            add_issue(critical, "seo", f"Canonical mismatch: {parser.canonical!r}", relative)
        if set(parser.hreflangs) < {"uk", "ru", "x-default"}:
            add_issue(critical, "seo", f"Incomplete hreflang set: {sorted(parser.hreflangs)}", relative)

        text = path.read_text(encoding="utf-8")
        for name, pattern in FORBIDDEN_PRODUCTION_PATTERNS.items():
            if pattern.search(text):
                add_issue(critical, "content-tail", f"Forbidden production marker found: {name}", relative)

        for image in parser.images:
            if not image.get("src"):
                add_issue(critical, "image", "Image has no src", relative)
            if "alt" not in image:
                add_issue(critical, "accessibility", f"Image lacks alt attribute: {image.get('src', '')}", relative)
            if not image.get("width") or not image.get("height"):
                add_issue(warnings, "layout-stability", f"Image lacks explicit width/height: {image.get('src', '')}", relative)

        for button in parser.buttons:
            if not button.get("type"):
                add_issue(warnings, "forms", f"Button lacks explicit type: {button.get('class', '')}", relative)

        for control in parser.inputs:
            if control.get("type", "").lower() in {"hidden", "submit", "button", "reset"}:
                continue
            control_id = control.get("id")
            aria = control.get("aria-label") or control.get("aria-labelledby")
            if not aria and (not control_id or control_id not in parser.labels_for):
                add_issue(critical, "accessibility", f"Unlabelled {control['tag']} control: {control.get('name', '')}", relative)

        for anchor in parser.anchors:
            href = anchor.get("href", "")
            if href == "#":
                add_issue(critical, "navigation", "Empty hash link remains", relative)
            if anchor.get("target") == "_blank" and "noopener" not in anchor.get("rel", "").lower():
                add_issue(warnings, "security", f"target=_blank link lacks noopener: {href}", relative)

        route_ids = set(parser.ids)
        for tag, attr, value in parser.refs:
            if value.startswith(("mailto:", "tel:", "data:", "javascript:")):
                continue
            target, url_path, fragment = local_file_for_url(value, route)
            if target is None:
                continue
            try:
                relative_target = target.relative_to(ROOT).as_posix()
            except ValueError:
                add_issue(critical, "path", f"Reference escapes repository: {value}", relative)
                continue
            referenced_local_files.add(relative_target)
            if not target.is_file():
                add_issue(critical, "broken-reference", f"Missing local target for {tag}[{attr}]={value!r}", relative)
                continue
            target_route = route_for_file(target)
            if tag == "a" and target_route:
                graph[route].add(target_route)
            if fragment:
                if target == path:
                    target_ids = route_ids
                elif target_route and target_route in page_data:
                    target_ids = set(page_data[target_route].ids)
                elif target_route:
                    target_ids = set(parse_page(target).ids)
                else:
                    target_ids = set()
                if fragment not in target_ids:
                    add_issue(critical, "broken-fragment", f"Missing fragment target #{fragment} in {url_path}", relative)

    # Link graph reachability from both locale homes.
    for start in ("/", "/ru/"):
        seen = {start}
        queue = deque([start])
        while queue:
            current = queue.popleft()
            for target in graph.get(current, set()):
                if target not in seen:
                    seen.add(target)
                    queue.append(target)
        locale_routes = {
            route for route in ROUTES
            if (route.startswith("/ru/") or route == "/ru/") == (start == "/ru/")
        }
        unreachable = sorted(locale_routes - seen)
        if unreachable:
            add_issue(critical, "link-graph", f"Routes unreachable from {start}: {', '.join(unreachable)}")

    # CSS url() integrity.
    css_url_pattern = re.compile(r"url\((?:['\"]?)([^)'\"]+)")
    for tracked in TRACKED:
        if not tracked.startswith("assets/css/") or not tracked.endswith(".css"):
            continue
        css_path = ROOT / tracked
        css = css_path.read_text(encoding="utf-8")
        for value in css_url_pattern.findall(css):
            value = value.strip()
            if value.startswith(("data:", "http://", "https://", "#")):
                continue
            clean = urllib.parse.urlparse(value).path
            target = (css_path.parent / clean).resolve()
            try:
                relative = target.relative_to(ROOT).as_posix()
            except ValueError:
                add_issue(critical, "css-reference", f"CSS url escapes repository: {value}", tracked)
                continue
            referenced_local_files.add(relative)
            if not target.is_file():
                add_issue(critical, "css-reference", f"Missing CSS url target: {value}", tracked)

    # Exact stale runtime candidates left by the static refactor.
    stale_inventory: dict[str, list[str]] = {}
    for candidate in STALE_ASSET_CANDIDATES:
        if candidate in TRACKED_SET:
            refs = grep_references(candidate)
            stale_inventory[candidate] = refs
            add_issue(critical, "stale-asset", "Obsolete post-refactor asset is still tracked", candidate)

    # Inventory unreferenced front-end assets as informational candidates only.
    for tracked in TRACKED:
        if not tracked.startswith("assets/"):
            continue
        if Path(tracked).suffix.lower() not in {".css", ".js", ".png", ".jpg", ".jpeg", ".webp", ".svg", ".ico"}:
            continue
        if tracked in referenced_local_files:
            continue
        if tracked in STALE_ASSET_CANDIDATES:
            continue
        refs = grep_references(tracked)
        if not refs:
            info.append({"category": "unreferenced-asset-candidate", "path": tracked})

    # Live production verification and public asset crawl.
    live_pages: dict[str, dict] = {}
    live_asset_urls: set[str] = set()
    for route in ROUTES:
        meta, body = fetch(f"{LIVE_ORIGIN}{route}")
        live_pages[route] = meta
        if not meta.get("ok") or meta.get("final_url") != f"{LIVE_ORIGIN}{route}":
            add_issue(critical, "live-route", f"Live route failed or redirected unexpectedly: {meta}", route)
            continue
        parser = PageParser()
        parser.feed(body)
        if parser.h1_count != 1:
            add_issue(critical, "live-semantics", f"Live page H1 count is {parser.h1_count}", route)
        robots = (parser.meta_robots or "").lower()
        if "noindex" in robots or "index" not in robots:
            add_issue(critical, "live-indexing", f"Live robots meta is {parser.meta_robots!r}", route)
        if parser.canonical != f"{LIVE_ORIGIN}{route}":
            add_issue(critical, "live-seo", f"Live canonical mismatch: {parser.canonical!r}", route)
        if parser.html_lang != ("ru" if route.startswith("/ru/") or route == "/ru/" else "uk"):
            add_issue(critical, "live-localization", f"Live html lang mismatch: {parser.html_lang!r}", route)
        if route in {"/consultations/", "/ru/consultations/"} and "site-config.v2.js" not in body:
            add_issue(critical, "live-form", "Production form configuration script is absent", route)
        for _, _, value in parser.refs:
            absolute = urllib.parse.urljoin(f"{LIVE_ORIGIN}{route}", value)
            parsed = urllib.parse.urlparse(absolute)
            if parsed.netloc in {"alinahorb.com", "www.alinahorb.com"} and not parsed.fragment:
                live_asset_urls.add(urllib.parse.urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", parsed.query, "")))

    config_meta, config_body = fetch(f"{LIVE_ORIGIN}/assets/js/site-config.v2.js")
    runtime_meta, runtime_body = fetch(f"{LIVE_ORIGIN}/assets/js/site.v2.js")
    if not config_meta.get("ok") or "https://formspree.io/f/mvzezana" not in config_body or "0x4AAAAAAD2wlldaSXK8Bp9f" not in config_body:
        add_issue(critical, "live-form", "Production Formspree or Turnstile configuration is missing")
    if not runtime_meta.get("ok") or "challenges.cloudflare.com/turnstile/v0/api.js?render=explicit" not in runtime_body or "cf-turnstile-response" not in runtime_body:
        add_issue(critical, "live-form", "Production Turnstile runtime is missing")

    broken_live_assets: list[dict] = []
    for url in sorted(live_asset_urls):
        parsed = urllib.parse.urlparse(url)
        if parsed.path.endswith("/") or parsed.path in {route for route in ROUTES}:
            continue
        meta, _ = fetch(url)
        if not meta.get("ok"):
            broken_live_assets.append({"url": url, **meta})
            add_issue(critical, "live-asset", f"Broken live asset: {url}")

    report = {
        "routes": len(ROUTES),
        "tracked_files": len(TRACKED),
        "critical": critical,
        "warnings": warnings,
        "info": info,
        "stale_inventory": stale_inventory,
        "live_pages": live_pages,
        "live_assets_checked": len(live_asset_urls),
        "broken_live_assets": broken_live_assets,
    }
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "Alina Horb post-refactor tail audit V1",
        f"Routes inspected: {len(page_data)}/{len(ROUTES)}",
        f"Tracked files inventoried: {len(TRACKED)}",
        f"Live assets discovered: {len(live_asset_urls)}",
        f"Critical findings: {len(critical)}",
        f"Warnings: {len(warnings)}",
        f"Informational orphan candidates: {len(info)}",
        "",
        "Critical:",
        *([f"- [{item['category']}] {item.get('path', '')}: {item['message']}" for item in critical] or ["- none"]),
        "",
        "Warnings:",
        *([f"- [{item['category']}] {item.get('path', '')}: {item['message']}" for item in warnings] or ["- none"]),
        "",
        "Stale asset reference inventory:",
    ]
    for candidate, refs in stale_inventory.items():
        lines.append(f"- {candidate}: {len(refs)} repository references")
        lines.extend(f"  - {ref}" for ref in refs[:20])
    if not stale_inventory:
        lines.append("- none")
    (OUTPUT / "summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))

    return 1 if STRICT and critical else 0


if __name__ == "__main__":
    sys.exit(main())
