(() => {
  const path = window.location.pathname || "/";
  const isRu = path === "/ru" || path.startsWith("/ru/");
  const home = isRu ? "/ru/" : "/";
  const notes = isRu ? "/ru/notes/" : "/notes/";
  const contact = `${home}#contact`;
  const about = `${home}#about`;
  const support = `${home}#support`;
  const otherLanguagePath = isRu
    ? (path.replace(/^\/ru/, "") || "/")
    : (`/ru${path === "/" ? "/" : path}`);

  const labels = isRu
    ? {
        brand: "Алина Горб — психолог",
        menu: "Открыть меню",
        close: "Закрыть меню",
        home: "Главная",
        support: "Поддержка",
        about: "Об Алине",
        notes: "Заметки",
        contact: "Контакты и запись",
        copyright: "© Алина Горб, 2026",
        made: "Разработано"
      }
    : {
        brand: "Аліна Горб — психолог",
        menu: "Відкрити меню",
        close: "Закрити меню",
        home: "Головна",
        support: "Підтримка",
        about: "Про Аліну",
        notes: "Нотатки",
        contact: "Контакти та запис",
        copyright: "© Аліна Горб, 2026",
        made: "Розроблено"
      };

  const logo = isRu
    ? "/assets/images/logos/alina-horb-logo-ru-dark.png"
    : "/assets/images/logos/alina-horb-logo-ua-dark.png";

  const header = document.querySelector(".site-header");
  if (header) {
    header.className = "site-header global-header-shell";
    header.id = "top";
    header.innerHTML = `
      <div class="page-shell global-header-row">
        <a class="global-brand" href="${home}" aria-label="${labels.brand}">
          <img src="${logo}" width="512" height="156" alt="${labels.brand}">
        </a>
        <div class="global-header-actions">
          <div class="global-language-switch" aria-label="${isRu ? "Выбор языка" : "Вибір мови"}">
            ${isRu ? `<a href="${otherLanguagePath}" lang="uk" hreflang="uk">UA</a><span aria-hidden="true">/</span><span aria-current="page">RU</span>` : `<span aria-current="page">UA</span><span aria-hidden="true">/</span><a href="${otherLanguagePath}" lang="ru" hreflang="ru">RU</a>`}
          </div>
          <button class="global-menu-toggle" type="button" aria-label="${labels.menu}" aria-expanded="false" aria-controls="global-menu-panel"><span aria-hidden="true"></span></button>
        </div>
        <nav class="global-menu-panel" id="global-menu-panel" aria-label="${isRu ? "Навигация" : "Навігація"}" hidden>
          <a href="${home}">${labels.home}</a>
          <a href="${support}">${labels.support}</a>
          <a href="${about}">${labels.about}</a>
          <a href="${notes}">${labels.notes}</a>
          <a href="${contact}">${labels.contact}</a>
        </nav>
      </div>`;

    const toggle = header.querySelector(".global-menu-toggle");
    const panel = header.querySelector(".global-menu-panel");
    const closeMenu = () => {
      panel.hidden = true;
      toggle.setAttribute("aria-expanded", "false");
      toggle.setAttribute("aria-label", labels.menu);
    };
    toggle.addEventListener("click", () => {
      const opening = panel.hidden;
      panel.hidden = !opening;
      toggle.setAttribute("aria-expanded", String(opening));
      toggle.setAttribute("aria-label", opening ? labels.close : labels.menu);
    });
    panel.addEventListener("click", (event) => {
      if (event.target.closest("a")) closeMenu();
    });
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") closeMenu();
    });
    document.addEventListener("click", (event) => {
      if (!header.contains(event.target)) closeMenu();
    });
  }

  const footer = document.querySelector(".site-footer");
  if (footer) {
    footer.className = "site-footer global-footer-shell";
    footer.innerHTML = `
      <div class="page-shell global-footer-top">
        <a class="global-footer-brand" href="${home}" aria-label="${labels.brand}">
          <img src="${logo}" width="512" height="156" alt="${labels.brand}">
        </a>
        <nav class="global-footer-nav" aria-label="${isRu ? "Ссылки в подвале" : "Посилання у футері"}">
          <a href="${home}">${labels.home}</a>
          <a href="${notes}">${labels.notes}</a>
          <a href="${contact}">${labels.contact}</a>
          <a href="mailto:alinahorb1991@gmail.com">Email</a>
          <a href="https://t.me/alina_horb1991" target="_blank" rel="noopener noreferrer">Telegram</a>
          <a href="https://instagram.com/ng_alina_dp" target="_blank" rel="noopener noreferrer">Instagram</a>
        </nav>
        <p class="global-footer-copy">${labels.copyright}</p>
      </div>
      <div class="page-shell global-footer-bottom">
        <span>alinahorb.com</span>
        <span class="global-maker"><span>${labels.made}</span><a href="https://proai-expert.com/" target="_blank" rel="noopener noreferrer">ProAI Expert</a></span>
      </div>`;
  }
})();
