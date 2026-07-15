#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count == 1:
        return text.replace(old, new, 1)
    if count == 0 and new in text:
        return text
    raise RuntimeError(f"Expected one {label}; found {count}")


def update_ua() -> None:
    path = ROOT / "index.html"
    text = path.read_text(encoding="utf-8")

    text = replace_once(
        text,
        '          <h3>Коротке звернення</h3>\n          <form class="contact-form" data-contact-form data-locale="uk" novalidate>',
        '          <h3>Коротке звернення</h3>\n          <p class="form-guidance"><strong>Для першого контакту достатньо кількох речень.</strong> Не надсилайте медичні документи, діагнози, копії посвідчень, платіжні дані або докладний опис кризової ситуації.</p>\n          <form class="contact-form" data-contact-form data-locale="uk" novalidate>\n            <div class="form-honeypot" aria-hidden="true"><label for="contact-website">Не заповнюйте це поле</label><input id="contact-website" name="website" type="text" tabindex="-1" autocomplete="off"></div>\n            <input name="startedAt" type="hidden" value="">',
        "UA form introduction",
    )
    text = replace_once(
        text,
        '<textarea id="contact-message" name="message" required maxlength="1200"></textarea>',
        '<textarea id="contact-message" name="message" required minlength="3" maxlength="600" aria-describedby="contact-message-help"></textarea><p id="contact-message-help" class="form-privacy-note">Коротко опишіть організаційне запитання або те, з чим хотіли б звернутися. Екстрені звернення через форму не обробляються.</p>',
        "UA message field",
    )
    text = replace_once(
        text,
        '<span>Я погоджуюся на надсилання цього звернення та обробку вказаних контактних даних для відповіді.</span>',
        '<span>Я погоджуюся на надсилання звернення та обробку вказаних контактних даних для відповіді відповідно до <a href="privacy/">Політики конфіденційності</a>.</span>',
        "UA consent",
    )
    text = replace_once(
        text,
        '<p class="contact-note">Не надсилайте у першому повідомленні медичні документи, кризові подробиці або інші чутливі дані.</p>',
        '<p class="contact-note">Не надсилайте у першому повідомленні медичні документи, кризові подробиці або інші чутливі дані. Сайт і форма не є екстреною службою.</p>',
        "UA contact warning",
    )
    text = replace_once(
        text,
        '<a href="mailto:hello@alinahorb.com">Email</a>\n        <a href="https://t.me/alina_horb1991"',
        '<a href="mailto:hello@alinahorb.com">Email</a>\n        <a href="privacy/">Конфіденційність</a>\n        <a href="https://t.me/alina_horb1991"',
        "UA footer privacy link",
    )
    path.write_text(text, encoding="utf-8")


def update_ru() -> None:
    path = ROOT / "ru/index.html"
    text = path.read_text(encoding="utf-8")

    text = replace_once(
        text,
        '<div class="contact-form-wrap" data-reveal><h3>Короткое обращение</h3><form class="contact-form" data-contact-form data-locale="ru" novalidate>',
        '<div class="contact-form-wrap" data-reveal><h3>Короткое обращение</h3><p class="form-guidance"><strong>Для первого контакта достаточно нескольких предложений.</strong> Не отправляйте медицинские документы, диагнозы, копии удостоверений, платёжные данные или подробное описание кризисной ситуации.</p><form class="contact-form" data-contact-form data-locale="ru" novalidate><div class="form-honeypot" aria-hidden="true"><label for="contact-website-ru">Не заполняйте это поле</label><input id="contact-website-ru" name="website" type="text" tabindex="-1" autocomplete="off"></div><input name="startedAt" type="hidden" value="">',
        "RU form introduction",
    )
    text = replace_once(
        text,
        '<textarea id="contact-message-ru" name="message" required maxlength="1200"></textarea>',
        '<textarea id="contact-message-ru" name="message" required minlength="3" maxlength="600" aria-describedby="contact-message-help-ru"></textarea><p id="contact-message-help-ru" class="form-privacy-note">Коротко опишите организационный вопрос или то, с чем хотели бы обратиться. Экстренные обращения через форму не обрабатываются.</p>',
        "RU message field",
    )
    text = replace_once(
        text,
        '<span>Я соглашаюсь на отправку этого обращения и обработку указанных контактных данных для ответа.</span>',
        '<span>Я соглашаюсь на отправку обращения и обработку указанных контактных данных для ответа в соответствии с <a href="privacy/">Политикой конфиденциальности</a>.</span>',
        "RU consent",
    )
    text = replace_once(
        text,
        '<p class="contact-note">Не отправляйте в первом сообщении медицинские документы, кризисные подробности или другие чувствительные данные.</p>',
        '<p class="contact-note">Не отправляйте в первом сообщении медицинские документы, кризисные подробности или другие чувствительные данные. Сайт и форма не являются экстренной службой.</p>',
        "RU contact warning",
    )
    text = replace_once(
        text,
        '<a href="mailto:hello@alinahorb.com">Email</a><a href="https://t.me/alina_horb1991"',
        '<a href="mailto:hello@alinahorb.com">Email</a><a href="privacy/">Конфиденциальность</a><a href="https://t.me/alina_horb1991"',
        "RU footer privacy link",
    )
    path.write_text(text, encoding="utf-8")


def main() -> None:
    update_ua()
    update_ru()
    print("Applied V3.2 privacy intake markup.")


if __name__ == "__main__":
    main()
