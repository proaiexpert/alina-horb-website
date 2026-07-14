#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise SystemExit(f"{label}: source text not found")
    return text.replace(old, new, 1)


def replace_regex(text: str, pattern: str, replacement: str, label: str) -> str:
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.S)
    if count != 1:
        raise SystemExit(f"{label}: expected 1 replacement, got {count}")
    return updated


# Site config
config_path = ROOT / "assets/js/site-config.v2.js"
config = config_path.read_text(encoding="utf-8")
config = config.replace('telegramUsername: ""', 'telegramUsername: "alina_horb1991"')
config_path.write_text(config, encoding="utf-8")

# Ukrainian page
ua_path = ROOT / "index.html"
ua = ua_path.read_text(encoding="utf-8")
ua = replace_once(
    ua,
    'Аліна — психолог для підлітків від 17 років, дорослих, жінок, чоловіків і сімейних звернень. Консультації українською та російською під час стресу, кризи, емоційного виснаження й складних змін. Онлайн; очно — за попереднім погодженням.',
    'Аліна — психолог для людей різного віку, пар і сімей. Формат роботи з неповнолітніми узгоджується окремо. Консультації українською та російською під час стресу, кризи, емоційного виснаження й складних змін. Онлайн; очно — за попереднім погодженням.',
    'UA hero audience',
)
ua = replace_once(
    ua,
    'Я — Аліна Горб, психолог і магістр психології. Практикую з 2016 року. Працюю з підлітками від 17 років, дорослими, жінками, чоловіками та сімейними зверненнями.',
    'Я — Аліна Горб, психолог і магістр психології. Практикую з 2016 року. Працюю з людьми різного віку, парами та сімейними зверненнями; формат роботи з неповнолітніми узгоджується окремо.',
    'UA about audience',
)
ua_topics = '''<div class="topics-list">
          <article class="topic-row" data-reveal><h3>Війна та вимушене переміщення</h3><p>Психологічна підтримка людей, які постраждали від війни, зокрема внутрішньо переміщених осіб, під час адаптації, втрати звичної опори та тривалої невизначеності.</p></article>
          <article class="topic-row" data-reveal><h3>Гострий і хронічний стрес</h3><p>Тривале напруження, виснаження, перевантаження, порушення відновлення та потреба стабілізувати стан.</p></article>
          <article class="topic-row" data-reveal><h3>Панічні атаки та їх наслідки</h3><p>Страх повторення нападу, тілесна тривога, уникання ситуацій і поступове повернення відчуття безпеки.</p></article>
          <article class="topic-row" data-reveal><h3>Тривожні стани</h3><p>Постійне занепокоєння, напруга, труднощі зі сном і психологічна підтримка при діагностованих тривожних розладах.</p></article>
          <article class="topic-row" data-reveal><h3>Травматичний досвід і симптоми ПТСР</h3><p>Нав’язливі спогади, уникання, підвищена настороженість та інші наслідки травматичних подій — без самодіагностики й обіцянок результату.</p></article>
          <article class="topic-row" data-reveal><h3>Нав’язливі думки та прояви ОКР</h3><p>Повторювані тривожні думки, ритуали й дії, які забирають час, посилюють напругу або ускладнюють повсякденне життя.</p></article>
          <article class="topic-row" data-reveal><h3>Домашнє насильство</h3><p>Психологічна підтримка, відновлення відчуття опори, робота з наслідками контролю, приниження, погроз або іншого насильства.</p></article>
          <article class="topic-row" data-reveal><h3>Кризи, стосунки та сім’я</h3><p>Втрати, розриви, конфлікти, повторювані сценарії, сімейні звернення та складні життєві зміни.</p></article>
        </div>
        <aside class="safety-notice" data-reveal aria-label="Важливо про кризові звернення"><strong>Важливо.</strong> Можна звернутися по первинну психологічну підтримку при гострому стресі або повторюваних думках про самогубство чи самопошкодження. Сайт і форма не є екстреною службою. Якщо є безпосередня загроза життю, конкретний план або неможливо залишатися в безпеці, негайно зверніться до місцевих екстрених чи кризових служб.</aside>'''
ua = replace_regex(ua, r'<div class="topics-list">.*?</div>\s*</div>\s*</section>', ua_topics + '\n      </div>\n    </section>', 'UA topics')
ua = replace_regex(
    ua,
    r'<ul class="contact-list">.*?</ul>',
    '''<ul class="contact-list">
            <li><strong>Telegram</strong><a class="contact-link" data-telegram-link href="https://t.me/alina_horb1991" target="_blank" rel="noopener noreferrer">@alina_horb1991</a></li>
            <li><strong>Instagram</strong><a class="contact-link" href="https://instagram.com/ng_alina_dp" target="_blank" rel="noopener noreferrer">@ng_alina_dp</a></li>
            <li><strong>Email</strong><a class="contact-link" href="mailto:alinahorb1991@gmail.com">alinahorb1991@gmail.com</a></li>
            <li><strong>Що буде далі</strong><span>Аліна відповість, уточнить організаційні деталі та запропонує доступний час.</span></li>
          </ul>''',
    'UA contacts',
)
ua = ua.replace('<option value="Telegram">Telegram</option><option value="Email">Email</option>', '<option value="Telegram">Telegram</option><option value="Instagram">Instagram</option><option value="Email">Email</option>')
ua = ua.replace('<span>© Аліна Горб, 2026</span>', '<a href="https://t.me/alina_horb1991" target="_blank" rel="noopener noreferrer">Telegram</a><a href="https://instagram.com/ng_alina_dp" target="_blank" rel="noopener noreferrer">Instagram</a><span>© Аліна Горб, 2026</span>')
ua_path.write_text(ua, encoding="utf-8")

