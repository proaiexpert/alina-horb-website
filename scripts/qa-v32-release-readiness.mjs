import { chromium } from "playwright";
import { mkdir, writeFile } from "node:fs/promises";

const baseUrl = "http://127.0.0.1:8080";
const outputDir = "qa-artifacts/release-readiness-v32";

const routes = [
  { key: "ua-home", path: "/", type: "home", screenshot: true },
  { key: "ru-home", path: "/ru/", type: "home", screenshot: true },
  { key: "ua-notes", path: "/notes/", type: "hub", screenshot: true },
  { key: "ru-notes", path: "/ru/notes/", type: "hub", screenshot: true },
  { key: "ua-first", path: "/notes/first-consultation/", type: "article", screenshot: true },
  { key: "ru-first", path: "/ru/notes/first-consultation/", type: "article", screenshot: true },
  { key: "ua-conversation", path: "/notes/how-to-start-the-conversation/", type: "article" },
  { key: "ru-conversation", path: "/ru/notes/how-to-start-the-conversation/", type: "article" },
  { key: "ua-coping", path: "/notes/when-coping-stops-helping/", type: "article" },
  { key: "ru-coping", path: "/ru/notes/when-coping-stops-helping/", type: "article" },
  { key: "ua-relocation", path: "/notes/stress-relocation-and-lost-support/", type: "article" },
  { key: "ru-relocation", path: "/ru/notes/stress-relocation-and-lost-support/", type: "article" },
  { key: "ua-privacy", path: "/privacy/", type: "privacy", screenshot: true },
  { key: "ru-privacy", path: "/ru/privacy/", type: "privacy", screenshot: true },
];

const viewports = [
  { key: "mobile-390", width: 390, height: 844, screenshot: true },
  { key: "tablet-768", width: 768, height: 1024 },
  { key: "landscape-844", width: 844, height: 390, screenshot: true },
  { key: "tablet-1024", width: 1024, height: 768 },
  { key: "desktop-1280", width: 1280, height: 800 },
  { key: "desktop-1366", width: 1366, height: 768, screenshot: true },
  { key: "desktop-1440", width: 1440, height: 900 },
];

await mkdir(outputDir, { recursive: true });
const browser = await chromium.launch();
const results = [];
let failed = false;

