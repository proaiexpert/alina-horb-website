window.ALINA_SITE_CONFIG = {
  email: "hello@alinahorb.com",
  telegramUsername: "alina_horb1991",
  formEndpoint: "",
  formMode: "mailto"
};

(() => {
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

  appendStylesheet("../css/site.v3-1-stability.css");
  appendStylesheet("../css/site.footer.v3-2.css");
  appendStylesheet("../css/site.privacy.v3-2.css");

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
