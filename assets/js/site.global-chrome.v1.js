(() => {
  "use strict";

  if (window.__ALINA_GLOBAL_CHROME_V1__) return;
  window.__ALINA_GLOBAL_CHROME_V1__ = true;

  const script = document.currentScript;
  if (!script) return;

  const appendStylesheet = (relativePath) => {
    const href = new URL(relativePath, script.src).href;
    if (document.querySelector(`link[href="${href}"]`)) return;
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = href;
    document.head.appendChild(link);
  };

  appendStylesheet("../css/site.global-chrome.v1.css?v=20260717-chrome1");

  const pathname = window.location.pathname;
  const projectMarker = "/alina-horb-website/";
  const rootPath = pathname.includes(projectMarker) ? projectMarker : "/";
  const relativePath = pathname.startsWith(rootPath) ? pathname.slice(rootPath.length) : pathname.replace(/^\//, "");
  const route = relativePath.replace(/index\.html$/, "");
  const isRu = document.documentElement.lang.toLowerCase().startsWith("ru") || route.startsWith("ru/");
  const cleanPath = route.replace(/^ru\//, "");
  const localeRoot = `${rootPath}${isRu ? "ru/" : ""}`;
  const alternateHref = isRu ? `${rootPath}${cleanPath}` : `${rootPath}ru/${cleanPath}`;
  const privacyHref = `${localeRoot}privacy/`;
  const bookingHref = `${localeRoot}consultations/#contact`;
  const logoUrl = new URL(`../images/logos/alina-horb-logo-${isRu ? "ru" : "ua"}-dark.png`, script.src).href;
  const currentYear = new Date().getFullYear();

  const pageKey = cleanPath === "" ? "home"
    : cleanPath.startsWith("about/") ? "about"
      : cleanPath.startsWith("consultations/") ? "consultations"
        : cleanPath.startsWith("notes/") ? "notes"
          : cleanPath.startsWith("privacy/") ? "privacy"
            : "other";

  const text = isRu ? {
    name: "Алина Горб",
    brand: "Алина Горб — главная",
    nav: "Основные разделы сайта",
    open: "Открыть меню",
    sections: "Разделы",
    contact: "Первый контакт",
    positioning: "Психологические консультации на русском и украинском языках · онлайн.",
    booking: "Записаться на консультацию",
    privacy: "Конфиденциальность",
    language: "Язык",
    developed: "Разработано",
    copyright: `© Алина Горб, ${currentYear}`
  } : {
    name: "Аліна Горб",
    brand: "Аліна Горб — головна",
    nav: "Основні розділи сайту",
    open: "Відкрити меню",
    sections: "Розділи",
    contact: "Перший контакт",
    positioning: "Психологічні консультації українською та російською мовами · онлайн.",
    booking: "Записатися на консультацію",
    privacy: "Конфіденційність",
    language: "Мова",
    developed: "Розроблено",
    copyright: `© Аліна Горб, ${currentYear}`
  };

  const pages = [
    { key: "home", label: isRu ? "Главная" : "Головна", href: localeRoot },
    { key: "about", label: isRu ? "Об Алине" : "Про Аліну", href: `${localeRoot}about/` },
    { key: "consultations", label: isRu ? "Консультации" : "Консультації", href: `${localeRoot}consultations/` },
    { key: "notes", label: isRu ? "Заметки" : "Нотатки", href: `${localeRoot}notes/` }
  ];

  const currentAttribute = (key) => key === pageKey ? ' aria-current="page"' : "";
  const languageSwitch = isRu
    ? `<div class="language-switch" aria-label="Выбор языка"><a href="${alternateHref}" lang="uk" hreflang="uk">UA</a><span aria-hidden="true">/</span><span aria-current="page">RU</span></div>`
    : `<div class="language-switch" aria-label="Вибір мови"><span aria-current="page">UA</span><span aria-hidden="true">/</span><a href="${alternateHref}" lang="ru" hreflang="ru">RU</a></div>`;

  const header = document.querySelector(".site-header");
  if (header) {
    header.id = "top";
    header.classList.add("site-header--canonical");
    const utilityHeader = pageKey === "privacy" || pageKey === "other" || document.body.classList.contains("article-template-v32") || Boolean(document.querySelector(".notes-hub-index"));
    header.classList.toggle("inner-page-header", utilityHeader);
    header.innerHTML = `
      <div class="page-shell header-row">
        <a class="brand" href="${localeRoot}" aria-label="${text.brand}">
          <img src="${logoUrl}" width="512" height="156" alt="${text.name}">
        </a>
        <nav class="inner-desktop-nav" aria-label="${text.nav}">
          ${pages.slice(1).map((page) => `<a href="${page.href}"${currentAttribute(page.key)}>${page.label}</a>`).join("")}
          <a class="editorial-header-booking" href="${bookingHref}">${isRu ? "Записаться" : "Записатися"}</a>
        </nav>
        <div class="header-tools">
          ${languageSwitch}
          <button class="mobile-nav-toggle" type="button" aria-label="${text.open}" aria-expanded="false" aria-controls="mobile-navigation" data-menu-toggle><span class="menu-icon" aria-hidden="true"></span></button>
        </div>
        <nav class="mobile-navigation" id="mobile-navigation" aria-label="${text.nav}" data-mobile-nav hidden></nav>
      </div>`;
  }

  let footer = document.querySelector(".site-footer");
  if (!footer) {
    footer = document.createElement("footer");
    footer.className = "site-footer";
    document.body.appendChild(footer);
  }

  footer.dataset.siteFooter = "canonical";
  footer.innerHTML = `
    <div class="page-shell footer-editorial-grid">
      <div class="footer-identity">
        <a class="footer-brand" href="${localeRoot}" aria-label="${text.brand}">
          <img src="${logoUrl}" width="512" height="156" alt="${text.name}">
        </a>
        <p>${text.positioning}</p>
      </div>
      <nav class="footer-navigation" aria-label="${text.nav}">
        <p class="footer-label">${text.sections}</p>
        ${pages.map((page) => `<a href="${page.href}"${currentAttribute(page.key)}>${page.label}</a>`).join("")}
      </nav>
      <div class="footer-contact">
        <p class="footer-label">${text.contact}</p>
        <a class="footer-booking" href="${bookingHref}"><span>${text.booking}</span><span aria-hidden="true">→</span></a>
        <div class="footer-contact-links">
          <a href="mailto:hello@alinahorb.com">Email</a>
          <a href="https://t.me/alina_horb1991" target="_blank" rel="noopener noreferrer">Telegram</a>
          <a href="https://instagram.com/ng_alina_dp" target="_blank" rel="noopener noreferrer">Instagram</a>
        </div>
      </div>
    </div>
    <div class="page-shell footer-utility">
      <div class="footer-utility-links">
        <a href="${localeRoot}">alinahorb.com</a>
        <a href="${privacyHref}"${pageKey === "privacy" ? ' aria-current="page"' : ""}>${text.privacy}</a>
        <span class="footer-language-label">${text.language}</span>
        ${languageSwitch}
      </div>
      <div class="footer-legal">
        <span>${text.copyright}</span>
        <span class="maker-credit"><small>${text.developed}</small><a href="https://proai-expert.com/" target="_blank" rel="noopener noreferrer">ProAI Expert</a></span>
      </div>
    </div>`;

  document.body.classList.add("global-chrome-v1");

  const toggle = header?.querySelector("[data-menu-toggle]");
  const menu = header?.querySelector("[data-mobile-nav]");
  if (toggle && menu) {
    const setOpen = (open) => {
      toggle.setAttribute("aria-expanded", String(open));
      menu.hidden = !open;
    };
    setOpen(false);
    toggle.addEventListener("click", () => setOpen(toggle.getAttribute("aria-expanded") !== "true"));
  }

  if (!document.querySelector('script[data-editorial-navigation-v1]')) {
    const navigationScript = document.createElement("script");
    navigationScript.src = `${rootPath}assets/js/site.navigation.v1.js?v=20260717-chrome1`;
    navigationScript.defer = true;
    navigationScript.dataset.editorialNavigationV1 = "";
    document.head.appendChild(navigationScript);
  }
})();
