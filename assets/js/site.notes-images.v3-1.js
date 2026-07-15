(() => {
  "use strict";

  const script = document.currentScript;
  if (!script) return;

  const apply = () => {
    const path = window.location.pathname;
    const isRu = document.documentElement.lang.toLowerCase().startsWith("ru") || /\/ru\//.test(path);
    const base = new URL("../images/notes/", script.src).href;
    const images = {
      first: {
        file: "alina-horb-note-first-consultation-v3.webp",
        alt: isRu ? "Два кресла в спокойном светлом пространстве для первой консультации" : "Два крісла у спокійному світлому просторі для першої консультації"
      },
      conversation: {
        file: "alina-horb-note-conversation-v3.webp",
        alt: isRu ? "Открытый блокнот как образ начала трудного разговора" : "Відкритий нотатник як образ початку складної розмови"
      },
      observation: {
        file: "alina-horb-note-observation-v3.webp",
        alt: isRu ? "Блокнот и ручка как образ внимательного наблюдения за своим состоянием" : "Нотатник і ручка як образ уважного спостереження за власним станом"
      },
      transition: {
        file: "alina-horb-note-transition-v3.webp",
        alt: isRu ? "Коробка, карта и ключ как образ переезда и восстановления опоры" : "Коробка, мапа і ключ як образ переїзду та відновлення опори"
      }
    };

    const picture = (key, eager = false) => {
      const item = images[key];
      return `<picture><img src="${base}${item.file}" width="1200" height="800" loading="${eager ? "eager" : "lazy"}" decoding="async" alt="${item.alt}"></picture>`;
    };

    const replaceIdentity = (selector, key) => {
      document.querySelectorAll(selector).forEach((element) => {
        element.classList.add("note-photo", `note-photo--${key}`);
        element.innerHTML = picture(key);
      });
    };

    const homeFeature = document.querySelector(".home-note-feature-media");
    if (homeFeature) {
      const index = homeFeature.querySelector(".home-note-index")?.outerHTML || "";
      homeFeature.innerHTML = `${picture("first")}${index}`;
    }

    const hubFeature = document.querySelector(".notes-hub-feature-media");
    if (hubFeature) {
      const number = hubFeature.querySelector(".notes-hub-feature-number")?.outerHTML || "";
      hubFeature.innerHTML = `${picture("first", true)}${number}`;
    }

    replaceIdentity(".note-identity--conversation", "conversation");
    replaceIdentity(".note-identity--observation", "observation");
    replaceIdentity(".note-identity--transition", "transition");

    const slugMap = {
      "first-consultation": "first",
      "how-to-start-the-conversation": "conversation",
      "when-coping-stops-helping": "observation",
      "stress-relocation-and-lost-support": "transition"
    };
    const slug = Object.keys(slugMap).find((value) => path.includes(`/notes/${value}/`));
    if (!slug) return;

    const key = slugMap[slug];
    document.body.dataset.note = key;
    const visual = document.querySelector(".article-hero-visual");
    const existingPicture = visual?.querySelector("picture");
    if (existingPicture) existingPicture.outerHTML = picture(key, true);

    const absoluteImage = `${base}${images[key].file}`;
    document.querySelectorAll('meta[property="og:image"], meta[property="og:image:secure_url"], meta[name="twitter:image"]').forEach((meta) => meta.setAttribute("content", absoluteImage));
    document.querySelectorAll('meta[property="og:image:width"]').forEach((meta) => meta.setAttribute("content", "1200"));
    document.querySelectorAll('meta[property="og:image:height"]').forEach((meta) => meta.setAttribute("content", "800"));
  };

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", apply, { once: true });
  else apply();
})();
