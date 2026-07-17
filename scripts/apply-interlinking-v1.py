#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
changed = []


def update(relative: str, transform) -> None:
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    revised = transform(text)
    if revised == text:
        raise SystemExit(f"{relative}: expected interlinking change was not applied")
    path.write_text(revised, encoding="utf-8")
    changed.append(relative)


def replace_required(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"missing expected pattern for {label}: {old}")
    return text.replace(old, new)


# Home pages: the no-JS mobile fallback must expose the real About page.
update("index.html", lambda text: replace_required(
    text,
    '<a href="#about">Про Аліну</a>',
    '<a href="about/">Про Аліну</a>',
    "UA home About fallback",
))
update("ru/index.html", lambda text: replace_required(
    text,
    '<a href="#about">Об Алине</a>',
    '<a href="about/">Об Алине</a>',
    "RU home About fallback",
))

# About pages: every principal consultation CTA uses the canonical booking endpoint.
for relative in ("about/index.html", "ru/about/index.html"):
    update(relative, lambda text, relative=relative: replace_required(
        text,
        'href="../consultations/">',
        'href="../consultations/#contact">',
        f"{relative} canonical booking CTA",
    ))

# Consultation pages: connect specialist context and the first-consultation article.
def consultations_ua(text: str) -> str:
    text = replace_required(
        text,
        '<a class="text-link" href="#process">Подивитися, як усе відбувається</a>',
        '<a class="text-link" href="../about/">Дізнатися про Аліну та професійний підхід</a>',
        "UA consultations About link",
    )
    text = replace_required(
        text,
        '<blockquote><p>Перша зустріч допомагає визначити напрям роботи; складні зміни зазвичай потребують часу, послідовності та спільної участі.</p></blockquote>',
        '<blockquote><p>Перша зустріч допомагає визначити напрям роботи; складні зміни зазвичай потребують часу, послідовності та спільної участі.</p></blockquote>\n          <p><a class="text-link" href="../notes/first-consultation/">Докладніше: що відбувається на першій консультації</a></p>',
        "UA first-consultation article link",
    )
    return text


def consultations_ru(text: str) -> str:
    text = replace_required(
        text,
        '<a class="text-link" href="#process">Посмотреть, как всё происходит</a>',
        '<a class="text-link" href="../about/">Узнать об Алине и профессиональном подходе</a>',
        "RU consultations About link",
    )
    text = replace_required(
        text,
        '<blockquote><p>Первая встреча помогает определить направление работы; сложные изменения обычно требуют времени, последовательности и совместного участия.</p></blockquote>',
        '<blockquote><p>Первая встреча помогает определить направление работы; сложные изменения обычно требуют времени, последовательности и совместного участия.</p></blockquote>\n          <p><a class="text-link" href="../notes/first-consultation/">Подробнее: что происходит на первой консультации</a></p>',
        "RU first-consultation article link",
    )
    return text


update("consultations/index.html", consultations_ua)
update("ru/consultations/index.html", consultations_ru)

# Notes hubs: create a restrained editorial bridge from reading to consultation.
ua_notes_cta = '''

    <section class="notes-hub-conversion" aria-labelledby="notes-consultation-title">
      <div class="page-shell notes-hub-conversion-inner">
        <div><p class="section-kicker">Від матеріалів до розмови</p><h2 id="notes-consultation-title">Коли читання вже недостатньо, можна перейти до консультації</h2></div>
        <div class="notes-hub-conversion-copy"><p>Не потрібно чекати, доки з’явиться ідеальне формулювання запиту. Для першого контакту достатньо кількох речень про те, що зараз потребує уваги.</p><a class="text-link" href="../consultations/#contact">Записатися на консультацію</a></div>
      </div>
    </section>'''
ru_notes_cta = '''

    <section class="notes-hub-conversion" aria-labelledby="notes-consultation-title">
      <div class="page-shell notes-hub-conversion-inner">
        <div><p class="section-kicker">От материалов к разговору</p><h2 id="notes-consultation-title">Когда чтения уже недостаточно, можно перейти к консультации</h2></div>
        <div class="notes-hub-conversion-copy"><p>Не нужно ждать идеальной формулировки запроса. Для первого контакта достаточно нескольких предложений о том, что сейчас требует внимания.</p><a class="text-link" href="../consultations/#contact">Записаться на консультацию</a></div>
      </div>
    </section>'''

