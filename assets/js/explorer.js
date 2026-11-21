/* Výběr bytů po patrech – axonometrický „rozpad“ domu + schematický půdorys + detail bytu.
   Data: window.NK_PROJECTS[slug] (assets/data/*.js). Nastavení cen: window.NK_CONFIG.priceMode. */
(() => {
  'use strict';

  const root = document.querySelector('[data-explorer]');
  if (!root) return;
  const P = (window.NK_PROJECTS || {})[root.dataset.explorer];
  if (!P) { console.warn('[explorer] chybí data projektu', root.dataset.explorer); return; }

  const CFG = window.NK_CONFIG || {};
  const priceMode = CFG.priceMode || 'public';           // 'public' | 'total' | 'onRequest'
  const imgBase = root.dataset.imgBase || '';
  const NS = 'http://www.w3.org/2000/svg';

  const $ = (s, r = root) => r.querySelector(s);
  const $$ = (s, r = root) => [...r.querySelectorAll(s)];
  const nf = new Intl.NumberFormat('cs-CZ');
  const nfa = new Intl.NumberFormat('cs-CZ', { minimumFractionDigits: 1, maximumFractionDigits: 2 });
  const area = (v) => `${nfa.format(v)} m²`;
  const STATUS = { available: 'Volný', reserved: 'Rezervovaný', sold: 'Prodaný' };

  const el = (tag, attrs = {}, parent) => {
    const n = document.createElementNS(NS, tag);
    for (const k in attrs) n.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(n);
    return n;
  };
  const html = (strings, ...v) => strings.reduce((a, s, i) => a + s + (v[i] ?? ''), '');
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  const unitById = Object.fromEntries(P.units.map((u) => [u.id, u]));
  const floorById = Object.fromEntries(P.floors.map((f) => [f.id, f]));
  const state = { floor: P.floors[0].id, unit: null };

  /* ---------- ceny ---------- */
  function priceInfo(u) {
    if (u.status !== 'available') return { main: STATUS[u.status], sub: '' };
    if (u.price == null || priceMode === 'onRequest') return { main: 'Cena na vyžádání', sub: '' };
    const sub = priceMode === 'public' ? `${nf.format(Math.round(u.price / u.area))} Kč/m²` : '';
    return { main: `${nf.format(u.price)} Kč`, sub };
  }

  /* ---------- axonometrie ---------- */
  const S = 6.2, C = Math.cos(Math.PI / 6);
  const iso = (x, y, z) => [(x - y) * C * S, (x + y) * 0.5 * S - z * S];
  const pt = (arr) => arr.map(([x, y, z]) => iso(x, y, z).map((n) => n.toFixed(1)).join(' ')).join('L');

  function isoBox(parent, r, z, h, cls, data = {}) {
    const x1 = r.x + r.w, y1 = r.y + r.d, zt = z + h;
    const g = el('g', { class: cls }, parent);
    for (const k in data) g.setAttribute(k, data[k]);
    el('path', { class: 'f-l', d: 'M' + pt([[r.x, y1, z], [x1, y1, z], [x1, y1, zt], [r.x, y1, zt]]) + 'Z' }, g);
    el('path', { class: 'f-r', d: 'M' + pt([[x1, r.y, z], [x1, y1, z], [x1, y1, zt], [x1, r.y, zt]]) + 'Z' }, g);
    el('path', { class: 'f-t', d: 'M' + pt([[r.x, r.y, zt], [x1, r.y, zt], [x1, y1, zt], [r.x, y1, zt]]) + 'Z' }, g);
    return g;
  }
  const centerKey = (r) => r.x + r.w / 2 + r.y + r.d / 2;

  function buildStack() {
    const svg = $('#ex-stack');
    svg.innerHTML = '';
    const defs = el('defs', {}, svg);
    const pat = el('pattern', { id: 'hatch-s', width: 5, height: 5, patternUnits: 'userSpaceOnUse', patternTransform: 'rotate(45)' }, defs);
    el('line', { x1: 0, y1: 0, x2: 0, y2: 5, stroke: 'currentColor', 'stroke-width': 1.1 }, pat);

    const world = el('g', { class: 'world' }, svg);
    let bb = { x0: 1e9, y0: 1e9, x1: -1e9, y1: -1e9 };
    const track = (r, z, h) => {
      for (const [x, y, zz] of [[r.x, r.y, z], [r.x + r.w, r.y, z], [r.x, r.y + r.d, z + h], [r.x + r.w, r.y + r.d, z], [r.x + r.w, r.y + r.d, z + h], [r.x, r.y, z + h]]) {
        const [a, b] = iso(x, y, zz);
        bb = { x0: Math.min(bb.x0, a), y0: Math.min(bb.y0, b), x1: Math.max(bb.x1, a), y1: Math.max(bb.y1, b) };
      }
    };

    [...P.floors].reverse().forEach((f) => {          // 1.PP první → 3.NP naposled (vykresluje se nad ním)
      const geo = P.geometry[f.id];
      const fg = el('g', { class: 'sf', 'data-floor': f.id, tabindex: 0, role: 'button', 'aria-label': `Zobrazit ${f.long}` }, world);
      const items = [];
      if (f.type === 'basement') {
        const o = geo.outline;
        items.push({ r: geo.garage || { x: o[0], y: o[1], w: o[2] - o[0], d: o[3] - o[1] }, h: 1.0, cls: 'sb-garage' });
      } else {
        geo.common.forEach((c) => items.push({ r: c, h: 1.0, cls: 'sb-common' }));
        Object.entries(geo.units).forEach(([id, g]) => {
          g.terraces.forEach((t) => items.push({ r: t, h: 0.35, cls: 'sb-terrace', unit: id }));
          items.push({ r: g.body, h: 1.6, cls: `su st-${unitById[id].status}`, unit: id, body: true });
        });
      }
      items.sort((a, b) => centerKey(a.r) - centerKey(b.r));
      items.forEach((it) => {
        const data = it.unit && it.body ? { 'data-unit': it.unit } : {};
        isoBox(fg, it.r, f.z, it.h, it.cls, data);
        track(it.r, f.z, it.h);
        if (it.body) {
          const [cx, cy] = iso(it.r.x + it.r.w / 2, it.r.y + it.r.d / 2, f.z + it.h);
          const t = el('text', { class: 'su-label', x: cx.toFixed(1), y: (cy + 3).toFixed(1), 'text-anchor': 'middle' }, fg);
          t.textContent = it.unit;
        }
      });
      // popisek patra vpravo od desky
      const o = geo.outline;
      const [lx, ly] = iso(o[0] + o[2], o[1] + o[3] * 0.5, f.z);
      const lab = el('text', { class: 'sf-label', x: (lx + 14).toFixed(1), y: (ly + 4).toFixed(1) }, fg);
      lab.textContent = f.label;
      bb.x1 = Math.max(bb.x1, lx + 60);
    });

    const pad = 14;
    svg.setAttribute('viewBox', `${(bb.x0 - pad).toFixed(0)} ${(bb.y0 - pad).toFixed(0)} ${(bb.x1 - bb.x0 + pad * 2).toFixed(0)} ${(bb.y1 - bb.y0 + pad * 2).toFixed(0)}`);
  }

  /* ---------- půdorys: skutečný obrázek se zónami bytů ---------- */
  const zoneBox = (pts, pad = 70) => {
    const xs = pts.map((p) => p[0]), ys = pts.map((p) => p[1]);
    const x0 = Math.min(...xs) - pad, y0 = Math.min(...ys) - pad;
    return { x: x0, y: y0, w: Math.max(...xs) + pad - x0, h: Math.max(...ys) + pad - y0 };
  };
  const ptsAttr = (pts) => pts.map((p) => p.join(',')).join(' ');

  function buildImagePlan(svg, f, pl) {
    const [W, H] = pl.size;
    svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
    svg.setAttribute('aria-label', `Půdorys – ${f.long}`);
    svg.classList.add('is-image');
    const defs = el('defs', {}, svg);
    const pat = el('pattern', { id: 'hatch-i', width: 22, height: 22, patternUnits: 'userSpaceOnUse', patternTransform: 'rotate(45)' }, defs);
    el('line', { x1: 0, y1: 0, x2: 0, y2: 22, stroke: '#000', 'stroke-width': 3.5 }, pat);
    el('image', { href: imgBase + pl.image, x: 0, y: 0, width: W, height: H, class: 'p-image' }, svg);
    Object.entries(pl.zones || {}).forEach(([id, pts]) => {
      const u = unitById[id];
      if (!u) return;
      const grp = el('g', {
        class: `pu pz st-${u.status}` + (state.unit === id ? ' is-selected' : ''),
        'data-unit': id, tabindex: 0, role: 'button', 'aria-pressed': state.unit === id,
        'aria-label': `Byt ${id}, ${u.disposition}, ${area(u.areaNV || u.area)}, ${STATUS[u.status]}`,
      }, svg);
      el('polygon', { class: 'pz-shape', points: ptsAttr(pts) }, grp);
      el('polygon', { class: 'pz-hatch', points: ptsAttr(pts) }, grp);
      const [ax, ay] = pl.anchors[id];
      const b = el('g', { class: 'pz-badge', transform: `translate(${ax} ${ay})` }, grp);
      el('rect', { x: -150, y: -56, width: 300, height: 112 }, b);
      const idt = el('text', { class: 'pz-id', x: -98, y: 24, 'text-anchor': 'middle' }, b); idt.textContent = id;
      el('line', { x1: -50, y1: -34, x2: -50, y2: 34 }, b);
      const t1 = el('text', { class: 'pz-t1', x: -32, y: -4 }, b); t1.textContent = u.disposition;
      const t2 = el('text', { class: 'pz-t2', x: -32, y: 30 }, b); t2.textContent = area(u.areaNV || u.area);
    });
  }

  /* ---------- půdorys (schéma) ---------- */
  function buildPlan() {
    const svg = $('#ex-plan');
    svg.innerHTML = '';
    svg.classList.remove('is-image');
    const f = floorById[state.floor];
    const pl = P.plans && P.plans[f.id];
    const note = $('#ex-note');
    if (pl) {
      if (note) note.textContent = P.planNote || 'Půdorys z projektové dokumentace.';
      return buildImagePlan(svg, f, pl);
    }
    if (note && !note.dataset.def) note.dataset.def = note.textContent;
    if (note) note.textContent = note.dataset.def;
    const geo = P.geometry[f.id];
    const o = geo.outline, pad = 1.6;
    svg.setAttribute('viewBox', `${o[0] - pad} ${o[1] - pad} ${o[2] - o[0] + pad * 2} ${o[3] - o[1] + pad * 2}`);
    svg.setAttribute('aria-label', `Schématický půdorys – ${f.long}`);
    svg.style.setProperty('--k', ((o[2] - o[0] + 2 * pad) / 32).toFixed(3));   // stálá velikost písma na obrazovce

    const defs = el('defs', {}, svg);
    const pat = el('pattern', { id: 'hatch-p', width: 0.7, height: 0.7, patternUnits: 'userSpaceOnUse', patternTransform: 'rotate(45)' }, defs);
    el('line', { x1: 0, y1: 0, x2: 0, y2: 0.7, stroke: 'currentColor', 'stroke-width': 0.09 }, pat);

    const label = (parent, x, y, text, cls, anchor = 'middle') => {
      const lines = String(text).split(' · ');
      const t = el('text', { x, y: lines.length > 1 ? y - 0.45 : y, class: cls, 'text-anchor': anchor }, parent);
      lines.forEach((ln, i) => { const ts = el('tspan', { x, dy: i ? 1.0 : 0 }, t); ts.textContent = ln; });
      return t;
    };

    if (f.type === 'basement') {
      const gr = geo.garage || { x: o[0], y: o[1], w: o[2] - o[0], d: o[3] - o[1] };
      el('rect', { class: 'p-garage', x: gr.x, y: gr.y, width: gr.w, height: gr.d }, svg);
      (geo.common || []).forEach((c) => {
        el('rect', { class: 'p-common', x: c.x, y: c.y, width: c.w, height: c.d }, svg);
        label(svg, c.x + c.w / 2, c.y + c.d / 2 + 0.3, c.label, 'p-small');
      });
      (geo.cellars || []).forEach((c, i) => {
        const g = el('g', { class: 'p-cellar' }, svg);
        el('title', {}, g).textContent = `Sklep ${i + 1} · ${area(P.cellars[i].area)}`;
        el('rect', { x: c.x, y: c.y, width: c.w, height: c.d }, g);
        label(g, c.x + c.w / 2, c.y + c.d / 2 + 0.45, `S${i + 1}`, 'p-num');
      });
      (geo.stalls || []).forEach((s, i) => {
        const g = el('g', { class: 'p-stall' + (P.parking[i].accessible ? ' is-accessible' : '') }, svg);
        el('title', {}, g).textContent = `Stání ${i + 1}${P.parking[i].accessible ? ' (pro osoby s omezenou schopností pohybu)' : ''}`;
        el('rect', { x: s.x, y: s.y, width: s.w, height: s.d }, g);
        label(g, s.x + s.w / 2, s.y + s.d - 0.9, String(i + 1), 'p-num');
      });
      if (geo.lane) label(svg, geo.lane[0], geo.lane[1], 'jízdní pás', 'p-small p-muted');
      return;
    }

    geo.common.forEach((c) => {
      el('rect', { class: 'p-common', x: c.x, y: c.y, width: c.w, height: c.d }, svg);
      label(svg, c.x + c.w / 2, c.y + c.d / 2 + 0.3, c.label, 'p-small');
    });

    Object.entries(geo.units).forEach(([id, g]) => {
      const u = unitById[id];
      const grp = el('g', {
        class: `pu st-${u.status}` + (state.unit === id ? ' is-selected' : ''),
        'data-unit': id, tabindex: 0, role: 'button', 'aria-pressed': state.unit === id,
        'aria-label': `Byt ${id}, ${u.disposition}, ${area(u.areaNV || u.area)}, ${STATUS[u.status]}`,
      }, svg);
      g.terraces.forEach((t) => el('rect', { class: 'p-terrace', x: t.x, y: t.y, width: t.w, height: t.d }, grp));
      const b = g.body;
      el('rect', { class: 'p-body', x: b.x, y: b.y, width: b.w, height: b.d }, grp);
      el('rect', { class: 'p-hatch', x: b.x, y: b.y, width: b.w, height: b.d }, grp);
      const cx = b.x + b.w / 2, cy = b.y + b.d / 2;
      label(grp, cx, cy - 0.2, id, 'p-id');
      label(grp, cx, cy + 1.5, `${u.disposition} · ${area(u.area)}`, 'p-meta');
      const t0 = g.terraces[0];
      if (t0) label(grp, t0.x + t0.w / 2, t0.y + t0.d / 2 + 0.3, u.terrace != null ? `terasa · ${area(u.terrace)}` : (u.outdoor || 'terasa'), 'p-small p-terlabel');
    });
  }

  /* ---------- patra (tlačítka) ---------- */
  function buildFloors() {
    const ul = $('#ex-floors');
    ul.innerHTML = '';
    P.floors.forEach((f) => {
      let meta;
      if (f.type === 'basement') meta = f.meta;
      else {
        const us = P.units.filter((u) => u.floor === f.id);
        const free = us.filter((u) => u.status === 'available').length;
        meta = `${us.length} ${us.length === 1 ? 'byt' : us.length < 5 ? 'byty' : 'bytů'} · ${free} volné`;
      }
      const li = document.createElement('li');
      li.innerHTML = html`<button type="button" role="tab" data-floor="${f.id}" aria-selected="false"><strong>${f.label}</strong><small>${meta}</small></button>`;
      ul.appendChild(li);
    });
  }

  /* ---------- detail ---------- */
  function renderDetail() {
    const d = $('#ex-detail');
    const f = floorById[state.floor];

    if (f.type === 'basement') {
      d.innerHTML = html`
        <div class="detail__head"><h3>${f.title}</h3><span class="badge">${f.label}</span></div>
        <dl class="stats">${f.stats.map(([k, v]) => `<div><dt>${esc(k)}</dt><dd>${esc(v)}</dd></div>`).join('')}</dl>
        <p class="detail__text">${f.text}</p>
        ${f.priceNote ? `<p class="detail__price"><strong>${esc(f.priceNote[0])}</strong><span>${esc(f.priceNote[1])}</span></p>` : ''}
        ${f.cta ? `<div class="detail__actions"><button class="btn" type="button" data-reserve-extra>${esc(f.cta)} <i class="arrow" aria-hidden="true">→</i></button></div>` : ''}`;
      return;
    }

    const u = state.unit && unitById[state.unit];
    if (!u) {
      const us = P.units.filter((x) => x.floor === f.id);
      d.innerHTML = html`
        <div class="detail__head"><h3>${f.long}</h3></div>
        <p class="detail__text">Vyberte byt v&nbsp;půdorysu nebo v&nbsp;přehledu níže.</p>
        <ul class="detail__list">${us.map((x) => `<li><button type="button" data-unit="${x.id}"><strong>Byt ${x.id}</strong><span>${x.disposition} · ${area(x.areaNV || x.area)}</span><em class="tag tag--${x.status}">${STATUS[x.status]}</em></button></li>`).join('')}</ul>`;
      return;
    }

    const pr = priceInfo(u);
    const canReserve = u.status === 'available';
    const pl = P.plans && P.plans[u.floor];
    const zone = pl && pl.zones && pl.zones[u.id];
    let figure = '';
    if (zone) {
      const b = zoneBox(zone);
      const dim = `M${b.x} ${b.y}h${b.w}v${b.h}h${-b.w}Z M${zone.map((p) => p.join(' ')).join(' L')}Z`;
      figure = html`<figure class="unitplan">
        <svg viewBox="${b.x} ${b.y} ${b.w} ${b.h}" role="img" aria-label="Půdorys bytu ${u.id}">
          <image href="${imgBase + pl.image}" x="0" y="0" width="${pl.size[0]}" height="${pl.size[1]}"/>
          <path class="unitplan__dim" fill-rule="evenodd" d="${dim}"/>
          <polygon class="unitplan__line" points="${ptsAttr(zone)}"/>
        </svg>
        <figcaption>Půdorys bytu ${u.id}</figcaption>
      </figure>`;
    }
    const outdoorLabel = u.terrace != null ? (u.outdoorLabel || 'Terasa') : 'Venkovní prostor';
    const outdoorVal = u.terrace != null ? area(u.terrace) : esc(u.outdoor || '–');
    d.innerHTML = html`
      <div class="detail__head"><h3>Byt ${u.id}</h3><span class="tag tag--${u.status}">${STATUS[u.status]}</span></div>
      <div class="detail__body${figure ? ' has-plan' : ''}">
        <div class="detail__info">
          <dl class="stats">
            <div><dt>Dispozice</dt><dd>${u.disposition}</dd></div>
            <div><dt>Podlaží</dt><dd>${floorById[u.floor].label}</dd></div>
            <div><dt>${u.areaNV ? 'Plocha dle NV 366/2013' : 'Součet místností'}</dt><dd>${area(u.areaNV || u.area)}</dd></div>
            <div><dt>${outdoorLabel}</dt><dd>${outdoorVal}</dd></div>
          </dl>
          ${u.total != null ? `<p class="detail__total"><span>Celkem včetně venkovního prostoru</span><strong>${area(u.total)}</strong></p>` : ''}
          <p class="detail__price"><strong>${pr.main}</strong>${pr.sub ? `<span>${pr.sub}</span>` : (canReserve && pr.main === 'Cena na vyžádání' ? `<span><button class="link" type="button" data-reserve="${u.id}">Vyžádat ceník</button></span>` : '')}</p>
          ${P.reservation && canReserve && u.price != null && priceMode !== 'onRequest' ? (() => { const [dep, disc] = P.reservation.tiers[P.reservation.tiers.length - 1]; return `<p class="detail__text detail__res">Při rezervaci se zálohou ${nf.format(dep / 1e6)} mil. Kč v&nbsp;průběhu stavebního řízení: sleva ${nf.format(disc * 100)} %, cena <strong>${nf.format(Math.round(u.price * (1 - disc) / 1000) * 1000)} Kč</strong>. <a href="#rezervace">Podmínky rezervace</a></p>`; })() : ''}
          <p class="detail__text">${u.terraceNote ? u.terraceNote[0].toUpperCase() + u.terraceNote.slice(1) + '. ' : ''}${P.accessoriesNote || ''}</p>
          <details class="rooms" open><summary>Místnosti</summary>
            <table><tbody>${u.rooms.map(([n, a]) => `<tr><th scope="row">${esc(n)}</th><td>${area(a)}</td></tr>`).join('')}</tbody><tfoot><tr><th scope="row">Součet místností</th><td>${area(Math.round(u.rooms.reduce((t, r) => t + r[1], 0) * 100) / 100)}</td></tr></tfoot></table>
          </details>
          <div class="detail__actions">
            ${canReserve
              ? html`<button class="btn" type="button" data-reserve="${u.id}">${priceMode === 'onRequest' ? 'Mám zájem o byt' : ((P.cta && P.cta.unit) || 'Rezervovat byt')} ${u.id} <i class="arrow" aria-hidden="true">→</i></button>`
              : html`<p class="detail__text">Tento byt už není k&nbsp;dispozici. Napište nám a dáme vám vědět o&nbsp;podobných bytech.</p><a class="btn btn--ghost" href="#rezervace" data-reserve="">Napsat nám</a>`}
            <button class="btn btn--ghost" type="button" data-cad>Celé podlaží</button>
          </div>
        </div>
        ${figure}
      </div>`;
  }

  /* ---------- tabulka ---------- */
  function buildTable() {
    const tb = $('#ex-table tbody');
    tb.innerHTML = '';
    const hasTer = P.units.some((u) => u.terrace != null);
    const ths = $$('#ex-table thead th');
    const hasNV = P.units.some((u) => u.areaNV);
    ths[3].textContent = hasNV ? 'Plocha (NV 366/2013)' : 'Součet místností';
    ths[4].textContent = hasTer ? (P.outdoorHeader || 'Terasa') : 'Venkovní prostor';
    ths[5].hidden = !hasTer;
    const showPrice = priceMode !== 'onRequest' && P.units.some((u) => u.price != null);
    ths[6].hidden = !showPrice;
    [...P.units].sort((a, b) => P.floors.indexOf(floorById[b.floor]) - P.floors.indexOf(floorById[a.floor]) || a.id.localeCompare(b.id)).forEach((u) => {
      const pr = priceInfo(u);
      const tr = document.createElement('tr');
      tr.dataset.unit = u.id;
      tr.className = `st-${u.status}`;
      tr.innerHTML = html`
        <th scope="row">${u.id}</th>
        <td>${floorById[u.floor].label}</td>
        <td>${u.disposition}</td>
        <td>${area(u.areaNV || u.area)}</td>
        <td>${hasTer ? (u.terrace != null ? area(u.terrace) : '–') : esc(u.outdoor || '–')}</td>
        ${hasTer ? `<td>${u.total != null ? area(u.total) : '–'}</td>` : ''}
        ${showPrice ? `<td>${u.status === 'available' ? pr.main : '–'}</td>` : ''}
        <td><span class="tag tag--${u.status}">${STATUS[u.status]}</span></td>
        <td><button type="button" class="link" data-unit="${u.id}" aria-label="Zobrazit byt ${u.id}">Detail →</button></td>`;
      tb.appendChild(tr);
    });
  }

  /* ---------- výběr ---------- */
  function render() {
    buildPlan();
    renderDetail();
    $$('#ex-floors button').forEach((b) => b.setAttribute('aria-selected', String(b.dataset.floor === state.floor)));
    $$('.sf', $('#ex-stack')).forEach((g) => g.classList.toggle('is-active', g.dataset.floor === state.floor));
    $('#ex-stack').classList.add('has-active');
    $$('.su', $('#ex-stack')).forEach((g) => g.classList.toggle('is-selected', g.dataset.unit === state.unit));
    $$('#ex-table tbody tr').forEach((tr) => tr.classList.toggle('is-selected', tr.dataset.unit === state.unit));
    $('#ex-floor-title').textContent = floorById[state.floor].long;
    $('#ex-cad').hidden = !P.planImages[state.floor];
    document.dispatchEvent(new CustomEvent('nk:unit', { detail: { unit: state.unit, floor: state.floor } }));
  }

  function selectFloor(id) {
    state.floor = id;
    if (state.unit && unitById[state.unit].floor !== id) state.unit = null;
    render();
  }
  function selectUnit(id, scroll) {
    const u = unitById[id];
    if (!u) return;
    state.unit = id; state.floor = u.floor;
    render();
    try { history.replaceState(null, '', `#byt-${id}`); } catch (e) { /* file:// */ }
    if (scroll) $('.ex__plan').scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  /* ---------- rezervační formulář ---------- */
  function fillReservationForm() {
    const sel = document.querySelector('#rezervace select[name="unit"]');
    if (!sel) return;
    sel.innerHTML = '<option value="">Zatím nevím / obecný dotaz</option>' +
      P.units.filter((u) => u.status === 'available').map((u) => `<option value="${u.id}">Byt ${u.id} · ${u.disposition} · ${area(u.areaNV || u.area)}</option>`).join('');
  }
  function goReserve(unitId, extra) {
    const sec = document.querySelector('#rezervace');
    if (!sec) return;
    const sel = sec.querySelector('select[name="unit"]');
    if (sel && unitId) sel.value = unitId;
    if (extra) sec.querySelectorAll('input[name="parking"], input[name="cellar"]').forEach((i) => { i.checked = true; });
    sec.scrollIntoView({ behavior: 'smooth', block: 'start' });
    setTimeout(() => { const first = sec.querySelector('input[name="name"]'); if (first) first.focus({ preventScroll: true }); }, 600);
  }

  /* ---------- půdorys z projektu (lightbox) ---------- */
  const dlg = $('#ex-dialog');
  function openCad() {
    const file = P.planImages[state.floor];
    if (!file || !dlg) return;
    $('img', dlg).src = imgBase + file;
    $('img', dlg).alt = `Půdorys ${floorById[state.floor].long} z projektové dokumentace`;
    $('.dialog__title', dlg).textContent = floorById[state.floor].long;
    dlg.showModal();
  }

  /* ---------- události ---------- */
  root.addEventListener('click', (e) => {
    const t = e.target;
    const floorBtn = t.closest('#ex-floors button[data-floor]');
    if (floorBtn) return selectFloor(floorBtn.dataset.floor);
    const sf = t.closest('.sf');
    if (sf && $('#ex-stack').contains(sf)) {
      const su = t.closest('.su');
      return su ? selectUnit(su.dataset.unit) : selectFloor(sf.dataset.floor);
    }
    const pu = t.closest('.pu');
    if (pu) return selectUnit(pu.dataset.unit);
    const tableBtn = t.closest('#ex-table [data-unit], #ex-detail [data-unit]');
    if (tableBtn) return selectUnit(tableBtn.dataset.unit, !!t.closest('#ex-table'));
    const res = t.closest('[data-reserve]');
    if (res) { e.preventDefault(); return goReserve(res.dataset.reserve); }
    if (t.closest('[data-reserve-extra]')) return goReserve('', true);
    if (t.closest('[data-cad]') || t.closest('#ex-cad')) return openCad();
    if (t.closest('[data-dialog-close]')) return dlg.close();
    if (t === dlg) return dlg.close();
  });
  root.addEventListener('keydown', (e) => {
    if (e.key !== 'Enter' && e.key !== ' ') return;
    const g = e.target.closest && e.target.closest('.pu, .sf');
    if (!g) return;
    e.preventDefault();
    if (g.dataset.unit) selectUnit(g.dataset.unit); else selectFloor(g.dataset.floor);
  });

  /* ---------- poznámka k plochám ---------- */
  const areaNote = $('#ex-areanote');
  if (areaNote) {
    areaNote.textContent = P.units.some((u) => u.areaNV)
      ? 'Plocha bytu je podlahová plocha podle nařízení vlády č. 366/2013 Sb. (včetně příček), orientační odhad z půdorysů. Závazná plocha bude v prohlášení vlastníka. Součet místností je v detailu bytu. Sklepy nejsou součástí plochy bytu.'
      : 'Plochy jsou součtem místností podle projektové dokumentace. Podlahová plocha podle nařízení vlády č. 366/2013 Sb. (včetně příček a konstrukcí uvnitř bytu) bude o několik procent větší. Doplníme ji po výpočtu architekta.';
  }

  window.NK_EXPLORER = { project: P.slug, selectUnit, selectFloor, state };

  /* ---------- start ---------- */
  buildStack();
  buildFloors();
  buildTable();
  fillReservationForm();
  const m = location.hash.match(/^#byt-(\w+)$/);
  if (m && unitById[m[1]]) { state.unit = m[1]; state.floor = unitById[m[1]].floor; }
  render();
})();
