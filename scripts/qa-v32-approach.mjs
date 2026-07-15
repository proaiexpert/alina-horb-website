import { chromium } from "playwright";
import { mkdir, writeFile } from "node:fs/promises";

const baseUrl = "http://127.0.0.1:8080";
const outputDir = "qa-artifacts/approach";
const pages = [["ua", "/"], ["ru", "/ru/"]];
const viewports = [
  ["mobile-390", { width: 390, height: 844 }],
  ["landscape-844", { width: 844, height: 390 }],
  ["desktop-1366", { width: 1366, height: 768 }]
];

await mkdir(outputDir, { recursive: true });
const browser = await chromium.launch({ headless: true });
const report = [];
let failed = false;

for (const [viewportName, viewport] of viewports) {
  const context = await browser.newContext({ viewport, deviceScaleFactor: 1 });
  for (const [language, route] of pages) {
    const page = await context.newPage();
    const consoleErrors = [];
    page.on("console", message => { if (message.type() === "error") consoleErrors.push(message.text()); });
    page.on("pageerror", error => consoleErrors.push(error.message));

    const response = await page.goto(`${baseUrl}${route}`, { waitUntil: "networkidle" });
    await page.waitForTimeout(450);
    const about = page.locator("#about");
    await about.scrollIntoViewIfNeeded();
    await page.waitForTimeout(150);

    const checks = await page.evaluate(() => {
      const ids = [...document.querySelectorAll("[id]")].map(element => element.id);
      const duplicateIds = [...new Set(ids.filter((id, index) => ids.indexOf(id) !== index))];
      const about = document.querySelector("#about");
      const text = about?.innerText ?? "";
      const bodyText = document.body.innerText.toLowerCase();
      const isRu = document.documentElement.lang.startsWith("ru");
      const expected = isRu
        ? ["Подход в работе", "Клиент-центрированный подход", "Гештальт-инструменты и метафорические карты", "Вера, ценности и поиск смысла", "Алина Горб · о внутренней опоре"]
        : ["Підхід у роботі", "Клієнт-центрований підхід", "Гештальт-інструменти та метафоричні картки", "Віра, цінності та пошук сенсу", "Аліна Горб · про внутрішню опору"];
      const missing = expected.filter(item => !text.includes(item));
      const aboutRect = about?.getBoundingClientRect();
      const aboutOverflow = Boolean(aboutRect && (aboutRect.left < -1 || aboutRect.right > window.innerWidth + 1 || about.scrollWidth > about.clientWidth + 1));
      return {
        h1Count: document.querySelectorAll("h1").length,
        duplicateIds,
        methodCount: document.querySelectorAll(".approach-method").length,
        topicCount: document.querySelectorAll("#topics .topic-row").length,
        principleCount: document.querySelectorAll(".principles-list > li").length,
        missing,
        pageOverflow: document.documentElement.scrollWidth > window.innerWidth + 1,
        aboutOverflow,
        innerWidth: window.innerWidth,
        innerHeight: window.innerHeight,
        noindex: Boolean(document.querySelector('meta[name="robots"][content="noindex, nofollow"]')),
        supervisionClaim: bodyText.includes("супервізія") || bodyText.includes("супервизия")
      };
    });

    const screenshot = `${outputDir}/${language}-${viewportName}.png`;
    await about.screenshot({ path: screenshot });
    const correctViewport = checks.innerWidth === viewport.width && checks.innerHeight === viewport.height;
    const ok = Boolean(response?.ok()) && correctViewport && checks.h1Count === 1 && checks.duplicateIds.length === 0 && checks.methodCount === 3 && checks.topicCount === 10 && checks.principleCount === 4 && checks.missing.length === 0 && !checks.pageOverflow && !checks.aboutOverflow && checks.noindex && !checks.supervisionClaim && consoleErrors.length === 0;
    if (!ok) failed = true;
    report.push({ language, route, viewportName, expectedViewport: viewport, status: response?.status(), correctViewport, ok, consoleErrors, ...checks, screenshot });
    await page.close();
  }
  await context.close();
}

await browser.close();
await writeFile(`${outputDir}/report.json`, JSON.stringify(report, null, 2));
console.log(JSON.stringify(report, null, 2));
if (failed) process.exit(1);
