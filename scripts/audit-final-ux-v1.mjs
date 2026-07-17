#!/usr/bin/env node
import { chromium } from "playwright";
import fs from "node:fs/promises";
import path from "node:path";

const baseURL = process.env.AUDIT_BASE_URL || "http://127.0.0.1:4173";
const strict = process.env.AUDIT_STRICT === "1";
const screenshotMode = process.env.AUDIT_SCREENSHOTS === "1";
const outputDir = process.env.AUDIT_OUTPUT_DIR || "qa/final-ux";

const routes = [
  "/",
  "/ru/",
  "/about/",
  "/ru/about/",
  "/consultations/",
  "/ru/consultations/",
  "/notes/",
  "/ru/notes/",
  "/notes/first-consultation/",
  "/ru/notes/first-consultation/",
  "/notes/how-to-start-the-conversation/",
  "/ru/notes/how-to-start-the-conversation/",
  "/notes/when-coping-stops-helping/",
  "/ru/notes/when-coping-stops-helping/",
  "/notes/stress-relocation-and-lost-support/",
  "/ru/notes/stress-relocation-and-lost-support/",
  "/privacy/",
  "/ru/privacy/"
];

const viewports = [
  { name: "mobile", width: 390, height: 844 },
  { name: "tablet", width: 768, height: 1024 },
  { name: "tablet-wide", width: 1024, height: 900 },
  { name: "desktop", width: 1440, height: 1000 }
];

const screenshotRoutes = new Set([
  "/",
  "/ru/",
  "/about/",
  "/ru/about/",
  "/consultations/",
  "/ru/consultations/",
  "/notes/",
  "/ru/notes/",
  "/notes/first-consultation/",
  "/ru/notes/first-consultation/",
  "/privacy/",
  "/ru/privacy/"
]);

const critical = [];
const warnings = [];
const pageReports = [];
const brokenCache = new Map();

const pushIssue = (bucket, viewport, route, message) => {
  bucket.push({ viewport: viewport.name, route, message });
};

const localPathFromURL = (value) => {
  const url = new URL(value);
  if (url.origin !== new URL(baseURL).origin) return null;
  return `${url.pathname}${url.search}`;
};

await fs.mkdir(outputDir, { recursive: true });

