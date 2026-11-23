/* Nico & Kai Development — atmosféra v hero obrázku: jemná ranní mlha (mist) nebo sníh (snow).
   Použití: <section class="hero-media" data-atmo="mist|snow"> … <canvas class="hero-media__atmo"></canvas>
   Šetrné: běží jen když je hero na obrazovce, respektuje prefers-reduced-motion, DPR max 1.5. */
(() => {
  'use strict';
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const heroes = [...document.querySelectorAll('.hero-media[data-atmo]')];
  if (!heroes.length) return;

  heroes.forEach((hero) => {
    const canvas = hero.querySelector('.hero-media__atmo');
    if (!canvas) return;
    const ctx = canvas.getContext('2d', { alpha: true });
    const mode = hero.dataset.atmo;
    const dpr = Math.min(1.5, devicePixelRatio || 1);
    let W = 0, H = 0, running = false, raf = 0, last = 0;
    let blobs = [], flakes = [];

    const rnd = (a, b) => a + Math.random() * (b - a);

    /* ---- mlha: měkké světlé skvrny, které pomalu plují a dýchají ---- */
    const blobSprite = (r, light) => {
      const c = document.createElement('canvas'); c.width = c.height = r * 2;
      const g = c.getContext('2d');
      const grad = g.createRadialGradient(r, r, 0, r, r, r);
      grad.addColorStop(0, `rgba(${light},${light},${light},.55)`);
      grad.addColorStop(.45, `rgba(${light},${light},${light},.22)`);
      grad.addColorStop(1, `rgba(${light},${light},${light},0)`);
      g.fillStyle = grad; g.fillRect(0, 0, r * 2, r * 2);
      return c;
    };
    const initMist = () => {
      blobs = [];
      const n = Math.round(W / 180) + 5;
      for (let i = 0; i < n; i++) {
        const r = Math.max(24, rnd(W * 0.18, W * 0.42));
        blobs.push({
          x: rnd(-r, W), y: rnd(H * 0.35, H * 1.05), r, sprite: blobSprite(Math.round(r), 235 + Math.round(rnd(0, 20))),
          vx: rnd(4, 11) * (Math.random() < .85 ? 1 : -1), vy: rnd(-1.2, 1.2),
          a: rnd(.05, .13), ph: rnd(0, Math.PI * 2), fr: rnd(.08, .2),
        });
      }
    };
    const drawMist = (t, dt) => {
      ctx.clearRect(0, 0, W, H);
      ctx.globalCompositeOperation = 'lighter';
      blobs.forEach((b) => {
        b.x += b.vx * dt; b.y += b.vy * dt;
        if (b.vx > 0 && b.x - b.r > W) b.x = -b.r * 2;
        if (b.vx < 0 && b.x + b.r < 0) b.x = W + b.r * 2;
        if (b.y + b.r < H * 0.2) b.y = H * 1.05;
        if (b.y - b.r > H * 1.1) b.y = H * 0.3;
        ctx.globalAlpha = b.a * (0.75 + 0.25 * Math.sin(t * b.fr + b.ph));
        ctx.drawImage(b.sprite, b.x - b.r, b.y - b.r, b.r * 2, b.r * 2);
      });
      ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over';
    };

    /* ---- sníh: pomalé vločky s mírným větrem, blízké větší a ostřejší ---- */
    const initSnow = () => {
      flakes = [];
      const n = Math.round(W * H / 9000);
      for (let i = 0; i < n; i++) flakes.push(newFlake(true));
    };
    const newFlake = (anywhere) => {
      const depth = Math.random();                       // 0 = daleko, 1 = blízko
      return {
        x: rnd(-20, W + 20), y: anywhere ? rnd(-20, H) : rnd(-30, -5),
        r: 0.7 + depth * 2.4, vy: 14 + depth * 34, sway: rnd(8, 26), ph: rnd(0, Math.PI * 2), sf: rnd(.4, 1.1),
        a: .35 + depth * .55, depth,
      };
    };
    let wind = 0, windTarget = 0;
    const drawSnow = (t, dt) => {
      ctx.clearRect(0, 0, W, H);
      if (Math.random() < .004) windTarget = rnd(-22, 22);
      wind += (windTarget - wind) * Math.min(1, dt * .25);
      ctx.fillStyle = '#fff';
      flakes.forEach((f, i) => {
        f.y += f.vy * dt;
        f.x += (Math.sin(t * f.sf + f.ph) * f.sway * .35 + wind * (0.4 + f.depth)) * dt;
        if (f.y - f.r > H || f.x < -30 || f.x > W + 30) flakes[i] = newFlake(false);
        ctx.globalAlpha = f.a;
        ctx.beginPath(); ctx.arc(f.x, f.y, f.r, 0, Math.PI * 2); ctx.fill();
      });
      ctx.globalAlpha = 1;
    };

    const resize = () => {
      const r = hero.getBoundingClientRect();
      W = Math.max(1, Math.round(r.width)); H = Math.max(1, Math.round(r.height));
      if (W < 8 || H < 8) return;
      canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
      canvas.style.width = `${W}px`; canvas.style.height = `${H}px`;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      if (mode === 'snow') initSnow(); else initMist();
    };
    const frame = (now) => {
      if (!running) return;
      if (W < 8 || H < 8) { resize(); raf = requestAnimationFrame(frame); return; }   // hero ještě nemá rozměr (skrytý panel)
      const t = now / 1000, dt = Math.min(.05, last ? (now - last) / 1000 : .016); last = now;
      if (mode === 'snow') drawSnow(t, dt); else drawMist(t, dt);
      raf = requestAnimationFrame(frame);
    };
    const start = () => { if (running) return; running = true; last = 0; raf = requestAnimationFrame(frame); };
    const stop = () => { running = false; cancelAnimationFrame(raf); };

    resize();
    let rt; addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(resize, 150); }, { passive: true });
    new IntersectionObserver((es) => es.forEach((e) => (e.isIntersecting && !document.hidden ? start() : stop())), { threshold: 0.02 }).observe(hero);
    document.addEventListener('visibilitychange', () => { if (document.hidden) stop(); else if (hero.getBoundingClientRect().bottom > 0) start(); });
    canvas.classList.add('is-on');
  });
})();
