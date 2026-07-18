#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def write(relative: str, text: str) -> None:
    (ROOT / relative).write_text(text, encoding="utf-8")


def replace_once(text: str, old: str, new: str, relative: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{relative}: expected one occurrence of {old!r}, found {count}")
    return text.replace(old, new, 1)


def replace_form(relative: str, locale: str, variant: str) -> None:
    text = read(relative)
    is_ru = locale == "ru"
    is_consult = variant == "consult"

    if is_ru:
        guidance = (
            '<p class="form-guidance"><strong>Заполните имя, контакт и короткое сообщение.</strong> '
            'Остальные организационные поля — необязательные.</p>'
        )
        required = "обязательно"
        optional = "необязательно"
        name_label = "Имя"
        contact_label = "Ваш контакт"
        contact_placeholder = "@username, телефон или email"
        channel_label = "Как удобнее ответить"
        channel_empty = "Можно не выбирать"
        service_label = "Формат консультации"
        timezone_label = "Страна или часовой пояс"
        timezone_placeholder = "Например, Германия / CET"
        availability_label = "Удобное время для связи"
        availability_placeholder = "Дни или примерное время"
        message_label = "Коротко о запросе или вопросе"
        message_help = "Достаточно нескольких предложений. Не отправляйте документы, платёжные данные или подробное описание кризисной ситуации."
        consent = 'Я соглашаюсь на отправку обращения и обработку указанных контактных данных для ответа в соответствии с'
        privacy_label = "Политикой конфиденциальности"
        submit = "Отправить обращение"
        success_kicker = "Обращение отправлено"
        success_title = "Спасибо. Сообщение получено."
        success_text = "Алина ответит по указанному контакту и предложит доступное время или уточнит организационные детали."
    else:
        guidance = (
            '<p class="form-guidance"><strong>Заповніть ім’я, контакт і коротке повідомлення.</strong> '
            'Решта організаційних полів — необов’язкові.</p>'
        )
        required = "обов’язково"
        optional = "необов’язково"
        name_label = "Ім’я"
        contact_label = "Ваш контакт"
        contact_placeholder = "@username, телефон або email"
        channel_label = "Як зручніше відповісти"
        channel_empty = "Можна не обирати"
        service_label = "Формат консультації"
        timezone_label = "Країна або часовий пояс"
        timezone_placeholder = "Наприклад, Німеччина / CET"
        availability_label = "Зручний час для зв’язку"
        availability_placeholder = "Дні або приблизний час"
        message_label = "Коротко про запит або запитання"
        message_help = "Достатньо кількох речень. Не надсилайте документи, платіжні дані або докладний опис кризової ситуації."
        consent = 'Я погоджуюся на надсилання звернення та обробку вказаних контактних даних для відповіді відповідно до'
        privacy_label = "Політики конфіденційності"
        submit = "Надіслати звернення"
        success_kicker = "Звернення надіслано"
        success_title = "Дякуємо. Повідомлення отримано."
        success_text = "Аліна відповість за вказаним контактом і запропонує доступний час або уточнить організаційні деталі."

    if relative == "index.html":
        ids = {key: f"contact-{key}" for key in ("website", "name", "reply", "channel", "service", "timezone", "availability", "message", "message-help", "consent")}
        privacy_href = "privacy/"
    elif relative == "ru/index.html":
        ids = {key: f"contact-{key}-ru" for key in ("website", "name", "reply", "channel", "service", "timezone", "availability", "message", "message-help", "consent")}
        privacy_href = "privacy/"
    else:
        ids = {key: f"consult-{key}" for key in ("website", "name", "reply", "channel", "service", "timezone", "availability", "message", "message-help", "consent")}
        privacy_href = "../privacy/"

    if is_consult:
        if is_ru:
            service_options = [
                ("Индивидуальная онлайн-консультация", "Индивидуальная онлайн-консультация"),
                ("Парная или семейная консультация", "Парная или семейная консультация"),
                ("Очная консультация по согласованию", "Очная консультация по согласованию"),
                ("Нужна помощь с выбором формата", "Нужна помощь с выбором формата"),
            ]
        else:
            service_options = [
                ("Індивідуальна онлайн-консультація", "Індивідуальна онлайн-консультація"),
                ("Парна або сімейна консультація", "Парна або сімейна консультація"),
                ("Очна консультація за погодженням", "Очна консультація за погодженням"),
                ("Потрібна допомога з вибором формату", "Потрібна допомога з вибором формату"),
            ]
    else:
        if is_ru:
            service_options = [
                ("Онлайн", "Онлайн"),
                ("Очно по предварительному согласованию", "Очно по предварительному согласованию"),
                ("Нужна помощь с выбором формата", "Нужна помощь с выбором формата"),
            ]
        else:
            service_options = [
                ("Онлайн", "Онлайн"),
                ("Очно за попереднім погодженням", "Очно за попереднім погодженням"),
                ("Потрібна допомога з вибором формату", "Потрібна допомога з вибором формату"),
            ]

    options = "".join(f'<option value="{value}">{label}</option>' for value, label in service_options)
    form_html = f'''<form class="contact-form" data-contact-form data-locale="{locale}" novalidate>
            <div class="form-honeypot" aria-hidden="true"><label for="{ids['website']}">{'Не заполняйте это поле' if is_ru else 'Не заповнюйте це поле'}</label><input id="{ids['website']}" name="website" type="text" tabindex="-1" autocomplete="off"></div>
            <input name="startedAt" type="hidden" value="">
            <div class="form-field"><label for="{ids['name']}">{name_label}<span class="field-flag field-required">{required}</span></label><input id="{ids['name']}" name="name" type="text" autocomplete="name" required maxlength="100"></div>
            <div class="form-field"><label for="{ids['reply']}">{contact_label}<span class="field-flag field-required">{required}</span></label><input id="{ids['reply']}" name="reply" type="text" autocomplete="off" required maxlength="160" placeholder="{contact_placeholder}"></div>
            <div class="form-field"><label for="{ids['channel']}">{channel_label}<span class="field-flag field-optional">{optional}</span></label><select id="{ids['channel']}" name="channel"><option value="" selected>{channel_empty}</option><option value="Telegram">Telegram</option><option value="Instagram">Instagram</option><option value="Email">Email</option><option value="Телефон">{'Телефон' if is_ru else 'Телефон'}</option></select></div>
            <div class="form-field form-field-full"><label for="{ids['service']}">{service_label}<span class="field-flag field-optional">{optional}</span></label><select id="{ids['service']}" name="service"><option value="" selected>{channel_empty}</option>{options}</select></div>
            <div class="form-field"><label for="{ids['timezone']}">{timezone_label}<span class="field-flag field-optional">{optional}</span></label><input id="{ids['timezone']}" name="timezone" type="text" autocomplete="country-name" maxlength="100" placeholder="{timezone_placeholder}"></div>
            <div class="form-field"><label for="{ids['availability']}">{availability_label}<span class="field-flag field-optional">{optional}</span></label><input id="{ids['availability']}" name="availability" type="text" autocomplete="off" maxlength="160" placeholder="{availability_placeholder}"></div>
            <div class="form-field form-field-full"><label for="{ids['message']}">{message_label}<span class="field-flag field-required">{required}</span></label><textarea id="{ids['message']}" name="message" required minlength="3" maxlength="600" aria-describedby="{ids['message-help']}"></textarea><p id="{ids['message-help']}" class="form-privacy-note">{message_help}</p></div>
            <label class="form-consent" for="{ids['consent']}"><input id="{ids['consent']}" name="consent" type="checkbox" required><span>{consent} <a href="{privacy_href}">{privacy_label}</a>.</span></label>
            <div class="form-actions"><button class="button button-filled" type="submit">{submit}</button></div>
            <p class="form-status" data-form-status data-state="idle" aria-live="polite"></p>
          </form>
          <div class="form-success-panel" data-form-success hidden tabindex="-1" role="status" aria-live="polite">
            <p class="section-kicker">{success_kicker}</p>
            <h3>{success_title}</h3>
            <p>{success_text}</p>
          </div>'''

    text, count = re.subn(
        rf'<p class="form-guidance">.*?</p>\s*<form class="contact-form" data-contact-form data-locale="{locale}" novalidate>.*?</form>',
        guidance + "\n          " + form_html,
        text,
        count=1,
        flags=re.S,
    )
    if count != 1:
        raise SystemExit(f"{relative}: form block replacement failed")

    if relative == "index.html":
        text = text.replace(
            "Одна коротка форма допоможе узгодити зручний спосіб зв’язку, мову та формат консультації.",
            "Одна коротка форма допоможе залишити контакт і, за бажанням, вказати зручний час та формат консультації.",
            1,
        )
    elif relative == "ru/index.html":
        text = text.replace(
            "Одна короткая форма поможет согласовать удобный способ связи, язык и формат консультации.",
            "Одна короткая форма поможет оставить контакт и, при желании, указать удобное время и формат консультации.",
            1,
        )

    if 'name="language"' in text:
        raise SystemExit(f"{relative}: redundant language field remains")
    if text.count("data-form-success") != 1:
        raise SystemExit(f"{relative}: success confirmation missing")
    write(relative, text)


for relative, locale, variant in (
    ("index.html", "uk", "home"),
    ("ru/index.html", "ru", "home"),
    ("consultations/index.html", "uk", "consult"),
    ("ru/consultations/index.html", "ru", "consult"),
):
    replace_form(relative, locale, variant)


js_path = "assets/js/site.v2.js"
js = read(js_path)
new_copy = '''  const copy = {
    uk: {
      subject: "Звернення через сайт Аліни Горб",
      loading: "Надсилаємо звернення…",
      success: "Звернення підготовлено. Відкриваємо поштову програму.",
      sent: "Звернення надіслано.",
      fallback: "Сервіс форми тимчасово недоступний. Відкриваємо поштову програму, щоб звернення не втратилося.",
      error: "Не вдалося надіслати звернення. Перевірте дані або напишіть на email.",
      invalid: "Перевірте, будь ласка, обов’язкові поля.",
      blocked: "Не вдалося надіслати форму. Зачекайте кілька секунд і спробуйте ще раз.",
      submit: "Надіслати звернення",
      fields: { name: "Ім’я", reply: "Контакт", channel: "Як відповісти", service: "Формат консультації", timezone: "Країна або часовий пояс", availability: "Зручний час", message: "Повідомлення" }
    },
    ru: {
      subject: "Обращение через сайт Алины Горб",
      loading: "Отправляем обращение…",
      success: "Обращение подготовлено. Открываем почтовую программу.",
      sent: "Обращение отправлено.",
      fallback: "Сервис формы временно недоступен. Открываем почтовую программу, чтобы обращение не потерялось.",
      error: "Не удалось отправить обращение. Проверьте данные или напишите на email.",
      invalid: "Проверьте, пожалуйста, обязательные поля.",
      blocked: "Не удалось отправить форму. Подождите несколько секунд и попробуйте ещё раз.",
      submit: "Отправить обращение",
      fields: { name: "Имя", reply: "Контакт", channel: "Как ответить", service: "Формат консультации", timezone: "Страна или часовой пояс", availability: "Удобное время", message: "Сообщение" }
    }
  };
'''
js, count = re.subn(r'  const copy = \{.*?\n  \};\n', new_copy, js, count=1, flags=re.S)
if count != 1:
    raise SystemExit("site.v2.js: copy replacement failed")

new_contact = '''  const initContactForm = () => {
    const form = document.querySelector("[data-contact-form]");
    if (!form) return;
    const locale = form.dataset.locale === "ru" ? "ru" : "uk";
    const text = copy[locale];
    const status = form.querySelector("[data-form-status]");
    const successPanel = form.parentElement?.querySelector("[data-form-success]");
    const button = form.querySelector("button[type='submit']");
    const honeypot = form.querySelector("[name='website']");
    const startedAtField = form.querySelector("[name='startedAt']");
    const endpoint = String(config.formEndpoint || "").trim();
    let openedAt = Date.now();
    let interacted = false;
    let submitting = false;
    if (startedAtField) startedAtField.value = String(openedAt);

    const setState = (state, message) => {
      if (status) { status.dataset.state = state; status.textContent = message; }
      if (button) { button.disabled = state === "loading"; button.textContent = state === "loading" ? text.loading : text.submit; }
      form.setAttribute("aria-busy", String(state === "loading"));
    };

    const payloadFromForm = () => {
      const data = new FormData(form);
      return {
        name: String(data.get("name") || "").trim(),
        reply: String(data.get("reply") || "").trim(),
        channel: String(data.get("channel") || "").trim(),
        service: String(data.get("service") || "").trim(),
        timezone: String(data.get("timezone") || "").trim(),
        availability: String(data.get("availability") || "").trim(),
        message: String(data.get("message") || "").trim(),
        consent: data.get("consent") === "on"
      };
    };

    const providerPayloadFrom = (payload) => {
      const fields = text.fields;
      const provider = {
        subject: text.subject,
        [fields.name]: payload.name,
        [fields.reply]: payload.reply,
        [fields.message]: payload.message
      };
      if (payload.channel) provider[fields.channel] = payload.channel;
      if (payload.service) provider[fields.service] = payload.service;
      if (payload.timezone) provider[fields.timezone] = payload.timezone;
      if (payload.availability) provider[fields.availability] = payload.availability;
      return provider;
    };

    const mailtoFallback = (payload) => {
      const fields = text.fields;
      const body = [
        `${fields.name}: ${payload.name}`,
        `${fields.reply}: ${payload.reply}`,
        payload.channel ? `${fields.channel}: ${payload.channel}` : null,
        payload.service ? `${fields.service}: ${payload.service}` : null,
        payload.timezone ? `${fields.timezone}: ${payload.timezone}` : null,
        payload.availability ? `${fields.availability}: ${payload.availability}` : null,
        "", `${fields.message}:`, payload.message
      ].filter((line) => line !== null).join("\n");
      const email = String(config.email || "hello@alinahorb.com").trim();
      setState("success", text.success);
      window.location.href = `mailto:${email}?subject=${encodeURIComponent(text.subject)}&body=${encodeURIComponent(body)}`;
    };

    const showSuccessConfirmation = () => {
      setState("success", text.sent);
      form.hidden = true;
      if (!successPanel) return;
      successPanel.hidden = false;
      window.requestAnimationFrame(() => {
        successPanel.focus({ preventScroll: true });
        successPanel.scrollIntoView({ behavior: reducedMotion ? "auto" : "smooth", block: "center" });
      });
    };

    const markInteraction = () => { interacted = true; };
    form.addEventListener("pointerdown", markInteraction, { passive: true });
    form.addEventListener("keydown", markInteraction);
    form.addEventListener("input", () => { interacted = true; if (status?.dataset.state === "error") setState("idle", ""); });

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      if (submitting) return;
      if (!form.reportValidity()) { setState("error", text.invalid); return; }
      const payload = payloadFromForm();
      const elapsed = Date.now() - openedAt;
      const trapped = Boolean(String(honeypot?.value || "").trim());
      const meaningful = payload.name.length > 0 && payload.reply.length > 2 && payload.message.length > 2 && payload.consent;
      if (trapped || elapsed < 1500 || !interacted) { setState("error", text.blocked); return; }
      if (!meaningful) { setState("error", text.invalid); return; }
      submitting = true;
      setState("loading", text.loading);
      if (!endpoint || config.formMode === "mailto") {
        window.setTimeout(() => { submitting = false; mailtoFallback(payload); }, reducedMotion ? 0 : 240);
        return;
      }
      const controller = new AbortController();
      const timeoutId = window.setTimeout(() => controller.abort(), 10000);
      try {
        const response = await fetch(endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json", "Accept": "application/json" },
          body: JSON.stringify(providerPayloadFrom(payload)), signal: controller.signal
        });
        if (!response.ok) { const requestError = new Error(`HTTP ${response.status}`); requestError.status = response.status; throw requestError; }
        form.reset(); openedAt = Date.now(); interacted = false;
        if (startedAtField) startedAtField.value = String(openedAt);
        showSuccessConfirmation();
      } catch (error) {
        console.error("Contact form submission failed", error);
        const statusCode = Number(error?.status || 0);
        const recoverable = error?.name === "AbortError" || statusCode === 0 || statusCode >= 500;
        if (recoverable) { setState("error", text.fallback); window.setTimeout(() => mailtoFallback(payload), reducedMotion ? 0 : 360); }
        else setState("error", text.error);
      } finally { window.clearTimeout(timeoutId); submitting = false; }
    });
  };
'''
js, count = re.subn(r'  const initContactForm = \(\) => \{.*?\n  \};\n\n  const initMobileBookingCta', new_contact + "\n  const initMobileBookingCta", js, count=1, flags=re.S)
if count != 1:
    raise SystemExit("site.v2.js: contact form runtime replacement failed")
if "source: window.location.href" in js or 'data.get("language")' in js or 'data.get("format")' in js:
    raise SystemExit("site.v2.js: noisy legacy payload remains")
write(js_path, js)


turnstile = '''#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "assets/js/site.v2.js"
text = PATH.read_text(encoding="utf-8")


def replace_once(old: str, new: str, label: str) -> None:
    global text
    if new in text:
        return
    if old not in text:
        raise SystemExit(f"Turnstile patch point missing: {label}")
    text = text.replace(old, new, 1)


replace_once(
    '      blocked: "Не вдалося надіслати форму. Зачекайте кілька секунд і спробуйте ще раз.",\n      submit: "Надіслати звернення",',
    '      blocked: "Не вдалося надіслати форму. Зачекайте кілька секунд і спробуйте ще раз.",\n      verification: "Підтвердьте, будь ласка, що ви не робот.",\n      submit: "Надіслати звернення",',
    "Ukrainian verification message",
)
replace_once(
    '      blocked: "Не удалось отправить форму. Подождите несколько секунд и попробуйте ещё раз.",\n      submit: "Отправить обращение",',
    '      blocked: "Не удалось отправить форму. Подождите несколько секунд и попробуйте ещё раз.",\n      verification: "Подтвердите, пожалуйста, что вы не робот.",\n      submit: "Отправить обращение",',
    "Russian verification message",
)
replace_once(
    '    const endpoint = String(config.formEndpoint || "").trim();\n    let openedAt = Date.now();',
    '    const endpoint = String(config.formEndpoint || "").trim();\n    const turnstileSiteKey = String(config.turnstileSiteKey || "").trim();\n    let turnstileWidgetId = null;\n    let turnstileToken = "";\n    let openedAt = Date.now();',
    "Turnstile state",
)
replace_once(
    '      return provider;\n    };',
    '      return { ...provider, "cf-turnstile-response": turnstileToken };\n    };',
    "Turnstile provider payload",
)
replace_once(
    '    const markInteraction = () => { interacted = true; };',
    '''    const resetTurnstile = () => {
      turnstileToken = "";
      if (window.turnstile && turnstileWidgetId !== null) window.turnstile.reset(turnstileWidgetId);
    };

    const initTurnstile = () => {
      if (!turnstileSiteKey || config.formMode !== "formspree") return;
      const actions = form.querySelector(".form-actions");
      if (!actions || form.querySelector("[data-turnstile-container]")) return;
      const container = document.createElement("div");
      container.dataset.turnstileContainer = "";
      container.className = "form-turnstile";
      container.style.cssText = "min-height:65px;margin:4px 0 18px;";
      container.setAttribute("aria-label", locale === "ru" ? "Проверка безопасности" : "Перевірка безпеки");
      actions.before(container);

      const render = () => {
        if (!window.turnstile || turnstileWidgetId !== null) return;
        turnstileWidgetId = window.turnstile.render(container, {
          sitekey: turnstileSiteKey,
          theme: "light",
          size: "flexible",
          callback: (token) => { turnstileToken = String(token || ""); if (status?.dataset.state === "error") setState("idle", ""); },
          "expired-callback": () => { turnstileToken = ""; },
          "error-callback": () => { turnstileToken = ""; setState("error", text.verification); }
        });
      };

      let script = document.querySelector("script[data-alina-turnstile]");
      if (window.turnstile) { render(); return; }
      if (!script) {
        script = document.createElement("script");
        script.src = "https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit";
        script.defer = true;
        script.dataset.alinaTurnstile = "";
        document.head.appendChild(script);
      }
      script.addEventListener("load", render, { once: true });
      script.addEventListener("error", () => setState("error", text.verification), { once: true });
    };

    initTurnstile();

    const markInteraction = () => { interacted = true; };''',
    "Turnstile renderer",
)
replace_once(
    '      if (!meaningful) { setState("error", text.invalid); return; }\n      submitting = true;',
    '      if (!meaningful) { setState("error", text.invalid); return; }\n      if (config.formMode === "formspree" && turnstileSiteKey && !turnstileToken) { setState("error", text.verification); return; }\n      submitting = true;',
    "Turnstile submit gate",
)
replace_once(
    '        if (startedAtField) startedAtField.value = String(openedAt);\n        showSuccessConfirmation();',
    '        if (startedAtField) startedAtField.value = String(openedAt);\n        resetTurnstile();\n        showSuccessConfirmation();',
    "Turnstile reset after success",
)
replace_once(
    '        else setState("error", text.error);\n      } finally',
    '        else { resetTurnstile(); setState("error", text.error); }\n      } finally',
    "Turnstile reset after provider rejection",
)

PATH.write_text(text, encoding="utf-8")
print("Cloudflare Turnstile runtime applied")
'''
write("scripts/apply-turnstile-v3-2.py", turnstile)


css_path = "assets/css/site.intake.v3-2.css"
css = read(css_path)
addition = '''

.field-flag {
  display: inline-block;
  margin-inline-start: 8px;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: .08em;
  line-height: 1;
  text-transform: uppercase;
}

.field-required {
  color: var(--terracotta);
}

.field-optional {
  color: var(--muted);
  font-weight: 500;
}

.form-success-panel {
  min-height: 290px;
  padding: clamp(30px, 6vw, 58px);
  border: 1px solid color-mix(in srgb, var(--sage) 42%, transparent);
  border-radius: 2px;
  background: color-mix(in srgb, var(--sage-light) 58%, var(--paper));
  display: flex;
  flex-direction: column;
  justify-content: center;
  outline: none;
}

.form-success-panel[hidden] {
  display: none;
}

.form-success-panel h3 {
  max-width: 520px;
  margin: 8px 0 14px;
  font-family: var(--serif);
  font-size: clamp(30px, 4vw, 46px);
  font-weight: 500;
  line-height: 1.05;
}

.form-success-panel > p:last-child {
  max-width: 560px;
  margin: 0;
  color: var(--muted);
  font-size: 15px;
  line-height: 1.75;
}
'''
if ".form-success-panel" not in css:
    css += addition
write(css_path, css)


validate_form = '''#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
js = (ROOT / "assets/js/site.v2.js").read_text(encoding="utf-8")
config = (ROOT / "assets/js/site-config.v2.js").read_text(encoding="utf-8")
robots_meta = '<meta name="robots" content="index, follow, max-image-preview:large">'

required = [
    'let submitting = false;',
    'if (submitting) return;',
    'const controller = new AbortController();',
    'controller.abort(), 10000',
    '"Accept": "application/json"',
    'signal: controller.signal',
    'requestError.status = response.status',
    'error?.name === "AbortError"',
    'statusCode >= 500',
    'mailtoFallback(payload)',
    'providerPayloadFrom(payload)',
    'showSuccessConfirmation();',
    'form.hidden = true;',
    'successPanel.hidden = false;',
    'subject: text.subject',
    'const turnstileSiteKey = String(config.turnstileSiteKey || "").trim();',
    'https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit',
    '"cf-turnstile-response": turnstileToken',
    'window.turnstile.render',
    'resetTurnstile();',
    'text.verification',
]

missing = [needle for needle in required if needle not in js]
if missing:
    raise SystemExit("Missing form hardening contracts:\n- " + "\n- ".join(missing))

for forbidden in ('source: window.location.href', 'data.get("language")', 'data.get("format")', 'locale, subject'):
    if forbidden in js:
        raise SystemExit(f"Noisy form payload remains: {forbidden}")

if js.count('form.addEventListener("submit"') != 1:
    raise SystemExit("Expected exactly one form submit handler")
if 'formEndpoint: "https://formspree.io/f/mvzezana"' not in config:
    raise SystemExit("Approved Formspree endpoint is not configured")
if 'formMode: "formspree"' not in config:
    raise SystemExit("Production form mode is not enabled")
if 'turnstileSiteKey: "0x4AAAAAAD2wlldaSXK8Bp9f"' not in config:
    raise SystemExit("Approved public Turnstile site key is not configured")

for relative in ("index.html", "ru/index.html", "consultations/index.html", "ru/consultations/index.html"):
    html = (ROOT / relative).read_text(encoding="utf-8")
    if 'data-form-success' not in html:
        raise SystemExit(f"{relative}: visible success confirmation missing")
    if 'name="language"' in html:
        raise SystemExit(f"{relative}: redundant language field remains")
    if html.count('field-required') < 3 or html.count('field-optional') < 4:
        raise SystemExit(f"{relative}: required/optional field labels are incomplete")

for relative in ("index.html", "ru/index.html"):
    html = (ROOT / relative).read_text(encoding="utf-8")
    if robots_meta not in html or "noindex" in html.lower():
        raise SystemExit(f"{relative}: public indexing directive is not active")

print("Production Formspree, compact email payload, confirmation UX and Turnstile integration: OK")
'''
write("scripts/validate-form-hardening.py", validate_form)


consult_validator = '''#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "consultations/index.html": {
        "lang": "uk",
        "canonical": "https://alinahorb.com/consultations/",
        "ua": "https://alinahorb.com/consultations/",
        "ru": "https://alinahorb.com/ru/consultations/",
        "title": "Консультації психолога Аліни Горб",
    },
    "ru/consultations/index.html": {
        "lang": "ru",
        "canonical": "https://alinahorb.com/ru/consultations/",
        "ua": "https://alinahorb.com/consultations/",
        "ru": "https://alinahorb.com/ru/consultations/",
        "title": "Консультации психолога Алины Горб",
    },
}

errors = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


for relative, expected in PAGES.items():
    path = ROOT / relative
    require(path.is_file(), f"Missing page: {relative}")
    if not path.is_file():
        continue
    text = path.read_text(encoding="utf-8")
    require(f'<html lang="{expected["lang"]}"' in text, f"{relative}: language mismatch")
    require(text.count("<h1") == 1, f"{relative}: expected one H1")
    require(expected["title"] in text, f"{relative}: title copy missing")
    require(text.count(f'<link rel="canonical" href="{expected["canonical"]}">') == 1, f"{relative}: canonical mismatch")
    require(text.count(f'<link rel="alternate" hreflang="uk" href="{expected["ua"]}">') == 1, f"{relative}: UA hreflang mismatch")
    require(text.count(f'<link rel="alternate" hreflang="ru" href="{expected["ru"]}">') == 1, f"{relative}: RU hreflang mismatch")
    require(text.count('<meta name="robots" content="noindex, nofollow">') + text.count('<meta name="robots" content="index, follow, max-image-preview:large">') == 1, f"{relative}: indexing directive mismatch")
    require('"@type": "Service"' in text, f"{relative}: Service schema missing")
    require('"@type": "FAQPage"' in text, f"{relative}: FAQPage schema missing")
    require('"@type": "BreadcrumbList"' in text, f"{relative}: BreadcrumbList schema missing")
    require('priceCurrency": "UAH"' in text and '"price": "600"' in text, f"{relative}: price schema mismatch")
    require('data-contact-form' in text and 'data-form-status' in text and 'data-form-success' in text, f"{relative}: form or success state missing")
    require('name="service"' in text and 'name="message"' in text and 'name="availability"' in text, f"{relative}: compact consultation fields missing")
    require('name="language"' not in text and 'name="format"' not in text, f"{relative}: redundant intake fields remain")
    require(text.count('field-required') >= 3 and text.count('field-optional') >= 4, f"{relative}: required/optional labels missing")
    require('name="channel" required' not in text and 'name="service" required' not in text and 'name="timezone" required' not in text and 'name="availability" required' not in text, f"{relative}: optional field is still required")
    require('site-config.v2.js' in text and 'site.v2.js' in text, f"{relative}: form runtime missing")
    require('site.consultations.v1.css' in text, f"{relative}: page stylesheet missing")
    require('50' in text and '600' in text, f"{relative}: confirmed duration/price missing")
    require('financialstreamllc@gmail.com' not in text and 'alinahorb1991@gmail.com' not in text, f"{relative}: legacy email found")
    require(not re.search(r'\b(TODO|TBD)\b', text, re.I), f"{relative}: unfinished content token found")
    ids = re.findall(r'\bid="([^"]+)"', text)
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    require(not duplicates, f"{relative}: duplicate IDs {duplicates}")
    for script in re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', text, re.S):
        try:
            json.loads(script)
        except json.JSONDecodeError as exc:
            errors.append(f"{relative}: invalid JSON-LD: {exc}")

css = ROOT / "assets/css/site.consultations.v1.css"
require(css.is_file(), "Consultations stylesheet missing")
if css.is_file():
    content = css.read_text(encoding="utf-8")
    for token in (".consult-hero", ".condition-ledger", ".consult-faq", "@media (max-width: 620px)"):
        require(token in content, f"Consultations stylesheet missing {token}")

if errors:
    print("Consultations pages validation failed:")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("Consultations pages validation passed for compact UA and RU intake forms")
'''
write("scripts/validate-consultations-pages-v1.py", consult_validator)


privacy_path = "scripts/validate-privacy-intake.py"
privacy = read(privacy_path)
privacy = privacy.replace(
    "        'site.navigation.v1.js?v=20260717-ux1',\n    )",
    "        'site.navigation.v1.js?v=20260717-ux1',\n        'data-form-success',\n        'field-optional',\n    )",
    2,
)
privacy = replace_once(
    privacy,
    '    require(ROOT / "assets/css/site.intake.v3-2.css", ".form-honeypot", ".form-guidance", ".form-consent a")',
    '    require(ROOT / "assets/css/site.intake.v3-2.css", ".form-honeypot", ".form-guidance", ".form-consent a", ".form-success-panel", ".field-optional")',
    privacy_path,
)
insert = '''    for path in (ROOT / "index.html", ROOT / "ru/index.html"):
        text = path.read_text(encoding="utf-8")
        if 'name="language"' in text:
            raise AssertionError(f"Redundant language field remains in {path.relative_to(ROOT)}")
        if text.count('field-required') < 3 or text.count('field-optional') < 4:
            raise AssertionError(f"Required/optional form labels missing in {path.relative_to(ROOT)}")
'''
marker = '    if ua.count(\'name="website"\') != 1 or ru.count(\'name="website"\') != 1:\n'
if insert not in privacy:
    privacy = privacy.replace(marker, insert + "\n" + marker, 1)
write(privacy_path, privacy)

print("Compact bilingual form email and visible success confirmation patch applied.")
