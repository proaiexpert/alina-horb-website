(() => {
  "use strict";

  const script = document.currentScript;
  if (!script) return;

  const appendStylesheet = (relativePath) => {
    const href = new URL(relativePath, script.src).href;
    if (document.querySelector(`link[href="${href}"]`)) return;
    const stylesheet = document.createElement("link");
    stylesheet.rel = "stylesheet";
    stylesheet.href = href;
    document.head.appendChild(stylesheet);
  };

  appendStylesheet("../css/site.chrome.v3.css");
  appendStylesheet("../css/site.notes-images.v3.css");

  const faviconUrl = new URL("../images/logos/favicon-ag.svg", script.src).href;
  let favicon = document.querySelector('link[rel~="icon"]');
  if (!favicon) {
    favicon = document.createElement("link");
    favicon.rel = "icon";
    document.head.appendChild(favicon);
  }
  favicon.type = "image/svg+xml";
  favicon.href = faviconUrl;

  const pathname = window.location.pathname;
  const projectMarker = "/alina-horb-website/";
  const rootPath = pathname.includes(projectMarker) ? projectMarker : "/";
  const relativePath = pathname.startsWith(rootPath) ? pathname.slice(rootPath.length) : pathname.replace(/^\//, "");
  const isRu = document.documentElement.lang.toLowerCase().startsWith("ru") || relativePath.startsWith("ru/");
  const noteAssetBase = new URL("../images/notes/", script.src).href;

  const noteImages = {
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

  const pictureMarkup = (item) => `<picture><img src="${noteAssetBase}${item.file}" width="1200" height="800" loading="${relativePath.endsWith("first-consultation/") ? "eager" : "lazy"}" decoding="async" alt="${item.alt}"></picture>`;

  const replaceIdentity = (selector, key) => {
    const element = document.querySelector(selector);
    if (!element) return;
    element.classList.add("note-photo", `note-photo--${key}`);
    element.innerHTML = pictureMarkup(noteImages[key]);
  };

  const applyNotesImages = () => {
    const feature = document.querySelector(".notes-hub-feature-media");
    if (feature) {
      const number = feature.querySelector(".notes-hub-feature-number")?.outerHTML || "";
      feature.innerHTML = `${pictureMarkup(noteImages.first)}${number}`;
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
    const slug = Object.keys(slugMap).find((value) => relativePath.includes(`/notes/${value}/`) || relativePath.endsWith(`notes/${value}/`));
    if (!slug) return;

    const key = slugMap[slug];
    document.body.dataset.note = key;
    const visual = document.querySelector(".article-hero-visual");
    const currentPicture = visual?.querySelector("picture");
    if (currentPicture) currentPicture.outerHTML = pictureMarkup(noteImages[key]);

    const absoluteImage = `${noteAssetBase}${noteImages[key].file}`;
    document.querySelectorAll('meta[property="og:image"], meta[property="og:image:secure_url"], meta[name="twitter:image"]').forEach((meta) => meta.setAttribute("content", absoluteImage));
    document.querySelectorAll('meta[property="og:image:width"]').forEach((meta) => meta.setAttribute("content", "1200"));
    document.querySelectorAll('meta[property="og:image:height"]').forEach((meta) => meta.setAttribute("content", "800"));
  };

  applyNotesImages();

  if (!document.querySelector('script[data-global-chrome-v1]')) {
    const globalChrome = document.createElement("script");
    globalChrome.src = `${rootPath}assets/js/site.global-chrome.v1.js?v=20260717-chrome1`;
    globalChrome.defer = true;
    globalChrome.dataset.globalChromeV1 = "";
    document.head.appendChild(globalChrome);
  }
})();
