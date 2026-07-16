#!/usr/bin/env python3
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
    '        consent: data.get("consent") === "on", locale, subject: text.subject, source: window.location.href\n',
    '        consent: data.get("consent") === "on", locale, subject: text.subject, source: window.location.href,\n        "cf-turnstile-response": turnstileToken\n',
    "Turnstile payload",
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
    '        if (startedAtField) startedAtField.value = String(openedAt);\n        setState("success", text.sent);',
    '        if (startedAtField) startedAtField.value = String(openedAt);\n        resetTurnstile();\n        setState("success", text.sent);',
    "Turnstile reset after success",
)
replace_once(
    '        else setState("error", text.error);\n      } finally',
    '        else { resetTurnstile(); setState("error", text.error); }\n      } finally',
    "Turnstile reset after provider rejection",
)

PATH.write_text(text, encoding="utf-8")
print("Cloudflare Turnstile runtime applied")
