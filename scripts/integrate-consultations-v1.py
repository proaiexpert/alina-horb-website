#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: str, old: str, new: str, label: str) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    if new in text:
        return
    if old not in text:
        raise SystemExit(f"{path}: patch point missing: {label}")
    target.write_text(text.replace(old, new, 1), encoding="utf-8")


def insert_after(path: str, anchor: str, addition: str, label: str) -> None:
    replace_once(path, anchor, anchor + addition, label)


replace_once(
    "assets/js/site.v2.js",
    '      fields: { name: "Ім’я", reply: "Контакт", channel: "Спосіб зв’язку", language: "Мова", format: "Формат", message: "Повідомлення" }',
    '      fields: { name: "Ім’я", reply: "Контакт", channel: "Спосіб зв’язку", language: "Мова", format: "Формат", service: "Тип консультації", timezone: "Країна або часовий пояс", availability: "Зручний час", message: "Повідомлення" }',
    "Ukrainian form labels",
)
replace_once(
    "assets/js/site.v2.js",
    '      fields: { name: "Имя", reply: "Контакт", channel: "Способ связи", language: "Язык", format: "Формат", message: "Сообщение" }',
    '      fields: { name: "Имя", reply: "Контакт", channel: "Способ связи", language: "Язык", format: "Формат", service: "Тип консультации", timezone: "Страна или часовой пояс", availability: "Удобное время", message: "Сообщение" }',
    "Russian form labels",
)
replace_once(
    "assets/js/site.v2.js",
    '''        channel: String(data.get("channel") || "").trim(), language: String(data.get("language") || "").trim(),
        format: String(data.get("format") || "").trim(), message: String(data.get("message") || "").trim(),
        consent: data.get("consent") === "on", locale, subject: text.subject, source: window.location.href''',
    '''        channel: String(data.get("channel") || "").trim(), language: String(data.get("language") || "").trim(),
        format: String(data.get("format") || "").trim(), service: String(data.get("service") || "").trim(),
        timezone: String(data.get("timezone") || "").trim(), availability: String(data.get("availability") || "").trim(),
        message: String(data.get("message") || "").trim(),
        consent: data.get("consent") === "on", locale, subject: text.subject, source: window.location.href''',
    "extended form payload",
)
replace_once(
    "assets/js/site.v2.js",
    '''        `${fields.name}: ${payload.name}`, `${fields.reply}: ${payload.reply}`, `${fields.channel}: ${payload.channel}`,
        `${fields.language}: ${payload.language}`, `${fields.format}: ${payload.format}`, "", `${fields.message}:`, payload.message
      ].join("\\n");''',
    '''        `${fields.name}: ${payload.name}`, `${fields.reply}: ${payload.reply}`, `${fields.channel}: ${payload.channel}`,
        `${fields.language}: ${payload.language}`, `${fields.format}: ${payload.format}`,
        payload.service ? `${fields.service}: ${payload.service}` : null,
        payload.timezone ? `${fields.timezone}: ${payload.timezone}` : null,
        payload.availability ? `${fields.availability}: ${payload.availability}` : null,
        "", `${fields.message}:`, payload.message
      ].filter((line) => line !== null).join("\\n");''',
    "extended mail fallback",
)

insert_after(
    "scripts/apply-indexing-launch-v3-2.py",
    '    "ru/about/index.html",\n',
    '    "consultations/index.html",\n    "ru/consultations/index.html",\n',
    "indexing routes",
)
insert_after(
    "scripts/validate-release-readiness.py",
    '    ("ru/about/index.html", f"{BASE}/ru/about/", f"{BASE}/about/", f"{BASE}/ru/about/"),\n',
    '    ("consultations/index.html", f"{BASE}/consultations/", f"{BASE}/consultations/", f"{BASE}/ru/consultations/"),\n    ("ru/consultations/index.html", f"{BASE}/ru/consultations/", f"{BASE}/consultations/", f"{BASE}/ru/consultations/"),\n',
    "release routes",
)
insert_after(
    "sitemap.xml",
    '  <url><loc>https://alinahorb.com/ru/about/</loc><lastmod>2026-07-16</lastmod></url>\n',
    '  <url><loc>https://alinahorb.com/consultations/</loc><lastmod>2026-07-17</lastmod></url>\n  <url><loc>https://alinahorb.com/ru/consultations/</loc><lastmod>2026-07-17</lastmod></url>\n',
    "sitemap consultations routes",
)

