(() => {
  const script = document.currentScript;
  if (!script) return;

  const appendStylesheet = (relativePath) => {
    const href = new URL(relativePath, script.src).href;
    if (document.querySelector(`link[href="${href}"]`)) return;
    const stylesheet = document.createElement("link");
    stylesheet.rel = "stylesheet";
    stylesheet.href = href;
    document.head.appendChild(stylesheet);
  };

  appendStylesheet("../css/site.chrome.v3.css");
  appendStylesheet("../css/site.footer.v3-2.css");

  const faviconUrl = new URL("../images/logos/favicon-ag.svg", script.src).href;
  let favicon = document.querySelector('link[rel~="icon"]');
  if (!favicon) {
    favicon = document.createElement("link");
    favicon.rel = "icon";
    document.head.appendChild(favicon);
  }
  favicon.type = "image/svg+xml";
  favicon.href = faviconUrl;

  const pathname = window.location.pathname;
  const projectMarker = "/alina-horb-website/";
  const rootPath = pathname.includes(projectMarker) ? projectMarker : "/";
  const relativePath = pathname.startsWith(rootPath) ? pathname.slice(rootPath.length) : pathname.replace(/^\//, "");
  const isRu = document.documentElement.lang.toLowerCase().startsWith("ru") || relativePath.startsWith("ru/");
  const uaRelative = relativePath.replace(/^ru\//, "");
  const ruRelative = relativePath.startsWith("ru/") ? relativePath : `ru/${relativePath}`;
  const homeHref = `${rootPath}${isRu ? "ru/" : ""}`;
  const notesHref = `${rootPath}${isRu ? "ru/notes/" : "notes/"}`;
  const privacyHref = `${rootPath}${isRu ? "ru/privacy/" : "privacy/"}`;
  const alternateHref = `${rootPath}${isRu ? uaRelative : ruRelative}`;
  const logoUrl = new URL(`../images/logos/alina-horb-logo-${isRu ? "ru" : "ua"}-dark.png`, script.src).href;

  const text = isRu ? {
    brand: "Алина Горб — главная",
    nav: "Навигация по сайту",
    open: "Открыть меню",
    close: "Закрыть меню",
    home: "Главная",
    topics: "Направления",
    about: "Об Алине",
    process: "Процесс",
    notes: "Заметки",
    contact: "Контакты",
    privacy: "Конфиденциальность",
    developed: "Разработано",
    copyright: "© Алина Горб, 2026"
  } : {
    brand: "Аліна Горб — головна",
    nav: "Навігація сайтом",
    open: "Відкрити меню",
    close: "Закрити меню",
    home: "Головна",
    topics: "Напрями",
    about: "Про Аліну",
    process: "Процес",
    notes: "Нотатки",
    contact: "Контакти",
    privacy: "Конфіденційність",
    developed: "Розроблено",
    copyright: "© Аліна Горб, 2026"
  };

  const links = [
    [text.home, homeHref],
    [text.topics, `${homeHref}#topics`],
    [text.about, `${homeHref}#about`],
    [text.process, `${homeHref}#process`],
    [text.notes, notesHref],
    [text.contact, `${homeHref}#contact`]
  ];
  const desktopLinks = [links[0], links[1], links[4], links[5]];

  const languageSwitch = isRu
    ? `<div class="language-switch" aria-label="Выбор языка"><a href="${alternateHref}" lang="uk" hreflang="uk">UA</a><span aria-hidden="true">/</span><span aria-current="page">RU</span></div>`
    : `<div class="language-switch" aria-label="Вибір мови"><span aria-current="page">UA</span><span aria-hidden="true">/</span><a href="${alternateHref}" lang="ru" hreflang="ru">RU</a></div>`;

  const header = document.querySelector(".site-header");
  if (header) {
    header.id = "top";
    header.className = "site-header inner-page-header";
    header.innerHTML = `
      <div class="page-shell header-row">
        <a class="brand" href="${homeHref}" aria-label="${text.brand}">
          <img src="${logoUrl}" width="512" height="156" alt="${isRu ? "Алина Горб" : "Аліна Горб"}">
        </a>
        <nav class="inner-desktop-nav" aria-label="${text.nav}">
          ${desktopLinks.map(([label, href]) => `<a href="${href}">${label}</a>`).join("")}
        </nav>
        <div class="header-tools">
          ${languageSwitch}
          <button class="mobile-nav-toggle" type="button" aria-label="${text.open}" aria-expanded="false" aria-controls="inner-navigation" data-inner-menu-toggle><span class="menu-icon" aria-hidden="true"></span></button>
        </div>
        <nav class="mobile-navigation" id="inner-navigation" aria-label="${text.nav}" data-inner-menu hidden>
          ${links.map(([label, href]) => `<a href="${href}">${label}</a>`).join("")}
        </nav>
      </div>`;
  }

  const footer = document.querySelector(".site-footer");
  if (footer) {
    footer.innerHTML = `
      <div class="page-shell footer-main">
        <a class="footer-brand" href="${homeHref}" aria-label="${text.brand}">
          <img src="${logoUrl}" width="512" height="156" alt="${isRu ? "Алина Горб" : "Аліна Горб"}">
        </a>
        <nav class="footer-links" aria-label="${text.nav}">
          ${languageSwitch}
          <a href="mailto:hello@alinahorb.com">Email</a>
          <a href="https://t.me/alina_horb1991" target="_blank" rel="noopener noreferrer">Telegram</a>
          <a href="https://instagram.com/ng_alina_dp" target="_blank" rel="noopener noreferrer">Instagram</a>
          <a href="${privacyHref}">${text.privacy}</a>
        </nav>
        <div class="footer-meta"><span>${text.copyright}</span></div>
      </div>
      <div class="page-shell footer-bottom">
        <a href="${homeHref}">alinahorb.com</a>
        <span class="maker-credit"><small>${text.developed}</small><a href="https://proai-expert.com/" target="_blank" rel="noopener noreferrer">ProAI Expert</a></span>
      </div>`;
  }

  const toggle = document.querySelector("[data-inner-menu-toggle]");
  const menu = document.querySelector("[data-inner-menu]");
  if (!toggle || !menu) return;

  const closeMenu = () => {
    menu.hidden = true;
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-label", text.open);
  };

  const openMenu = () => {
    menu.hidden = false;
    toggle.setAttribute("aria-expanded", "true");
    toggle.setAttribute("aria-label", text.close);
  };

  toggle.addEventListener("click", () => {
    if (menu.hidden) openMenu(); else closeMenu();
  });

  menu.addEventListener("click", (event) => {
    if (event.target.closest("a")) closeMenu();
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeMenu();
  });

  document.addEventListener("click", (event) => {
    if (!menu.hidden && !event.target.closest(".inner-page-header")) closeMenu();
  });
})();