# Russian page
ru_path = ROOT / "ru/index.html"
ru = ru_path.read_text(encoding="utf-8")
ru = replace_once(
    ru,
    'Алина — психолог для подростков от 17 лет, взрослых, женщин, мужчин и семейных обращений. Консультации на русском и украинском во время стресса, кризиса, эмоционального истощения и сложных перемен. Онлайн; очно — по предварительному согласованию.',
    'Алина — психолог для людей разного возраста, пар и семей. Формат работы с несовершеннолетними согласуется отдельно. Консультации на русском и украинском во время стресса, кризиса, эмоционального истощения и сложных перемен. Онлайн; очно — по предварительному согласованию.',
    'RU hero audience',
)
ru = replace_once(
    ru,
    'Я — Алина Горб, психолог и магистр психологии. Практикую с 2016 года. Работаю с подростками от 17 лет, взрослыми, женщинами, мужчинами и семейными обращениями.',
    'Я — Алина Горб, психолог и магистр психологии. Практикую с 2016 года. Работаю с людьми разного возраста, парами и семейными обращениями; формат работы с несовершеннолетними согласуется отдельно.',
    'RU about audience',
)
ru_topics = '''<div class="topics-list"><article class="topic-row" data-reveal><h3>Война и вынужденное перемещение</h3><p>Психологическая поддержка людей, пострадавших от войны, включая внутренне перемещённых лиц, во время адаптации, потери привычной опоры и длительной неопределённости.</p></article><article class="topic-row" data-reveal><h3>Острый и хронический стресс</h3><p>Длительное напряжение, истощение, перегрузка, трудности с восстановлением и потребность стабилизировать состояние.</p></article><article class="topic-row" data-reveal><h3>Панические атаки и их последствия</h3><p>Страх повторения приступа, телесная тревога, избегание ситуаций и постепенное возвращение чувства безопасности.</p></article><article class="topic-row" data-reveal><h3>Тревожные состояния</h3><p>Постоянное беспокойство, напряжение, трудности со сном и психологическая поддержка при диагностированных тревожных расстройствах.</p></article><article class="topic-row" data-reveal><h3>Травматический опыт и симптомы ПТСР</h3><p>Навязчивые воспоминания, избегание, повышенная настороженность и другие последствия травматических событий — без самодиагностики и обещаний результата.</p></article><article class="topic-row" data-reveal><h3>Навязчивые мысли и проявления ОКР</h3><p>Повторяющиеся тревожные мысли, ритуалы и действия, которые отнимают время, усиливают напряжение или осложняют повседневную жизнь.</p></article><article class="topic-row" data-reveal><h3>Домашнее насилие</h3><p>Психологическая поддержка, восстановление чувства опоры, работа с последствиями контроля, унижения, угроз или другого насилия.</p></article><article class="topic-row" data-reveal><h3>Кризисы, отношения и семья</h3><p>Потери, расставания, конфликты, повторяющиеся сценарии, семейные обращения и сложные жизненные перемены.</p></article></div><aside class="safety-notice" data-reveal aria-label="Важно о кризисных обращениях"><strong>Важно.</strong> Можно обратиться за первичной психологической поддержкой при остром стрессе или повторяющихся мыслях о самоубийстве либо самоповреждении. Сайт и форма не являются экстренной службой. При непосредственной угрозе жизни, наличии конкретного плана или невозможности оставаться в безопасности немедленно обратитесь в местные экстренные или кризисные службы.</aside>'''
ru = replace_regex(ru, r'<div class="topics-list">.*?</div></div></section>', ru_topics + '</div></section>', 'RU topics')
ru = replace_regex(
    ru,
    r'<ul class="contact-list">.*?</ul>',
    '<ul class="contact-list"><li><strong>Telegram</strong><a class="contact-link" data-telegram-link href="https://t.me/alina_horb1991" target="_blank" rel="noopener noreferrer">@alina_horb1991</a></li><li><strong>Instagram</strong><a class="contact-link" href="https://instagram.com/ng_alina_dp" target="_blank" rel="noopener noreferrer">@ng_alina_dp</a></li><li><strong>Email</strong><a class="contact-link" href="mailto:alinahorb1991@gmail.com">alinahorb1991@gmail.com</a></li><li><strong>Что будет дальше</strong><span>Алина ответит, уточнит организационные детали и предложит доступное время.</span></li></ul>',
    'RU contacts',
)
ru = ru.replace('<option value="Telegram">Telegram</option><option value="Email">Email</option>', '<option value="Telegram">Telegram</option><option value="Instagram">Instagram</option><option value="Email">Email</option>')
ru = ru.replace('<span>© Алина Горб, 2026</span>', '<a href="https://t.me/alina_horb1991" target="_blank" rel="noopener noreferrer">Telegram</a><a href="https://instagram.com/ng_alina_dp" target="_blank" rel="noopener noreferrer">Instagram</a><span>© Алина Горб, 2026</span>')
ru_path.write_text(ru, encoding="utf-8")

# CSS
css_path = ROOT / "assets/css/site.v2.css"
css = css_path.read_text(encoding="utf-8")
if '.safety-notice {' not in css:
    css += '''\n\n.safety-notice {\n  grid-column: 1 / -1;\n  margin-top: 30px;\n  border: 1px solid rgba(198, 83, 63, .32);\n  padding: 22px 24px;\n  background: rgba(198, 83, 63, .055);\n  color: var(--muted);\n  font-size: 14px;\n  line-height: 1.75;\n}\n.safety-notice strong { color: var(--graphite); }\n@media (max-width: 700px) { .safety-notice { padding: 18px; font-size: 13px; } }\n'''
css_path.write_text(css, encoding="utf-8")

print('Contacts and safety update applied.')
