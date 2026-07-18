#!/usr/bin/env node
import { chromium } from "playwright";

const baseUrl = process.env.FORM_TEST_BASE_URL || "http://127.0.0.1:4173";
const cases = [
  {
    route: "/consultations/",
    locale: "uk",
    name: "Тестове ім’я",
    reply: "test@example.com",
    message: "Тестове звернення без надсилання до Formspree.",
    success: "Дякуємо. Повідомлення отримано.",
    requiredKeys: ["subject", "Ім’я", "Контакт", "Повідомлення"],
    forbiddenKeys: ["Мова", "locale", "source", "consent", "Формат"],
  },
  {
    route: "/ru/consultations/",
    locale: "ru",
    name: "Тестовое имя",
    reply: "@test_contact",
    message: "Тестовое обращение без отправки в Formspree.",
    success: "Спасибо. Сообщение получено.",
    requiredKeys: ["subject", "Имя", "Контакт", "Сообщение", "Удобное время"],
    forbiddenKeys: ["Язык", "locale", "source", "consent", "Формат"],
    availability: "Будни после 18:00",
  },
];

const failures = [];
const browser = await chromium.launch({ headless: true });

try {
  for (const testCase of cases) {
    const context = await browser.newContext({ reducedMotion: "reduce" });
    const page = await context.newPage();
    let submittedPayload = null;

    page.on("pageerror", (error) => failures.push(`${testCase.route}: page error: ${error.message}`));
    await page.route("https://formspree.io/f/mvzezana", async (route) => {
      try {
        submittedPayload = JSON.parse(route.request().postData() || "{}");
      } catch (error) {
        failures.push(`${testCase.route}: invalid JSON payload: ${error.message}`);
      }
      await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ ok: true }) });
    });

    await page.goto(`${baseUrl}${testCase.route}`, { waitUntil: "networkidle" });
    const form = page.locator("[data-contact-form]");
    const successPanel = page.locator("[data-form-success]");

    if ((await form.getAttribute("data-locale")) !== testCase.locale) {
      failures.push(`${testCase.route}: locale marker mismatch`);
    }

    const optionalRequired = await form.locator('[name="channel"][required], [name="service"][required], [name="timezone"][required], [name="availability"][required]').count();
    if (optionalRequired !== 0) failures.push(`${testCase.route}: optional fields remain required`);
    if (await form.locator('[name="language"]').count()) failures.push(`${testCase.route}: redundant language field remains`);

    await form.locator('[name="name"]').fill(testCase.name);
    await form.locator('[name="reply"]').fill(testCase.reply);
    await form.locator('[name="message"]').fill(testCase.message);
    if (testCase.availability) await form.locator('[name="availability"]').fill(testCase.availability);
    await form.locator('[name="consent"]').check();

    // The anti-bot timer deliberately rejects unrealistically fast submissions.
    await page.waitForTimeout(1650);
    await form.locator('button[type="submit"]').click();
    await successPanel.waitFor({ state: "visible", timeout: 5000 });

    if (await form.isVisible()) failures.push(`${testCase.route}: form remains visible after successful response`);
    const heading = (await successPanel.locator("h3").textContent())?.trim();
    if (heading !== testCase.success) failures.push(`${testCase.route}: success heading mismatch: ${heading}`);
    if (!submittedPayload) failures.push(`${testCase.route}: no intercepted Formspree payload`);

    if (submittedPayload) {
      for (const key of testCase.requiredKeys) {
        if (!(key in submittedPayload)) failures.push(`${testCase.route}: missing payload key ${key}`);
      }
      for (const key of testCase.forbiddenKeys) {
        if (key in submittedPayload) failures.push(`${testCase.route}: noisy payload key remains: ${key}`);
      }
      if (!testCase.availability && "Зручний час" in submittedPayload) failures.push(`${testCase.route}: blank optional field was submitted`);
    }

    await context.close();
  }
} finally {
  await browser.close();
}

if (failures.length) {
  console.error("Form success browser test failed:");
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}

console.log(`Form success browser test passed for ${cases.length} localized routes`);
