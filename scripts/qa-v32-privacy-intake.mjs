import { chromium } from "playwright";
import { mkdir, writeFile } from "node:fs/promises";

const baseUrl = "http://127.0.0.1:8080";
const outputDir = "qa-artifacts/privacy-intake";
const routes = [
  ["ua-home", "/", "home", "uk"],
  ["ru-home", "/ru/", "home", "ru"],
  ["ua-privacy", "/privacy/", "privacy", "uk"],
  ["ru-privacy", "/ru/privacy/", "privacy", "ru"],
  ["ua-notes", "/notes/", "inner", "uk"],
  ["ru-notes", "/ru/notes/", "inner", "ru"]
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

  for (const [name, route, kind, language] of routes) {
    const page = await context.newPage();
    const consoleErrors = [];
    page.on("console", message => { if (message.type() === "error") consoleErrors.push(message.text()); });
    page.on("pageerror", error => consoleErrors.push(error.message));

    const response = await page.goto(`${baseUrl}${route}`, { waitUntil: "domcontentloaded" });
    await page.waitForTimeout(650);

    const checks = await page.evaluate(({ kind, language }) => {
      const ids = [...document.querySelectorAll("[id]")].map(element => element.id);
      const duplicateIds = [...new Set(ids.filter((id, index) => ids.indexOf(id) !== index))];
      const emailLinks = [...document.querySelectorAll('a[href^="mailto:"]')].map(link => link.getAttribute("href"));
      const privacyLinks = [...document.querySelectorAll('a[href*="privacy/"]')].map(link => link.getAttribute("href"));
      const expectedPrivacyFragment = language === "ru" ? "/ru/privacy/" : "/privacy/";
      const footer = document.querySelector(".site-footer");
      const footerPrivacy = [...(footer?.querySelectorAll('a[href*="privacy/"]') ?? [])].some(link => {
        try { return new URL(link.href).pathname.endsWith(expectedPrivacyFragment); }
        catch { return false; }
      });
      const base = {
        h1Count: document.querySelectorAll("h1").length,
        duplicateIds,
        pageOverflow: document.documentElement.scrollWidth > window.innerWidth + 1,
        noindex: Boolean(document.querySelector('meta[name="robots"][content="noindex, nofollow"]')),
        emailLinks,
        oldEmailVisible: document.documentElement.innerHTML.includes("alinahorb1991@gmail.com"),
        privacyLinks,
        footerPrivacy,
        footerVisible: Boolean(footer && getComputedStyle(footer).display !== "none"),
        innerWidth: window.innerWidth,
        innerHeight: window.innerHeight
      };

      if (kind === "home") {
        const form = document.querySelector("[data-contact-form]");
        const honeypot = form?.querySelector('[name="website"]');
        const startedAt = form?.querySelector('[name="startedAt"]');
        const message = form?.querySelector('[name="message"]');
        const consentPrivacy = form?.querySelector('.form-consent a[href*="privacy/"]');
        return {
          ...base,
          formPresent: Boolean(form),
          honeypotPresent: Boolean(honeypot),
          honeypotHidden: Boolean(honeypot && (honeypot.getBoundingClientRect().left < -1000 || getComputedStyle(honeypot).opacity === "0")),
          startedAtSet: Boolean(startedAt?.value),
          messageMaxLength: message?.maxLength ?? null,
          consentPrivacy: Boolean(consentPrivacy),
          emergencyBoundary: document.querySelector("#contact")?.innerText.toLowerCase().includes(language === "ru" ? "не являются экстренной службой" : "не є екстреною службою") ?? false
        };
      }

      if (kind === "privacy") {
        return {
          ...base,
          policySections: document.querySelectorAll(".privacy-content > section").length,
          policyEmail: document.querySelector(".privacy-content")?.innerText.includes("hello@alinahorb.com") ?? false,
          emergencyBoundary: document.querySelector(".privacy-content")?.innerText.toLowerCase().includes(language === "ru" ? "неэкстренный" : "неекстрений") ?? false
        };
      }

      return base;
    }, { kind, language });

    let spamCheck = null;
    let mobileCtaHiddenOverAbout = null;
    if (kind === "home") {
      if (viewport.width === 390) {
        await page.locator('[name="name"]').fill(language === "ru" ? "Тест" : "Тест");
        await page.locator('[name="reply"]').fill("test@example.com");
        await page.locator('[name="channel"]').selectOption("Email");
        await page.locator('[name="language"]').selectOption({ index: 1 });
        await page.locator('[name="format"]').selectOption({ index: 1 });
        await page.locator('[name="message"]').fill(language === "ru" ? "Организационный вопрос" : "Організаційне запитання");
        await page.locator('[name="consent"]').check();
        await page.locator('[name="website"]').evaluate(element => { element.value = "spam.example"; });
        await page.locator('button[type="submit"]').click();
        await page.waitForTimeout(100);
        spamCheck = await page.locator("[data-form-status]").evaluate(element => ({
          state: element.dataset.state,
          text: element.textContent
        }));

        await page.locator("#about").scrollIntoViewIfNeeded();
        await page.waitForTimeout(350);
        mobileCtaHiddenOverAbout = await page.locator("[data-mobile-booking-cta]").evaluate(element => element.hidden || element.getAttribute("aria-hidden") === "true" || !element.classList.contains("is-visible"));
      }

      await page.locator("#contact").screenshot({ path: `${outputDir}/${name}-${viewportName}.png` });
    } else if (kind === "privacy") {
      await page.locator(".privacy-main").screenshot({ path: `${outputDir}/${name}-${viewportName}.png` });
    }

    const correctViewport = checks.innerWidth === viewport.width && checks.innerHeight === viewport.height;
    const commonOk = Boolean(response?.ok())
      && correctViewport
      && checks.h1Count === 1
      && checks.duplicateIds.length === 0
      && !checks.pageOverflow
      && checks.noindex
      && !checks.oldEmailVisible
      && checks.emailLinks.length > 0
      && checks.emailLinks.every(href => href === "mailto:hello@alinahorb.com")
      && checks.footerPrivacy
      && checks.footerVisible
      && consoleErrors.length === 0;

    const kindOk = kind === "home"
      ? checks.formPresent && checks.honeypotPresent && checks.honeypotHidden && checks.startedAtSet && checks.messageMaxLength === 600 && checks.consentPrivacy && checks.emergencyBoundary && (viewport.width !== 390 || (spamCheck?.state === "error" && mobileCtaHiddenOverAbout))
      : kind === "privacy"
        ? checks.policySections >= 10 && checks.policyEmail && checks.emergencyBoundary
        : true;

    const ok = commonOk && kindOk;
    if (!ok) failed = true;
    report.push({ name, route, kind, language, viewportName, expectedViewport: viewport, status: response?.status(), correctViewport, ok, consoleErrors, spamCheck, mobileCtaHiddenOverAbout, ...checks });
    await page.close();
  }

  await context.close();
}

await browser.close();
await writeFile(`${outputDir}/report.json`, JSON.stringify(report, null, 2));
console.log(JSON.stringify(report, null, 2));
if (failed) process.exit(1);
