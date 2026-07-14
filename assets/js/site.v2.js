(() => {
  "use strict";

  const config = window.ALINA_SITE_CONFIG || {};
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const copy = {
    uk: {
      subject: "Звернення через сайт Аліни Горб",
      loading: "Готуємо звернення…",
      success: "Звернення підготовлено. Відкриваємо поштову програму.",
      error: "Не вдалося підготувати звернення. Напишіть на email.",
      invalid: "Перевірте, будь ласка, обов’язкові поля.",
      submit: "Надіслати звернення",
      fields: { name: "Ім’я", reply: "Контакт", channel: "Спосіб зв’язку", language: "Мова", format: "Формат", message: "Повідомлення" }
    },
    ru: {
      subject: "Обращение через сайт Алины Горб",
      loading: "Готовим обращение…",
      success: "Обращение подготовлено. Открываем почтовую программу.",
      error: "Не удалось подготовить обращение. Напишите на email.",
      invalid: "Проверьте, пожалуйста, обязательные поля.",
      submit: "Отправить обращение",
      fields: { name: "Имя", reply: "Контакт", channel: "Способ связи", language: "Язык", format: "Формат", message: "Сообщение" }
    }
  };

  const initMobileNavigation = () => {
    const toggle = document.querySelector("[data-menu-toggle]");
    const nav = document.querySelector("[data-mobile-nav]");
    if (!toggle || !nav) return;

    const setOpen = (open) => {
      toggle.setAttribute("aria-expanded", String(open));
      nav.hidden = !open;
    };

    setOpen(false);
    toggle.addEventListener("click", () => setOpen(toggle.getAttribute("aria-expanded") !== "true"));
    nav.querySelectorAll("a").forEach((link) => link.addEventListener("click", () => setOpen(false)));
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
        setOpen(false);
        toggle.focus();
      }
    });
  };

  const initReveals = () => {
    const portrait = document.querySelector(".hero-portrait");
    const elements = document.querySelectorAll("[data-reveal], .process-timeline");
    if (portrait) window.requestAnimationFrame(() => portrait.classList.add("is-visible"));
    if (reducedMotion || !("IntersectionObserver" in window)) {
      elements.forEach((element) => element.classList.add("is-visible"));
      return;
    }

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      });
    }, { threshold: .14, rootMargin: "0px 0px -6%" });

    elements.forEach((element) => observer.observe(element));
  };

  const initActiveNavigation = () => {
    const links = [...document.querySelectorAll(".side-navigation a")];
    if (!links.length || !("IntersectionObserver" in window)) return;
    const sections = links.map((link) => document.querySelector(link.getAttribute("href"))).filter(Boolean);
    const nav = document.querySelector(".side-navigation");

    const activate = (id) => {
      const index = links.findIndex((link) => link.getAttribute("href") === `#${id}`);
      if (index < 0) return;
      links.forEach((link, linkIndex) => link.classList.toggle("is-active", linkIndex === index));
      if (nav) nav.style.setProperty("--nav-progress", `${9 + (index / Math.max(links.length - 1, 1)) * 82}%`);
    };

    const observer = new IntersectionObserver((entries) => {
      const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio);
      if (visible[0]) activate(visible[0].target.id);
    }, { threshold: [.2, .45, .7], rootMargin: "-20% 0px -55%" });

    sections.forEach((section) => observer.observe(section));
    if (sections[0]) activate(sections[0].id);
  };

  const initFaq = () => {
    document.querySelectorAll(".faq-list details").forEach((detail) => {
      detail.addEventListener("toggle", () => {
        detail.querySelector("summary")?.setAttribute("aria-expanded", String(detail.open));
      });
    });
  };

  const initTelegram = () => {
    const username = String(config.telegramUsername || "").trim().replace(/^@/, "");
    const links = document.querySelectorAll("[data-telegram-link]");
    const placeholders = document.querySelectorAll("[data-telegram-placeholder]");
    if (!username) {
      links.forEach((link) => { link.hidden = true; });
      placeholders.forEach((placeholder) => { placeholder.hidden = false; });
      return;
    }
    links.forEach((link) => {
      link.href = `https://t.me/${username}`;
      link.hidden = false;
    });
    placeholders.forEach((placeholder) => { placeholder.hidden = true; });
  };

  const initContactForm = () => {
    const form = document.querySelector("[data-contact-form]");
    if (!form) return;
    const locale = form.dataset.locale === "ru" ? "ru" : "uk";
    const text = copy[locale];
    const status = form.querySelector("[data-form-status]");
    const button = form.querySelector("button[type='submit']");
    const endpoint = String(config.formEndpoint || "").trim();

    const setState = (state, message) => {
      if (status) {
        status.dataset.state = state;
        status.textContent = message;
      }
      if (button) {
        button.disabled = state === "loading";
        button.textContent = state === "loading" ? text.loading : text.submit;
      }
      form.setAttribute("aria-busy", String(state === "loading"));
    };

    const payloadFromForm = () => {
      const data = new FormData(form);
      return {
        name: String(data.get("name") || "").trim(),
        reply: String(data.get("reply") || "").trim(),
        channel: String(data.get("channel") || "").trim(),
        language: String(data.get("language") || "").trim(),
        format: String(data.get("format") || "").trim(),
        message: String(data.get("message") || "").trim(),
        consent: data.get("consent") === "on",
        locale
      };
    };

    const mailtoFallback = (payload) => {
      const fields = text.fields;
      const body = [
        `${fields.name}: ${payload.name}`,
        `${fields.reply}: ${payload.reply}`,
        `${fields.channel}: ${payload.channel}`,
        `${fields.language}: ${payload.language}`,
        `${fields.format}: ${payload.format}`,
        "",
        `${fields.message}:`,
        payload.message
      ].join("\n");
      const email = String(config.email || "alinahorb1991@gmail.com").trim();
      setState("success", text.success);
      window.location.href = `mailto:${email}?subject=${encodeURIComponent(text.subject)}&body=${encodeURIComponent(body)}`;
    };

    form.addEventListener("input", () => {
      if (status?.dataset.state === "error") setState("idle", "");
    });

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      if (!form.reportValidity()) {
        setState("error", text.invalid);
        return;
      }

      const payload = payloadFromForm();
      setState("loading", text.loading);

      if (!endpoint || config.formMode === "mailto") {
        window.setTimeout(() => mailtoFallback(payload), reducedMotion ? 0 : 240);
        return;
      }

      try {
        const response = await fetch(endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        form.reset();
        setState("success", text.success);
      } catch (error) {
        console.error("Contact form submission failed", error);
        setState("error", text.error);
      }
    });
  };

  const initMobileBookingCta = () => {
    const cta = document.querySelector("[data-mobile-booking-cta]");
    const heroCta = document.querySelector(".hero-actions .button");
    const contact = document.querySelector("#contact");
    const footer = document.querySelector(".site-footer");
    if (!cta || !heroCta || !contact) return;

    const mobile = window.matchMedia("(max-width: 800px)");
    let frame = 0;
    let hideTimer = 0;

    const setVisible = (visible) => {
      window.clearTimeout(hideTimer);
      if (visible) {
        cta.hidden = false;
        window.requestAnimationFrame(() => cta.classList.add("is-visible"));
        cta.setAttribute("aria-hidden", "false");
        return;
      }
      cta.classList.remove("is-visible");
      cta.setAttribute("aria-hidden", "true");
      hideTimer = window.setTimeout(() => { cta.hidden = true; }, reducedMotion ? 0 : 240);
    };

    const update = () => {
      frame = 0;
      if (!mobile.matches) {
        setVisible(false);
        return;
      }
      const heroBottom = heroCta.getBoundingClientRect().bottom;
      const contactRect = contact.getBoundingClientRect();
      const footerRect = footer?.getBoundingClientRect();
      const contactVisible = contactRect.top < window.innerHeight && contactRect.bottom > 0;
      const footerVisible = Boolean(footerRect && footerRect.top < window.innerHeight && footerRect.bottom > 0);
      setVisible(heroBottom < 0 && !contactVisible && !footerVisible);
    };

    const requestUpdate = () => {
      if (frame) return;
      frame = window.requestAnimationFrame(update);
    };

    window.addEventListener("scroll", requestUpdate, { passive: true });
    window.addEventListener("resize", requestUpdate);
    mobile.addEventListener?.("change", requestUpdate);
    cta.addEventListener("click", () => setVisible(false));
    update();
  };

  const init = () => {
    initMobileNavigation();
    initReveals();
    initActiveNavigation();
    initFaq();
    initTelegram();
    initContactForm();
    initMobileBookingCta();
  };

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init, { once: true });
  else init();
})();