for (const route of routes) {
  for (const viewport of viewports) {
    const page = await browser.newPage({ viewport, reducedMotion: "reduce" });
    const consoleErrors = [];
    const assetErrors = [];

    page.on("console", message => {
      if (message.type() === "error") consoleErrors.push(message.text());
    });
    page.on("pageerror", error => consoleErrors.push(String(error)));
    page.on("requestfailed", request => {
      if (request.url().startsWith(baseUrl)) assetErrors.push(`FAILED ${request.url()}`);
    });
    page.on("response", response => {
      if (response.url().startsWith(baseUrl) && response.status() >= 400) {
        assetErrors.push(`${response.status()} ${response.url()}`);
      }
    });

    const response = await page.goto(baseUrl + route.path, { waitUntil: "networkidle" });
    await page.addStyleTag({ content: `
      *, *::before, *::after { animation-duration: .01ms !important; transition-duration: .01ms !important; }
      [data-reveal] { opacity: 1 !important; transform: none !important; }
      .hero-portrait { clip-path: none !important; }
    ` });

    await page.evaluate(async () => {
      const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
      const step = Math.max(420, Math.round(window.innerHeight * 0.75));
      for (let y = 0; y < document.documentElement.scrollHeight; y += step) {
        window.scrollTo(0, y);
        await delay(35);
      }
      window.scrollTo(0, document.documentElement.scrollHeight);
      await delay(180);
    });

    const checks = {};
    checks.http200 = response?.status() === 200;
    checks.oneH1 = (await page.locator("h1").count()) === 1;
    checks.noDuplicateIds = await page.evaluate(() => {
      const ids = [...document.querySelectorAll("[id]")].map(element => element.id);
      return new Set(ids).size === ids.length;
    });
    checks.noOverflow = await page.evaluate(() =>
      document.documentElement.scrollWidth <= window.innerWidth + 1 &&
      document.body.scrollWidth <= window.innerWidth + 1
    );
    checks.noConsoleErrors = consoleErrors.length === 0;
    checks.noAssetErrors = assetErrors.length === 0;
    checks.imagesLoaded = await page.evaluate(() => [...document.images].every(image => image.complete && image.naturalWidth > 0));
    checks.stylesheetsLoaded = await page.evaluate(() => {
      const localLinks = [...document.querySelectorAll('link[rel="stylesheet"]')]
        .filter(link => new URL(link.href, location.href).origin === location.origin);
      const loaded = new Set([...document.styleSheets].map(sheet => sheet.href).filter(Boolean));
      return localLinks.every(link => loaded.has(link.href));
    });
    checks.headerInsideViewport = await page.locator(".site-header").evaluate(element => {
      const rect = element.getBoundingClientRect();
      return rect.left >= -1 && rect.right <= window.innerWidth + 1;
    });
    checks.footerInsideViewport = await page.locator(".site-footer").evaluate(element => {
      const rect = element.getBoundingClientRect();
      return rect.left >= -1 && rect.right <= window.innerWidth + 1;
    });
    checks.h1InsideViewport = await page.locator("h1").evaluate(element => {
      const rect = element.getBoundingClientRect();
      return rect.width <= window.innerWidth + 1 && rect.left >= -1 && rect.right <= window.innerWidth + 1;
    });
    checks.footerNotCoveredByMobileCta = await page.evaluate(() => {
      const footer = document.querySelector(".site-footer");
      const cta = document.querySelector(".mobile-booking-cta");
      if (!footer || !cta) return true;
      const style = getComputedStyle(cta);
      if (style.display === "none" || style.visibility === "hidden" || Number(style.opacity) < 0.1) return true;
      const a = footer.getBoundingClientRect();
      const b = cta.getBoundingClientRect();
      return a.right <= b.left || a.left >= b.right || a.bottom <= b.top || a.top >= b.bottom;
    });

    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForTimeout(80);
    const skipLink = page.locator(".skip-link");
    await skipLink.focus();
    checks.keyboardFocusVisible = await skipLink.evaluate(element => {
      const style = getComputedStyle(element);
      return document.activeElement === element && element.matches(":focus") &&
        style.display !== "none" && style.visibility !== "hidden";
    });
    await page.keyboard.press("Tab");
    checks.keyboardTabProgresses = await page.evaluate(() => {
      const active = document.activeElement;
      return Boolean(active && !active.classList.contains("skip-link") &&
        active.matches('a[href], button, input, select, textarea, summary, [tabindex]:not([tabindex="-1"])'));
    });
    await page.evaluate(() => document.activeElement?.blur());

    if (route.type === "home") {
      checks.homeStylesExplicit = await page.evaluate(() => [
        "site.v3-1-stability.css",
        "site.footer.v3-2.css",
        "site.privacy.v3-2.css",
        "site.intake.v3-2.css",
        "site.notes-hub.v3-2.css",
      ].every(name => [...document.querySelectorAll('link[rel="stylesheet"]')].some(link => link.href.includes(name))));
      checks.formPresent = (await page.locator("[data-contact-form]").count()) === 1;
    }

    const passed = Object.values(checks).every(Boolean);
    if (!passed) failed = true;

    let screenshot = null;
    if (route.screenshot && viewport.screenshot) {
      screenshot = `${outputDir}/${route.key}-${viewport.key}.png`;
      await page.screenshot({ path: screenshot, fullPage: true });
    }

    results.push({
      route: route.path,
      type: route.type,
      viewport,
      checks,
      consoleErrors,
      assetErrors: [...new Set(assetErrors)],
      passed,
      screenshot,
    });
    await page.close();
  }
}

await browser.close();

const summary = {
  total: results.length,
  passed: results.filter(result => result.passed).length,
  failed: results.filter(result => !result.passed).length,
};
await writeFile(`${outputDir}/results.json`, JSON.stringify({ summary, results }, null, 2));

for (const result of results) {
  console.log(`${result.passed ? "PASS" : "FAIL"} ${result.route} ${result.viewport.key}`, result.checks);
  if (result.consoleErrors.length) console.log("console", result.consoleErrors);
  if (result.assetErrors.length) console.log("assets", [...new Set(result.assetErrors)]);
}
console.log(summary);

if (failed) process.exit(1);
