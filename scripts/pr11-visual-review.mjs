import { chromium, webkit } from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';

const base = 'http://127.0.0.1:4173';
const out = path.resolve('visual-review-v2');
const results = [];

const pages = [
  { id: 'ua-desktop-1440', url: '/', width: 1440, height: 1000 },
  { id: 'ua-laptop-1280', url: '/', width: 1280, height: 900 },
  { id: 'ua-mobile-390', url: '/', width: 390, height: 844, mobile: true },
  { id: 'ru-desktop-1440', url: '/ru/', width: 1440, height: 1000 },
  { id: 'ru-mobile-390', url: '/ru/', width: 390, height: 844, mobile: true },
];

const sections = [
  { id: 'ua-hero-desktop', url: '/', width: 1440, height: 1000, selector: '.hero' },
  { id: 'ua-hero-mobile', url: '/', width: 390, height: 844, selector: '.hero', mobile: true },
  { id: 'ru-hero-desktop', url: '/ru/', width: 1440, height: 1000, selector: '.hero' },
  { id: 'notes-desktop', url: '/', width: 1440, height: 1000, selector: '#notes' },
  { id: 'notes-mobile', url: '/', width: 390, height: 844, selector: '#notes', mobile: true },
  { id: 'contact-desktop', url: '/', width: 1440, height: 1000, selector: '#contact' },
  { id: 'contact-mobile', url: '/', width: 390, height: 844, selector: '#contact', mobile: true },
  { id: 'ua-article', url: '/notes/when-coping-stops-helping/', width: 1280, height: 900, selector: 'main' },
  { id: 'ru-article', url: '/ru/notes/when-coping-stops-helping/', width: 1280, height: 900, selector: 'main' },
];

async function settle(page) {
  await page.evaluate(() => document.fonts?.ready);
  await page.evaluate(async () => {
    const pause = (ms) => new Promise(resolve => setTimeout(resolve, ms));
    const step = Math.max(260, Math.floor(window.innerHeight * 0.72));
    const max = Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);
    for (let y = 0; y < max; y += step) {
      window.scrollTo(0, y);
      await pause(90);
    }
    window.scrollTo(0, max);
    await pause(250);
    window.scrollTo(0, 0);
    await pause(350);
  });
  await page.waitForLoadState('networkidle').catch(() => {});
  await page.waitForTimeout(350);
}

async function collectMetrics(page) {
  return page.evaluate(() => {
    const doc = document.documentElement;
    const heroImage = document.querySelector('.hero-portrait img');
    const form = document.querySelector('.contact-form-wrap');
    const telegramPlaceholder = document.querySelector('[data-telegram-placeholder]');
    const telegramLink = document.querySelector('[data-telegram-link]');
    const brokenImages = [...document.images]
      .filter(img => !img.complete || img.naturalWidth === 0)
      .map(img => img.currentSrc || img.src);
    const visible = (element) => Boolean(element && getComputedStyle(element).display !== 'none' && !element.hidden);
    return {
      title: document.title,
      path: location.pathname,
      h1Count: document.querySelectorAll('h1').length,
      horizontalOverflow: Math.max(doc.scrollWidth, document.body.scrollWidth) - window.innerWidth,
      brokenImages,
      heroImage: heroImage ? {
        currentSrc: heroImage.currentSrc,
        naturalWidth: heroImage.naturalWidth,
        naturalHeight: heroImage.naturalHeight,
        rendered: heroImage.getBoundingClientRect().toJSON(),
      } : null,
      contactFormWidth: form ? Math.round(form.getBoundingClientRect().width) : null,
      telegramPlaceholderVisible: visible(telegramPlaceholder),
      telegramLinkVisible: visible(telegramLink),
    };
  });
}

async function runBrowser(browserType, browserName) {
  const browser = await browserType.launch();
  const browserDir = path.join(out, browserName);
  await fs.mkdir(browserDir, { recursive: true });

  for (const item of pages) {
    const context = await browser.newContext({
      viewport: { width: item.width, height: item.height },
      deviceScaleFactor: 1,
      isMobile: Boolean(item.mobile),
      hasTouch: Boolean(item.mobile),
    });
    const page = await context.newPage();
    const consoleErrors = [];
    const pageErrors = [];
    const badResponses = [];
    page.on('console', message => { if (message.type() === 'error') consoleErrors.push(message.text()); });
    page.on('pageerror', error => pageErrors.push(String(error)));
    page.on('response', response => {
      if (response.url().startsWith(base) && response.status() >= 400) {
        badResponses.push({ status: response.status(), url: response.url() });
      }
    });
    const response = await page.goto(base + item.url, { waitUntil: 'networkidle', timeout: 45000 });
    await settle(page);
    const metrics = await collectMetrics(page);
    await page.screenshot({ path: path.join(browserDir, `${item.id}.png`), fullPage: true });
    results.push({ browser: browserName, id: item.id, httpStatus: response?.status() ?? null, consoleErrors, pageErrors, badResponses, ...metrics });
    await context.close();
  }

  if (browserName === 'chromium') {
    for (const item of sections) {
      const context = await browser.newContext({
        viewport: { width: item.width, height: item.height },
        deviceScaleFactor: 1,
        isMobile: Boolean(item.mobile),
        hasTouch: Boolean(item.mobile),
      });
      const page = await context.newPage();
      await page.goto(base + item.url, { waitUntil: 'networkidle', timeout: 45000 });
      await settle(page);
      const locator = page.locator(item.selector).first();
      await locator.scrollIntoViewIfNeeded();
      await page.waitForTimeout(500);
      await locator.screenshot({ path: path.join(browserDir, `${item.id}.png`) });
      await context.close();
    }
  }

  await browser.close();
}

try {
  await fs.mkdir(out, { recursive: true });
  await runBrowser(chromium, 'chromium');
  await runBrowser(webkit, 'webkit');
  await fs.writeFile(path.join(out, 'report.json'), JSON.stringify(results, null, 2));
  const failures = results.filter(result =>
    result.httpStatus !== 200 ||
    result.consoleErrors.length ||
    result.pageErrors.length ||
    result.badResponses.length ||
    result.brokenImages.length ||
    result.horizontalOverflow > 1 ||
    result.h1Count !== 1 ||
    (result.id.includes('desktop') && result.contactFormWidth && result.contactFormWidth > 600) ||
    result.telegramLinkVisible
  );
  await fs.writeFile(path.join(out, 'summary.txt'), failures.length ? JSON.stringify(failures, null, 2) : 'Automated visual checks passed.\n');
} catch (error) {
  await fs.mkdir(out, { recursive: true });
  await fs.writeFile(path.join(out, 'fatal.txt'), String(error?.stack || error));
  console.error(error);
}
