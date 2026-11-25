#!/usr/bin/env node
/* Nico & Kai Development — zámek webu heslem.

   Vygenerovanou stránku zašifruje (AES-256-GCM, klíč z hesla přes PBKDF2-SHA256) a uloží místo ní vstupní obrazovku,
   která obsah po zadání hesla dešifruje přímo v prohlížeči. Heslo se do webu ani do repozitáře neukládá:
   bere se z proměnné NK_HESLO (tools/build-pages.py ji plní ze souboru mimo web).

   Zamknout (volá build-pages.py):   NK_HESLO=… node tools/protect.mjs <kořen webu> <stránka.html> …
   Zkontrolovat / přečíst stránku:   NK_HESLO=… node tools/protect.mjs --decrypt <stránka.html>      (vypíše původní HTML)

   Co zámek chrání: texty a strukturu stránek. Obrázky, styly, skripty a data v assets/ šifrované nejsou –
   kdo zná jejich přesnou adresu, stáhne si je i bez hesla. */
import { readFileSync, writeFileSync } from 'node:fs';
import { createCipheriv, createDecipheriv, createHash, createHmac, pbkdf2Sync } from 'node:crypto';
import { join } from 'node:path';

const ITER = 250000;
const SALT = createHash('sha256').update('nicoandkai.com · gate · v1').digest().subarray(0, 16);
const STORE = 'nk-gate-key';
const MARK = 'data-nk-gate';

/* Heslo se porovnává bez mezer a pomlček a bez ohledu na velikost písmen (stejně jako ve vstupní obrazovce). */
const normalize = (s) => String(s).replace(/[\s\-‐-―_.]/g, '').toUpperCase();

const args = process.argv.slice(2);
const pw = normalize(process.env.NK_HESLO || '');
if (pw.length < 8) { console.error('protect: chybí heslo (proměnná NK_HESLO, aspoň 8 znaků).'); process.exit(1); }
const key = pbkdf2Sync(pw, SALT, ITER, 32, 'sha256');

const payloadOf = (html) => {
  const m = html.match(/const D = (\{[^\n]*\});/);
  if (!m) throw new Error('stránka není zamčená');
  return JSON.parse(m[1]);
};
const decrypt = (html) => {
  const D = payloadOf(html);
  const data = Buffer.from(D.c, 'base64');
  const dec = createDecipheriv('aes-256-gcm', key, Buffer.from(D.i, 'base64'));
  dec.setAuthTag(data.subarray(data.length - 16));
  return Buffer.concat([dec.update(data.subarray(0, data.length - 16)), dec.final()]).toString('utf8');
};

if (args[0] === '--decrypt') {
  try { process.stdout.write(decrypt(readFileSync(args[1], 'utf8'))); } catch (e) { console.error('protect: nejde dešifrovat –', e.message); process.exit(1); }
  process.exit(0);
}

const TEXT = {
  cs: { eyebrow: 'Soukromý náhled', h1: ['Web je přístupný', 'na heslo.'], lead: 'Stránky Nico &amp; Kai Development zatím nejsou veřejné. Zadejte prosím heslo, které jste od nás dostali.',
        label: 'Heslo', button: 'Vstoupit', busy: 'Ověřuji…', wrong: 'Heslo nesouhlasí. Zkuste to prosím znovu.', nocrypto: 'Tento prohlížeč stránku neumí odemknout. Otevřete ji prosím v aktuálním Safari nebo Chromu.',
        noscript: 'Pro zobrazení webu je potřeba zapnutý JavaScript.' },
  en: { eyebrow: 'Private preview', h1: ['This site is', 'password protected.'], lead: 'The Nico &amp; Kai Development website is not public yet. Please enter the password you received from us.',
        label: 'Password', button: 'Enter', busy: 'Checking…', wrong: 'That password does not match. Please try again.', nocrypto: 'This browser cannot unlock the page. Please open it in a current version of Safari or Chrome.',
        noscript: 'JavaScript is required to view this website.' },
  de: { eyebrow: 'Private Vorschau', h1: ['Diese Website ist', 'passwortgeschützt.'], lead: 'Die Website von Nico &amp; Kai Development ist noch nicht öffentlich. Bitte geben Sie das Passwort ein, das Sie von uns erhalten haben.',
        label: 'Passwort', button: 'Eintreten', busy: 'Wird geprüft…', wrong: 'Das Passwort stimmt nicht. Bitte versuchen Sie es erneut.', nocrypto: 'Dieser Browser kann die Seite nicht entsperren. Bitte öffnen Sie sie in einer aktuellen Version von Safari oder Chrome.',
        noscript: 'Für diese Website wird JavaScript benötigt.' },
};

