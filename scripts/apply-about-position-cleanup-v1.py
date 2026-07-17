#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def sub_required(text: str, pattern: str, replacement: str, label: str, count: int = 1) -> str:
    updated, matches = re.subn(pattern, replacement, text, count=count, flags=re.S)
    if matches != count:
        raise SystemExit(f"{label}: expected {count} match(es), found {matches}")
    return updated


ABOUT = {
    "about/index.html": {
        "mobile": '<a href="#path">Шлях</a><a href="#methods">Підхід</a><a href="#education">Освіта</a><a href="#contact">Запис</a>',
        "side": '''        <a href="#path"><b>01</b><span>Шлях</span></a>\n        <a href="#methods"><b>02</b><span>Підхід</span></a>\n        <a href="#education"><b>03</b><span>Освіта</span></a>\n        <a href="#scope"><b>04</b><span>Запити</span></a>\n        <a href="#boundaries"><b>05</b><span>Відповідальність</span></a>''',
        "meta_old": "Освіта, професійна позиція, підхід і межі роботи психолога Аліни Горб.",
        "meta_new": "Освіта, підхід, напрями роботи та професійна відповідальність психолога Аліни Горб.",
        "editorial": '''        <div class="profile-editorial-voice" data-reveal>\n          <p class="section-kicker">Підхід у роботі</p>\n          <h2 id="editorial-title">Чітка мета, дбайливий темп і помітні зміни</h2>\n          <blockquote class="profile-editorial-quote">\n            <p>У роботі для мене важливі чітка мета, дбайливий темп і зміни, які людина поступово помічає у своєму повсякденному житті.</p>\n            <footer>Аліна Горб · про підхід до роботи</footer>\n          </blockquote>\n        </div>''',
        "renumber": {
            "03 · Підхід у роботі": "02 · Підхід у роботі",
            "04 · Освіта": "03 · Освіта",
            "05 · З чим можна звернутися": "04 · З чим можна звернутися",
            "06 · Професійна відповідальність": "05 · Професійна відповідальність",
        },
        "headline": "Чітка мета, дбайливий темп і помітні зміни",
    },
    "ru/about/index.html": {
        "mobile": '<a href="#path">Путь</a><a href="#methods">Подход</a><a href="#education">Образование</a><a href="#contact">Запись</a>',
        "side": '''        <a href="#path"><b>01</b><span>Путь</span></a>\n        <a href="#methods"><b>02</b><span>Подход</span></a>\n        <a href="#education"><b>03</b><span>Образование</span></a>\n        <a href="#scope"><b>04</b><span>Запросы</span></a>\n        <a href="#boundaries"><b>05</b><span>Ответственность</span></a>''',
        "meta_old": "Образование, профессиональная позиция, подход и границы работы психолога Алины Горб.",
        "meta_new": "Образование, подход, направления работы и профессиональная ответственность психолога Алины Горб.",
        "editorial": '''        <div class="profile-editorial-voice" data-reveal>\n          <p class="section-kicker">Подход в работе</p>\n          <h2 id="editorial-title">Ясная цель, бережный темп и заметные изменения</h2>\n          <blockquote class="profile-editorial-quote">\n            <p>В работе для меня важны ясная цель, бережный темп и изменения, которые человек постепенно замечает в своей повседневной жизни.</p>\n            <footer>Алина Горб · о подходе к работе</footer>\n          </blockquote>\n        </div>''',
        "renumber": {
            "03 · Подход в работе": "02 · Подход в работе",
            "04 · Образование": "03 · Образование",
            "05 · С чем можно обратиться": "04 · С чем можно обратиться",
            "06 · Профессиональная ответственность": "05 · Профессиональная ответственность",
        },
        "headline": "Ясная цель, бережный темп и заметные изменения",
    },
}

for relative, cfg in ABOUT.items():
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")

    text = sub_required(
        text,
        r'(<nav class="mobile-navigation"[^>]*>\s*)(.*?)(\s*</nav>)',
        lambda m: m.group(1) + cfg["mobile"] + m.group(3),
        f"{relative}: mobile navigation",
    )
    text = sub_required(
        text,
        r'(<nav class="side-navigation profile-side-navigation"[^>]*>\s*)(.*?)(\s*</nav>)',
        lambda m: m.group(1) + cfg["side"] + m.group(3),
        f"{relative}: side navigation",
    )

    if cfg["meta_old"] not in text:
        raise SystemExit(f"{relative}: old social description not found")
    text = text.replace(cfg["meta_old"], cfg["meta_new"])

    text = sub_required(
        text,
        r'\n\s*<section class="profile-position section-block" id="position" aria-labelledby="position-title">.*?</section>\s*(?=<section class="profile-editorial section-block")',
        "\n\n    ",
        f"{relative}: remove green position section",
    )
    text = sub_required(
        text,
        r'        <div class="profile-editorial-voice" data-reveal>.*?        </div>(?=\n        <figure class="profile-editorial-figure")',
        cfg["editorial"],
        f"{relative}: editorial consolidation",
    )

    for old, new in cfg["renumber"].items():
        if old not in text:
            raise SystemExit(f"{relative}: numbering token missing: {old}")
        text = text.replace(old, new, 1)

    forbidden = ("#position", "profile-position section-block", "position-principles")
    for token in forbidden:
        if token in text:
            raise SystemExit(f"{relative}: removed token remains: {token}")
    if cfg["headline"] not in text:
        raise SystemExit(f"{relative}: refined headline missing")

    path.write_text(text, encoding="utf-8")

