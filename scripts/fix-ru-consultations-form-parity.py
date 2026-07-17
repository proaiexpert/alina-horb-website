#!/usr/bin/env python3
from pathlib import Path

path = Path("ru/consultations/index.html")
text = path.read_text(encoding="utf-8")

replacements = {
    '<p class="form-guidance"><strong>Нескольких предложений достаточно.</strong> Укажите удобный контакт, язык, формат и несколько предложений о том, что происходит. Часовой пояс можно указать в сообщении.</p>':
    '<p class="form-guidance"><strong>Нескольких предложений достаточно.</strong> Укажите удобный контакт, язык, часовой пояс и интересующий формат.</p>',
    '<div class="form-field form-field-full"><label for="consult-service">Какой формат вас интересует</label><select id="consult-service" name="format" required><option value="" selected disabled>Выберите формат</option><option value="Индивидуальная онлайн-консультация">Индивидуальная онлайн-консультация</option><option value="Парная или семейная консультация">Парная или семейная консультация</option><option value="Очная консультация по согласованию">Очная консультация по согласованию</option><option value="Нужна помощь с выбором формата">Нужна помощь с выбором формата</option></select></div>':
    '<div class="form-field form-field-full"><label for="consult-service">Какой формат вас интересует</label><select id="consult-service" name="service" required><option value="" selected disabled>Выберите формат</option><option value="Индивидуальная онлайн-консультация">Индивидуальная онлайн-консультация</option><option value="Парная или семейная консультация">Парная или семейная консультация</option><option value="Очная консультация по согласованию">Очная консультация по согласованию</option><option value="Нужна помощь с выбором формата">Нужна помощь с выбором формата</option></select></div>\n            <div class="form-field"><label for="consult-timezone">Страна или часовой пояс</label><input id="consult-timezone" name="timezone" type="text" autocomplete="country-name" required maxlength="100" placeholder="Например, Германия / CET"></div>\n            <div class="form-field"><label for="consult-availability">Удобное время для связи</label><input id="consult-availability" name="availability" type="text" autocomplete="off" maxlength="160" placeholder="Дни или примерное время"></div>\n            <input name="format" type="hidden" value="Консультация со страницы условий">',
}

for old, new in replacements.items():
    if new in text:
        continue
    if old not in text:
        raise SystemExit(f"Expected Russian consultations form block not found: {old[:80]}")
    text = text.replace(old, new, 1)

path.write_text(text, encoding="utf-8")
print("Russian consultations form aligned with Ukrainian intake fields")
