/* Nico & Kai Development — chování webu: splash, hero, galerie + lightbox, interaktivní fasáda, ceník a rezervace */
(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const CFG = window.NK_CONFIG || {};
  const nf = new Intl.NumberFormat('cs-CZ');
  const nfa = new Intl.NumberFormat('cs-CZ', { minimumFractionDigits: 1, maximumFractionDigits: 2 });
  const kc = (n) => `${nf.format(n)} Kč`;
  const area = (v) => `${nfa.format(v)} m²`;
  const STATUS = { available: 'Volný', reserved: 'Rezervovaný', sold: 'Prodaný' };
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  /* ---------- splash (jen jednou za návštěvu) ---------- */
  const splash = $('.splash');
  if (splash) {
    let seen = false;
    try { seen = sessionStorage.getItem('nk-splash') === '1'; } catch (e) { /* private mode */ }
    if (seen || reduce) { splash.remove(); document.documentElement.classList.remove('has-splash'); }
    else {
      document.documentElement.classList.add('has-splash');
      const done = () => { splash.classList.add('is-done'); document.documentElement.classList.remove('has-splash'); setTimeout(() => splash.remove(), 1200); try { sessionStorage.setItem('nk-splash', '1'); } catch (e) { /* ignore */ } };
      setTimeout(done, 1500);
      splash.addEventListener('click', done);
    }
  }

  /* ---------- hero: Ken Burns + prolínání ---------- */
  $$('.hero-media').forEach((h) => {
    const slides = $$('.hero-media__bg.is-slides img', h);
    const start = () => h.classList.add('is-ready');
    const first = $('.hero-media__bg img', h);
    if (first && !first.complete) first.addEventListener('load', start, { once: true }); else start();
    if (slides.length > 1 && !reduce) {
      let i = 0; slides[0].classList.add('is-on');
      setInterval(() => { slides[i].classList.remove('is-on'); i = (i + 1) % slides.length; slides[i].classList.add('is-on'); }, 7000);
    } else if (slides.length) slides[0].classList.add('is-on');
  });

  $$('.facade__img').forEach((img) => { if (img.complete) img.classList.add('is-loaded'); else img.addEventListener('load', () => img.classList.add('is-loaded'), { once: true }); });

  /* ---------- galerie: líné načtení + lightbox ---------- */
  $$('.gallery img').forEach((img) => { if (img.complete) img.classList.add('is-loaded'); else img.addEventListener('load', () => img.classList.add('is-loaded'), { once: true }); });
  let lb = $('#lightbox');
  if (!lb && $('.gallery')) {
    lb = document.createElement('dialog'); lb.id = 'lightbox'; lb.className = 'lightbox';
    lb.innerHTML = '<div class="lightbox__stage"><img alt=""><button class="lightbox__btn lightbox__prev" type="button" aria-label="Předchozí">←</button><button class="lightbox__btn lightbox__next" type="button" aria-label="Další">→</button><button class="lightbox__close" type="button">Zavřít ✕</button><p class="lightbox__cap"></p></div>';
    document.body.appendChild(lb);
  }
  if (lb) {
    let items = [], idx = 0;
    const img = $('img', lb), cap = $('.lightbox__cap', lb);
    const show = (i) => { idx = (i + items.length) % items.length; const it = items[idx]; img.src = it.full; img.alt = it.alt; cap.textContent = `${it.cap ? it.cap + ' · ' : ''}${idx + 1} / ${items.length}`; };
    $$('.gallery').forEach((g) => {
      const figs = $$('figure', g);
      figs.forEach((f, i) => {
        f.setAttribute('tabindex', '0'); f.setAttribute('role', 'button');
        const open = () => { items = figs.map((x) => { const im = $('img', x); return { full: im.dataset.full || im.currentSrc || im.src, alt: im.alt, cap: $('figcaption', x) ? $('figcaption', x).textContent : '' }; }); show(i); lb.showModal(); };
        f.addEventListener('click', open);
        f.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); } });
      });
    });
    $('.lightbox__prev', lb).addEventListener('click', () => show(idx - 1));
    $('.lightbox__next', lb).addEventListener('click', () => show(idx + 1));
    $('.lightbox__close', lb).addEventListener('click', () => lb.close());
    lb.addEventListener('click', (e) => { if (e.target === lb || e.target.classList.contains('lightbox__stage')) lb.close(); });
    lb.addEventListener('keydown', (e) => { if (e.key === 'ArrowLeft') show(idx - 1); if (e.key === 'ArrowRight') show(idx + 1); });
    let tx = null;
    lb.addEventListener('touchstart', (e) => { tx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', (e) => { if (tx === null) return; const dx = e.changedTouches[0].clientX - tx; if (Math.abs(dx) > 50) show(idx + (dx < 0 ? 1 : -1)); tx = null; });
  }

  /* ---------- interaktivní fasáda ---------- */
  const NS = 'http://www.w3.org/2000/svg';
  $$('[data-facade]').forEach((root) => {
    const P = (window.NK_PROJECTS || {})[root.dataset.facade];
    if (!P || !P.facade) return;
    const F = P.facade; const [W, H] = F.size;
    const unitById = Object.fromEntries(P.units.map((u) => [u.id, u]));
    const svg = document.createElementNS(NS, 'svg'); svg.setAttribute('class', 'facade__svg'); svg.setAttribute('viewBox', `0 0 ${W} ${H}`); svg.setAttribute('preserveAspectRatio', 'none');
    const tip = document.createElement('div'); tip.className = 'facade__tip'; tip.setAttribute('aria-hidden', 'true');
    Object.entries(F.zones).forEach(([id, pts]) => {
      const u = unitById[id]; if (!u) return;
      const poly = document.createElementNS(NS, 'polygon');
      poly.setAttribute('points', pts.map((p) => p.join(',')).join(' '));
      poly.setAttribute('class', `facade__zone st-${u.status}`);
      poly.setAttribute('tabindex', '0'); poly.setAttribute('role', 'button');
      poly.setAttribute('aria-label', `Byt ${id}, ${u.disposition}, ${area(u.areaNV || u.area)}, ${STATUS[u.status]}`);
      poly.dataset.unit = id;
      const bx = pts.map((p) => p[0]), by = pts.map((p) => p[1]);
      const cx = (Math.min(...bx) + Math.max(...bx)) / 2, cy = (Math.min(...by) + Math.max(...by)) / 2;
      const label = document.createElementNS(NS, 'text'); label.setAttribute('class', 'facade__label'); label.setAttribute('x', cx); label.setAttribute('y', cy + 18); label.setAttribute('text-anchor', 'middle'); label.setAttribute('font-size', Math.round(W / 42)); label.textContent = id;
      svg.appendChild(poly); svg.appendChild(label);
      const showTip = () => {
        tip.innerHTML = `<strong>Byt ${esc(id)}</strong><span>${esc(u.disposition)} · ${area(u.areaNV || u.area)}${u.terrace != null ? ` + ${area(u.terrace)} ${esc((u.outdoorLabel || 'terasa').toLowerCase())}` : ''}</span>${u.status === 'available' && u.price != null && CFG.priceMode !== 'onRequest' ? `<span>${kc(u.price)}</span>` : ''}<em class="st-${u.status}">${STATUS[u.status]}</em>`;
        const r = root.getBoundingClientRect(); const xs = pts.map((p) => p[0]), ys = pts.map((p) => p[1]);
        tip.style.left = `${((Math.min(...xs) + Math.max(...xs)) / 2 / W) * r.width}px`;
        tip.style.top = `${(Math.min(...ys) / H) * r.height + 8}px`;
        tip.classList.add('is-on');
      };
      poly.addEventListener('mouseenter', showTip); poly.addEventListener('focus', showTip);
      poly.addEventListener('mouseleave', () => tip.classList.remove('is-on')); poly.addEventListener('blur', () => tip.classList.remove('is-on'));
      const go = () => {
        if (u.status === 'sold') return;
        $$('.facade__zone', svg).forEach((z) => z.classList.toggle('is-selected', z === poly));
        if (window.NK_EXPLORER && window.NK_EXPLORER.project === P.slug) { window.NK_EXPLORER.selectUnit(id, true); }
        else { const t = $('#byty'); if (t) t.scrollIntoView({ behavior: 'smooth' }); }
      };
      poly.addEventListener('click', go);
      poly.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); } });
    });
    root.appendChild(svg); root.appendChild(tip);
    document.addEventListener('nk:unit', (e) => { $$('.facade__zone', svg).forEach((z) => z.classList.toggle('is-selected', z.dataset.unit === e.detail.unit)); });
    // ukázat štítky, dokud uživatel nenajede myší
    root.classList.add('show-labels');
    root.addEventListener('mouseenter', () => root.classList.remove('show-labels'), { once: true });
  });

  /* ---------- příslušenství + rezervační tabulka ---------- */
  const pricesPublic = CFG.priceMode !== 'onRequest';
  const range = (arr) => arr.length ? (Math.min(...arr) === Math.max(...arr) ? kc(arr[0]) : `${kc(Math.min(...arr))} – ${kc(Math.max(...arr))}`) : 'na vyžádání';
  $$('[data-extras]').forEach((el) => {
    const P = (window.NK_PROJECTS || {})[el.dataset.extras]; if (!P || !P.pricing) return;
    const cells = pricesPublic ? P.cellars.map((c) => c.price).filter((p) => p != null) : [];
    const carea = P.cellars.map((c) => c.area);
    const prices = pricesPublic ? P.units.filter((u) => u.status === 'available').map((u) => u.price).filter((p) => p != null) : [];
    const park = pricesPublic && P.pricing.parking.price != null ? kc(P.pricing.parking.price) : 'na vyžádání';
    el.innerHTML = `
      <div><dt>${esc(P.pricing.parking.label)}</dt><dd>${park}<small>${P.pricing.parking.count} stání v garáži${P.parking.some((p) => p.accessible) ? ', 1 bezbariérové' : ''}</small></dd></div>
      <div><dt>Sklep</dt><dd>${range(cells)}<small>${P.cellars.length} sklepů · ${area(Math.min(...carea))} – ${area(Math.max(...carea))}</small></dd></div>
      <div><dt>Ceny bytů</dt><dd>${range(prices)}<small>${P.units.filter((u) => u.status === 'available').length} z ${P.units.length} bytů volných</small></dd></div>`;
  });
  $$('[data-reservation]').forEach((el) => {
    const P = (window.NK_PROJECTS || {})[el.dataset.reservation]; if (!P || !P.reservation) return;
    const R = P.reservation;
    const withPrices = pricesPublic && P.units.some((u) => u.status === 'available' && u.price != null);
    if (withPrices) {
      const head = R.tiers.map(([dep, disc]) => `<th scope="col">Záloha ${nf.format(dep / 1e6)} mil. Kč<small>sleva ${nf.format(disc * 100)} %</small></th>`).join('');
      const rows = P.units.map((u) => {
        const ok = u.status === 'available' && u.price != null;
        const cells = R.tiers.map(([dep, disc], i) => ok ? `<td${i === R.tiers.length - 1 ? ' class="is-best"' : ''}>${kc(Math.round(u.price * (1 - disc) / 1000) * 1000)}</td>` : '<td>–</td>').join('');
        return `<tr class="st-${u.status}"><th scope="row">Byt ${esc(u.id)}</th><td>${ok ? kc(u.price) : (u.status === 'available' ? 'na vyžádání' : STATUS[u.status])}</td>${cells}</tr>`;
      }).join('');
      el.innerHTML = `<table class="reserve-table"><thead><tr><th scope="col">Byt</th><th scope="col">Cena bytu</th>${head}</tr></thead><tbody>${rows}</tbody></table>`;
    } else {
      el.innerHTML = `<div class="reserve-tiers">${R.tiers.map(([dep, disc], i) => `<div class="reserve-tier${i === R.tiers.length - 1 ? ' is-best' : ''}"><small>Záloha</small><strong>${nf.format(dep / 1e6)} mil. Kč</strong><span>sleva ${nf.format(disc * 100)} % z ceny bytu</span></div>`).join('')}</div>`;
    }
    const d = new Date(R.deadline);
    $$('[data-reservation-deadline]').forEach((x) => { x.textContent = `${d.getDate()}. ${d.getMonth() + 1}. ${d.getFullYear()}`; });
  });
  $$('[data-if-prices]').forEach((e) => { e.hidden = !pricesPublic; });
  $$('[data-if-no-prices]').forEach((e) => { e.hidden = pricesPublic; });

  /* ---------- čísla: nápočet ---------- */
  const counters = $$('[data-count]');
  if (counters.length && !reduce) {
    const io = new IntersectionObserver((es) => es.forEach((e) => {
      if (!e.isIntersecting) return; io.unobserve(e.target);
      const el = e.target, to = parseFloat(el.dataset.count), dec = (el.dataset.count.split('.')[1] || '').length, t0 = performance.now();
      const tick = (t) => { const k = Math.min(1, (t - t0) / 1400), v = to * (1 - Math.pow(1 - k, 3)); el.textContent = new Intl.NumberFormat('cs-CZ', { minimumFractionDigits: dec, maximumFractionDigits: dec, useGrouping: !(to >= 1900 && to < 2200) }).format(v); if (k < 1) requestAnimationFrame(tick); };
      requestAnimationFrame(tick);
    }), { threshold: .6 });
    counters.forEach((c) => io.observe(c));
  }

  /* ---------- jednotky bez výběru (Vysoké) ---------- */
  $$('[data-units-cards]').forEach((el) => {
    const P = (window.NK_PROJECTS || {})[el.dataset.unitsCards]; if (!P) return;
    el.innerHTML = P.units.map((u) => `<article class="ucard" data-reveal>
      <div class="ucard__head"><span class="ucard__id">${esc(u.id)}</span><span class="tag tag--${u.status}">${u.status === 'available' ? 'Volný' : STATUS[u.status]}</span></div>
      <dl>
        <div><dt>Dům</dt><dd>${esc(u.house || '–')}</dd></div>
        <div><dt>Dispozice</dt><dd>${u.disposition ? esc(u.disposition) : 'doplníme'}</dd></div>
        <div><dt>Plocha</dt><dd>${u.area ? area(u.area) : 'doplníme'}</dd></div>
        <div><dt>Cena</dt><dd>${u.price != null ? kc(u.price) : 'na vyžádání'}</dd></div>
      </dl>
      <p>${esc(u.note || '')}</p>
      <a class="btn btn--ghost" href="#kontakt"><span>Mám zájem o ${esc(u.id)}</span></a>
    </article>`).join('');
  });
})();
