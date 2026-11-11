'use strict';
(() => {
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#site-nav');
  if (toggle && nav) {
    const close = () => { nav.classList.remove('is-open'); toggle.setAttribute('aria-expanded', 'false'); };
    toggle.addEventListener('click', () => {
      const open = toggle.getAttribute('aria-expanded') !== 'true';
      toggle.setAttribute('aria-expanded', String(open)); nav.classList.toggle('is-open', open);
    });
    nav.addEventListener('click', event => { if (event.target.closest('a')) close(); });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') { close(); toggle.focus(); }
    });
    window.matchMedia('(min-width:1001px)').addEventListener('change', event => { if (event.matches) close(); });
  }

  // A choice made by the visitor, never an IP- or browser-language redirect.
  const supported = ['en', 'pl'];
  let preferred = document.documentElement.lang === 'pl' ? 'pl' : 'en';
  try { const saved = localStorage.getItem('go404-language'); if (supported.includes(saved)) preferred = saved; } catch {}
  const home = preferred === 'pl' ? '/pl/' : '/';
  if (!document.body.classList.contains('landing-page')) {
    for (const link of document.querySelectorAll('[data-home-link]')) link.href = home;
    for (const link of document.querySelectorAll('[data-home-section]')) link.href = home + '#' + link.dataset.homeSection;
  }
  for (const link of document.querySelectorAll('[data-language]')) {
    // Language selection opens the homepage from the top, without a section hash.
    link.addEventListener('click', () => { try { localStorage.setItem('go404-language', link.dataset.language); } catch {} });
  }

  for (const group of document.querySelectorAll('[role="tablist"]')) {
    const tabs = [...group.querySelectorAll('[role="tab"]')];
    const select = tab => {
      for (const button of tabs) {
        const active = button === tab;
        button.setAttribute('aria-selected', String(active)); button.tabIndex = active ? 0 : -1;
        const panel = document.getElementById(button.getAttribute('aria-controls'));
        if (panel) panel.hidden = !active;
      }
    };
    for (const tab of tabs) {
      tab.addEventListener('click', () => select(tab));
      tab.addEventListener('keydown', event => {
        let index = tabs.indexOf(tab);
        if (event.key === 'ArrowRight') index = (index + 1) % tabs.length;
        else if (event.key === 'ArrowLeft') index = (index - 1 + tabs.length) % tabs.length;
        else if (event.key === 'Home') index = 0;
        else if (event.key === 'End') index = tabs.length - 1;
        else return;
        event.preventDefault(); select(tabs[index]); tabs[index].focus();
      });
    }
  }

  const dialog = document.querySelector('.image-dialog');
  let opener = null;
  if (dialog) {
    for (const button of document.querySelectorAll('.image-open')) button.addEventListener('click', () => {
      opener = button;
      const img = dialog.querySelector('img');
      img.src = button.dataset.image; img.alt = button.dataset.alt || button.querySelector('img')?.alt || 'GØ-404';
      dialog.showModal();
    });
    dialog.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
    dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
    dialog.addEventListener('close', () => { opener?.focus(); });
  }
  function openHash() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const target = id && document.getElementById(id);
    if (target?.tagName === 'DETAILS') {
      target.open = true;
      requestAnimationFrame(() => target.scrollIntoView({ block: 'start', behavior: matchMedia('(prefers-reduced-motion:reduce)').matches ? 'instant' : 'smooth' }));
    }
  }
  addEventListener('hashchange', openHash); openHash();
})();
