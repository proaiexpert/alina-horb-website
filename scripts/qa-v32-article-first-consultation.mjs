import { chromium } from "playwright";
import { mkdir, writeFile } from "node:fs/promises";

const baseUrl = "http://127.0.0.1:8080";
const outputDir = "qa-artifacts/article-first-consultation";
const routes = [
  { key: "ua", path: "/notes/first-consultation/", alternate: "/ru/notes/first-consultation/", privacy: "/privacy/" },
  { key: "ru", path: "/ru/notes/first-consultation/", alternate: "/notes/first-consultation/", privacy: "/ru/privacy/" }
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
    page.on("console", message => {
      if (message.type() === "error") consoleErrors.push(message.text());
    });
    page.on("pageerror", error => pageErrors.push(String(error)));

    const response = await page.goto(`${baseUrl}${route.path}`, { waitUntil: "networkidle" });
    const checks = await page.evaluate(({ alternate, privacy, viewportWidth }) => {
      const ids = [...document.querySelectorAll("[id]")].map(node => node.id);
      const duplicates = [...new Set(ids.filter((id, index) => ids.indexOf(id) !== index))];
      const heroVisual = document.querySelector(".article-hero-visual");
      const answer = document.querySelector(".article-answer-card");
      const tocLinks = [...document.querySelectorAll('.article-toc a[href^="#"]')];
      const footerPrivacy = [...document.querySelectorAll(".site-footer a")].find(link => new URL(link.href).pathname === privacy);
      const languageLink = [...document.querySelectorAll(".language-switch a")].find(link => new URL(link.href).pathname === alternate);
      const related = [...document.querySelectorAll(".article-related-card")];
      const contentSections = ["purpose", "start", "questions", "ending", "prepare"].map(id => document.getElementById(id));
      const heroRect = heroVisual?.getBoundingClientRect();
      const answerRect = answer?.getBoundingClientRect();
      return {
        h1Count: document.querySelectorAll("h1").length,
        footerCount: document.querySelectorAll(".site-footer").length,
        duplicates,
        overflow: document.documentElement.scrollWidth - viewportWidth,
        heroVisible: Boolean(heroVisual && heroRect && heroRect.width > 280 && heroRect.height > 280),
        answerVisible: Boolean(answer && answerRect && answerRect.width > 280 && answer.textContent.trim().length > 200),
        tocCount: tocLinks.length,
        contentSections: contentSections.every(Boolean),
        author: Boolean(document.querySelector(".article-author-card")),
        source: Boolean(document.querySelector(".article-source-note")),
        relatedCount: related.length,
        cta: Boolean(document.querySelector(".article-cta-band .button")),
        privacy: Boolean(footerPrivacy),
        alternate: Boolean(languageLink),
        articleSchema: [...document.querySelectorAll('script[type="application/ld+json"]')].some(node => node.textContent.includes('"Article"')),
        breadcrumbSchema: [...document.querySelectorAll('script[type="application/ld+json"]')].some(node => node.textContent.includes('"BreadcrumbList"')),
        cssDisplay: heroVisual ? getComputedStyle(heroVisual.closest(".article-hero-grid")).display : "missing"
      };
    }, { alternate: route.alternate, privacy: route.privacy, viewportWidth: viewport.width });

    const linkedPaths = route.key === "ua"
      ? ["/notes/", "/notes/how-to-start-the-conversation/", "/notes/when-coping-stops-helping/", "/privacy/", "/ru/notes/first-consultation/"]
      : ["/ru/notes/", "/ru/notes/how-to-start-the-conversation/", "/ru/notes/when-coping-stops-helping/", "/ru/privacy/", "/notes/first-consultation/"];
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
    if (!checks.heroVisible) problems.push("hero visual missing/small");
    if (!checks.answerVisible) problems.push("direct answer missing/small");
    if (checks.tocCount !== 5) problems.push(`toc=${checks.tocCount}`);
    if (!checks.contentSections) problems.push("content section missing");
    if (!checks.author) problems.push("author card missing");
    if (!checks.source) problems.push("source note missing");
    if (checks.relatedCount !== 2) problems.push(`related=${checks.relatedCount}`);
    if (!checks.cta) problems.push("CTA missing");
    if (!checks.privacy) problems.push("privacy footer link missing");
    if (!checks.alternate) problems.push("language counterpart missing");
    if (!checks.articleSchema || !checks.breadcrumbSchema) problems.push("structured data missing");
    if (checks.cssDisplay !== "grid") problems.push(`hero grid display=${checks.cssDisplay}`);
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
