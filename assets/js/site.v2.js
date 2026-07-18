(() => {
  "use strict";

  const config = window.ALINA_SITE_CONFIG || {};
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const copy = {
    uk: {
      subject: "Звернення через сайт Аліни Горб",
      loading: "Готуємо звернення…",
      success: "Звернення підготовлено. Відкриваємо поштову програму.",
      sent: "Звернення надіслано. Аліна відповість через обраний канал зв’язку.",
      fallback: "Сервіс форми тимчасово недоступний. Відкриваємо поштову програму, щоб звернення не втратилося.",
      error: "Не вдалося надіслати звернення. Перевірте дані або напишіть на email.",
      invalid: "Перевірте, будь ласка, обов’язкові поля.",
      blocked: "Не вдалося надіслати форму. Зачекайте кілька секунд і спробуйте ще раз.",
      verification: "Підтвердьте, будь ласка, що ви не робот.",
      submit: "Надіслати звернення",
      fields: { name: "Ім’я", reply: "Контакт", channel: "Спосіб зв’язку", language: "Мова", format: "Формат", service: "Тип консультації", timezone: "Країна або часовий пояс", availability: "Зручний час", message: "Повідомлення" }
    },
    ru: {
      subject: "Обращение через сайт Алины Горб",
      loading: "Готовим обращение…",
      success: "Обращение подготовлено. Открываем почтовую программу.",
      sent: "Обращение отправлено. Алина ответит через выбранный канал связи.",
      fallback: "Сервис формы временно недоступен. Открываем почтовую программу, чтобы обращение не потерялось.",
      error: "Не удалось отправить обращение. Проверьте данные или напишите на email.",
      invalid: "Проверьте, пожалуйста, обязательные поля.",
      blocked: "Не удалось отправить форму. Подождите несколько секунд и попробуйте ещё раз.",
      verification: "Подтвердите, пожалуйста, что вы не робот.",
      submit: "Отправить обращение",
      fields: { name: "Имя", reply: "Контакт", channel: "Способ связи", language: "Язык", format: "Формат", service: "Тип консультации", timezone: "Страна или часовой пояс", availability: "Удобное время", message: "Сообщение" }
    }
  };

  const initReveals = () => {
    const portrait = document.querySelector(".hero-portrait");
    const elements = document.querySelectorAll("[data-reveal], .process-timeline");
    if (portrait) window.requestAnimationFrame(() => portrait.classList.add("is-visible"));
    if (reducedMotion || !("IntersectionObserver" in window)) { elements.forEach((element) => element.classList.add("is-visible")); return; }
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => { if (!entry.isIntersecting) return; entry.target.classList.add("is-visible"); observer.unobserve(entry.target); });
    }, { threshold: .14, rootMargin: "0px 0px -6%" });
    elements.forEach((element) => observer.observe(element));
  };

  const initFaq = () => {
    document.querySelectorAll(".faq-list details").forEach((detail) => detail.addEventListener("toggle", () => detail.querySelector("summary")?.setAttribute("aria-expanded", String(detail.open))));
  };

  const initTelegram = () => {
    const username = String(config.telegramUsername || "").trim().replace(/^@/, "");
    const links = document.querySelectorAll("[data-telegram-link]");
    const placeholders = document.querySelectorAll("[data-telegram-placeholder]");
    if (!username) { links.forEach((link) => { link.hidden = true; }); placeholders.forEach((placeholder) => { placeholder.hidden = false; }); return; }
    links.forEach((link) => { link.href = `https://t.me/${username}`; link.hidden = false; });
    placeholders.forEach((placeholder) => { placeholder.hidden = true; });
  };

  const initContactForm = () => {
    const form = document.querySelector("[data-contact-form]");
    if (!form) return;
    const locale = form.dataset.locale === "ru" ? "ru" : "uk";
    const text = copy[locale];
    const status = form.querySelector("[data-form-status]");
    const button = form.querySelector("button[type='submit']");
    const honeypot = form.querySelector("[name='website']");
    const startedAtField = form.querySelector("[name='startedAt']");
    const endpoint = String(config.formEndpoint || "").trim();
    const turnstileSiteKey = String(config.turnstileSiteKey || "").trim();
    let turnstileWidgetId = null;
    let turnstileToken = "";
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
        name: String(data.get("name") || "").trim(), reply: String(data.get("reply") || "").trim(),
        channel: String(data.get("channel") || "").trim(), language: String(data.get("language") || "").trim(),
        format: String(data.get("format") || "").trim(), service: String(data.get("service") || "").trim(),
        timezone: String(data.get("timezone") || "").trim(), availability: String(data.get("availability") || "").trim(),
        message: String(data.get("message") || "").trim(),
        consent: data.get("consent") === "on", locale, subject: text.subject, source: window.location.href,
        "cf-turnstile-response": turnstileToken
      };
    };

    const mailtoFallback = (payload) => {
      const fields = text.fields;
      const body = [
        `${fields.name}: ${payload.name}`, `${fields.reply}: ${payload.reply}`, `${fields.channel}: ${payload.channel}`,
        `${fields.language}: ${payload.language}`, `${fields.format}: ${payload.format}`,
        payload.service ? `${fields.service}: ${payload.service}` : null,
        payload.timezone ? `${fields.timezone}: ${payload.timezone}` : null,
        payload.availability ? `${fields.availability}: ${payload.availability}` : null,
        "", `${fields.message}:`, payload.message
      ].filter((line) => line !== null).join("\n");
      const email = String(config.email || "hello@alinahorb.com").trim();
      setState("success", text.success);
      window.location.href = `mailto:${email}?subject=${encodeURIComponent(text.subject)}&body=${encodeURIComponent(body)}`;
    };

    const resetTurnstile = () => {
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
      if (config.formMode === "formspree" && turnstileSiteKey && !turnstileToken) { setState("error", text.verification); return; }
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
          body: JSON.stringify(payload), signal: controller.signal
        });
        if (!response.ok) { const requestError = new Error(`HTTP ${response.status}`); requestError.status = response.status; throw requestError; }
        form.reset(); openedAt = Date.now(); interacted = false;
        if (startedAtField) startedAtField.value = String(openedAt);
        resetTurnstile();
        setState("success", text.sent);
      } catch (error) {
        console.error("Contact form submission failed", error);
        const statusCode = Number(error?.status || 0);
        const recoverable = error?.name === "AbortError" || statusCode === 0 || statusCode >= 500;
        if (recoverable) { setState("error", text.fallback); window.setTimeout(() => mailtoFallback(payload), reducedMotion ? 0 : 360); }
        else { resetTurnstile(); setState("error", text.error); }
      } finally { window.clearTimeout(timeoutId); submitting = false; }
    });
  };

  const initMobileBookingCta = () => {
    const cta = document.querySelector("[data-mobile-booking-cta]");
    const heroCta = document.querySelector(".hero-actions .button");
    const about = document.querySelector("#about");
    const contact = document.querySelector("#contact");
    const footer = document.querySelector(".site-footer");
    if (!cta || !heroCta || !contact) return;

    const mobile = window.matchMedia("(max-width: 800px)");
    let frame = 0;
    let hideTimer = 0;
    let idleTimer = 0;
    let autoHideTimer = 0;
    let visible = false;
    let lastScrollY = Math.max(window.scrollY, 0);

    Object.assign(cta.style, {
      left: "50%",
      right: "auto",
      bottom: "calc(18px + env(safe-area-inset-bottom))",
      width: "min(280px, calc(100% - 32px))",
      minHeight: "50px",
      borderRadius: "999px",
      transform: "translate(-50%, calc(100% + 40px))"
    });

    const clearBehaviorTimers = () => {
      window.clearTimeout(idleTimer);
      window.clearTimeout(autoHideTimer);
    };

    const setVisible = (nextVisible) => {
      window.clearTimeout(hideTimer);
      if (visible === nextVisible && (nextVisible || cta.hidden)) return;
      visible = nextVisible;
      if (nextVisible) {
        cta.hidden = false;
        window.requestAnimationFrame(() => {
          cta.classList.add("is-visible");
          cta.style.transform = "translate(-50%, 0)";
        });
        cta.setAttribute("aria-hidden", "false");
        return;
      }
      cta.classList.remove("is-visible");
      cta.style.transform = "translate(-50%, calc(100% + 40px))";
      cta.setAttribute("aria-hidden", "true");
      hideTimer = window.setTimeout(() => { cta.hidden = true; }, reducedMotion ? 0 : 280);
    };

    const inViewport = (element) => {
      if (!element) return false;
      const rect = element.getBoundingClientRect();
      return rect.top < window.innerHeight && rect.bottom > 0;
    };

    const canShow = () => mobile.matches
      && heroCta.getBoundingClientRect().bottom < 0
      && !inViewport(about)
      && !inViewport(contact)
      && !inViewport(footer);

    const showTemporarily = () => {
      window.clearTimeout(autoHideTimer);
      if (!canShow()) { setVisible(false); return; }
      setVisible(true);
      autoHideTimer = window.setTimeout(() => setVisible(false), 4200);
    };

    const update = () => {
      frame = 0;
      const currentScrollY = Math.max(window.scrollY, 0);
      const delta = currentScrollY - lastScrollY;
      lastScrollY = currentScrollY;

      window.clearTimeout(idleTimer);
      if (!canShow()) {
        clearBehaviorTimers();
        setVisible(false);
        return;
      }

      if (delta > 3) setVisible(false);
      else if (delta < -3) showTemporarily();

      idleTimer = window.setTimeout(() => showTemporarily(), 650);
    };

    const requestUpdate = () => {
      if (frame) return;
      frame = window.requestAnimationFrame(update);
    };

    window.addEventListener("scroll", requestUpdate, { passive: true });
    window.addEventListener("resize", requestUpdate);
    window.visualViewport?.addEventListener("resize", requestUpdate);
    mobile.addEventListener?.("change", requestUpdate);
    cta.addEventListener("click", () => {
      clearBehaviorTimers();
      setVisible(false);
    });
    update();
  };

  const init = () => {
    initReveals();
    initFaq();
    initTelegram();
    initContactForm();
    initMobileBookingCta();
  };

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init, { once: true });
  else init();

})();
