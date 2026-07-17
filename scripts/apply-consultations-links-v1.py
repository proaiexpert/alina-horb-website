#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(relative: str, old: str, new: str, label: str) -> None:
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    if new in text:
        return
    if old not in text:
        raise SystemExit(f"Consultations link patch point missing in {relative}: {label}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


replace_once("index.html", '<a class="text-link" href="#process">Дізнатися, як проходить консультація</a>', '<a class="text-link" href="consultations/">Формат і умови консультації</a>', "UA home hero link")
replace_once("index.html", '<a href="#about">Про Аліну</a><a href="#notes">Нотатки</a>', '<a href="#about">Про Аліну</a><a href="consultations/">Консультації</a><a href="#notes">Нотатки</a>', "UA home mobile navigation")
replace_once("index.html", '<a href="about/">Про Аліну</a>\n        <a href="mailto:hello@alinahorb.com">Email</a>', '<a href="about/">Про Аліну</a>\n        <a href="consultations/">Консультації</a>\n        <a href="mailto:hello@alinahorb.com">Email</a>', "UA home footer")

replace_once("ru/index.html", '<a class="text-link" href="#process">Узнать, как проходит консультация</a>', '<a class="text-link" href="consultations/">Формат и условия консультации</a>', "RU home hero link")
replace_once("ru/index.html", '<a href="#about">Об Алине</a><a href="#notes">Заметки</a>', '<a href="#about">Об Алине</a><a href="consultations/">Консультации</a><a href="#notes">Заметки</a>', "RU home mobile navigation")
replace_once("ru/index.html", '<a href="about/">Об Алине</a><a href="mailto:hello@alinahorb.com">Email</a>', '<a href="about/">Об Алине</a><a href="consultations/">Консультации</a><a href="mailto:hello@alinahorb.com">Email</a>', "RU home footer")

replace_once("about/index.html", '<a class="button button-filled" href="#contact">Записатися на консультацію</a>', '<a class="button button-filled" href="../consultations/">Записатися на консультацію</a>', "UA About hero CTA")
replace_once("about/index.html", '<a class="button button-filled" href="../#contact">Записатися на консультацію</a>', '<a class="button button-filled" href="../consultations/#contact">Записатися на консультацію</a>', "UA About final CTA")
replace_once("about/index.html", '<a class="mobile-booking-cta" href="../#contact" data-mobile-booking-cta hidden>Записатися</a>', '<a class="mobile-booking-cta" href="../consultations/#contact" data-mobile-booking-cta hidden>Записатися</a>', "UA About mobile CTA")
replace_once("about/index.html", '<a href="../">Головна</a>\n        <a href="../notes/">Нотатки</a>', '<a href="../">Головна</a>\n        <a href="../consultations/">Консультації</a>\n        <a href="../notes/">Нотатки</a>', "UA About footer")

replace_once("ru/about/index.html", '<a class="button button-filled" href="#contact">Записаться на консультацию</a>', '<a class="button button-filled" href="../consultations/">Записаться на консультацию</a>', "RU About hero CTA")
replace_once("ru/about/index.html", '<a class="button button-filled" href="../#contact">Записаться на консультацию</a>', '<a class="button button-filled" href="../consultations/#contact">Записаться на консультацию</a>', "RU About final CTA")
replace_once("ru/about/index.html", '<a class="mobile-booking-cta" href="../#contact" data-mobile-booking-cta hidden>Записаться</a>', '<a class="mobile-booking-cta" href="../consultations/#contact" data-mobile-booking-cta hidden>Записаться</a>', "RU About mobile CTA")
replace_once("ru/about/index.html", '<a href="../">Главная</a>\n        <a href="../notes/">Заметки</a>', '<a href="../">Главная</a>\n        <a href="../consultations/">Консультации</a>\n        <a href="../notes/">Заметки</a>', "RU About footer")

print("Consultations navigation links applied to UA/RU home and About pages")
