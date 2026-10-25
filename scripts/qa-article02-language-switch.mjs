#!/usr/bin/env node
// TASK 041 — Article #2 independent header/footer language switch regression.
// Actual Chromium clicks; both viewports; never silently accept Article #1.
import { chromium } from "playwright";
import fs from "node:fs/promises";
import path from "node:path";

const base = (process.env.AUDIT_BASE_URL || "http://127.0.0.1:4173").replace(/\/$/, "");
const output = process.env.AUDIT_LANGUAGE_OUTPUT_DIR || "qa/article02-language-switch";
const cases = [
  {
    source: "/notes/fear-of-another-panic-attack/",
    destination: "/ru/notes/fear-of-another-panic-attack/",
    expectedHref: "../../ru/notes/fear-of-another-panic-attack/",
    locale: "ru",
    targetH1: "Страх повторения панической атаки"
  },
  {
    source: "/ru/notes/fear-of-another-panic-attack/",
    destination: "/notes/fear-of-another-panic-attack/",
    expectedHref: "../../../notes/fear-of-another-panic-attack/",
    locale: "uk",
    targetH1: "Страх повторення панічної атаки"
  }
];
const viewports = [
  { name: "mobile", width: 390, height: 844 },
  { name: "desktop", width: 1440, height: 1000 }
];
const placements = [
  { name: "header", selector: ".site-header--canonical .header-tools .language-switch" },
  { name: "footer", selector: ".site-footer[data-site-footer='canonical'] .footer-utility .language-switch" }
];
const failures = [];
const results = [];

await fs.mkdir(output, { recursive: true });
const browser = await chromium.launch({ headless: true });
try {
  for (const viewport of viewports) {
    const context = await browser.newContext({ viewport: { width: viewport.width, height: viewport.height }, reducedMotion: "reduce" });
    for (const pair of cases) {
      for (const location of placements) {
        const page = await context.newPage();
        const result = { viewport: viewport.name, source: pair.source, destination: pair.destination, placement: location.name, hrefValid: false, clickNavigated: false, targetArticle2: false, noArticle1: false, passed: false };
        try {
          const response = await page.goto(base + pair.source, { waitUntil: "domcontentloaded", timeout: 30000 });
          if (!response || response.status() !== 200) throw new Error("Source not HTTP 200");
          const link = page.locator(location.selector + ' a[hreflang="' + pair.locale + '"]');
          if (await link.count() !== 1) throw new Error("Expected exactly one " + location.name + " counterpart link");
          const rawHref = await link.getAttribute("href");
          result.actualHref = rawHref;
          result.hrefValid = rawHref === pair.expectedHref;
          if (!result.hrefValid) throw new Error("Wrong " + location.name + " relative href: " + rawHref);
          const intended = new URL(rawHref, page.url()).pathname;
          if (intended !== pair.destination) throw new Error("Resolved relative route mismatch: " + intended);
          if (location.name === "footer") await link.scrollIntoViewIfNeeded({ timeout: 10000 });
          await link.click({ timeout: 10000 });
          await page.waitForURL(url => url.pathname === pair.destination, { timeout: 12000 });
          const destResponse = await page.waitForLoadState("domcontentloaded");
          result.clickNavigated = new URL(page.url()).pathname === pair.destination;
          const header = await page.locator("main h1").first().textContent({ timeout: 10000 });
          result.targetArticle2 = (await page.locator('body[data-note="panic"]').count()) === 1 && header.includes(pair.targetH1);
          result.noArticle1 = !page.url().includes("constant-arguments-with-partner") && (await page.locator('body[data-note="conflict"]').count()) === 0;
          if (!result.targetArticle2 || !result.noArticle1) throw new Error("Destination is not Article #2: " + page.url());
          result.passed = true;
        } catch (error) {
          result.error = String(error.message || error);
          failures.push(result);
        } finally {
          results.push(result);
          await page.close();
        }
      }
    }
    await context.close();
  }
} finally {
  await browser.close();
}
const report = { suite: "TASK 041 Article #2 UA/RU header and footer navigation", baseURL: base, cases: results.length, failures, results };
await fs.writeFile(path.join(output, "task041-links.json"), JSON.stringify(report, null, 2) + "\n");
console.log("TASK 041 Chromium navigation: " + (results.length - failures.length) + "/" + results.length + " PASS; failures=" + failures.length);
if (failures.length) {
  for (const f of failures) console.error(JSON.stringify(f));
  process.exitCode = 1;
}
