import { chromium } from "playwright";
import { mkdir, writeFile } from "node:fs/promises";

const baseUrl = "http://127.0.0.1:8080";
const outputDir = "qa-artifacts/footer";

const routes = [
  ["ua-home", "/"],
  ["ru-home", "/ru/"],
  ["ua-notes", "/notes/"],
  ["ru-notes", "/ru/notes/"],
  ["ua-article", "/notes/stress-relocation-and-lost-support/"],
  ["ru-article", "/ru/notes/stress-relocation-and-lost-support/"]
];

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
  for (const [routeName, route] of routes) {
    const page = await context.newPage();
    const consoleErrors = [];
    page.on("console", message => {
      if (message.type() === "error") consoleErrors.push(message.text());
    });
    page.on("pageerror", error => consoleErrors.push(error.message));

    const response = await page.goto(`${baseUrl}${route}`, { waitUntil: "networkidle" });
    await page.waitForTimeout(500);
    const footer = page.locator(".site-footer");
    await footer.scrollIntoViewIfNeeded();
    await page.waitForTimeout(150);

    const checks = await page.evaluate(() => {
      const footerElement = document.querySelector(".site-footer");
      const text = footerElement?.innerText ?? "";
      const isRu = document.documentElement.lang.startsWith("ru");
      const required = [
        "alinahorb.com",
        "ProAI Expert",
        isRu ? "© Алина Горб, 2026" : "© Аліна Горб, 2026",
        isRu ? "Разработано" : "Розроблено",
        "Email",
        "Telegram",
        "Instagram"
      ];
      const missing = required.filter(item => !text.includes(item));
      const visible = element => {
        if (!element) return false;
        const style = getComputedStyle(element);
        const rect = element.getBoundingClientRect();
        return style.display !== "none" && style.visibility !== "hidden" && Number(style.opacity) !== 0 && rect.width > 0 && rect.height > 0;
      };
      const elements = {
        footer: footerElement,
        brand: footerElement?.querySelector(".footer-brand"),
        links: footerElement?.querySelector(".footer-links"),
        copyright: footerElement?.querySelector(".footer-meta"),
        bottom: footerElement?.querySelector(".footer-bottom"),
        maker: footerElement?.querySelector(".maker-credit"),
        makerLabel: footerElement?.querySelector(".maker-credit small")
      };
      const hidden = Object.entries(elements).filter(([, element]) => !visible(element)).map(([name]) => name);
      return {
        missing,
        hidden,
        overflow: document.documentElement.scrollWidth > window.innerWidth + 1,
        scrollWidth: document.documentElement.scrollWidth,
        innerWidth: window.innerWidth,
        innerHeight: window.innerHeight,
        footerCount: document.querySelectorAll(".site-footer").length
      };
    });

    const screenshot = `${outputDir}/${routeName}-${viewportName}.png`;
    await footer.screenshot({ path: screenshot });

    const correctViewport = checks.innerWidth === viewport.width && checks.innerHeight === viewport.height;
    const ok = Boolean(response?.ok()) && correctViewport && checks.footerCount === 1 && !checks.overflow && checks.missing.length === 0 && checks.hidden.length === 0 && consoleErrors.length === 0;
    if (!ok) failed = true;
    report.push({ route, routeName, viewportName, expectedViewport: viewport, status: response?.status(), correctViewport, ok, consoleErrors, ...checks, screenshot });
    await page.close();
  }
  await context.close();
}

await browser.close();
await writeFile(`${outputDir}/report.json`, JSON.stringify(report, null, 2));
console.log(JSON.stringify(report, null, 2));
if (failed) process.exit(1);
