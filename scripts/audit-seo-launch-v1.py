#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'qa' / 'seo-launch-v1'
BASE = 'https://alinahorb.com'
PUBLIC_ROBOTS = 'index, follow, max-image-preview:large'
PRIVATE_ROBOTS = 'noindex, follow'
STRICT = os.environ.get('AUDIT_STRICT') == '1'

ROUTES = [
    ('/', 'index.html', 'uk', True),
    ('/ru/', 'ru/index.html', 'ru', True),
    ('/about/', 'about/index.html', 'uk', True),
    ('/ru/about/', 'ru/about/index.html', 'ru', True),
    ('/consultations/', 'consultations/index.html', 'uk', True),
    ('/ru/consultations/', 'ru/consultations/index.html', 'ru', True),
    ('/notes/', 'notes/index.html', 'uk', True),
    ('/ru/notes/', 'ru/notes/index.html', 'ru', True),
    ('/notes/first-consultation/', 'notes/first-consultation/index.html', 'uk', True),
    ('/ru/notes/first-consultation/', 'ru/notes/first-consultation/index.html', 'ru', True),
    ('/notes/how-to-start-the-conversation/', 'notes/how-to-start-the-conversation/index.html', 'uk', True),
    ('/ru/notes/how-to-start-the-conversation/', 'ru/notes/how-to-start-the-conversation/index.html', 'ru', True),
    ('/notes/when-coping-stops-helping/', 'notes/when-coping-stops-helping/index.html', 'uk', True),
    ('/ru/notes/when-coping-stops-helping/', 'ru/notes/when-coping-stops-helping/index.html', 'ru', True),
    ('/notes/stress-relocation-and-lost-support/', 'notes/stress-relocation-and-lost-support/index.html', 'uk', True),
    ('/ru/notes/stress-relocation-and-lost-support/', 'ru/notes/stress-relocation-and-lost-support/index.html', 'ru', True),
    ('/privacy/', 'privacy/index.html', 'uk', False),
    ('/ru/privacy/', 'ru/privacy/index.html', 'ru', False),
]

ARTICLE_ROUTES = {route for route, _, _, _ in ROUTES if '/notes/' in route and route not in {'/notes/', '/ru/notes/'}}
NOTES_HUB_ROUTES = {'/notes/', '/ru/notes/'}


class Parser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.html_lang = ''
        self.title_parts: list[str] = []
        self.in_title = False
        self.h1_count = 0
        self.meta: dict[tuple[str, str], str] = {}
        self.links: list[dict[str, str]] = []
        self.scripts: list[dict[str, str]] = []
        self.in_json_ld = False
        self.json_ld_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key: value or '' for key, value in attrs}
        if tag == 'html':
            self.html_lang = data.get('lang', '')
        elif tag == 'title':
            self.in_title = True
        elif tag == 'h1':
            self.h1_count += 1
        elif tag == 'meta':
            if data.get('name'):
                self.meta[('name', data['name'].lower())] = data.get('content', '')
            if data.get('property'):
                self.meta[('property', data['property'].lower())] = data.get('content', '')
        elif tag == 'link':
            self.links.append(data)
        elif tag == 'script' and data.get('type', '').lower() == 'application/ld+json':
            self.in_json_ld = True
            self.json_ld_parts = []

    def handle_endtag(self, tag: str) -> None:
        if tag == 'title':
            self.in_title = False
        elif tag == 'script' and self.in_json_ld:
            self.in_json_ld = False
            self.scripts.append({'content': ''.join(self.json_ld_parts).strip()})

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)
        if self.in_json_ld:
            self.json_ld_parts.append(data)

    @property
    def title(self) -> str:
        return ' '.join(''.join(self.title_parts).split())


def add(target: list[dict], category: str, message: str, path: str = '') -> None:
    target.append({'category': category, 'path': path, 'message': message})


def link_value(parser: Parser, rel: str, hreflang: str | None = None) -> str | None:
    for link in parser.links:
        rel_tokens = link.get('rel', '').lower().split()
        if rel not in rel_tokens:
            continue
        if hreflang is not None and link.get('hreflang', '').lower() != hreflang:
            continue
        return link.get('href')
    return None


def schema_nodes(parser: Parser, critical: list[dict], path: str) -> list[dict]:
    nodes: list[dict] = []
    for script in parser.scripts:
        try:
            payload = json.loads(script['content'])
        except json.JSONDecodeError as error:
            add(critical, 'structured-data', f'Invalid JSON-LD: {error}', path)
            continue
        if isinstance(payload, dict) and isinstance(payload.get('@graph'), list):
            nodes.extend(item for item in payload['@graph'] if isinstance(item, dict))
        elif isinstance(payload, dict):
            nodes.append(payload)
        elif isinstance(payload, list):
            nodes.extend(item for item in payload if isinstance(item, dict))
    return nodes


