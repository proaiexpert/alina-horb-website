window.ALINA_SITE_CONFIG = {
  email: "alinahorb1991@gmail.com",
  telegramUsername: "alina_horb1991",
  formEndpoint: "",
  formMode: "mailto"
};

(() => {
  const script = document.currentScript;
  if (!script) return;

  const stylesheet = document.createElement("link");
  stylesheet.rel = "stylesheet";
  stylesheet.href = new URL("../css/site.v3-1-stability.css", script.src).href;
  document.head.appendChild(stylesheet);

  const faviconUrl = new URL("../images/logos/favicon-ag.svg", script.src).href;
  let favicon = document.querySelector('link[rel~="icon"]');
  if (!favicon) {
    favicon = document.createElement("link");
    favicon.rel = "icon";
    document.head.appendChild(favicon);
  }
  favicon.type = "image/svg+xml";
  favicon.href = faviconUrl;
})();
