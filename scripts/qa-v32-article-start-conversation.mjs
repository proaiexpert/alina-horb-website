import { chromium } from "playwright";
import { mkdir, writeFile } from "node:fs/promises";

const baseUrl = "http://127.0.0.1:8080";
const outputDir = "qa-artifacts/article-start-conversation";
const routes = [
  { key: "ua", path: "/notes/how-to-start-the-conversation/", alternate: "/ru/notes/how-to-start-the-conversation/", privacy: "/privacy/" },
  { key: "ru", path: "/ru/notes/how-to-start-the-conversation/", alternate: "/notes/how-to-start-the-conversation/", privacy: "/ru/privacy/" }
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
      const visual = document.querySelector(".article-hero-visual--conversation");
      const note = document.querySelector(".article-conversation-note");
      const visualRect = visual?.getBoundingClientRect();
      const noteRect = note?.getBoundingClientRect();
      const footerPrivacy = [...document.querySelectorAll(".site-footer a")].find(link => new URL(link.href).pathname === privacy);
      const languageLink = [...document.querySelectorAll(".language-switch a")].find(link => new URL(link.href).pathname === alternate);
      return {
        h1Count: document.querySelectorAll("h1").length,
        footerCount: document.querySelectorAll(".site-footer").length,
        duplicates,
        overflow: document.documentElement.scrollWidth - viewportWidth,
        heroVisible: Boolean(visualRect && visualRect.width > 280 && visualRect.height > 280),
        noteVisible: Boolean(noteRect && noteRect.width > 220 && noteRect.height > 80 && note.textContent.trim().length > 40),
        noteInsideHero: Boolean(visualRect && noteRect && noteRect.left >= visualRect.left - 1 && noteRect.right <= visualRect.right + 1 && noteRect.bottom <= visualRect.bottom + 1),
        tocCount: document.querySelectorAll('.article-toc a[href^="#"]').length,
        sections: ["request", "begin", "phrases", "limits", "send"].every(id => document.getElementById(id)),
        openingCards: document.querySelectorAll(".article-opening-card").length,
        softSteps: document.querySelectorAll(".article-soft-step").length,
        messageExample: Boolean(document.querySelector(".article-message-example")),
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
      ? ["/notes/", "/notes/first-consultation/", "/notes/when-coping-stops-helping/", "/privacy/", "/ru/notes/how-to-start-the-conversation/"]
      : ["/ru/notes/", "/ru/notes/first-consultation/", "/ru/notes/when-coping-stops-helping/", "/ru/privacy/", "/notes/how-to-start-the-conversation/"];
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
    if (!checks.heroVisible) problems.push("conversation Hero missing/small");
    if (!checks.noteVisible) problems.push("Hero phrase note missing/small");
    if (!checks.noteInsideHero) problems.push("Hero phrase note outside visual");
    if (checks.tocCount !== 5) problems.push(`toc=${checks.tocCount}`);
    if (!checks.sections) problems.push("content section missing");
    if (checks.openingCards !== 4) problems.push(`openingCards=${checks.openingCards}`);
    if (checks.softSteps !== 3) problems.push(`softSteps=${checks.softSteps}`);
    if (!checks.messageExample) problems.push("message example missing");
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
