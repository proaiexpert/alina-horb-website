#!/usr/bin/env python3
"""TASK 039: targeted bilingual medical-routing, schema and social PNG QA (stdlib only)."""
import json
import re
import struct
import zlib
from pathlib import Path
from html import unescape

ROOT = Path(__file__).resolve().parents[1]
PNG = ROOT / "assets/images/social/alina-horb-article02-og.png"
IMAGE = "https://alinahorb.com/assets/images/social/alina-horb-article02-og.png"
AHA = "https://www.heart.org/en/about-us/heart-attack-and-stroke-symptoms"
checks = {}

def check(name, ok):
    checks[name] = bool(ok)
    if not ok:
        raise AssertionError(name)

def plain(s):
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"\*\*|__|\[|\]\(https://[^)]+\)", "", s)
    return re.sub(r"\s+", " ", unescape(s)).strip()

def attr(html, name, value):
    pat = r'<meta\s+(?:name|property)="' + re.escape(name) + r'"\s+content="([^"]+)"'
    found = re.search(pat, html)
    return bool(found and found.group(1) == value)

def png_check():
    b = PNG.read_bytes()
    check("png_signature", b[:8] == b"\x89PNG\r\n\x1a\n")
    ptr, data, sizes = 8, bytearray(), None
    while ptr < len(b):
        length = struct.unpack(">I", b[ptr:ptr+4])[0]
        typ = b[ptr+4:ptr+8]
        body = b[ptr+8:ptr+8+length]
        crc = struct.unpack(">I", b[ptr+8+length:ptr+12+length])[0]
        check("png_crc_" + str(ptr), (zlib.crc32(typ+body) & 0xffffffff) == crc)
        if typ == b"IHDR":
            width, height, depth, color, _, _, _ = struct.unpack(">IIBBBBB", body)
            sizes = (width, height, depth, color)
        if typ == b"IDAT": data.extend(body)
        ptr += length+12
        if typ == b"IEND": break
    check("png_dimensions", sizes == (1200,630,8,3))
    raw = zlib.decompress(data)
    check("png_scanlines", len(raw) == 630*1201 and all(raw[y*1201] == 0 for y in range(630)))
    check("png_repo_size", len(b) < 2_000_000)
    return len(b)

file_bytes = png_check()
for lang, (html_path, md_path, action, title, tokens, canonical, other) in {
    "ua": (
       "notes/fear-of-another-panic-attack/index.html",
       "content/article02/UA_MASTER_TASK036.md",
       "Негайно викликайте місцеві екстрені служби",
       "Коли потрібна медична оцінка, а коли — екстрена допомога",
       ["руки", "спину", "шию", "щелепу", "інсульту", "рівноваги"],
       "https://alinahorb.com/notes/fear-of-another-panic-attack/",
       "https://alinahorb.com/ru/notes/fear-of-another-panic-attack/"
    ),
    "ru": (
       "ru/notes/fear-of-another-panic-attack/index.html",
       "content/article02/RU_MASTER_TASK036.md",
       "Немедленно вызывайте местные экстренные службы",
       "Когда нужна медицинская оценка, а когда — экстренная помощь",
       ["руки", "спину", "шею", "челюсть", "инсульта", "равновесия"],
       "https://alinahorb.com/ru/notes/fear-of-another-panic-attack/",
       "https://alinahorb.com/notes/fear-of-another-panic-attack/"
    )
}.items():
    h=(ROOT/html_path).read_text(encoding="utf-8")
    m=(ROOT/md_path).read_text(encoding="utf-8")
    sec=re.search(r'<section id="section-6">([\s\S]*?)</section>', h)
    check(lang+"_emergency_section", bool(sec))
    s=sec.group(1)
    urgent=re.search(r'<div class="panic-care-block panic-care-block--urgent">([\s\S]*?)</div>', s)
    check(lang+"_urgent_card", bool(urgent))
    u=urgent.group(1)
    check(lang+"_first_visual_action", bool(re.match(
       r'\s*<h3 class="panic-urgent-action">'+re.escape(action)+r'</h3>',u)))
    check(lang+"_markdown_action", "### "+action in m)
    check(lang+"_section_title_sync", title in m and "<h2>"+title+"</h2>" in s)
    check(lang+"_danger_examples", u.count("<li>") == 3)
    check(lang+"_danger_keywords", all(v in u and v in m for v in tokens))
    check(lang+"_source", AHA in u and AHA in m)
    check(lang+"_non_exhaustive", ("неповний" if lang=="ua" else "неполный") in u)
    check(lang+"_crisis_distinct", ("кризової служби" if lang=="ua" else "кризисную службу") in u)
    check(lang+"_planned_care", "panic-care-block--planned" in s)
    check(lang+"_author_methods", "КПТ" in h and "NICE" in h and "NIMH" in h and "експозиційні" in h if lang=="ua" else "КПТ" in h and "NICE" in h and "NIMH" in h and "экспозиционные" in h)
    check(lang+"_five_stages", set(re.findall(r'data-step="(\d\d)"',h))=={"01","02","03","04","05"})
    check(lang+"_faq_visual", h.count('class="article-qa"')==6)
    check(lang+"_cta", 'article-cta-band--v21' in h)
    check(lang+"_canonical", f'rel="canonical" href="{canonical}"' in h)
    check(lang+"_language_pair", f'rel="alternate" hreflang="{"ru" if lang=="ua" else "uk"}" href="{other}"' in h)
    check(lang+"_og", attr(h,"og:image",IMAGE) and attr(h,"og:image:secure_url",IMAGE))
    check(lang+"_png_type", attr(h,"og:image:type","image/png"))
    check(lang+"_og_size",attr(h,"og:image:width","1200") and attr(h,"og:image:height","630"))
    check(lang+"_twitter", attr(h,"twitter:image",IMAGE))
    check(lang+"_no_svg_social", "alina-horb-article02-og.svg" not in h)
    jsonld=re.search(r'<script type="application/ld\+json">([\s\S]*?)</script>', h)
    check(lang+"_jsonld", bool(jsonld))
    ld=json.loads(jsonld.group(1))
    graph=ld.get("@graph",[])
    article=[node for node in graph if node.get("@type")=="Article"]
    faq=[node for node in graph if node.get("@type")=="FAQPage"]
    check(lang+"_schema_article",len(article)==1 and article[0].get("image")==IMAGE)
    check(lang+"_schema_no_fictitious_publication", "datePublished" not in article[0])
    check(lang+"_schema_FAQ",len(faq)==1 and len(faq[0].get("mainEntity",[]))==6)

assert len(checks) > 70
print(json.dumps({"status":"PASS","test_count":len(checks),"png_bytes":file_bytes,"checks":checks},indent=2,ensure_ascii=False))
