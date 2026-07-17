(() => {
  "use strict";

  if (window.__ALINA_EDITORIAL_NAV_V1__) return;
  window.__ALINA_EDITORIAL_NAV_V1__ = true;

  const pathname = window.location.pathname;
  const projectMarker = "/alina-horb-website/";
  const rootPath = pathname.includes(projectMarker) ? projectMarker : "/";
  const relativePath = pathname.startsWith(rootPath) ? pathname.slice(rootPath.length) : pathname.replace(/^\//, "");
  const isRu = document.documentElement.lang.toLowerCase().startsWith("ru") || relativePath.startsWith("ru/");
  const cleanPath = relativePath.replace(/^ru\//, "");
  const isHome = cleanPath === "" || cleanPath === "index.html";
  const isNotesHub = Boolean(document.querySelector(".notes-hub-index"));
  const isArticle = Boolean(document.querySelector(".article-toc")) || document.body.classList.contains("article-template-v32");
  const pageKey = isHome ? "home"
    : cleanPath.startsWith("about/") ? "about"
      : cleanPath.startsWith("consultations/") ? "consultations"
        : cleanPath.startsWith("notes/") ? "notes"
          : "other";

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
    materials: "Материалы",
    contents: "Содержание",
    booking: "Записаться",
    bookingFull: "Записаться на консультацию",
    nav: "Основная навигация сайта и разделы текущей страницы",
    fallbackNav: "Основные разделы сайта",
    open: "Открыть меню",
    close: "Закрыть меню"
  } : {
    site: "Розділи сайту",
    local: "На цій сторінці",
    materials: "Матеріали",
    contents: "Зміст",
    booking: "Записатися",
    bookingFull: "Записатися на консультацію",
    nav: "Основна навігація сайту та розділи поточної сторінки",
    fallbackNav: "Основні розділи сайту",
    open: "Відкрити меню",
    close: "Закрити меню"
  };

  const localLabel = isArticle ? text.contents : isNotesHub ? text.materials : text.local;
  const escapeHtml = (value) => String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");

  const pageLinksMarkup = (mobile = false) => pages.map((page, index) => {
    const current = page.key === pageKey ? ' aria-current="page"' : "";
    const className = mobile ? "editorial-mobile-page" : "rail-page-link";
    const labelMarkup = mobile
      ? `<strong>${escapeHtml(page.label)}</strong>`
      : `<span>${escapeHtml(page.label)}</span>`;
    return `<a class="${className}" href="${page.href}"${current}><span class="rail-page-number">${String(index + 1).padStart(2, "0")}</span>${labelMarkup}<span class="rail-page-arrow" aria-hidden="true">→</span></a>`;
  }).join("");

  const hashTarget = (href) => {
    if (!href || href[0] !== "#") return null;
    try {
      return document.getElementById(decodeURIComponent(href.slice(1)));
    } catch {
      return null;
    }
  };

  const getLocalLinks = () => {
    const existingRail = document.querySelector(".side-navigation");
    let source = [];

    if (existingRail) {
      source = [...existingRail.querySelectorAll('a[href^="#"]')].map((link) => ({
        href: link.getAttribute("href"),
        label: link.querySelector("span")?.textContent?.trim() || link.textContent.trim()
      }));
    }
    if (!source.length && isNotesHub) {
      source = [...document.querySelectorAll('.notes-hub-index a[href^="#"]')].map((link) => ({
        href: link.getAttribute("href"),
        label: link.textContent.trim()
      }));
      document.body.classList.add("notes-hub-page");
    } else if (!source.length && isArticle) {
      source = [...document.querySelectorAll('.article-toc a[href^="#"]')].map((link) => ({
        href: link.getAttribute("href"),
        label: link.textContent.trim()
      }));
    }

    const allowedHome = new Set(["#support", "#topics", "#process", "#contact"]);
    if (pageKey === "home") source = source.filter((item) => allowedHome.has(item.href));
    if (pageKey === "consultations") source = source.filter((item) => item.href !== "#boundaries");

    const seen = new Set();
    return source.filter((item) => {
      if (!item.href || !item.label || seen.has(item.href) || !hashTarget(item.href)) return false;
      seen.add(item.href);
      return true;
    }).slice(0, 6);
  };

  const localLinks = getLocalLinks();
  const localDesktopMarkup = localLinks.map((item) =>
    `<a class="rail-local-link" href="${item.href}">${escapeHtml(item.label)}</a>`
  ).join("");
  const localMobileMarkup = localLinks.map((item) =>
    `<a class="editorial-mobile-local-link" href="${item.href}">${escapeHtml(item.label)}</a>`
  ).join("");

  const railMarkup = `
    <div class="rail-group rail-primary">
      <p class="rail-label">${text.site}</p>
      <div class="rail-primary-links">${pageLinksMarkup(false)}</div>
      <a class="rail-booking-link" href="${bookingHref}"><span>${text.booking}</span><span aria-hidden="true">→</span></a>
    </div>
    ${localLinks.length ? `<div class="rail-group rail-local"><p class="rail-label">${localLabel}</p><div class="rail-local-links">${localDesktopMarkup}</div></div>` : ""}`;

  let rail = document.querySelector(".side-navigation");
  if (rail) {
    rail.classList.add("editorial-rail");
    rail.classList.remove("editorial-rail-placeholder");
    rail.removeAttribute("aria-hidden");
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

  const fallbackDesktopNav = document.querySelector(".inner-desktop-nav");
  if (rail) {
    fallbackDesktopNav?.setAttribute("hidden", "");
  } else if (fallbackDesktopNav) {
    fallbackDesktopNav.setAttribute("aria-label", text.fallbackNav);
    fallbackDesktopNav.innerHTML = `
      ${pages.slice(1).map((page) => `<a href="${page.href}"${page.key === pageKey ? ' aria-current="page"' : ""}>${escapeHtml(page.label)}</a>`).join("")}
      <a class="editorial-header-booking" href="${bookingHref}">${text.booking}</a>`;
  }

  const mobileMenu = document.querySelector(".mobile-navigation");
  const mobileToggle = document.querySelector("[data-menu-toggle], [data-inner-menu-toggle]");
  const header = document.querySelector(".site-header");

  if (mobileMenu) {
    if (!mobileMenu.id) mobileMenu.id = "editorial-navigation";
    mobileMenu.classList.add("editorial-mobile-menu");
    mobileMenu.setAttribute("aria-label", text.nav);
    mobileMenu.setAttribute("role", "dialog");
    mobileMenu.setAttribute("aria-modal", "true");
    mobileMenu.innerHTML = `
      <div class="editorial-mobile-inner ${localLinks.length ? "has-local-navigation" : "is-global-only"}">
        <div class="editorial-mobile-primary">
          <p class="editorial-mobile-label">${text.site}</p>
          ${pageLinksMarkup(true)}
          <a class="editorial-mobile-booking" href="${bookingHref}"><span>${text.bookingFull}</span><span aria-hidden="true">→</span></a>
        </div>
        ${localLinks.length ? `<div class="editorial-mobile-local"><p class="editorial-mobile-label">${localLabel}</p><div class="editorial-mobile-local-links">${localMobileMarkup}</div></div>` : ""}
      </div>`;
  }

  if (mobileToggle && mobileMenu) {
    mobileToggle.setAttribute("aria-controls", mobileMenu.id);
    mobileToggle.setAttribute("aria-expanded", "false");
    mobileToggle.setAttribute("aria-label", text.open);
    mobileMenu.hidden = true;
  }

  const updateHeaderHeight = () => {
    const height = Math.round(header?.getBoundingClientRect().height || (window.innerWidth <= 759 ? 72 : 86));
    document.documentElement.style.setProperty("--editorial-header-height", `${height}px`);
  };

  let lockedScrollY = 0;
  let bodyStyleSnapshot = null;
  const inertTargets = [...document.body.children].filter((element) => element !== header && !["SCRIPT", "STYLE", "LINK"].includes(element.tagName));
  const inertSnapshot = inertTargets.map((element) => ({
    element,
    hadInert: element.hasAttribute("inert")
  }));

  const setBackgroundInert = (inert) => {
    inertSnapshot.forEach(({ element, hadInert }) => {
      if (inert) element.setAttribute("inert", "");
      else if (!hadInert) element.removeAttribute("inert");
    });
  };

  const lockPage = () => {
    if (bodyStyleSnapshot) return;
    lockedScrollY = Math.max(window.scrollY, 0);
    bodyStyleSnapshot = {
      position: document.body.style.position,
      top: document.body.style.top,
      left: document.body.style.left,
      right: document.body.style.right,
      width: document.body.style.width,
      overflow: document.body.style.overflow
    };
    Object.assign(document.body.style, {
      position: "fixed",
      top: `-${lockedScrollY}px`,
      left: "0",
      right: "0",
      width: "100%",
      overflow: "hidden"
    });
  };

  const unlockPage = () => {
    if (!bodyStyleSnapshot) return;
    Object.assign(document.body.style, bodyStyleSnapshot);
    bodyStyleSnapshot = null;
    window.scrollTo(0, lockedScrollY);
  };

  let menuWasOpen = false;
  const syncMenuState = ({ focusFirst = false } = {}) => {
    if (!mobileToggle || !mobileMenu) return;
    const open = mobileToggle.getAttribute("aria-expanded") === "true" && !mobileMenu.hidden;
    document.body.classList.toggle("editorial-menu-open", open);
    mobileToggle.setAttribute("aria-label", open ? text.close : text.open);

    if (open) {
      updateHeaderHeight();
      setBackgroundInert(true);
      lockPage();
      if (!menuWasOpen || focusFirst) {
        window.requestAnimationFrame(() => {
          const current = mobileMenu.querySelector('[aria-current="page"]');
          const first = current || mobileMenu.querySelector("a, button, [tabindex]:not([tabindex='-1'])");
          first?.focus({ preventScroll: true });
        });
      }
    } else {
      setBackgroundInert(false);
      unlockPage();
    }

    menuWasOpen = open;
  };

  const setMenuOpen = (open, { restoreFocus = false, focusFirst = false } = {}) => {
    if (!mobileToggle || !mobileMenu) return;
    mobileMenu.hidden = !open;
    mobileToggle.setAttribute("aria-expanded", String(open));
    syncMenuState({ focusFirst });
    if (!open && restoreFocus) mobileToggle.focus({ preventScroll: true });
  };

  const closeMenu = ({ restoreFocus = false } = {}) => setMenuOpen(false, { restoreFocus });

  if (mobileToggle && mobileMenu) {
    mobileToggle.addEventListener("click", () => {
      const open = mobileToggle.getAttribute("aria-expanded") === "true" && !mobileMenu.hidden;
      setMenuOpen(!open, { focusFirst: !open });
    });
    syncMenuState();
  }

  mobileMenu?.addEventListener("click", (event) => {
    if (event.target.closest("a")) closeMenu();
  });

  document.addEventListener("keydown", (event) => {
    if (!mobileToggle || !mobileMenu) return;
    const open = mobileToggle.getAttribute("aria-expanded") === "true" && !mobileMenu.hidden;
    if (!open) return;

    if (event.key === "Escape") {
      event.preventDefault();
      closeMenu({ restoreFocus: true });
      return;
    }

    if (event.key !== "Tab") return;
    const focusable = [mobileToggle, ...mobileMenu.querySelectorAll(
      'a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])'
    )].filter((element) => !element.hidden && element.getClientRects().length > 0);

    if (!focusable.length) return;
    const first = focusable[0];
    const last = focusable[focusable.length - 1];

    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });

  const tabletQuery = window.matchMedia("(max-width: 1180px)");
  const handleViewportChange = () => {
    updateHeaderHeight();
    if (!tabletQuery.matches) closeMenu();
  };
  window.addEventListener("resize", handleViewportChange);
  window.visualViewport?.addEventListener("resize", handleViewportChange);
  tabletQuery.addEventListener?.("change", handleViewportChange);
  updateHeaderHeight();

  const localRailLinks = [...document.querySelectorAll(".editorial-rail .rail-local-link")];
  if (localRailLinks.length && "IntersectionObserver" in window) {
    const sections = localRailLinks.map((link) => hashTarget(link.getAttribute("href"))).filter(Boolean);
    const activate = (id) => localRailLinks.forEach((link) => {
      link.classList.toggle("is-active", link.getAttribute("href") === `#${id}`);
    });
    const observer = new IntersectionObserver((entries) => {
      const visible = entries
        .filter((entry) => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio);
      if (visible[0]) activate(visible[0].target.id);
    }, {
      threshold: [.18, .42, .68],
      rootMargin: "-18% 0px -58%"
    });
    sections.forEach((section) => observer.observe(section));
    if (sections[0]) activate(sections[0].id);
  }
})();
