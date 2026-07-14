#!/usr/bin/env python3
"""Validate local assets referenced by the production HTML and CSS files."""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = (ROOT / "index.html", ROOT / "ru" / "index.html")
LOCAL_SCHEMES = {"", "file"}
CSS_URL = re.compile(r"url\(\s*(['\"]?)(.*?)\1\s*\)", re.IGNORECASE)


def local_path(value: str, source: Path) -> Path | None:
    value = value.strip()
    if not value or value.startswith(("#", "data:", "mailto:", "tel:", "javascript:")):
        return None
    parsed = urlsplit(value)
    if parsed.scheme not in LOCAL_SCHEMES or parsed.netloc:
        return None
    clean = unquote(parsed.path)
    if not clean:
        return None
    return (ROOT / clean.lstrip("/")) if clean.startswith("/") else (source.parent / clean)


class AssetParser(HTMLParser):
    def __init__(self, source: Path) -> None:
        super().__init__(convert_charrefs=True)
        self.source = source
        self.references: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {name.lower(): value or "" for name, value in attrs}
        if tag in {"img", "script"} and values.get("src"):
            self.references.append((f"{tag}[src]", values["src"]))
        if tag == "source" and values.get("srcset"):
            self._add_srcset(values["srcset"])
        if tag == "img" and values.get("srcset"):
            self._add_srcset(values["srcset"])
        if tag == "link" and values.get("href"):
            rel = set(values.get("rel", "").lower().split())
            if rel.intersection({"stylesheet", "preload", "icon"}):
                self.references.append((f"link[{','.join(sorted(rel))}]", values["href"]))
        if tag == "a" and values.get("href"):
            suffix = Path(urlsplit(values["href"]).path).suffix.lower()
            if suffix in {".jpg", ".jpeg", ".png", ".webp", ".svg", ".pdf"}:
                self.references.append(("a[href]", values["href"]))

    def _add_srcset(self, srcset: str) -> None:
        for candidate in srcset.split(","):
            url = candidate.strip().split()[0] if candidate.strip() else ""
            if url:
                self.references.append(("source[srcset]", url))


def validate_html(source: Path) -> tuple[list[str], set[Path]]:
    parser = AssetParser(source)
    parser.feed(source.read_text(encoding="utf-8"))
    errors: list[str] = []
    css_files: set[Path] = set()
    for kind, value in parser.references:
        target = local_path(value, source)
        if target is None:
            continue
        target = target.resolve()
        if not target.is_file():
            errors.append(f"{source.relative_to(ROOT)}: missing {kind} -> {value}")
        elif target.suffix.lower() == ".css":
            css_files.add(target)
    return errors, css_files


def validate_css(source: Path) -> list[str]:
    text = source.read_text(encoding="utf-8")
    errors: list[str] = []
    if re.search(r"@import\b", text, re.IGNORECASE):
        errors.append(f"{source.relative_to(ROOT)}: CSS @import is not allowed")
    for _, value in CSS_URL.findall(text):
        target = local_path(value, source)
        if target is not None and not target.resolve().is_file():
            errors.append(f"{source.relative_to(ROOT)}: missing CSS url() -> {value}")
    return errors


def main() -> int:
    errors: list[str] = []
    css_files: set[Path] = set()
    for html_file in HTML_FILES:
        html_errors, html_css = validate_html(html_file)
        errors.extend(html_errors)
        css_files.update(html_css)
    for css_file in css_files:
        errors.extend(validate_css(css_file))

    if errors:
        print("Asset validation failed:", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    print(f"Asset validation passed for {len(HTML_FILES)} HTML files and {len(css_files)} stylesheet(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
