import { chromium } from "playwright";
import { mkdir, writeFile } from "node:fs/promises";

const baseUrl = "http://127.0.0.1:8080";
const outputDir = "qa-artifacts/article-coping-support";
const routes = [
  { key: "ua", path: "/notes/when-coping-stops-helping/", alternate: "/ru/notes/when-coping-stops-helping/", privacy: "/privacy/" },
  { key: "ru", path: "/ru/notes/when-coping-stops-helping/", alternate: "/notes/when-coping-stops-helping/", privacy: "/ru/privacy/" }
];
const viewports = [
  { key: "mobile-390", width: 390, height: 844 },
  { key: "landscape-844", width: 844, height: 390 },
  { key: "tablet-1024", width: 1024, height: 768 },
  { key: "desktop-1366", width: 1366, height: 768 }
];

await mkdir(outputDir, { recursive: true });
const browser = await chromium.launch({ headless: true });
const results = [];
let failed = false;

for (const route of routes) {
  for (const viewport of viewports) {
    const context = await browser.newContext({ viewport });
    const page = await context.newPage();
    const consoleErrors = [];
    const pageErrors = [];
    page.on("console", message => { if (message.type() === "error") consoleErrors.push(message.text()); });
    page.on("pageerror", error => pageErrors.push(String(error)));

    const response = await page.goto(`${baseUrl}${route.path}`, { waitUntil: "networkidle" });
    const checks = await page.evaluate(({ alternate, privacy, viewportWidth }) => {
      const ids = [...document.querySelectorAll("[id]")].map(node => node.id);
      const duplicates = [...new Set(ids.filter((id, index) => ids.indexOf(id) !== index))];
      const visual = document.querySelector(".article-hero-visual--observation");
      const panel = document.querySelector(".article-observation-panel");
      const visualRect = visual?.getBoundingClientRect();
      const panelRect = panel?.getBoundingClientRect();
      const footerPrivacy = [...document.querySelectorAll(".site-footer a")].find(link => new URL(link.href).pathname === privacy);
      const languageLink = [...document.querySelectorAll(".language-switch a")].find(link => new URL(link.href).pathname === alternate);
      return {
        h1Count: document.querySelectorAll("h1").length,
        footerCount: document.querySelectorAll(".site-footer").length,
        duplicates,
        overflow: document.documentElement.scrollWidth - viewportWidth,
        heroVisible: Boolean(visualRect && visualRect.width > 280 && visualRect.height > 320),
        panelVisible: Boolean(panelRect && panelRect.width > 260 && panelRect.height > 200),
        panelInsideHero: Boolean(visualRect && panelRect && panelRect.left >= visualRect.left - 1 && panelRect.right <= visualRect.right + 1 && panelRect.top >= visualRect.top - 1 && panelRect.bottom <= visualRect.bottom + 1),
        tocCount: document.querySelectorAll('.article-toc a[href^="#"]').length,
        sections: ["baseline", "dimensions", "observe", "support", "contact-step"].every(id => document.getElementById(id)),
        observationRows: document.querySelectorAll(".article-observation-row").length,
        changeCards: document.querySelectorAll(".article-change-card").length,
        journalLines: document.querySelectorAll(".article-journal-line").length,
        supportLevels: document.querySelectorAll(".article-support-level").length,
        author: Boolean(document.querySelector(".article-author-card")),
        source: Boolean(document.querySelector(".article-source-note")),
        related: document.querySelectorAll(".article-related-card").length,
        cta: Boolean(document.querySelector(".article-cta-band .button")),
        privacy: Boolean(footerPrivacy),
        alternate: Boolean(languageLink),
        articleSchema: [...document.querySelectorAll('script[type="application/ld+json"]')].some(node => node.textContent.includes('"Article"')),
        breadcrumbSchema: [...document.querySelectorAll('script[type="application/ld+json"]')].some(node => node.textContent.includes('"BreadcrumbList"')),
        heroDisplay: visual ? getComputedStyle(visual.closest(".article-hero-grid")).display : "missing"
      };
    }, { alternate: route.alternate, privacy: route.privacy, viewportWidth: viewport.width });

    const linkedPaths = route.key === "ua"
      ? ["/notes/", "/notes/first-consultation/", "/notes/how-to-start-the-conversation/", "/notes/stress-relocation-and-lost-support/", "/privacy/", "/ru/notes/when-coping-stops-helping/"]
      : ["/ru/notes/", "/ru/notes/first-consultation/", "/ru/notes/how-to-start-the-conversation/", "/ru/notes/stress-relocation-and-lost-support/", "/ru/privacy/", "/notes/when-coping-stops-helping/"];
    const linkedStatus = {};
    for (const path of linkedPaths) {
      const linkedResponse = await context.request.get(`${baseUrl}${path}`);
      linkedStatus[path] = linkedResponse.status();
    }

    const problems = [];
    if (!response || response.status() !== 200) problems.push(`HTTP ${response?.status()}`);
    if (checks.h1Count !== 1) problems.push(`H1=${checks.h1Count}`);
    if (checks.footerCount !== 1) problems.push(`footer=${checks.footerCount}`);
    if (checks.duplicates.length) problems.push(`duplicate IDs=${checks.duplicates.join(",")}`);
    if (checks.overflow > 1) problems.push(`overflow=${checks.overflow}`);
    if (!checks.heroVisible) problems.push("observation Hero missing/small");
    if (!checks.panelVisible) problems.push("observation panel missing/small");
    if (!checks.panelInsideHero) problems.push("observation panel outside Hero");
    if (checks.tocCount !== 5) problems.push(`toc=${checks.tocCount}`);
    if (!checks.sections) problems.push("content section missing");
    if (checks.observationRows !== 4) problems.push(`observationRows=${checks.observationRows}`);
    if (checks.changeCards !== 4) problems.push(`changeCards=${checks.changeCards}`);
    if (checks.journalLines !== 4) problems.push(`journalLines=${checks.journalLines}`);
    if (checks.supportLevels !== 4) problems.push(`supportLevels=${checks.supportLevels}`);
    if (!checks.author) problems.push("author card missing");
    if (!checks.source) problems.push("source note missing");
    if (checks.related !== 2) problems.push(`related=${checks.related}`);
    if (!checks.cta) problems.push("CTA missing");
    if (!checks.privacy) problems.push("privacy footer link missing");
    if (!checks.alternate) problems.push("language counterpart missing");
    if (!checks.articleSchema || !checks.breadcrumbSchema) problems.push("structured data missing");
    if (checks.heroDisplay !== "grid") problems.push(`hero grid display=${checks.heroDisplay}`);
    for (const [path, status] of Object.entries(linkedStatus)) {
      if (status !== 200) problems.push(`${path} HTTP ${status}`);
    }
    if (consoleErrors.length) problems.push(`console=${consoleErrors.join(" | ")}`);
    if (pageErrors.length) problems.push(`pageerror=${pageErrors.join(" | ")}`);

    await page.screenshot({ path: `${outputDir}/${route.key}-${viewport.key}.png`, fullPage: true });
    results.push({ route: route.path, viewport, checks, linkedStatus, consoleErrors, pageErrors, problems });
    if (problems.length) failed = true;
    await context.close();
  }
}

await browser.close();
await writeFile(`${outputDir}/report.json`, JSON.stringify(results, null, 2));
for (const result of results) {
  console.log(`${result.route} ${result.viewport.width}x${result.viewport.height}: ${result.problems.length ? `FAIL — ${result.problems.join("; ")}` : "OK"}`);
}
if (failed) process.exit(1);