FAQ = {
    "consultations/index.html": (
        r'\s*<details><summary aria-expanded="false">Чи потрібно заздалегідь знати, з чого почати\?</summary>.*?</details>\s*<details><summary aria-expanded="false">Чи можна звернутися без точного запиту\?</summary>.*?</details>',
        '\n          <details><summary aria-expanded="false">Чи потрібно заздалегідь формулювати точний запит?</summary><p>Ні. Можна почати з того, що зараз найбільше турбує, або прямо сказати, що сформулювати запит поки складно. На першій зустрічі ми разом уточнимо, що потребує найбільшої уваги.</p></details>',
    ),
    "ru/consultations/index.html": (
        r'\s*<details><summary aria-expanded="false">Нужно ли заранее знать, с чего начать\?</summary>.*?</details>\s*<details><summary aria-expanded="false">Можно ли обратиться без точного запроса\?</summary>.*?</details>',
        '\n          <details><summary aria-expanded="false">Нужно ли заранее формулировать точный запрос?</summary><p>Нет. Можно начать с того, что сейчас больше всего беспокоит, или прямо сказать, что сформулировать запрос пока трудно. На первой встрече мы вместе уточним, что требует наибольшего внимания.</p></details>',
    ),
}

for relative, (pattern, replacement) in FAQ.items():
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    text = sub_required(text, pattern, replacement, f"{relative}: merge duplicate FAQ")
    path.write_text(text, encoding="utf-8")

css_path = ROOT / "assets/css/site.about.v1.css"
css = css_path.read_text(encoding="utf-8")
marker = "/* About-page mobile booking CTA: compact footprint and safe final-section spacing. */"
if marker not in css:
    css += '''\n\n/* About-page mobile booking CTA: compact footprint and safe final-section spacing. */\n@media (max-width: 700px) {\n  .page-about-profile .mobile-booking-cta {\n    right: 16px;\n    bottom: calc(12px + env(safe-area-inset-bottom));\n    left: 16px;\n    width: auto;\n    min-height: 52px;\n    border-radius: 999px;\n    box-shadow: 0 14px 38px rgba(47, 48, 45, .2);\n  }\n\n  .page-about-profile .profile-final-inner {\n    padding-bottom: calc(58px + env(safe-area-inset-bottom));\n  }\n}\n'''
css_path.write_text(css, encoding="utf-8")

validator_path = ROOT / "scripts/validate-about-pages-v1.py"
validator = validator_path.read_text(encoding="utf-8")
validator = validator.replace('"about", "path", "position", "methods", "education", "scope",', '"about", "path", "methods", "education", "scope",')
validator = validator.replace('"profile-timeline", "position-principles", "profile-method-list",', '"profile-timeline", "profile-editorial", "profile-method-list",')
validator = validator.replace('require(section_count >= 9,', 'require(section_count >= 8,')
validator = validator.replace('".profile-hero-layout", ".profile-section-grid", ".position-principles",', '".profile-hero-layout", ".profile-section-grid", ".profile-editorial-layout",')
anchor = '    require("TODO" not in text and "placeholder" not in text.lower(), f"{relative}: unfinished marker found")\n'
checks = '''    require('#position' not in text and 'profile-position section-block' not in text, f"{relative}: removed professional-position section still present")\n    require('position-principles' not in text, f"{relative}: removed principle grid still present")\n    require(('Чітка мета, дбайливий темп і помітні зміни' in text) or ('Ясная цель, бережный темп и заметные изменения' in text), f"{relative}: refined editorial positioning missing")\n'''
if checks not in validator:
    if anchor not in validator:
        raise SystemExit("About validator insertion anchor missing")
    validator = validator.replace(anchor, anchor + checks, 1)
validator_path.write_text(validator, encoding="utf-8")

for relative, cfg in ABOUT.items():
    text = (ROOT / relative).read_text(encoding="utf-8")
    if len(re.findall(r'<section\b', text, flags=re.I)) < 8:
        raise SystemExit(f"{relative}: page structure unexpectedly short")
    if cfg["headline"] not in text:
        raise SystemExit(f"{relative}: final headline check failed")

print("About positioning simplified, FAQ deduplicated, and mobile CTA footprint refined.")
