#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


def sub_once(text: str, pattern: str, replacement: str, label: str) -> str:
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.S)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one regex match, found {count}")
    return updated


ABOUT = {
    "about/index.html": {
        "mobile_old": '<a href="#path">Шлях</a><a href="#position">Позиція</a><a href="#education">Освіта</a><a href="#contact">Запис</a>',
        "mobile_new": '<a href="#path">Шлях</a><a href="#methods">Підхід</a><a href="#education">Освіта</a><a href="#contact">Запис</a>',
        "side_old": '''        <a href="#path"><b>01</b><span>Шлях</span></a>\n        <a href="#position"><b>02</b><span>Позиція</span></a>\n        <a href="#methods"><b>03</b><span>Підхід</span></a>\n        <a href="#education"><b>04</b><span>Освіта</span></a>\n        <a href="#scope"><b>05</b><span>Запити</span></a>\n        <a href="#boundaries"><b>06</b><span>Межі</span></a>''',
        "side_new": '''        <a href="#path"><b>01</b><span>Шлях</span></a>\n        <a href="#methods"><b>02</b><span>Підхід</span></a>\n        <a href="#education"><b>03</b><span>Освіта</span></a>\n        <a href="#scope"><b>04</b><span>Запити</span></a>\n        <a href="#boundaries"><b>05</b><span>Відповідальність</span></a>''',
        "meta_old": 'Освіта, професійна позиція, підхід і межі роботи психолога Аліни Горб.',
        "meta_new": 'Освіта, підхід, напрями роботи та професійна відповідальність психолога Аліни Горб.',
        "editorial_old": '''          <p class="section-kicker">Професійна інтонація</p>\n          <h2 id="editorial-title">Повернути можливість спокійно відчувати, помічати й розуміти</h2>\n          <blockquote class="profile-editorial-quote">\n            <p>Для мене важливо не квапити людину з висновками та рішеннями. Іноді спочатку потрібно повернути можливість спокійно відчувати, помічати й розуміти те, що відбувається.</p>\n            <footer>Аліна Горб · професійна позиція</footer>\n          </blockquote>''',
        "editorial_new": '''          <p class="section-kicker">Підхід у роботі</p>\n          <h2 id="editorial-title">Чітка мета, дбайливий темп і помітні зміни</h2>\n          <blockquote class="profile-editorial-quote">\n            <p>У роботі для мене важливі чітка мета, дбайливий темп і зміни, які людина поступово помічає у своєму повсякденному житті.</p>\n            <footer>Аліна Горб · про підхід до роботи</footer>\n          </blockquote>''',
        "numbers": [
            ('03 · Підхід у роботі', '02 · Підхід у роботі'),
            ('04 · Освіта', '03 · Освіта'),
            ('05 · З чим можна звернутися', '04 · З чим можна звернутися'),
            ('06 · Професійна відповідальність', '05 · Професійна відповідальність'),
        ],
        "expected": [
            'Чітка мета, дбайливий темп і помітні зміни',
            'У роботі для мене важливі чітка мета, дбайливий темп',
            '05 · Професійна відповідальність',
        ],
    },
    "ru/about/index.html": {
        "mobile_old": '<a href="#path">Путь</a><a href="#position">Позиция</a><a href="#education">Образование</a><a href="#contact">Запись</a>',
        "mobile_new": '<a href="#path">Путь</a><a href="#methods">Подход</a><a href="#education">Образование</a><a href="#contact">Запись</a>',
        "side_old": '''        <a href="#path"><b>01</b><span>Путь</span></a>\n        <a href="#position"><b>02</b><span>Позиция</span></a>\n        <a href="#methods"><b>03</b><span>Подход</span></a>\n        <a href="#education"><b>04</b><span>Образование</span></a>\n        <a href="#scope"><b>05</b><span>Запросы</span></a>\n        <a href="#boundaries"><b>06</b><span>Границы</span></a>''',
        "side_new": '''        <a href="#path"><b>01</b><span>Путь</span></a>\n        <a href="#methods"><b>02</b><span>Подход</span></a>\n        <a href="#education"><b>03</b><span>Образование</span></a>\n        <a href="#scope"><b>04</b><span>Запросы</span></a>\n        <a href="#boundaries"><b>05</b><span>Ответственность</span></a>''',
        "meta_old": 'Образование, профессиональная позиция, подход и границы работы психолога Алины Горб.',
        "meta_new": 'Образование, подход, направления работы и профессиональная ответственность психолога Алины Горб.',
        "editorial_old": '''          <p class="section-kicker">Профессиональная интонация</p>\n          <h2 id="editorial-title">Вернуть возможность спокойно чувствовать, замечать и понимать</h2>\n          <blockquote class="profile-editorial-quote">\n            <p>Для меня важно не торопить человека с выводами и решениями. Иногда сначала нужно вернуть возможность спокойно чувствовать, замечать и понимать то, что происходит.</p>\n            <footer>Алина Горб · профессиональная позиция</footer>\n          </blockquote>''',
        "editorial_new": '''          <p class="section-kicker">Подход в работе</p>\n          <h2 id="editorial-title">Ясная цель, бережный темп и заметные изменения</h2>\n          <blockquote class="profile-editorial-quote">\n            <p>В работе для меня важны ясная цель, бережный темп и изменения, которые человек постепенно замечает в своей повседневной жизни.</p>\n            <footer>Алина Горб · о подходе к работе</footer>\n          </blockquote>''',
        "numbers": [
            ('03 · Подход в работе', '02 · Подход в работе'),
            ('04 · Образование', '03 · Образование'),
            ('05 · С чем можно обратиться', '04 · С чем можно обратиться'),
            ('06 · Профессиональная ответственность', '05 · Профессиональная ответственность'),
        ],
        "expected": [
            'Ясная цель, бережный темп и заметные изменения',
            'В работе для меня важны ясная цель, бережный темп',
            '05 · Профессиональная ответственность',
        ],
    },
}