const gate = (lang, rel, D) => {
  const T = TEXT[lang];
  const langs = [['cs', ''], ['en', 'en/'], ['de', 'de/']]
    .map(([l, p]) => `<a href="${rel}${p}"${l === lang ? ' aria-current="true"' : ''} hreflang="${l}" lang="${l}">${l.toUpperCase()}</a>`).join('');
  return `<!doctype html>
<html lang="${lang}" ${MARK}>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="robots" content="noindex, nofollow">
  <meta name="theme-color" content="#000000">
  <title>Nico &amp; Kai Development</title>
  <link rel="icon" href="${rel}assets/img/icons/favicon.ico" sizes="48x48">
  <link rel="icon" href="${rel}assets/img/logo/nk-ikona-cerna.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="${rel}assets/img/icons/apple-touch-icon.png">
  <script>try{if(localStorage.getItem('${STORE}')||sessionStorage.getItem('${STORE}'))document.documentElement.className='has-key'}catch(e){}</script>
  <style>
    @font-face{font-family:"Manrope";src:url("${rel}assets/fonts/Manrope-Variable.woff2") format("woff2");font-weight:200 800;font-style:normal;font-display:swap}
    *,*::before,*::after{box-sizing:border-box}
    html{background:#000;color:#fff;-webkit-text-size-adjust:100%}
    html.has-key{background:#fff}
    body{margin:0;font:400 1.0625rem/1.6 "Manrope",system-ui,-apple-system,"Segoe UI",sans-serif;-webkit-font-smoothing:antialiased}
    [hidden]{display:none!important}
    .gate{--pad:clamp(1.25rem,4.2vw,3.75rem);min-height:100vh;min-height:100svh;display:grid;grid-template-rows:auto 1fr auto;gap:2.5rem;padding:max(var(--pad),env(safe-area-inset-top)) max(var(--pad),env(safe-area-inset-right)) max(var(--pad),env(safe-area-inset-bottom)) max(var(--pad),env(safe-area-inset-left))}
    .gate__logo{display:block;width:168px;height:auto}
    .gate__box{align-self:center;max-width:46rem;padding-bottom:4vh}
    .gate__eyebrow{display:flex;align-items:center;gap:.9rem;margin:0 0 clamp(1.5rem,4vw,2.75rem);font-size:.75rem;font-weight:800;letter-spacing:.16em;text-transform:uppercase}
    .gate__eyebrow::after{content:"";flex:0 0 clamp(2rem,6vw,5rem);height:1px;background:rgba(255,255,255,.4)}
    .gate h1{margin:0;font-size:clamp(2.5rem,7.4vw,6.5rem);font-weight:800;letter-spacing:-.04em;line-height:.98}
    .gate h1 span{display:block;font-weight:300;letter-spacing:-.045em}
    .gate__lead{margin:clamp(1.25rem,3vw,2rem) 0 0;max-width:31em;color:#c9c9c5;text-wrap:pretty}
    .gate form{margin-top:clamp(2rem,5vw,3.5rem);max-width:31rem}
    .gate label{display:block;font-size:.75rem;font-weight:800;letter-spacing:.16em;text-transform:uppercase;color:#c9c9c5}
    .gate__row{display:flex;align-items:stretch;gap:1rem;margin-top:.5rem}
    .gate input{flex:1;min-width:0;padding:.85rem 0;background:none;border:0;border-bottom:1px solid rgba(255,255,255,.45);border-radius:0;color:#fff;font:600 1.125rem/1.3 "Manrope",system-ui,-apple-system,"Segoe UI",sans-serif;letter-spacing:.1em;outline:none;transition:border-color .3s,box-shadow .3s}
    .gate input:focus{border-color:#fff;box-shadow:0 1px 0 #fff}
    .gate button{flex:none;display:inline-flex;align-items:center;justify-content:space-between;gap:1rem;min-height:3.35rem;padding:0 1.5rem;border:1px solid #fff;border-radius:0;background:#fff;color:#000;font:700 .9375rem/1.2 "Manrope",system-ui,-apple-system,"Segoe UI",sans-serif;cursor:pointer;transition:background .35s,color .35s}
    .gate button i{font-style:normal;transition:transform .35s}
    .gate button:hover,.gate button:focus-visible{background:transparent;color:#fff;outline:none}
    .gate button:hover i{transform:translateX(4px)}
    .gate button[disabled]{opacity:.6;cursor:progress}
    .gate__msg{min-height:1.6em;margin:.9rem 0 0;font-size:.9375rem;font-weight:700}
    .gate__foot{display:flex;justify-content:space-between;align-items:center;gap:1rem;flex-wrap:wrap;margin:0;font-size:.75rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#8a8a85}
    .gate__foot nav{display:flex;gap:1.1rem}
    .gate__foot a{color:inherit;text-decoration:none;padding:.4rem 0;transition:color .3s}
    .gate__foot a[aria-current],.gate__foot a:hover,.gate__foot a:focus-visible{color:#fff}
    .gate>*{opacity:0;transform:translateY(16px);transition:opacity .9s cubic-bezier(.2,.7,.2,1),transform .9s cubic-bezier(.2,.7,.2,1)}
    .gate.is-in>*{opacity:1;transform:none}
    .gate.is-in>.gate__box{transition-delay:.12s}
    .gate.is-in>.gate__foot{transition-delay:.3s}
    .is-wrong .gate__row{animation:nk-shake .4s}
    @keyframes nk-shake{20%{transform:translateX(-6px)}40%{transform:translateX(6px)}60%{transform:translateX(-4px)}80%{transform:translateX(3px)}}
    @media (max-width:520px){.gate__row{flex-direction:column;gap:1.25rem}}
    @media (prefers-reduced-motion:reduce){.gate>*{transition:none}.is-wrong .gate__row{animation:none}}
    noscript p{margin:0;padding:2rem;font-weight:700}
  </style>
</head>
<body>
  <main class="gate" id="gate" hidden>
    <img class="gate__logo" src="${rel}assets/img/logo/nk-logo-horizontalni-bile.svg" alt="Nico &amp; Kai Development" width="168" height="30">
    <div class="gate__box">
      <p class="gate__eyebrow">${T.eyebrow}</p>
      <h1>${T.h1[0]}<span>${T.h1[1]}</span></h1>
      <p class="gate__lead">${T.lead}</p>
      <form id="gate-form" novalidate>
        <label for="gate-pw">${T.label}</label>
        <div class="gate__row">
          <input id="gate-pw" name="password" type="password" autocomplete="current-password" autocapitalize="off" autocorrect="off" spellcheck="false" required>
          <button type="submit"><span>${T.button}</span><i aria-hidden="true">→</i></button>
        </div>
        <p class="gate__msg" id="gate-msg" role="alert"></p>
      </form>
    </div>
    <footer class="gate__foot"><span>© Nico &amp; Kai Development</span><nav aria-label="Language">${langs}</nav></footer>
  </main>
  <noscript><p>${T.noscript}</p></noscript>
  <script>
  (async () => {
    const D = ${JSON.stringify(D)};
    const T = ${JSON.stringify({ button: T.button, busy: T.busy, wrong: T.wrong, nocrypto: T.nocrypto })};
    const K = '${STORE}';
    const el = (id) => document.getElementById(id);
    const bytes = (s) => Uint8Array.from(atob(s), (c) => c.charCodeAt(0));
    const saved = () => { try { return localStorage.getItem(K) || sessionStorage.getItem(K); } catch (e) { return null; } };
    const remember = (v) => { try { localStorage.setItem(K, v); } catch (e) { try { sessionStorage.setItem(K, v); } catch (e2) { /* soukromý režim */ } } };
    const forget = () => { try { localStorage.removeItem(K); sessionStorage.removeItem(K); } catch (e) { /* nic */ } };
    const decrypt = async (raw) => {
      const key = await crypto.subtle.importKey('raw', raw, 'AES-GCM', false, ['decrypt']);
      return new TextDecoder().decode(await crypto.subtle.decrypt({ name: 'AES-GCM', iv: bytes(D.i) }, key, bytes(D.c)));
    };
    const open = (html) => {
      const hash = location.hash;
      document.open(); document.write(html); document.close();
      if (hash.length > 1) setTimeout(() => { const t = document.getElementById(decodeURIComponent(hash.slice(1))); if (t) t.scrollIntoView(); }, 500);
    };
    const ok = !!(window.crypto && crypto.subtle);
    const had = ok && saved();
    if (had) { try { return open(await decrypt(bytes(had))); } catch (e) { forget(); } }

    document.documentElement.className = '';
    const gate = el('gate'), form = el('gate-form'), input = el('gate-pw'), msg = el('gate-msg'), btn = form.querySelector('button'), lbl = btn.querySelector('span');
    gate.hidden = false;
    setTimeout(() => gate.classList.add('is-in'), 30);
    if (!ok) { msg.textContent = T.nocrypto; btn.disabled = true; return; }
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const pw = input.value.replace(/[\\s\\-\\u2010-\\u2015_.]/g, '').toUpperCase();
      if (!pw) { input.focus(); return; }
      btn.disabled = true; lbl.textContent = T.busy; msg.textContent = ''; form.classList.remove('is-wrong');
      try {
        const base = await crypto.subtle.importKey('raw', new TextEncoder().encode(pw), 'PBKDF2', false, ['deriveBits']);
        const raw = new Uint8Array(await crypto.subtle.deriveBits({ name: 'PBKDF2', salt: bytes(D.s), iterations: D.n, hash: 'SHA-256' }, base, 256));
        const html = await decrypt(raw);
        remember(btoa(String.fromCharCode(...raw)));
        open(html);
      } catch (err) {
        btn.disabled = false; lbl.textContent = T.button; msg.textContent = T.wrong;
        void form.offsetWidth; form.classList.add('is-wrong');
        input.select(); input.focus();
      }
    });
  })();
  </script>
</body>
</html>
`;
};

