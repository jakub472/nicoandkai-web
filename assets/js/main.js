(() => {
  'use strict';

  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const cfg = window.NK_CONFIG || { company: {} };
  const tr = (k) => { const key = String(k).replace(/\u00a0/g, ' '); return (window.NK_DICT && Object.prototype.hasOwnProperty.call(window.NK_DICT, key)) ? window.NK_DICT[key] : k; };
  const tpl = (k, vars) => tr(k).replace(/\{(\w+)\}/g, (m, v) => (v in vars ? vars[v] : m));
  const LOC = window.NK_LOCALE || 'cs-CZ';
  const getCfg = (path) => path.split('.').reduce((o, k) => (o ? o[k] : undefined), cfg);

  /* ---------- config → DOM (prázdné hodnoty se skryjí) ---------- */
  $$('[data-cfg]').forEach((el) => {
    const v = String(getCfg(el.dataset.cfg) || '').trim();
    const wrap = el.closest('[data-cfg-wrap]');
    if (!v) { if (wrap) wrap.hidden = true; return; }
    el.textContent = v;
    if (el.dataset.cfgHref) el.href = el.dataset.cfgHref + v.replace(/\s+/g, '');
  });
  $$('[data-cfg-group]').forEach((g) => { if (!$$('li:not([hidden])', g).length) g.hidden = true; });
  $$('[data-year]').forEach((el) => { el.textContent = new Date().getFullYear(); });

  /* ---------- česká typografie: jednopísmenné předložky nezůstanou na konci řádku ---------- */
  if (document.documentElement.lang === 'cs') {
    const nbspRe = /(^|[\s(„])([ksvzouaiKSVZOUAI])\s+(?=\S)/g;
    const walker = document.createTreeWalker($('main'), NodeFilter.SHOW_TEXT, {
      acceptNode: (n) => (n.parentElement.closest('script,style,textarea,option') ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT),
    });
    for (let n = walker.nextNode(); n; n = walker.nextNode()) {
      const t = n.nodeValue.replace(nbspRe, '$1$2 ').replace(nbspRe, '$1$2 ');
      if (t !== n.nodeValue) n.nodeValue = t;
    }
  }

  /* ---------- hlavička: schovat při scrollu dolů, progress, aktivní odkaz ---------- */
  const header = $('#header');
  const progress = $('.progress');
  const menu = $('#menu');
  const menuBtn = $('.menu-btn');
  const darkSections = $$('section.dark, footer.dark');
  let lastY = scrollY, ticking = false;

  const onScroll = () => {
    const y = scrollY;
    const max = document.documentElement.scrollHeight - innerHeight;
    progress.style.setProperty('--p', max > 0 ? Math.min(1, y / max).toFixed(4) : 0);
    const menuOpen = menuBtn.getAttribute('aria-expanded') === 'true';
    if (!menuOpen) header.classList.toggle('is-hidden', y > 240 && y > lastY + 4);
    if (y < lastY - 4) header.classList.remove('is-hidden');
    header.classList.toggle('is-top', y < 40);
    lastY = y;

    // hlavička přebarví na tmavou, když je nad tmavou sekcí
    const probe = header.offsetHeight / 2;
    const overDark = darkSections.some((s) => { const r = s.getBoundingClientRect(); return r.top <= probe && r.bottom >= probe; });
    header.classList.toggle('dark', overDark && !menuOpen);

    if (!reduce) {
      $$('[data-parallax]').forEach((el) => {
        const r = el.parentElement.getBoundingClientRect();
        if (r.bottom < -200 || r.top > innerHeight + 200) return;
        el.style.transform = `translate3d(0, ${(y * parseFloat(el.dataset.parallax)).toFixed(1)}px, 0)`;
      });
    }
    ticking = false;
  };
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();

  const navLinks = $$('[data-nav]');
  const sectionIO = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      navLinks.forEach((a) => a.classList.toggle('is-active', a.dataset.nav === e.target.id));
    });
  }, { rootMargin: '-45% 0px -50% 0px' });
  navLinks.forEach((a) => { const s = document.getElementById(a.dataset.nav); if (s) sectionIO.observe(s); });

  /* ---------- mobilní menu ---------- */
  const setMenu = (open) => {
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.querySelector('.menu-btn__label').textContent = open ? tr('Zavřít') : tr('Menu');
    menu.hidden = !open;
    document.body.style.overflow = open ? 'hidden' : '';
    header.classList.remove('is-hidden');
    if (open) { header.classList.remove('dark'); $('a', menu).focus({ preventScroll: true }); } else onScroll();
  };
  menuBtn.addEventListener('click', () => setMenu(menuBtn.getAttribute('aria-expanded') !== 'true'));
  $$('a', menu).forEach((a) => a.addEventListener('click', () => setMenu(false)));
  addEventListener('keydown', (e) => { if (e.key === 'Escape' && !menu.hidden) { setMenu(false); menuBtn.focus(); } });
  matchMedia('(min-width: 881px)').addEventListener('change', (m) => { if (m.matches && !menu.hidden) setMenu(false); });

  /* ---------- odhalování obsahu ---------- */
  const revealIO = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      e.target.classList.add('is-in');
      revealIO.unobserve(e.target);
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
  const hero = $('.hero, .hero-media') || document.body;
  $$('[data-reveal], .mask__in[data-in]').forEach((el) => { if (!hero.contains(el)) revealIO.observe(el); });

  /* ---------- kresba: nakreslí se po načtení / při příchodu do záběru ---------- */
  const drawings = $$('.drawing');
  if (!reduce) drawings.forEach((d) => d.classList.add('is-armed'));
  const drawIO = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      e.target.classList.add('is-drawn');
      drawIO.unobserve(e.target);
    });
  }, { threshold: 0.25 });
  drawings.forEach((d) => drawIO.observe(d));

  const start = () => requestAnimationFrame(() => hero.classList.add('is-ready'));
  (document.fonts && document.fonts.ready ? Promise.race([document.fonts.ready, new Promise((r) => setTimeout(r, 900))]) : Promise.resolve()).then(start);

  /* ---------- formuláře (kontakt, rezervace) ---------- */
  const emailOk = (v) => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);

  function initLeadForm(form) {
    const status = $('.form__status', form);
    const btn = $('button[type="submit"]', form);
    const project = form.dataset.project || 'Nico & Kai Development';

    const setError = (el, on, msg) => {
      const host = el.closest('.field') || el.closest('.check');
      host.classList.toggle('is-invalid', on);
      if (host.classList.contains('field')) { if (on) host.dataset.error = msg; else delete host.dataset.error; }
      el.setAttribute('aria-invalid', on ? 'true' : 'false');
    };
    const validate = () => {
      const { name, email, consent } = form.elements;
      const bad = [];
      const nOk = !!name.value.trim();
      setError(name, !nOk, tr('Napište prosím své jméno.')); if (!nOk) bad.push(name);
      const eOk = emailOk(email.value.trim());
      setError(email, !eOk, tr('Zadejte prosím platný e-mail.')); if (!eOk) bad.push(email);
      setError(consent, !consent.checked, ''); if (!consent.checked) bad.push(consent);
      return bad;
    };
    form.addEventListener('input', (e) => { if (e.target.getAttribute('aria-invalid') === 'true') validate(); });

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      status.textContent = '';
      const bad = validate();
      if (bad.length) {
        bad[0].focus();
        status.textContent = bad[0] === form.elements.consent ? tr('Pro odeslání potvrďte prosím souhlas.') : '';
        return;
      }
      if (form.elements.website.value) return; // honeypot

      const fd = new FormData(form);
      const data = Object.fromEntries(fd);
      delete data.website;
      data.project = project;
      if ('parking' in form.elements) data.parking = form.elements.parking.checked;
      if ('cellar' in form.elements) data.cellar = form.elements.cellar.checked;

      if (cfg.formEndpoint) {
        btn.disabled = true;
        try {
          const res = await fetch(cfg.formEndpoint, {
            method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(data),
          });
          if (!res.ok) throw new Error(String(res.status));
          form.reset();
          $$('.is-invalid', form).forEach((n) => n.classList.remove('is-invalid'));
          status.textContent = tr('Děkujeme, vaše žádost byla odeslána. Brzy se vám ozveme.');
        } catch {
          status.textContent = tr('Odeslání se nezdařilo. Zkuste to prosím znovu.');
        } finally {
          btn.disabled = false;
        }
      } else if (cfg.company && cfg.company.email) {
        const lines = [
          `${tr('Projekt:')} ${project}`,
          data.unit ? `${tr('Byt:')} ${data.unit}` : null,
          data.parking ? tr('Zájem o garážové stání: ano') : null,
          data.cellar ? tr('Zájem o sklep: ano') : null,
          `${tr('Jméno:')} ${data.name}`, `${tr('E-mail:')} ${data.email}`, `${tr('Telefon:')} ${data.phone || '-'}`, '', data.message || '',
        ].filter((l) => l !== null);
        location.href = `mailto:${cfg.company.email}?subject=${encodeURIComponent(`${tpl('Zájem: {project}', { project })}${data.unit ? tr(' – byt ') + data.unit : ''}`)}&body=${encodeURIComponent(lines.join('\n'))}`;
        status.textContent = tr('Otevíráme váš e-mailový program…');
      } else {
        // Formulář ještě není napojený (viz assets/js/config.js).
        status.textContent = tr('Formulář zatím není napojen na příjem zpráv.');
        console.warn('[Nico & Kai] Nastavte NK_CONFIG.formEndpoint nebo NK_CONFIG.company.email v assets/js/config.js.');
      }
    });
  }
  $$('.js-lead-form, #contact-form').forEach((f, i, all) => { if (all.indexOf(f) === i) initLeadForm(f); });
})();