update("notes/index.html", lambda text: replace_required(text, "\n  </main>", f"{ua_notes_cta}\n  </main>", "UA Notes conversion bridge"))
update("ru/notes/index.html", lambda text: replace_required(text, "\n  </main>", f"{ru_notes_cta}\n  </main>", "RU Notes conversion bridge"))

# Article templates: author identity points to About, service context to Consultations,
# and the final conversion action to the canonical consultation form.
article_paths = sorted((ROOT / "notes").glob("*/index.html")) + sorted((ROOT / "ru/notes").glob("*/index.html"))
for path in article_paths:
    relative = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding="utf-8")
    is_ru = relative.startswith("ru/")
    prefix = "../../../" if is_ru else "../../"
    before = text

    text = text.replace("https://alinahorb.com/#about", "https://alinahorb.com/about/")
    text = text.replace("https://alinahorb.com/ru/#about", "https://alinahorb.com/ru/about/")
    text = text.replace(f'href="{prefix}#about"', f'href="{prefix}about/"')
    text = text.replace(f'href="{prefix}#contact"', f'href="{prefix}consultations/#contact"')
    text = text.replace(f'href="{prefix}#process"', f'href="{prefix}consultations/#process"')

    if text == before:
        raise SystemExit(f"{relative}: no article interlinking replacements applied")
    path.write_text(text, encoding="utf-8")
    changed.append(relative)

# Shared chrome fallbacks must never send About or Contact traffic to obsolete home anchors.
def chrome_links(text: str) -> str:
    text = replace_required(text, '[text.about, `${homeHref}#about`]', '[text.about, `${homeHref}about/`]', "shared About route")
    text = replace_required(text, '[text.contact, `${homeHref}#contact`]', '[text.contact, `${homeHref}consultations/#contact`]', "shared booking route")
    return text


update("assets/js/site.chrome.v3.js", chrome_links)

# Premium Notes conversion treatment, shared by UA and RU hubs.
def notes_css(text: str) -> str:
    marker = "/* Interlinking V1: editorial bridge from materials to consultation. */"
    if marker in text:
        raise SystemExit("Notes interlinking styles already present")
    return text.rstrip() + '''

/* Interlinking V1: editorial bridge from materials to consultation. */
.notes-hub-conversion {
  position: relative;
  overflow: hidden;
  border-top: 1px solid var(--line-strong);
  padding-block: clamp(72px, 9vw, 118px);
  background:
    radial-gradient(circle at 88% 18%, rgba(135, 146, 127, .16), transparent 25rem),
    var(--ivory);
}
.notes-hub-conversion::before {
  position: absolute;
  top: -180px;
  right: -120px;
  width: 430px;
  height: 430px;
  border: 1px solid rgba(198, 83, 63, .14);
  border-radius: 50%;
  pointer-events: none;
  content: "";
}
.notes-hub-conversion-inner {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: minmax(0, 1.18fr) minmax(300px, .82fr);
  gap: clamp(48px, 8vw, 112px);
  align-items: end;
}
.notes-hub-conversion h2 {
  max-width: 760px;
  margin: 0;
  font-size: clamp(50px, 5.7vw, 78px);
  line-height: .92;
  text-wrap: balance;
}
.notes-hub-conversion-copy {
  max-width: 520px;
  border-top: 1px solid var(--line-strong);
  padding-top: 24px;
}
.notes-hub-conversion-copy p {
  margin: 0 0 26px;
  color: var(--muted);
  font-size: 15px;
  line-height: 1.75;
}
@media (max-width: 800px) {
  .notes-hub-conversion-inner { grid-template-columns: minmax(0, 1fr); gap: 34px; }
  .notes-hub-conversion-copy { max-width: none; }
}
@media (max-width: 520px) {
  .notes-hub-conversion { padding-block: 62px; }
  .notes-hub-conversion h2 { font-size: 46px; }
}
'''


update("assets/css/site.notes-hub.v3-2.css", notes_css)

print("Interlinking V1 applied:")
for relative in changed:
    print(f"- {relative}")
