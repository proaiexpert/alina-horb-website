#!/usr/bin/env node
import { chromium } from "playwright";
import AxeBuilder from "@axe-core/playwright";
import fs from "node:fs/promises";
import path from "node:path";

const baseURL = process.env.AUDIT_BASE_URL || "http://127.0.0.1:4173";
const strict = process.env.AUDIT_STRICT === "1";
const outputDir = process.env.AUDIT_OUTPUT_DIR || "qa/accessibility";

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
  "/notes/constant-arguments-with-partner/",
  "/ru/notes/constant-arguments-with-partner/",
  "/notes/fear-of-another-panic-attack/",
  "/ru/notes/fear-of-another-panic-attack/",
  "/privacy/",
  "/ru/privacy/",
  "/404.html"
];

const viewports = [
  { name: "mobile", width: 390, height: 844 },
  { name: "landscape", width: 844, height: 390 },
  { name: "desktop", width: 1440, height: 1000 }
];

const critical = [];
const warnings = [];
const seen = new Set();
const pageReports = [];
const responsiveChecks = [];
  const mobileTocChecks = [];

const pushViolation = (bucket, viewport, route, violation, node) => {
  const targets = (node.target || []).map((target) => Array.isArray(target) ? target.join(" ") : String(target));
  const key = [viewport.name, route, violation.id, ...targets].join("|");
  if (seen.has(key)) return;
  seen.add(key);
  bucket.push({
    viewport: viewport.name,
    route,
    rule: violation.id,
    impact: violation.impact || "unknown",
    help: violation.help,
    helpUrl: violation.helpUrl,
    targets,
    html: node.html
  });
};

await fs.mkdir(outputDir, { recursive: true });
const browser = await chromium.launch({ headless: true });