def types_for(nodes: list[dict]) -> set[str]:
    result: set[str] = set()
    for node in nodes:
        value = node.get('@type')
        if isinstance(value, str):
            result.add(value)
        elif isinstance(value, list):
            result.update(item for item in value if isinstance(item, str))
    return result


def expected_hreflang(route: str) -> tuple[str, str, str]:
    clean = route.removeprefix('/ru')
    if not clean:
        clean = '/'
    return f'{BASE}{clean}', f'{BASE}/ru{clean}', f'{BASE}{clean}'


def mime_for(url: str) -> str | None:
    suffix = Path(urlparse(url).path).suffix.lower()
    return {
        '.webp': 'image/webp',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
    }.get(suffix)


def valid_iso_date(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value[:10])
        return True
    except ValueError:
        return False


def main() -> int:
    critical: list[dict] = []
    warnings: list[dict] = []
    titles: list[str] = []
    descriptions: list[str] = []
    route_report: dict[str, dict] = {}

    for route, relative, language, indexable in ROUTES:
        path = ROOT / relative
        canonical = f'{BASE}{route}'
        if not path.is_file():
            add(critical, 'route', 'HTML file is missing', relative)
            continue
        text = path.read_text(encoding='utf-8')
        parser = Parser()
        parser.feed(text)
        title = parser.title
        description = parser.meta.get(('name', 'description'), '')
        robots = parser.meta.get(('name', 'robots'), '')
        expected_robots = PUBLIC_ROBOTS if indexable else PRIVATE_ROBOTS
        ua_url, ru_url, x_default = expected_hreflang(route)

        route_report[route] = {
            'path': relative,
            'language': language,
            'indexable': indexable,
            'title': title,
            'title_length': len(title),
            'description_length': len(description),
            'robots': robots,
            'canonical': link_value(parser, 'canonical'),
        }

        if parser.html_lang != language:
            add(critical, 'localization', f'Expected html lang={language!r}, found {parser.html_lang!r}', relative)
        if parser.h1_count != 1:
            add(critical, 'semantics', f'Expected exactly one H1, found {parser.h1_count}', relative)
        if not title:
            add(critical, 'title', 'Document title is missing', relative)
        else:
            titles.append(title)
            if len(title) < 25 or len(title) > 75:
                add(warnings, 'title-length', f'Title length is {len(title)} characters', relative)
        if not description:
            add(critical, 'description', 'Meta description is missing', relative)
        else:
            descriptions.append(description)
            if len(description) < 90 or len(description) > 180:
                add(warnings, 'description-length', f'Description length is {len(description)} characters', relative)
        if robots != expected_robots:
            add(critical, 'indexing', f'Expected robots={expected_robots!r}, found {robots!r}', relative)
        if link_value(parser, 'canonical') != canonical:
            add(critical, 'canonical', f'Canonical must be {canonical}', relative)
        if link_value(parser, 'alternate', 'uk') != ua_url:
            add(critical, 'hreflang', f'UK alternate must be {ua_url}', relative)
        if link_value(parser, 'alternate', 'ru') != ru_url:
            add(critical, 'hreflang', f'RU alternate must be {ru_url}', relative)
        if link_value(parser, 'alternate', 'x-default') != x_default:
            add(critical, 'hreflang', f'x-default alternate must be {x_default}', relative)

        if language == 'ru' and 'коли важко сформулювати запит' in text.lower():
            add(critical, 'localization', 'Ukrainian phrase leaked into Russian content', relative)

        nodes = schema_nodes(parser, critical, relative)
        schema_types = types_for(nodes)

        if indexable:
            required_meta = [
                ('property', 'og:title'), ('property', 'og:description'), ('property', 'og:url'),
                ('property', 'og:image'), ('property', 'og:image:width'), ('property', 'og:image:height'),
                ('name', 'twitter:card'), ('name', 'twitter:title'), ('name', 'twitter:description'), ('name', 'twitter:image'),
            ]
            for key in required_meta:
                if not parser.meta.get(key):
                    add(critical, 'social-preview', f'Missing {key[1]}', relative)
            if parser.meta.get(('property', 'og:url')) != canonical:
                add(critical, 'social-preview', 'og:url does not match canonical', relative)
            og_image = parser.meta.get(('property', 'og:image'), '')
            og_type = parser.meta.get(('property', 'og:image:type'), '')
            expected_mime = mime_for(og_image)
            if expected_mime and og_type != expected_mime:
                add(critical, 'social-preview', f'OG image MIME {og_type!r} does not match {expected_mime!r}', relative)
            if parser.meta.get(('name', 'twitter:image')) != og_image:
                add(warnings, 'social-preview', 'Twitter image differs from Open Graph image', relative)
            if not nodes:
                add(critical, 'structured-data', 'Indexable page has no JSON-LD', relative)

        expected_types: set[str]
        if route in {'/', '/ru/'}:
            expected_types = {'WebSite', 'Person'}
        elif route in {'/about/', '/ru/about/'}:
            expected_types = {'ProfilePage', 'Person', 'BreadcrumbList'}
        elif route in {'/consultations/', '/ru/consultations/'}:
            expected_types = {'Service', 'FAQPage', 'BreadcrumbList'}
        elif route in NOTES_HUB_ROUTES:
            expected_types = {'CollectionPage', 'ItemList', 'BreadcrumbList'}
        elif route in ARTICLE_ROUTES:
            expected_types = {'Article', 'BreadcrumbList'}
        else:
            expected_types = set()
        missing_types = expected_types - schema_types
        if missing_types:
            add(critical, 'structured-data', f'Missing schema types: {sorted(missing_types)}', relative)

        if route in ARTICLE_ROUTES:
            article = next((node for node in nodes if node.get('@type') == 'Article'), None)
            if not article:
                continue
            for field in ('headline', 'description', 'mainEntityOfPage', 'image', 'author', 'dateModified'):
                if not article.get(field):
                    add(critical, 'article-schema', f'Missing Article.{field}', relative)
            if article.get('mainEntityOfPage') != canonical:
                add(critical, 'article-schema', 'mainEntityOfPage does not match canonical', relative)
            if not valid_iso_date(article.get('dateModified')):
                add(critical, 'article-schema', 'dateModified is not an ISO date', relative)
            author = article.get('author')
            if not isinstance(author, dict) or author.get('@type') != 'Person' or not author.get('name') or not author.get('url'):
                add(critical, 'article-schema', 'Article author must be an identified Person with name and URL', relative)

        if route in NOTES_HUB_ROUTES:
            item_list = next((node for node in nodes if node.get('@type') == 'ItemList'), None)
            if not item_list or item_list.get('numberOfItems') != 4 or len(item_list.get('itemListElement', [])) != 4:
                add(critical, 'collection-schema', 'Notes ItemList must contain exactly four articles', relative)

    duplicate_titles = [value for value, count in Counter(titles).items() if count > 1]
    duplicate_descriptions = [value for value, count in Counter(descriptions).items() if count > 1]
    if duplicate_titles:
        add(critical, 'title', f'Duplicate titles: {duplicate_titles}')
    if duplicate_descriptions:
        add(warnings, 'description', f'Duplicate descriptions: {duplicate_descriptions}')

    sitemap_path = ROOT / 'sitemap.xml'
    if not sitemap_path.is_file():
        add(critical, 'sitemap', 'sitemap.xml is missing')
        sitemap_locations: list[str] = []
    else:
        root = ET.parse(sitemap_path).getroot()
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        sitemap_locations = [node.text or '' for node in root.findall('sm:url/sm:loc', ns)]
        expected_locations = [f'{BASE}{route}' for route, _, _, indexable in ROUTES if indexable]
        if sitemap_locations != expected_locations:
            add(critical, 'sitemap', 'Sitemap must contain exactly the 16 indexable canonical URLs in route order')
        if any('/privacy/' in location for location in sitemap_locations):
            add(critical, 'sitemap', 'Privacy noindex URLs must not appear in sitemap')

    robots_path = ROOT / 'robots.txt'
    robots_text = robots_path.read_text(encoding='utf-8') if robots_path.is_file() else ''
    if 'User-agent: *' not in robots_text or 'Allow: /' not in robots_text or f'Sitemap: {BASE}/sitemap.xml' not in robots_text:
        add(critical, 'robots', 'robots.txt contract is incomplete')
    if 'Disallow:' in robots_text:
        add(critical, 'robots', 'robots.txt must not block crawl access to noindex pages')

    report = {
        'routes_checked': len(route_report),
        'indexable_routes': sum(1 for *_, indexable in ROUTES if indexable),
        'noindex_routes': sum(1 for *_, indexable in ROUTES if not indexable),
        'sitemap_urls': sitemap_locations,
        'critical': critical,
        'warnings': warnings,
        'routes': route_report,
    }
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = [
        'Alina Horb SEO Launch & Indexing Audit V1',
        f'Routes checked: {len(route_report)}/{len(ROUTES)}',
        f'Indexable routes: {report["indexable_routes"]}',
        f'Noindex privacy routes: {report["noindex_routes"]}',
        f'Sitemap URLs: {len(sitemap_locations)}',
        f'Critical findings: {len(critical)}',
        f'Warnings: {len(warnings)}',
        '',
        'Critical:',
        *([f'- [{item["category"]}] {item.get("path", "")}: {item["message"]}' for item in critical] or ['- none']),
        '',
        'Warnings:',
        *([f'- [{item["category"]}] {item.get("path", "")}: {item["message"]}' for item in warnings] or ['- none']),
    ]
    (OUTPUT / 'summary.txt').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('\n'.join(lines))
    if critical or (STRICT and warnings):
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
