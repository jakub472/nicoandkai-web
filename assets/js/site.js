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

  /* ---------- interaktivní fasáda: reflektor na byt, kreslený obrys, štítek ---------- */
  const NS = 'http://www.w3.org/2000/svg';
  $$('[data-facade]').forEach((root) => {
    const P = (window.NK_PROJECTS || {})[root.dataset.facade];
    if (!P || !P.facade) return;
    const F = P.facade; const [W, H] = F.size; const uid = String(P.slug).replace(/[^a-z0-9]/gi, '');
    const unitById = Object.fromEntries(P.units.map((u) => [u.id, u]));
    const mk = (tag, attrs = {}, parent) => { const n = document.createElementNS(NS, tag); for (const k in attrs) n.setAttribute(k, attrs[k]); if (parent) parent.appendChild(n); return n; };
    const ptsAttr = (pts) => pts.map((p) => p.join(',')).join(' ');
    const bbox = (pts) => { const xs = pts.map((p) => p[0]), ys = pts.map((p) => p[1]); return { x0: Math.min(...xs), x1: Math.max(...xs), y0: Math.min(...ys), y1: Math.max(...ys) }; };

    const svg = mk('svg', { class: 'facade__svg', viewBox: `0 0 ${W} ${H}`, preserveAspectRatio: 'none' });
    const defs = mk('defs', {}, svg);
    const blur = mk('filter', { id: `fz-blur-${uid}`, x: '-10%', y: '-10%', width: '120%', height: '120%' }, defs);
    mk('feGaussianBlur', { stdDeviation: Math.round(W / 120) }, blur);
    const hatch = mk('pattern', { id: `fz-hatch-${uid}`, width: 22, height: 22, patternUnits: 'userSpaceOnUse', patternTransform: 'rotate(45)' }, defs);
    mk('line', { x1: 0, y1: 0, x2: 0, y2: 22, stroke: 'rgba(255,255,255,.4)', 'stroke-width': 5 }, hatch);
    const mask = mk('mask', { id: `fz-mask-${uid}`, maskUnits: 'userSpaceOnUse', x: 0, y: 0, width: W, height: H }, defs);
    mk('rect', { width: W, height: H, fill: '#fff' }, mask);
    const hole = mk('polygon', { points: '', fill: '#000', filter: `url(#fz-blur-${uid})` }, mask);
    mk('rect', { class: 'facade__dim', width: W, height: H, mask: `url(#fz-mask-${uid})` }, svg);
    const glow = mk('polygon', { class: 'facade__glow', points: '', filter: `url(#fz-blur-${uid})` }, svg);
    const zonesG = mk('g', { class: 'facade__zones' }, svg);
    const marksG = mk('g', { class: 'facade__marks' }, svg);
    const card = document.createElement('div'); card.className = 'facade__card'; card.setAttribute('aria-hidden', 'true');

    const zones = {};
    let active = null, selected = null;

    const setLit = (id) => {
      active = id;
      const z = id && zones[id];
      Object.values(zones).forEach((o) => { o.g.classList.toggle('is-on', o === z); o.m.classList.toggle('is-on', o === z); });
      if (!z) { root.classList.remove('is-lit'); card.classList.remove('is-on'); return; }
      hole.setAttribute('points', z.pts); glow.setAttribute('points', z.pts);
      root.classList.add('is-lit', 'has-hovered');
      const u = z.u;
      card.innerHTML = `<strong>Byt ${esc(id)}</strong><span>${esc(u.disposition)} · ${area(u.areaNV || u.area)}${u.terrace != null ? ` + ${area(u.terrace)} ${esc((u.outdoorLabel || 'terasa').toLowerCase())}` : ''}</span>${u.status === 'available' && u.price != null && CFG.priceMode !== 'onRequest' ? `<span>${kc(u.price)}</span>` : ''}<em class="st-${u.status}">${STATUS[u.status]}</em>${u.status !== 'sold' ? '<i>Kliknutím otevřete detail a půdorys</i>' : ''}`;
      const r = root.getBoundingClientRect();
      const cx = ((z.b.x0 + z.b.x1) / 2 / W) * r.width;
      const top = (z.b.y0 / H) * r.height;
      card.style.left = `${Math.max(130, Math.min(r.width - 130, cx))}px`;
      card.style.top = `${top}px`;
      card.classList.toggle('is-below', top < 190);
      card.classList.add('is-on');
    };

    Object.entries(F.zones).forEach(([id, pts], i) => {
      const u = unitById[id]; if (!u) return;
      const b = bbox(pts);
      const g = mk('g', { class: `facade__zone st-${u.status}`, 'data-unit': id }, zonesG);
      const hit = mk('polygon', { class: 'facade__hit', points: ptsAttr(pts), tabindex: 0, role: 'button', 'aria-label': `Byt ${id}, ${u.disposition}, ${area(u.areaNV || u.area)}, ${STATUS[u.status]}` }, g);
      if (u.status === 'reserved') hit.style.fill = `url(#fz-hatch-${uid})`;
      mk('polygon', { class: 'facade__line', points: ptsAttr(pts), pathLength: 1 }, g);
      // značka bytu (klidový stav)
      const mx = (b.x0 + b.x1) / 2, my = (b.y0 + b.y1) / 2;      // pozice přes cx/cy – CSS animace používá transform
      const m = mk('g', { class: `facade__mark st-${u.status}` }, marksG);
      m.style.animationDelay = `${(i * 0.45) % 3.2}s`;
      mk('circle', { r: Math.round(W / 92), cx: mx, cy: my }, m);
      const t = mk('text', { x: mx, y: my, 'font-size': Math.round(W / 95) }, m); t.textContent = id;
      zones[id] = { g, m, u, b, pts: ptsAttr(pts) };

      const restore = () => setLit(selected);
      hit.addEventListener('mouseenter', () => setLit(id)); hit.addEventListener('focus', () => setLit(id));
      hit.addEventListener('mouseleave', restore); hit.addEventListener('blur', restore);
      const go = () => {
        if (u.status === 'sold') return;
        selected = id; setLit(id); root.classList.add('is-selected');
        if (window.NK_EXPLORER && window.NK_EXPLORER.project === P.slug) window.NK_EXPLORER.selectUnit(id, true);
        else { const tgt = $('#byty'); if (tgt) tgt.scrollIntoView({ behavior: 'smooth' }); }
      };
      hit.addEventListener('click', go);
      hit.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); } });
    });

    root.appendChild(svg); root.appendChild(card);
    document.addEventListener('nk:unit', (e) => {
      selected = e.detail.unit && zones[e.detail.unit] ? e.detail.unit : null;
      root.classList.toggle('is-selected', !!selected);
      setLit(selected);
    });
    addEventListener('resize', () => { if (active) setLit(active); }, { passive: true });
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