try {
  for (const viewport of viewports) {
    const context = await browser.newContext({
      viewport: { width: viewport.width, height: viewport.height },
      deviceScaleFactor: 1,
      reducedMotion: "reduce"
    });

    for (const route of routes) {
      const page = await context.newPage();
      try {
        const response = await page.goto(`${baseURL}${route}`, {
          waitUntil: "domcontentloaded",
          timeout: 45000
        });
        if (!response || response.status() >= 400) {
          critical.push({
            viewport: viewport.name,
            route,
            rule: "navigation",
            impact: "critical",
            help: `Route returned ${response?.status() ?? "no response"}`,
            helpUrl: null,
            targets: [],
            html: ""
          });
          await page.close();
          continue;
        }

        await page.waitForTimeout(400);
        const results = await new AxeBuilder({ page })
          .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"])
          .analyze();

        for (const violation of results.violations) {
          for (const node of violation.nodes) {
            const bucket = ["critical", "serious"].includes(violation.impact) ? critical : warnings;
            pushViolation(bucket, viewport, route, violation, node);
          }
        }

        // Control images: published Article #1, captured at identical viewports.
        if (route.includes("/constant-arguments-with-partner/")) {
          const controlShot = `article01-${route.startsWith("/ru/") ? "ru" : "ua"}-${viewport.name}.png`;
          await page.screenshot({
            path: path.join(outputDir, controlShot),
            fullPage: true,
            animations: "disabled"
          });
        }
        if (route.includes("/fear-of-another-panic-attack/")) {
          const responsive = await page.evaluate(() => ({
            scrollWidth: document.documentElement.scrollWidth,
            clientWidth: document.documentElement.clientWidth,
            menuPresent: Boolean(document.querySelector("[data-menu-toggle]"))
          }));
          const overflow = Math.max(0, responsive.scrollWidth - responsive.clientWidth);
          const isCompact = viewport.width <= 900;
          const disclosure = page.locator(".panic-toc-mobile");
          const tocCheck = {
            route, viewport: viewport.name,
            visible: await disclosure.isVisible(),
            initiallyClosed: !(await disclosure.evaluate((el) => el.open)),
            expandedByKeyboard: false,
            linkCount: await disclosure.locator("ol > li > a").count(),
            heroImageLoaded: await page.locator(".article-hero-visual img").evaluate(
              (img) => img.complete && img.naturalWidth > 0
            ),
            menuOpensAndCloses: null
          };
          if (isCompact && tocCheck.visible && tocCheck.initiallyClosed) {
            await disclosure.locator("summary").focus();
            await page.keyboard.press("Enter");
            tocCheck.expandedByKeyboard = await disclosure.evaluate((el) => el.open);
            await page.keyboard.press("Enter");
          }
          const toggle = page.locator("[data-menu-toggle]");
          if (isCompact && await toggle.isVisible()) {
            await toggle.click();
            const opened = (await toggle.getAttribute("aria-expanded")) === "true";
            await toggle.click();
            const closed = (await toggle.getAttribute("aria-expanded")) === "false";
            tocCheck.menuOpensAndCloses = opened && closed;
          }
          mobileTocChecks.push(tocCheck);
          const tocFailed = tocCheck.linkCount !== 10 ||
            !tocCheck.heroImageLoaded ||
            (isCompact && (!tocCheck.visible || !tocCheck.initiallyClosed ||
              !tocCheck.expandedByKeyboard || tocCheck.menuOpensAndCloses !== true)) ||
            (!isCompact && tocCheck.visible);
          if (tocFailed) {
            critical.push({
              viewport: viewport.name, route, rule: "article02-interactions",
              impact: "serious",
              help: JSON.stringify(tocCheck),
              helpUrl: null, targets: [".article-toc"], html: ""
            });
          }
          const screenshotName = `article02-${route.startsWith("/ru/") ? "ru" : "ua"}-${viewport.name}.png`;
          await page.screenshot({
            path: path.join(outputDir, screenshotName),
            fullPage: true,
            animations: "disabled"
          });
          responsiveChecks.push({
            route,
            viewport: viewport.name,
            overflowPixels: overflow,
            menuPresent: responsive.menuPresent,
            screenshot: screenshotName
          });
          if (overflow > 2 || !responsive.menuPresent) {
            critical.push({
              viewport: viewport.name,
              route,
              rule: overflow > 2 ? "horizontal-overflow" : "missing-mobile-menu",
              impact: "serious",
              help: overflow > 2 ? `Horizontal document overflow: ${overflow}px` : "Missing responsive menu toggle",
              helpUrl: null,
              targets: ["html"],
              html: ""
            });
          }
        }
        pageReports.push({
          viewport: viewport.name,
          route,
          violations: results.violations.map((item) => ({
            id: item.id,
            impact: item.impact,
            help: item.help,
            nodes: item.nodes.length
          }))
        });
      } catch (error) {
        critical.push({
          viewport: viewport.name,
          route,
          rule: "audit-runtime",
          impact: "critical",
          help: error.message,
          helpUrl: null,
          targets: [],
          html: ""
        });
      } finally {
        await page.close();
      }
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
  responsiveChecks,
  mobileTocChecks,
  pages: pageReports
};

await fs.writeFile(path.join(outputDir, "report.json"), `${JSON.stringify(report, null, 2)}\n`, "utf8");

const format = (item) =>
  `${item.impact.toUpperCase()} [${item.viewport}] ${item.route} — ${item.rule}: ${item.help}${item.targets.length ? ` — ${item.targets.join(", ")}` : ""}`;

const summary = [
  `Accessibility audit: ${routes.length} routes × ${viewports.length} viewports`,
  `Critical/serious findings: ${critical.length}`,
  `Moderate/minor findings: ${warnings.length}`,
  "",
  "Critical/serious:",
  ...(critical.length ? critical.map(format) : ["- none"]),
  "",
  "Moderate/minor:",
  ...(warnings.length ? warnings.map(format) : ["- none"])
].join("\n") + "\n";

await fs.writeFile(path.join(outputDir, "summary.txt"), summary, "utf8");
console.log(summary);

if (strict && (critical.length || warnings.length)) process.exit(1);