position_pattern = r'''\n    <section class="profile-position section-block" id="position" aria-labelledby="position-title">.*?\n    </section>\n(?=\n    <section class="profile-editorial section-block")'''

for relative, cfg in ABOUT.items():
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    text = replace_once(text, cfg["mobile_old"], cfg["mobile_new"], f"{relative} mobile navigation")
    text = replace_once(text, cfg["side_old"], cfg["side_new"], f"{relative} side navigation")
    if text.count(cfg["meta_old"]) != 2:
        raise SystemExit(f"{relative}: expected two social-description matches")
    text = text.replace(cfg["meta_old"], cfg["meta_new"])
    text = sub_once(text, position_pattern, "\n", f"{relative} remove professional-position section")
    text = replace_once(text, cfg["editorial_old"], cfg["editorial_new"], f"{relative} editorial copy")
    for old, new in cfg["numbers"]:
        text = replace_once(text, old, new, f"{relative} renumber {old}")
    if '#position' in text or 'profile-position section-block' in text or 'position-principles' in text:
        raise SystemExit(f"{relative}: removed position section or navigation still present")
    for phrase in cfg["expected"]:
        if phrase not in text:
            raise SystemExit(f"{relative}: missing required copy: {phrase}")
    path.write_text(text, encoding="utf-8")

FAQ_REPLACEMENTS = {
    "consultations/index.html": (
        '''          <details><summary aria-expanded="false">Чи потрібно заздалегідь знати, з чого почати?</summary><p>Ні. Можна почати з того, що зараз найбільше турбує, або прямо сказати, що сформулювати запит поки складно.</p></details>\n          <details><summary aria-expanded="false">Чи можна звернутися без точного запиту?</summary><p>Так. На першій зустрічі можна разом визначити, що зараз потребує найбільшої уваги.</p></details>''',
        '''          <details><summary aria-expanded="false">Чи потрібно заздалегідь формулювати точний запит?</summary><p>Ні. Можна почати з того, що зараз найбільше турбує, або прямо сказати, що сформулювати запит поки складно. На першій зустрічі ми разом уточнимо, що потребує найбільшої уваги.</p></details>''',
    ),
    "ru/consultations/index.html": (
        '''          <details><summary aria-expanded="false">Нужно ли заранее знать, с чего начать?</summary><p>Нет. Можно начать с того, что сейчас больше всего беспокоит, или прямо сказать, что сформулировать запрос пока трудно.</p></details>\n          <details><summary aria-expanded="false">Можно ли обратиться без точного запроса?</summary><p>Да. На первой встрече можно вместе определить, что сейчас требует наибольшего внимания.</p></details>''',
        '''          <details><summary aria-expanded="false">Нужно ли заранее формулировать точный запрос?</summary><p>Нет. Можно начать с того, что сейчас больше всего беспокоит, или прямо сказать, что сформулировать запрос пока трудно. На первой встрече мы вместе уточним, что требует наибольшего внимания.</p></details>''',
    ),
}

