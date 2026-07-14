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
})();