insert_after(".github/workflows/deploy-pages.yml", '          python3 scripts/validate-about-pages-v1.py\n', '          python3 scripts/validate-consultations-pages-v1.py\n', "deployment consultations validation")
insert_after(".github/workflows/deploy-pages.yml", '          cp -R about _site/\n', '          cp -R consultations _site/\n', "deployment route copy")
insert_after(".github/workflows/deploy-pages.yml", '          test -f _site/assets/css/site.about.v1.css\n', '          test -f _site/assets/css/site.consultations.v1.css\n', "deployment CSS assertion")
insert_after(".github/workflows/deploy-pages.yml", '          test -f _site/about/index.html\n', '          test -f _site/consultations/index.html\n', "deployment UA route assertion")
insert_after(".github/workflows/deploy-pages.yml", '          test -f _site/ru/about/index.html\n', '          test -f _site/ru/consultations/index.html\n', "deployment RU route assertion")
insert_after(
    ".github/workflows/deploy-pages.yml",
    '          grep -q \'content="index, follow, max-image-preview:large"\' _site/ru/about/index.html\n',
    '          grep -q \'content="index, follow, max-image-preview:large"\' _site/consultations/index.html\n          grep -q \'content="index, follow, max-image-preview:large"\' _site/ru/consultations/index.html\n',
    "deployment indexing assertions",
)

replace_once("index.html", '<a class="text-link" href="#process">Дізнатися, як проходить консультація</a>', '<a class="text-link" href="consultations/">Формат і умови консультації</a>', "UA hero consultation link")
replace_once("index.html", '<a href="#support">Підтримка</a><a href="#about">Про Аліну</a>', '<a href="#support">Підтримка</a><a href="consultations/">Консультації</a><a href="#about">Про Аліну</a>', "UA mobile navigation")
insert_after("index.html", '        <a href="about/">Про Аліну</a>\n', '        <a href="consultations/">Консультації</a>\n', "UA footer consultation link")
replace_once("ru/index.html", '<a class="text-link" href="#process">Узнать, как проходит консультация</a>', '<a class="text-link" href="consultations/">Формат и условия консультации</a>', "RU hero consultation link")
replace_once("ru/index.html", '<a href="#support">Поддержка</a><a href="#about">Об Алине</a>', '<a href="#support">Поддержка</a><a href="consultations/">Консультации</a><a href="#about">Об Алине</a>', "RU mobile navigation")
insert_after("ru/index.html", '<a href="about/">Об Алине</a>', '<a href="consultations/">Консультации</a>', "RU footer consultation link")

replace_once("about/index.html", '<a class="button button-filled" href="#contact">Записатися на консультацію</a>', '<a class="button button-filled" href="../consultations/">Записатися на консультацію</a>', "UA About hero CTA")
replace_once("about/index.html", '<a class="button button-filled" href="../#contact">Записатися на консультацію</a>', '<a class="button button-filled" href="../consultations/#contact">Записатися на консультацію</a>', "UA About final CTA")
replace_once("about/index.html", '<a class="mobile-booking-cta" href="../#contact"', '<a class="mobile-booking-cta" href="../consultations/#contact"', "UA About mobile CTA")
insert_after("about/index.html", '        <a href="../">Головна</a>\n', '        <a href="../consultations/">Консультації</a>\n', "UA About footer consultation link")
replace_once("ru/about/index.html", '<a class="button button-filled" href="#contact">Записаться на консультацию</a>', '<a class="button button-filled" href="../consultations/">Записаться на консультацию</a>', "RU About hero CTA")
replace_once("ru/about/index.html", '<a class="button button-filled" href="../#contact">Записаться на консультацию</a>', '<a class="button button-filled" href="../consultations/#contact">Записаться на консультацию</a>', "RU About final CTA")
replace_once("ru/about/index.html", '<a class="mobile-booking-cta" href="../#contact"', '<a class="mobile-booking-cta" href="../consultations/#contact"', "RU About mobile CTA")
insert_after("ru/about/index.html", '        <a href="../">Главная</a>', '<a href="../consultations/">Консультации</a>', "RU About footer consultation link")

print("Consultations pages integrated into the bilingual production site")
