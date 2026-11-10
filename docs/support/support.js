'use strict';
(() => {
  const box = document.querySelector('.support-search');
  const input = document.querySelector('#support-search');
  const clear = document.querySelector('#support-clear');
  const count = document.querySelector('#support-results');
  const empty = document.querySelector('#support-empty');
  const topics = [...document.querySelectorAll('#support-answers > details')];
  if (!box || !input || !clear || !count || !empty || !topics.length) return;
  const normalize = text => text.toLowerCase().replaceAll('ø', 'o')
    .normalize('NFKD').replace(/[\u0300-\u036f]/g, '');
  const words = topics.map(topic => normalize(topic.textContent));
  function filter() {
    const query = normalize(input.value.trim()).split(/\s+/).filter(Boolean);
    let visible = 0;
    topics.forEach((topic, index) => {
      const match = query.every(word => words[index].includes(word));
      topic.hidden = !match;
      if (match) visible++;
    });
    count.textContent = query.length
      ? `${visible} matching topic${visible === 1 ? '' : 's'}`
      : `${topics.length} guides · search by feature or control`;
    empty.hidden = visible !== 0;
  }
  function reset() { input.value = ''; filter(); }
  input.addEventListener('input', filter);
  input.addEventListener('keydown', event => {
    if (event.key === 'Escape') { event.preventDefault(); reset(); }
  });
  clear.addEventListener('click', () => { reset(); input.focus(); });
  document.querySelectorAll('.support-aside a[href^="#"]').forEach(link => {
    link.addEventListener('click', reset);
  });
  addEventListener('hashchange', reset);
  box.hidden = false;
  filter();
})();
