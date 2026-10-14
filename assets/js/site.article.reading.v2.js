/* TASK 028: conflict article only. Passive, rAF-batched reading mode. */
(() => {
  "use strict";
  if (!document.body.matches('.article-template-v32[data-note="conflict"]')) return;
  const header = document.querySelector(".site-header--canonical.inner-page-header");
  const menu = document.querySelector(".mobile-navigation");
  const toggle = document.querySelector("[data-menu-toggle]");
  if (!header) return;

  const mobile = window.matchMedia("(max-width: 1180px)");
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)");
  const isMenuOpen = () => document.body.classList.contains("editorial-menu-open") ||
    (toggle?.getAttribute("aria-expanded") === "true" && menu && !menu.hidden);
  let previousY = Math.max(0, window.scrollY);
  let accumulated = 0;
  let direction = 0;
  let hidden = false;
  let frame = 0;
  let lastWidth = window.innerWidth;
  let anchorHold = 0;

  function setHidden(next) {
    next = Boolean(next && mobile.matches && !isMenuOpen() && !header.contains(document.activeElement));
    if (hidden === next) return;
    hidden = next;
    header.classList.toggle("is-reading-hidden", next);
    header.toggleAttribute("inert", next);
    if (next) header.setAttribute("aria-hidden", "true");
    else header.removeAttribute("aria-hidden");
  }
  function tick() {
    frame = 0;
    const y = Math.max(0, window.scrollY);
    const delta = y - previousY;
    previousY = y;
    if (!mobile.matches || isMenuOpen() || y <= 18 || performance.now() < anchorHold) {
      accumulated = 0;
      direction = 0;
      setHidden(false);
      return;
    }
    // Before the initial reading scroll, keep the normal site header in place.
    if (y < Math.max(135, Math.min(window.innerHeight * 0.28, 235))) {
      accumulated = 0;
      direction = 0;
      setHidden(false);
      return;
    }
    if (Math.abs(delta) < 1.5) return;
    const nextDirection = delta > 0 ? 1 : -1;
    if (nextDirection !== direction) accumulated = 0;
    direction = nextDirection;
    accumulated = Math.min(120, accumulated + Math.abs(delta));
    if (direction > 0 && accumulated >= 28) setHidden(true);
    else if (direction < 0 && accumulated >= 16) setHidden(false);
  }
  function schedule() {
    if (!frame) frame = requestAnimationFrame(tick);
  }
  function showForNavigation() {
    anchorHold = performance.now() + 950;
    accumulated = 0;
    direction = 0;
    setHidden(false);
    previousY = Math.max(0, window.scrollY);
  }
  function onResize() {
    if (lastWidth !== window.innerWidth) {
      lastWidth = window.innerWidth;
      showForNavigation();
    }
    schedule();
  }
  window.addEventListener("scroll", schedule, { passive: true });
  window.addEventListener("resize", onResize, { passive: true });
  mobile.addEventListener?.("change", showForNavigation);
  document.addEventListener("click", event => {
    if (event.target.closest('a[href^="#"], [data-menu-toggle]')) showForNavigation();
  }, { capture: true });
  document.addEventListener("focusin", event => {
    if (header.contains(event.target)) showForNavigation();
  });
  document.addEventListener("keydown", event => {
    if (event.key === "Tab" && header.contains(document.activeElement)) showForNavigation();
  });
  const observer = new MutationObserver(() => {
    if (isMenuOpen()) showForNavigation();
    else {
      previousY = Math.max(0, window.scrollY);
      schedule();
    }
  });
  observer.observe(document.body, { attributes: true, attributeFilter: ["class"] });
  if (toggle) observer.observe(toggle, { attributes: true, attributeFilter: ["aria-expanded"] });
  window.addEventListener("hashchange", showForNavigation);
  window.addEventListener("popstate", showForNavigation);
  window.addEventListener("pageshow", showForNavigation);
  window.addEventListener("pagehide", () => { if (frame) cancelAnimationFrame(frame); setHidden(false); });
  // Reduced motion is implemented in CSS; no JS-driven animation is used.
  void reduced;
  schedule();
})();
