import { chromium } from "playwright";
import { mkdir, writeFile } from "node:fs/promises";

const baseUrl = "http://127.0.0.1:8080";
const outputDir = "qa-artifacts/notes-hub-v32";

const routes = [
  { key: "ua-home", path: "/", kind: "home" },
  { key: "ru-home", path: "/ru/", kind: "home" },
  { key: "ua-hub", path: "/notes/", kind: "hub" },
  { key: "ru-hub", path: "/ru/notes/", kind: "hub" },
];

const viewports = [
  { key: "mobile-390", width: 390, height: 844 },
  { key: "landscape-844", width: 844, height: 390 },
  { key: "tablet-1024", width: 1024, height: 768 },
  { key: "desktop-1366", width: 1366, height: 768 },
];

const articleSlugs = [
  "first-consultation/",
  "how-to-start-the-conversation/",
  "when-coping-stops-helping/",
  "stress-relocation-and-lost-support/",
];

await mkdir(outputDir, { recursive: true });
const browser = await chromium.launch();
const results = [];
let failed = false;

for (const route of routes) {
  for (const viewport of viewports) {
    const page = await browser.newPage({ viewport });
    const consoleErrors = [];
    page.on("console", message => {
      if (message.type() === "error") consoleErrors.push(message.text());
    });
    page.on("pageerror", error => consoleErrors.push(String(error)));

    const response = await page.goto(baseUrl + route.path, { waitUntil: "networkidle" });
    const checks = {};
    checks.http200 = response?.status() === 200;
    checks.oneH1 = (await page.locator("h1").count()) === 1;
    checks.noOverflow = await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1);
    checks.stylesheetLoaded = await page.evaluate(() => [...document.styleSheets].some(sheet => String(sheet.href || "").includes("site.notes-hub.v3-2.css")));
    checks.noConsoleErrors = consoleErrors.length === 0;
    checks.imagesLoaded = await page.evaluate(() => [...document.images].every(image => image.complete && image.naturalWidth > 0));

    if (route.kind === "home") {
      checks.featuredCount = (await page.locator(".home-note-feature").count()) === 1;
      checks.supportingCount = (await page.locator(".home-note-entry").count()) === 3;
      checks.distinctVisuals = await page.evaluate(() => [
        ".note-identity--conversation",
        ".note-identity--observation",
        ".note-identity--transition",
      ].every(selector => document.querySelectorAll(`#notes ${selector}`).length === 1));
      checks.sectionInsideViewport = await page.locator("#notes").evaluate(element => {
        const rect = element.getBoundingClientRect();
        return rect.width <= window.innerWidth + 1 && rect.left >= -1 && rect.right <= window.innerWidth + 1;
      });
    } else {
      checks.featuredCount = (await page.locator(".notes-hub-feature").count()) === 1;
      checks.supportingCount = (await page.locator(".notes-hub-card").count()) === 3;
      checks.distinctVisuals = await page.evaluate(() => [
        ".note-identity--conversation",
        ".note-identity--observation",
        ".note-identity--transition",
      ].every(selector => document.querySelectorAll(selector).length === 1));
      checks.heroInsideViewport = await page.locator(".notes-hub-hero-grid").evaluate(element => {
        const rect = element.getBoundingClientRect();
        return rect.width <= window.innerWidth + 1 && rect.left >= -1 && rect.right <= window.innerWidth + 1;
      });
    }

    checks.articleLinks = true;
    for (const slug of articleSlugs) {
      const locator = page.locator(`a[href$="${slug}"]`).first();
      if ((await locator.count()) !== 1) {
        checks.articleLinks = false;
        break;
      }
      const href = await locator.getAttribute("href");
      const target = new URL(href, baseUrl + route.path).href;
      const targetResponse = await page.request.get(target);
      if (targetResponse.status() !== 200) {
        checks.articleLinks = false;
        break;
      }
    }

    const screenshot = `${outputDir}/${route.key}-${viewport.key}.png`;
    await page.screenshot({ path: screenshot, fullPage: true });

    const passed = Object.values(checks).every(Boolean);
    if (!passed) failed = true;
    results.push({ route: route.path, viewport, checks, consoleErrors, passed, screenshot });
    await page.close();
  }
}

await browser.close();
await writeFile(`${outputDir}/results.json`, JSON.stringify(results, null, 2));

for (const result of results) {
  console.log(`${result.passed ? "PASS" : "FAIL"} ${result.route} ${result.viewport.key}`, result.checks);
  if (result.consoleErrors.length) console.log(result.consoleErrors);
}

if (failed) process.exit(1);