const [root, ...pages] = args;
if (!root || !pages.length) { console.error('protect: použití – node tools/protect.mjs <kořen webu> <stránka.html> …'); process.exit(1); }
let n = 0;
for (const rel of pages) {
  const file = join(root, rel);
  const html = readFileSync(file, 'utf8');
  if (html.includes(MARK)) { console.error(`protect: ${rel} už je zamčená, přeskakuji`); continue; }
  const parts = rel.split('/');
  const lang = parts[0] === 'en' || parts[0] === 'de' ? parts[0] : 'cs';
  const up = '../'.repeat(parts.length - 1);
  /* IV je odvozené z klíče a obsahu: stejná stránka dá při každém sestavení stejný soubor (žádné zbytečné změny v gitu). */
  const iv = createHmac('sha256', key).update('iv\0').update(html).digest().subarray(0, 12);
  const enc = createCipheriv('aes-256-gcm', key, iv);
  const data = Buffer.concat([enc.update(html, 'utf8'), enc.final(), enc.getAuthTag()]);
  const out = gate(lang, up, { s: SALT.toString('base64'), n: ITER, i: iv.toString('base64'), c: data.toString('base64') });
  if (decrypt(out) !== html) { console.error(`protect: kontrola selhala u ${rel}`); process.exit(1); }
  writeFileSync(file, out);
  n += 1;
}
console.log(`protect: zamčeno ${n} stránek`);
