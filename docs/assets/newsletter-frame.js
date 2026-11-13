// Same-origin official Brevo export: measure content, never mask overflow.
(() => {
  for (const frame of document.querySelectorAll('[data-newsletter-frame]')) {
    let observer;
    const attach = () => {
      observer?.disconnect();
      const doc = frame.contentDocument;
      if (!doc?.body) return; // Cross-origin navigation retains native scrolling fallback.
      const content = doc.querySelector('.sib-form');
      if (!content) return;
      const resize = () => {
        const height = Math.ceil(content.getBoundingClientRect().height);
        if (height > 0) frame.style.height = `${height}px`;
      };
      observer = new ResizeObserver(resize);
      observer.observe(content);
      doc.fonts?.ready.then(resize);
      resize();
    };
    frame.addEventListener('load', attach);
    attach();
  }
})();