for relative, (old, new) in FAQ_REPLACEMENTS.items():
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    text = replace_once(text, old, new, f"{relative} deduplicate FAQ")
    path.write_text(text, encoding="utf-8")

css_path = ROOT / "assets/css/site.about.v1.css"
css = css_path.read_text(encoding="utf-8")
marker = "/* About-page mobile booking CTA: compact footprint and safe final-section spacing. */"
if marker in css:
    raise SystemExit("About mobile CTA safety override already exists")
css += '''\n\n/* About-page mobile booking CTA: compact footprint and safe final-section spacing. */\n@media (max-width: 700px) {\n  .page-about-profile .mobile-booking-cta {\n    right: 16px;\n    bottom: calc(12px + env(safe-area-inset-bottom));\n    left: 16px;\n    width: auto;\n    min-height: 52px;\n    border-radius: 999px;\n    box-shadow: 0 14px 38px rgba(47, 48, 45, .2);\n  }\n\n  .page-about-profile .profile-final-inner {\n    padding-bottom: calc(58px + env(safe-area-inset-bottom));\n  }\n}\n'''
css_path.write_text(css, encoding="utf-8")

validator = ROOT / "scripts/validate-about-pages-v1.py"
text = validator.read_text(encoding="utf-8")
text = replace_once(
    text,
    '''REQUIRED_IDS = (\n    "about", "path", "position", "methods", "education", "scope",\n    "boundaries", "contact", "main-content",\n)''',
    '''REQUIRED_IDS = (\n    "about", "path", "methods", "education", "scope",\n    "boundaries", "contact", "main-content",\n)''',
    "About validator required IDs",
)
text = replace_once(
    text,
    '''REQUIRED_CLASSES = (\n    "profile-hero", "profile-hero-portrait", "profile-hero-facts",\n    "profile-timeline", "position-principles", "profile-method-list",\n    "profile-diploma", "scope-index", "boundaries-card", "profile-final",\n)''',
    '''REQUIRED_CLASSES = (\n    "profile-hero", "profile-hero-portrait", "profile-hero-facts",\n    "profile-timeline", "profile-editorial", "profile-method-list",\n    "profile-diploma", "scope-index", "boundaries-card", "profile-final",\n)''',
    "About validator required classes",
)
text = replace_once(text, 'require(section_count >= 9,', 'require(section_count >= 8,', "About validator section count")
text = replace_once(
    text,
    '''        ".profile-hero-layout", ".profile-section-grid", ".position-principles",\n        ".profile-method-list", ".profile-education-layout", ".scope-index",''',
    '''        ".profile-hero-layout", ".profile-section-grid", ".profile-editorial-layout",\n        ".profile-method-list", ".profile-education-layout", ".scope-index",''',
    "About validator CSS selectors",
)
insert_after = '    require("TODO" not in text and "placeholder" not in text.lower(), f"{relative}: unfinished marker found")\n'
addition = '''    require('#position' not in text and 'profile-position section-block' not in text, f"{relative}: removed professional-position section still present")\n    require('position-principles' not in text, f"{relative}: removed principle grid still present")\n    require(('Чітка мета, дбайливий темп і помітні зміни' in text) or ('Ясная цель, бережный темп и заметные изменения' in text), f"{relative}: refined editorial positioning missing")\n'''
text = replace_once(text, insert_after, insert_after + addition, "About validator refined-position checks")
validator.write_text(text, encoding="utf-8")

# Final cross-file checks.
for relative in ABOUT:
    text = (ROOT / relative).read_text(encoding="utf-8")
    if len(re.findall(r'<section\b', text, flags=re.I)) < 8:
        raise SystemExit(f"{relative}: unexpectedly short page after cleanup")

ru_consult = (ROOT / "ru/consultations/index.html").read_text(encoding="utf-8")
ua_consult = (ROOT / "consultations/index.html").read_text(encoding="utf-8")
if 'Нужно ли заранее знать, с чего начать?' in ru_consult or 'Можно ли обратиться без точного запроса?' in ru_consult:
    raise SystemExit("Russian duplicate FAQ remains")
if 'Чи потрібно заздалегідь знати, з чого почати?' in ua_consult or 'Чи можна звернутися без точного запиту?' in ua_consult:
    raise SystemExit("Ukrainian duplicate FAQ remains")

print("About-page position cleanup, editorial consolidation, FAQ deduplication and mobile CTA polish applied.")
