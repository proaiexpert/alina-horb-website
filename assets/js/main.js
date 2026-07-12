(() => {
  'use strict';

  const init = () => {
    const toggle = document.querySelector('.mobile-nav-toggle');
    const nav = document.getElementById('mobile-navigation');

    if (!toggle || !nav) return;

    nav.hidden = true;

    const setOpen = (open) => {
      toggle.setAttribute('aria-expanded', String(open));
      toggle.classList.toggle('is-open', open);
      nav.hidden = !open;
    };

    toggle.addEventListener('click', () => {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });

    nav.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => setOpen(false));
    });
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();
