(() => {
  "use strict";

  if (window.__ALINA_EDITORIAL_NAV_V1__) return;
  window.__ALINA_EDITORIAL_NAV_V1__ = true;

  const script = document.currentScript;
  if (!script) return;

  const stylesheetHref = new URL("../css/site.navigation.v1.css?v=20260717-nav1", script.src).href;
  if (!document.querySelector(`link[href="${stylesheetHref}"]`)) {
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = stylesheetHref;
    document.head.appendChild(link);
  }

  const pathname = window.location.pathname;
  const projectMarker = "/alina-horb-website/";
  const rootPath = pathname.includes(projectMarker) ? projectMarker : "/";
  const relativePath = pathname.startsWith(rootPath) ? pathname.slice(rootPath.length) : pathname.replace(/^\//, "");
  const isRu = document.documentElement.lang.toLowerCase().startsWith("ru") || relativePath.startsWith("ru/");
  const cleanPath = relativePath.replace(/^ru\//, "");
  const pageKey = cleanPath.startsWith("about/") ? "about"
    : cleanPath.startsWith("consultations/") ? "consultations"
      : cleanPath.startsWith("notes/") ? "notes"
        : "home";

  const localeRoot = `${rootPath}${isRu ? "ru/" : ""}`;
  const pages = [
    { key: "home", label: isRu ? "Главная" : "Головна", href: localeRoot },
    { key: "about", label: isRu ? "Об Алине" : "Про Аліну", href: `${localeRoot}about/` },
    { key: "consultations", label: isRu ? "Консультации" : "Консультації", href: `${localeRoot}consultations/` },
    { key: "notes", label: isRu ? "Заметки" : "Нотатки", href: `${localeRoot}notes/` }
  ];
  const bookingHref = `${localeRoot}consultations/#contact`;
  const text = isRu ? {
    site: "Разделы сайта",
    local: "На этой странице",
    booking: "Записаться",
    nav: "Основная навигация сайта и разделы текущей страницы",
    open: "Открыть меню",
    close: "Закрыть меню"
  } : {
    site: "Розділи сайту",
    local: "На цій сторінці",
    booking: "Записатися",
    nav: "Основна навігація сайту та розділи поточної сторінки",
    open: "Відкрити меню",
    close: "Закрити меню"
  };

  const escapeHtml = (value) => String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");

  const pageLinksMarkup = (mobile = false) => pages.map((page, index) => {
    const current = page.key === pageKey ? ' aria-current="page"' : "";
    const className = mobile ? "editorial-mobile-page" : "rail-page-link";
    return `<a class="${className}" href="${page.href}"${current}><span class="rail-page-number">${String(index + 1).padStart(2, "0")}</span>${mobile ? `<strong>${escapeHtml(page.label)}</strong>` : `<span>${escapeHtml(page.label)}</span>`}<span class="rail-page-arrow" aria-hidden="true">→</span></a>`;
  }).join("");

  const getLocalLinks = () => {
    const existingRail = document.querySelector(".side-navigation");
    let source = [];

    if (existingRail) {
      source = [...existingRail.querySelectorAll('a[href^="#"]')].map((link) => ({
        href: link.getAttribute("href"),
        label: link.querySelector("span")?.textContent?.trim() || link.textContent.trim()
      }));
    } else if (document.querySelector(".notes-hub-index")) {
      source = [...document.querySelectorAll('.notes-hub-index a[href^="#"]')].map((link) => ({ href: link.getAttribute("href"), label: link.textContent.trim() }));
      document.body.classList.add("notes-hub-page");
    } else if (document.querySelector(".article-toc")) {
      source = [...document.querySelectorAll('.article-toc a[href^="#"]')].map((link) => ({ href: link.getAttribute("href"), label: link.textContent.trim() }));
    }

    const allowedHome = new Set(["#support", "#topics", "#process", "#contact"]);
    if (pageKey === "home") source = source.filter((item) => allowedHome.has(item.href));
    if (pageKey === "consultations") source = source.filter((item) => item.href !== "#boundaries");

    const seen = new Set();
    return source.filter((item) => {
      if (!item.href || !item.label || seen.has(item.href)) return false;
      seen.add(item.href);
      return Boolean(document.querySelector(item.href));
    }).slice(0, 6);
  };

  const localLinks = getLocalLinks();
  const localDesktopMarkup = localLinks.map((item) => `<a class="rail-local-link" href="${item.href}">${escapeHtml(item.label)}</a>`).join("");
  const localMobileMarkup = localLinks.map((item) => `<a class="editorial-mobile-local-link" href="${item.href}">${escapeHtml(item.label)}</a>`).join("");

  const railMarkup = `
    <div class="rail-group rail-primary">
      <p class="rail-label">${text.site}</p>
      <div class="rail-primary-links">${pageLinksMarkup(false)}</div>
      <a class="rail-booking-link" href="${bookingHref}"><span>${text.booking}</span><span aria-hidden="true">→</span></a>
    </div>
    ${localLinks.length ? `<div class="rail-group rail-local"><p class="rail-label">${text.local}</p><div class="rail-local-links">${localDesktopMarkup}</div></div>` : ""}`;

  let rail = document.querySelector(".side-navigation");
  if (rail) {
    rail.classList.add("editorial-rail");
    rail.setAttribute("aria-label", text.nav);
    rail.innerHTML = railMarkup;
  } else {
    const host = document.querySelector(".notes-hub-hero-grid, .article-hero-grid");
    if (host) {
      rail = document.createElement("nav");
      rail.className = "editorial-rail";
      rail.setAttribute("aria-label", text.nav);
      rail.innerHTML = railMarkup;
      host.classList.add("has-editorial-rail");
      host.prepend(rail);
    }
  }

  const mobileMenu = document.querySelector(".mobile-navigation");
  const mobileToggle = document.querySelector("[data-menu-toggle], [data-inner-menu-toggle]");
  document.querySelector(".inner-desktop-nav")?.remove();

  if (mobileMenu) {
    mobileMenu.classList.add("editorial-mobile-menu");
    mobileMenu.setAttribute("aria-label", text.nav);
    mobileMenu.innerHTML = `
      <div class="editorial-mobile-inner">
        <div class="editorial-mobile-primary">
          <p class="editorial-mobile-label">${text.site}</p>
          ${pageLinksMarkup(true)}
          <a class="editorial-mobile-booking" href="${bookingHref}"><span>${text.booking}</span><span aria-hidden="true">→</span></a>
        </div>
        ${localLinks.length ? `<div class="editorial-mobile-local"><p class="editorial-mobile-label">${text.local}</p><div class="editorial-mobile-local-links">${localMobileMarkup}</div></div>` : ""}
      </div>`;
  }

  const syncMenuState = () => {
    if (!mobileToggle) return;
    const open = mobileToggle.getAttribute("aria-expanded") === "true";
    document.body.classList.toggle("editorial-menu-open", open);
    mobileToggle.setAttribute("aria-label", open ? text.close : text.open);
  };

  if (mobileToggle) {
    new MutationObserver(syncMenuState).observe(mobileToggle, { attributes: true, attributeFilter: ["aria-expanded"] });
    syncMenuState();
  }

  mobileMenu?.addEventListener("click", (event) => {
    if (!event.target.closest("a")) return;
    document.body.classList.remove("editorial-menu-open");
  });

  const localRailLinks = [...document.querySelectorAll(".editorial-rail .rail-local-link")];
  if (localRailLinks.length && "IntersectionObserver" in window) {
    const sections = localRailLinks.map((link) => document.querySelector(link.getAttribute("href"))).filter(Boolean);
    const activate = (id) => localRailLinks.forEach((link) => link.classList.toggle("is-active", link.getAttribute("href") === `#${id}`));
    const observer = new IntersectionObserver((entries) => {
      const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio);
      if (visible[0]) activate(visible[0].target.id);
    }, { threshold: [.18, .42, .68], rootMargin: "-18% 0px -58%" });
    sections.forEach((section) => observer.observe(section));
    if (sections[0]) activate(sections[0].id);
  }
})();
