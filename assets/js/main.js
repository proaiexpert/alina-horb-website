(() => {
  'use strict';

  const config = window.ALINA_SITE_CONFIG || {
    email: 'alinahorb1991@gmail.com',
    telegramUsername: '',
    phone: ''
  };

  const copy = {
    uk: {
      subject: 'Звернення через сайт Аліни Горб',
      name: 'Ім’я',
      reply: 'Контакт для відповіді',
      language: 'Зручна мова',
      message: 'Повідомлення',
      opening: 'Після натискання відкриється ваша поштова програма.'
    },
    ru: {
      subject: 'Обращение через сайт Алины Горб',
      name: 'Имя',
      reply: 'Контакт для ответа',
      language: 'Удобный язык',
      message: 'Сообщение',
      opening: 'После нажатия откроется ваше почтовое приложение.'
    }
  };

  const initNavigation = () => {
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

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        setOpen(false);
        toggle.focus();
      }
    });
  };

  const initTelegram = () => {
    const username = String(config.telegramUsername || '').trim().replace(/^@/, '');
    const activeLinks = document.querySelectorAll('[data-telegram-link]');
    const placeholders = document.querySelectorAll('[data-telegram-placeholder], [data-telegram-note]');

    if (!username) {
      activeLinks.forEach((link) => { link.hidden = true; });
      return;
    }

    const telegramUrl = `https://t.me/${username}`;
    activeLinks.forEach((link) => {
      link.href = telegramUrl;
      link.hidden = false;
    });
    placeholders.forEach((element) => { element.hidden = true; });
  };

  const initContactForm = () => {
    const form = document.getElementById('contact-form');
    if (!form) return;

    const locale = form.dataset.locale === 'ru' ? 'ru' : 'uk';
    const text = copy[locale];
    const status = form.querySelector('[data-form-status]');

    form.addEventListener('submit', (event) => {
      event.preventDefault();
      if (!form.reportValidity()) return;

      const formData = new FormData(form);
      const body = [
        `${text.name}: ${String(formData.get('name') || '').trim()}`,
        `${text.reply}: ${String(formData.get('reply') || '').trim()}`,
        `${text.language}: ${String(formData.get('language') || '').trim()}`,
        '',
        `${text.message}:`,
        String(formData.get('message') || '').trim()
      ].join('\n');

      if (status) status.textContent = text.opening;

      const email = String(config.email || 'alinahorb1991@gmail.com').trim();
      window.location.href = `mailto:${email}?subject=${encodeURIComponent(text.subject)}&body=${encodeURIComponent(body)}`;
    });
  };

  const init = () => {
    initNavigation();
    initTelegram();
    initContactForm();
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();