const browser = await chromium.launch({ headless: true });
try {
  for (const viewport of viewports) {
    const context = await browser.newContext({
      viewport: { width: viewport.width, height: viewport.height },
      deviceScaleFactor: 1,
      reducedMotion: "no-preference"
    });

    for (const route of routes) {
      const page = await context.newPage();
      const consoleErrors = [];
      const runtimeErrors = [];
      const requestFailures = [];

      await page.addInitScript(() => {
        window.__UX_AUDIT_CLS__ = 0;
        window.__UX_AUDIT_SHIFTS__ = [];
        try {
          new PerformanceObserver((list) => {
            for (const entry of list.getEntries()) {
              if (entry.hadRecentInput) continue;
              window.__UX_AUDIT_CLS__ += entry.value;
              const sources = (entry.sources || []).map((source) => {
                const node = source.node;
                let selector = null;
                if (node instanceof Element) {
                  selector = node.id ? `#${node.id}` : `${node.tagName.toLowerCase()}${node.classList.length ? `.${[...node.classList].join(".")}` : ""}`;
                }
                const serializeRect = (rect) => rect ? ({ x: rect.x, y: rect.y, width: rect.width, height: rect.height }) : null;
                return { selector, previousRect: serializeRect(source.previousRect), currentRect: serializeRect(source.currentRect) };
              });
              window.__UX_AUDIT_SHIFTS__.push({ value: entry.value, sources });
            }
          }).observe({ type: "layout-shift", buffered: true });
        } catch {}
      });

      page.on("console", (message) => {
        if (message.type() === "error") consoleErrors.push(message.text());
      });
      page.on("pageerror", (error) => runtimeErrors.push(error.message));
      page.on("requestfailed", (request) => {
        const url = request.url();
        if (/fonts\.(googleapis|gstatic)\.com/.test(url)) return;
        requestFailures.push(`${request.failure()?.errorText || "failed"}: ${url}`);
      });

      let response;
      try {
        response = await page.goto(`${baseURL}${route}`, { waitUntil: "networkidle", timeout: 45000 });
      } catch (error) {
        pushIssue(critical, viewport, route, `navigation failed: ${error.message}`);
        await page.close();
        continue;
      }

      if (!response || response.status() >= 400) {
        pushIssue(critical, viewport, route, `route returned ${response?.status() ?? "no response"}`);
      }

      await page.evaluate(async () => {
        try {
          await Promise.race([
            document.fonts?.ready || Promise.resolve(),
            new Promise((resolve) => setTimeout(resolve, 2500))
          ]);
        } catch {}
      });
      await page.waitForTimeout(500);

      const metrics = await page.evaluate(({ width, route }) => {
        const visible = (element) => {
          if (!element) return false;
          const style = getComputedStyle(element);
          const rect = element.getBoundingClientRect();
          return style.display !== "none" && style.visibility !== "hidden" && Number(style.opacity) > 0 && rect.width > 0 && rect.height > 0;
        };
        const rect = (element) => {
          if (!element) return null;
          const value = element.getBoundingClientRect();
          return { x: value.x, y: value.y, width: value.width, height: value.height, right: value.right, bottom: value.bottom };
        };
        const ids = [...document.querySelectorAll("[id]")].map((element) => element.id);
        const duplicates = [...new Set(ids.filter((id, index) => ids.indexOf(id) !== index))];
        const textLineWidth = (element) => {
          const range = document.createRange();
          range.selectNodeContents(element);
          const widths = [...range.getClientRects()].map((value) => value.width).filter((value) => value > 0);
          return widths.length ? Math.max(...widths) : 0;
        };
        const paragraphs = [...document.querySelectorAll("main p, main li")]
          .filter(visible)
          .map((element) => ({ width: textLineWidth(element), text: element.textContent.trim().slice(0, 90) }))
          .sort((a, b) => b.width - a.width);
        const form = document.querySelector("form[data-contact-form], .contact-form");
        const h1 = document.querySelector("h1");
        const footer = document.querySelector('.site-footer[data-site-footer="canonical"]');
        const header = document.querySelector(".site-header--canonical");
        const toggle = document.querySelector("[data-menu-toggle]");
        const rail = document.querySelector(".editorial-rail");
        const desktopNav = document.querySelector(".inner-desktop-nav");
        const skip = document.querySelector(".skip-link");
        const skipTarget = skip?.getAttribute("href")?.startsWith("#") ? document.querySelector(skip.getAttribute("href")) : null;
        const localImages = [...document.images].filter((image) => {
          try { return new URL(image.currentSrc || image.src, location.href).origin === location.origin; }
          catch { return false; }
        });
        const failedImages = localImages.filter((image) => image.complete && image.naturalWidth === 0).map((image) => image.currentSrc || image.src);
        const internalLinks = [...new Set([...document.querySelectorAll("a[href]")]
          .map((link) => link.href)
          .filter(Boolean)
          .filter((href) => {
            try {
              const url = new URL(href);
              return url.origin === location.origin && !url.pathname.startsWith("/cdn-cgi/");
            } catch { return false; }
          }))];
        const globalBookingLinks = [...document.querySelectorAll(".rail-booking-link, .editorial-header-booking, .editorial-mobile-booking, .footer-booking")]
          .map((link) => link.getAttribute("href"));
        const languageLink = document.querySelector('.site-header .language-switch a[hreflang], .site-header .language-switch a[lang]');
        const expectedBooking = `${location.pathname.startsWith("/ru/") ? "/ru" : ""}/consultations/#contact`;
        const h1Rect = rect(h1);
        return {
          route,
          viewportWidth: width,
          documentWidth: document.documentElement.scrollWidth,
          bodyWidth: document.body.scrollWidth,
          h1Count: document.querySelectorAll("h1").length,
          headerCount: document.querySelectorAll(".site-header--canonical").length,
          footerCount: document.querySelectorAll('.site-footer[data-site-footer="canonical"]').length,
          duplicateIds: duplicates,
          headerVisible: visible(header),
          footerVisible: visible(footer),
          toggleVisible: visible(toggle),
          railVisible: visible(rail),
          desktopNavVisible: visible(desktopNav),
          skipTargetExists: Boolean(skipTarget),
          failedImages,
          internalLinks,
          globalBookingLinks,
          expectedBooking,
          languageHref: languageLink?.getAttribute("href") || null,
          formWidth: form ? form.getBoundingClientRect().width : null,
          widestText: paragraphs[0] || null,
          h1Rect,
          h1Overflows: Boolean(h1Rect && (h1Rect.left < -1 || h1Rect.right > width + 1)),
          cls: Number(window.__UX_AUDIT_CLS__ || 0),
          shiftSources: window.__UX_AUDIT_SHIFTS__ || [],
          bodyClass: document.body.className
        };
      }, { width: viewport.width, route });

      if (metrics.documentWidth > viewport.width + 1 || metrics.bodyWidth > viewport.width + 1) {
        pushIssue(critical, viewport, route, `horizontal overflow: document=${metrics.documentWidth}px body=${metrics.bodyWidth}px viewport=${viewport.width}px`);
      }
      if (metrics.h1Count !== 1) pushIssue(critical, viewport, route, `expected one H1, found ${metrics.h1Count}`);
      if (metrics.headerCount !== 1 || !metrics.headerVisible) pushIssue(critical, viewport, route, `canonical header missing or hidden (${metrics.headerCount})`);
      if (metrics.footerCount !== 1 || !metrics.footerVisible) pushIssue(critical, viewport, route, `canonical footer missing or hidden (${metrics.footerCount})`);
      if (metrics.duplicateIds.length) pushIssue(critical, viewport, route, `duplicate IDs: ${metrics.duplicateIds.join(", ")}`);
      if (!metrics.skipTargetExists) pushIssue(critical, viewport, route, "skip-link target is missing");
      if (metrics.failedImages.length) pushIssue(critical, viewport, route, `failed local images: ${metrics.failedImages.join(", ")}`);
      if (metrics.h1Overflows) pushIssue(critical, viewport, route, "H1 extends outside the viewport");
      if (viewport.width >= 1181 && metrics.h1Rect?.width < 280) pushIssue(critical, viewport, route, `desktop H1 is squeezed into ${Math.round(metrics.h1Rect.width)}px`);
      if (metrics.cls > 0.25) pushIssue(critical, viewport, route, `excessive CLS ${metrics.cls.toFixed(3)}`);
      else if (metrics.cls > 0.1) pushIssue(warnings, viewport, route, `elevated CLS ${metrics.cls.toFixed(3)}`);
      if (metrics.formWidth && viewport.width >= 900 && metrics.formWidth > 680) {
        pushIssue(critical, viewport, route, `contact form is too wide (${Math.round(metrics.formWidth)}px)`);
      } else if (metrics.formWidth && viewport.width >= 900 && metrics.formWidth > 580) {
        pushIssue(warnings, viewport, route, `contact form exceeds compact premium target (${Math.round(metrics.formWidth)}px)`);
      }
      if (metrics.widestText?.width > 840) {
        pushIssue(warnings, viewport, route, `very wide text line (${Math.round(metrics.widestText.width)}px): ${metrics.widestText.text}`);
      }
      if (consoleErrors.length) pushIssue(critical, viewport, route, `console errors: ${consoleErrors.join(" | ")}`);
      if (runtimeErrors.length) pushIssue(critical, viewport, route, `runtime errors: ${runtimeErrors.join(" | ")}`);
      if (requestFailures.length) pushIssue(warnings, viewport, route, `request failures: ${requestFailures.join(" | ")}`);

      const wrongBooking = metrics.globalBookingLinks.filter((href) => {
        if (!href) return true;
        try {
          const url = new URL(href, page.url());
          return `${url.pathname}${url.hash}` !== metrics.expectedBooking;
        } catch { return true; }
      });
      if (wrongBooking.length) pushIssue(critical, viewport, route, `global booking routes are inconsistent: ${wrongBooking.join(", ")}`);
      if (!metrics.languageHref) pushIssue(critical, viewport, route, "language counterpart link is missing");

      for (const href of metrics.internalLinks) {
        const local = localPathFromURL(href);
        if (!local) continue;
        const cacheKey = local.replace(/#.*$/, "");
        if (!brokenCache.has(cacheKey)) {
          try {
            const linkResponse = await context.request.get(`${baseURL}${cacheKey}`, { timeout: 15000 });
            brokenCache.set(cacheKey, linkResponse.status());
          } catch {
            brokenCache.set(cacheKey, 0);
          }
        }
        const status = brokenCache.get(cacheKey);
        if (status >= 400 || status === 0) pushIssue(critical, viewport, route, `broken internal link ${cacheKey} (${status || "request failed"})`);
      }

      const mobileRange = viewport.width <= 1180;
      const toggle = page.locator("[data-menu-toggle]");
      if (mobileRange) {
        if (!metrics.toggleVisible) {
          pushIssue(critical, viewport, route, "hamburger is not visible in tablet/mobile range");
        } else {
          try {
            await toggle.click();
            await page.waitForTimeout(180);
            const opened = await page.evaluate(() => {
              const toggle = document.querySelector("[data-menu-toggle]");
              const menu = document.querySelector("[data-mobile-nav]");
              const main = document.querySelector("main");
              const focus = document.activeElement;
              return {
                expanded: toggle?.getAttribute("aria-expanded") === "true",
                menuHidden: Boolean(menu?.hidden),
                menuVisible: Boolean(menu && getComputedStyle(menu).display !== "none" && menu.getBoundingClientRect().height > 0),
                bodyOpen: document.body.classList.contains("editorial-menu-open"),
                mainInert: Boolean(main?.hasAttribute("inert")),
                focusInside: Boolean(menu?.contains(focus) || toggle === focus)
              };
            });
            if (!opened.expanded || opened.menuHidden || !opened.menuVisible || !opened.bodyOpen || !opened.mainInert || !opened.focusInside) {
              pushIssue(critical, viewport, route, `mobile menu open-state incomplete: ${JSON.stringify(opened)}`);
            }
            await page.keyboard.press("Escape");
            await page.waitForTimeout(120);
            const closed = await page.evaluate(() => {
              const toggle = document.querySelector("[data-menu-toggle]");
              const menu = document.querySelector("[data-mobile-nav]");
              return {
                expanded: toggle?.getAttribute("aria-expanded"),
                menuHidden: Boolean(menu?.hidden),
                bodyOpen: document.body.classList.contains("editorial-menu-open"),
                focusReturned: document.activeElement === toggle
              };
            });
            if (closed.expanded !== "false" || !closed.menuHidden || closed.bodyOpen || !closed.focusReturned) {
              pushIssue(critical, viewport, route, `mobile menu close-state incomplete: ${JSON.stringify(closed)}`);
            }
          } catch (error) {
            pushIssue(critical, viewport, route, `mobile menu interaction failed: ${error.message}`);
          }
        }
      } else {
        if (metrics.toggleVisible) pushIssue(critical, viewport, route, "hamburger remains visible on desktop");
        if (!metrics.railVisible && !metrics.desktopNavVisible) pushIssue(critical, viewport, route, "no visible global navigation on desktop");
      }

      const sticky = page.locator("[data-mobile-booking-cta]");
      if (viewport.width <= 800 && await sticky.count()) {
        await page.locator(".site-footer").scrollIntoViewIfNeeded();
        await page.waitForTimeout(900);
        const overlap = await page.evaluate(() => {
          const cta = document.querySelector("[data-mobile-booking-cta]");
          const footer = document.querySelector(".site-footer");
          if (!cta || !footer) return 0;
          const style = getComputedStyle(cta);
          if (style.display === "none" || style.visibility === "hidden" || Number(style.opacity) === 0) return 0;
          const a = cta.getBoundingClientRect();
          const b = footer.getBoundingClientRect();
          const width = Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left));
          const height = Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top));
          return width * height;
        });
        if (overlap > 1) pushIssue(critical, viewport, route, `mobile booking CTA overlaps footer (${Math.round(overlap)}px²)`);
      }

      if (screenshotMode && screenshotRoutes.has(route) && (viewport.name === "mobile" || viewport.name === "desktop")) {
        const slug = route === "/" ? "ua-home" : route.replace(/^\//, "").replace(/\/$/, "").replaceAll("/", "--");
        await page.screenshot({
          path: path.join(outputDir, `${viewport.name}--${slug}.png`),
          fullPage: true,
          animations: "disabled"
        });
      }

      pageReports.push({ viewport: viewport.name, route, metrics, consoleErrors, runtimeErrors, requestFailures });
      await page.close();
    }
    await context.close();
  }
} finally {
  await browser.close();
}

const report = {
  generatedAt: new Date().toISOString(),
  baseURL,
  routes: routes.length,
  viewports,
  critical,
  warnings,
  pages: pageReports
};

await fs.writeFile(path.join(outputDir, "report.json"), `${JSON.stringify(report, null, 2)}\n`, "utf8");
await fs.writeFile(path.join(outputDir, "summary.txt"), [
  `Final UX audit: ${routes.length} routes × ${viewports.length} viewports`,
  `Critical issues: ${critical.length}`,
  `Warnings: ${warnings.length}`,
  "",
  ...critical.map((item) => `CRITICAL [${item.viewport}] ${item.route} — ${item.message}`),
  ...warnings.map((item) => `WARNING [${item.viewport}] ${item.route} — ${item.message}`)
].join("\n") + "\n", "utf8");

console.log(await fs.readFile(path.join(outputDir, "summary.txt"), "utf8"));
if (strict && critical.length) process.exit(1);
