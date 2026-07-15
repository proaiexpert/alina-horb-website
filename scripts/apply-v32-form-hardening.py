#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "assets/js/site.v2.js"
text = path.read_text(encoding="utf-8")

replacements = [
    (
        '      success: "Звернення підготовлено. Відкриваємо поштову програму.",\n      error: "Не вдалося підготувати звернення. Напишіть на email.",',
        '      success: "Звернення підготовлено. Відкриваємо поштову програму.",\n      sent: "Звернення надіслано. Аліна відповість через обраний канал зв’язку.",\n      fallback: "Сервіс форми тимчасово недоступний. Відкриваємо поштову програму, щоб звернення не втратилося.",\n      error: "Не вдалося надіслати звернення. Перевірте дані або напишіть на email.",',
    ),
    (
        '      success: "Обращение подготовлено. Открываем почтовую программу.",\n      error: "Не удалось подготовить обращение. Напишите на email.",',
        '      success: "Обращение подготовлено. Открываем почтовую программу.",\n      sent: "Обращение отправлено. Алина ответит через выбранный канал связи.",\n      fallback: "Сервис формы временно недоступен. Открываем почтовую программу, чтобы обращение не потерялось.",\n      error: "Не удалось отправить обращение. Проверьте данные или напишите на email.",',
    ),
    (
        '    let openedAt = Date.now();\n    let interacted = false;',
        '    let openedAt = Date.now();\n    let interacted = false;\n    let submitting = false;',
    ),
    (
        '        consent: data.get("consent") === "on",\n        locale',
        '        consent: data.get("consent") === "on",\n        locale,\n        subject: text.subject,\n        source: window.location.href',
    ),
    (
        '    form.addEventListener("submit", async (event) => {\n      event.preventDefault();\n      if (!form.reportValidity()) {',
        '    form.addEventListener("submit", async (event) => {\n      event.preventDefault();\n      if (submitting) return;\n      if (!form.reportValidity()) {',
    ),
    (
        '      setState("loading", text.loading);\n\n      if (!endpoint || config.formMode === "mailto") {\n        window.setTimeout(() => mailtoFallback(payload), reducedMotion ? 0 : 240);\n        return;\n      }\n\n      try {\n        const response = await fetch(endpoint, {\n          method: "POST",\n          headers: { "Content-Type": "application/json" },\n          body: JSON.stringify(payload)\n        });\n        if (!response.ok) throw new Error(`HTTP ${response.status}`);\n        form.reset();\n        openedAt = Date.now();\n        interacted = false;\n        if (startedAtField) startedAtField.value = String(openedAt);\n        setState("success", text.success);\n      } catch (error) {\n        console.error("Contact form submission failed", error);\n        setState("error", text.error);\n      }',
        '      submitting = true;\n      setState("loading", text.loading);\n\n      if (!endpoint || config.formMode === "mailto") {\n        window.setTimeout(() => {\n          submitting = false;\n          mailtoFallback(payload);\n        }, reducedMotion ? 0 : 240);\n        return;\n      }\n\n      const controller = new AbortController();\n      const timeoutId = window.setTimeout(() => controller.abort(), 10000);\n\n      try {\n        const response = await fetch(endpoint, {\n          method: "POST",\n          headers: {\n            "Content-Type": "application/json",\n            "Accept": "application/json"\n          },\n          body: JSON.stringify(payload),\n          signal: controller.signal\n        });\n        if (!response.ok) {\n          const requestError = new Error(`HTTP ${response.status}`);\n          requestError.status = response.status;\n          throw requestError;\n        }\n        form.reset();\n        openedAt = Date.now();\n        interacted = false;\n        if (startedAtField) startedAtField.value = String(openedAt);\n        setState("success", text.sent);\n      } catch (error) {\n        console.error("Contact form submission failed", error);\n        const statusCode = Number(error?.status || 0);\n        const recoverable = error?.name === "AbortError" || statusCode === 0 || statusCode >= 500;\n        if (recoverable) {\n          setState("error", text.fallback);\n          window.setTimeout(() => mailtoFallback(payload), reducedMotion ? 0 : 360);\n        } else {\n          setState("error", text.error);\n        }\n      } finally {\n        window.clearTimeout(timeoutId);\n        submitting = false;\n      }',
    ),
]

for old, new in replacements:
    if new in text:
        continue
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"Expected one occurrence for patch; found {count}: {old[:80]!r}")
    text = text.replace(old, new, 1)

path.write_text(text, encoding="utf-8")
print("Production form hardening applied")
