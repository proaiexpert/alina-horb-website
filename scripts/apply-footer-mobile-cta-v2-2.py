#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def replace_footer(path: Path, locale: str) -> None:
    text = path.read_text(encoding="utf-8")
    if "data-mobile-booking-cta" in text and "footer-main" in text:
        return

    if locale == "uk":
        cta = '<a class="mobile-booking-cta" href="#contact" data-mobile-booking-cta hidden>Записатися</a>'
        footer = '''<footer class="site-footer">
    <div class="page-shell footer-main">
      <a class="footer-brand" href="#top" aria-label="Аліна Горб — психолог"><img src="assets/images/logos/alina-horb-logo-ua-dark.png" width="512" height="156" alt="Аліна Горб"></a>
      <nav class="footer-links" aria-label="Контакти та мова">
        <div class="language-switch"><span aria-current="page">UA</span><span>/</span><a href="./ru/" lang="ru" hreflang="ru">RU</a></div>
        <a href="mailto:alinahorb1991@gmail.com">Email</a>
        <a href="https://t.me/alina_horb1991" target="_blank" rel="noopener noreferrer">Telegram</a>
        <a href="https://instagram.com/ng_alina_dp" target="_blank" rel="noopener noreferrer">Instagram</a>
      </nav>
      <div class="footer-meta"><span>© Аліна Горб, 2026</span></div>
    </div>
    <div class="page-shell footer-bottom">
      <span>alinahorb.com</span>
      <span class="maker-credit"><small>Розроблено</small><a href="https://proai-expert.com/" target="_blank" rel="noopener noreferrer">ProAI Expert</a></span>
    </div>
  </footer>'''
    else:
        cta = '<a class="mobile-booking-cta" href="#contact" data-mobile-booking-cta hidden>Записаться</a>'
        footer = '''<footer class="site-footer"><div class="page-shell footer-main"><a class="footer-brand" href="#top" aria-label="Алина Горб — психолог"><img src="../assets/images/logos/alina-horb-logo-ru-dark.png" width="512" height="156" alt="Алина Горб"></a><nav class="footer-links" aria-label="Контакты и язык"><div class="language-switch"><a href="../" lang="uk" hreflang="uk">UA</a><span>/</span><span aria-current="page">RU</span></div><a href="mailto:alinahorb1991@gmail.com">Email</a><a href="https://t.me/alina_horb1991" target="_blank" rel="noopener noreferrer">Telegram</a><a href="https://instagram.com/ng_alina_dp" target="_blank" rel="noopener noreferrer">Instagram</a></nav><div class="footer-meta"><span>© Алина Горб, 2026</span></div></div><div class="page-shell footer-bottom"><span>alinahorb.com</span><span class="maker-credit"><small>Разработано</small><a href="https://proai-expert.com/" target="_blank" rel="noopener noreferrer">ProAI Expert</a></span></div></footer>'''

    pattern = r'<footer class="site-footer">.*?</footer>'
    updated, count = re.subn(pattern, cta + "\n  " + footer, text, count=1, flags=re.S)
    if count != 1:
        raise SystemExit(f"Footer not found in {path}")
    path.write_text(updated, encoding="utf-8")


replace_footer(ROOT / "index.html", "uk")
replace_footer(ROOT / "ru/index.html", "ru")

js_path = ROOT / "assets/js/site.v2.js"
js = js_path.read_text(encoding="utf-8")
if "const initMobileBookingCta" not in js:
    function = '''  const initMobileBookingCta = () => {
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

'''
    js = js.replace("  const init = () => {", function + "  const init = () => {", 1)
    js = js.replace("    initContactForm();\n", "    initContactForm();\n    initMobileBookingCta();\n", 1)
    js_path.write_text(js, encoding="utf-8")

css_path = ROOT / "assets/css/site.v2.css"
css = css_path.read_text(encoding="utf-8")
if "/* Footer + mobile conversion polish V2.2 */" not in css:
    css += '''

/* Footer + mobile conversion polish V2.2 */
.site-footer { border-top: 1px solid var(--line); background: var(--ivory); }
.footer-main {
  min-height: 108px;
  display: grid;
  grid-template-columns: 150px minmax(0, 1fr) auto;
  gap: 36px;
  align-items: center;
  padding-block: 26px 20px;
}
.footer-brand { width: 124px; align-self: center; }
.footer-brand img { width: 100%; height: auto; object-fit: contain; }
.footer-links { display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 4px 20px; font-size: 12px; }
.footer-links > a { min-height: 44px; display: inline-flex; align-items: center; }
.footer-meta { justify-self: end; color: var(--muted); font-size: 11px; text-align: right; white-space: nowrap; }
.footer-bottom { min-height: 48px; display: flex; align-items: center; justify-content: space-between; gap: 24px; border-top: 1px solid var(--line); padding-block: 12px 16px; color: var(--muted); font-size: 11px; }
.footer-bottom .maker-credit { display: inline-flex; align-items: baseline; gap: 8px; justify-self: auto; text-align: right; }
.footer-bottom .maker-credit small { display: inline; color: var(--muted); }
.footer-bottom .maker-credit a { color: var(--terracotta); font-family: var(--serif); font-size: 15px; }

.mobile-booking-cta { display: none; }

@media (max-width: 800px) {
  .footer-main { grid-template-columns: 118px minmax(0, 1fr); gap: 18px 28px; padding-block: 24px 16px; }
  .footer-brand { width: 108px; align-self: start; }
  .footer-links { justify-content: flex-start; gap: 0 16px; }
  .footer-meta { grid-column: 2; justify-self: start; text-align: left; }
  .footer-bottom { align-items: flex-start; flex-direction: column; gap: 5px; padding-block: 12px 18px; }

  .mobile-booking-cta {
    position: fixed;
    z-index: 60;
    left: 50%;
    bottom: max(14px, env(safe-area-inset-bottom));
    width: min(360px, calc(100% - 30px));
    min-height: 52px;
    align-items: center;
    justify-content: center;
    border: 1px solid var(--terracotta);
    border-radius: 2px;
    background: var(--terracotta);
    box-shadow: 0 12px 34px rgba(47, 48, 45, .2);
    color: #fff;
    font-size: 13px;
    font-weight: 600;
    opacity: 0;
    pointer-events: none;
    transform: translate(-50%, calc(100% + 30px));
    transition: opacity .22s ease, transform .3s var(--ease), background .2s ease;
  }
  .mobile-booking-cta:not([hidden]) { display: flex; }
  .mobile-booking-cta.is-visible { opacity: 1; pointer-events: auto; transform: translate(-50%, 0); }
  .mobile-booking-cta:active { background: var(--terracotta-dark); }
}

@media (max-width: 520px) {
  .footer-main { grid-template-columns: 1fr; gap: 12px; }
  .footer-brand { width: 104px; }
  .footer-links { justify-content: flex-start; }
  .footer-meta { grid-column: 1; }
}
'''
    css_path.write_text(css, encoding="utf-8")

print("Footer and mobile CTA polish applied.")
