# -*- coding: utf-8 -*-
"""Generátor stránek webu Nico & Kai Development ve třech jazycích. Spuštění: python3 tools/build-pages.py
Texty: tools/i18n.py. Výstup: index.html + en/ + de/ (úvod, 4 projekty, ochrana osobních údajů), 404.html, sitemap.xml, robots.txt."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i18n import LANGS, LANG_META, UI, PROJECTS, HOME, VYSOKE, VLNITA, LEGAL, NOTFOUND

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_URL = "https://nicoandkai.com"   # ostrá doména (canonical, hreflang, og:url, sitemap)
PAGES = ["home", "ke-schodum", "do-ctvrti", "vysoke", "vlnita", "privacy"]

def page_path(lang, key):
    """Cesta stránky od kořene jazyka (bez prefixu jazyka)."""
    return {"home": "", "ke-schodum": "ke-schodum/", "do-ctvrti": "do-ctvrti/", "vysoke": "apartmany-vysoke/", "vlnita": "rezidence-vlnita/",
            "privacy": LANG_META[lang]["privacy"] + "/"}[key]

class Ctx:
    """Kontext jazyka a hloubky stránky: rel = cesta ke kořeni webu (assets), home = cesta ke kořeni jazyka."""
    def __init__(self, lang, key):
        self.lang, self.key = lang, key
        self.T = UI[lang]
        self.prefix = LANG_META[lang]["prefix"]
        depth = (1 if self.prefix else 0) + (1 if page_path(lang, key) else 0)
        self.rel = "../" * depth
        self.home = self.rel + self.prefix
        self.privacy = self.home + LANG_META[lang]["privacy"] + "/"
    def alt(self, lang):
        """Relativní odkaz na tutéž stránku v jiném jazyce."""
        return self.rel + LANG_META[lang]["prefix"] + page_path(lang, self.key) or "./"

# ---------------------------------------------------------------------- obrázky
def avail(path):
    """Šířky, ve kterých obrázek na disku skutečně existuje (soubory <název>-<šířka>.webp)."""
    p = path
    while p.startswith("../"): p = p[3:]
    base = os.path.join(ROOT, p.rsplit(".", 1)[0])
    ws = tuple(w for w in (600, 1200, 1800, 2400, 3600) if os.path.exists(f"{base}-{w}.webp"))
    assert ws, f"obrázek nenalezen: {path}"
    return ws

def img(path, alt, widths=None, sizes="100vw", cls="", lazy=True, extra=""):
    widths = widths or avail(path)
    base = path.rsplit(".", 1)[0]
    srcset = ", ".join(f"{base}-{w}.webp {w}w" for w in widths)
    mid = widths[min(1, len(widths) - 1)]
    return (f'<img{(" class=\"" + cls + "\"") if cls else ""} src="{base}-{mid}.webp" srcset="{srcset}" sizes="{sizes}" '
            f'data-full="{base}-{widths[-1]}.webp" alt="{alt}"{" loading=\"lazy\"" if lazy else " fetchpriority=\"high\""}{extra}>')

def video(rel, name):
    """Hero video (mp4 z Veo 3.1 / Figma Weave). Načte se až skriptem (data-src); na malých displejích
    a při prefers-reduced-motion zůstane obrázek. 720p verze pro menší obrazovky."""
    return (f'<video class="hero-media__video" muted playsinline preload="none" aria-hidden="true" tabindex="-1" '
            f'data-src="{rel}assets/video/{name}.mp4" data-src-sm="{rel}assets/video/{name}-720.mp4"></video>')

def fig(path, alt, cap="", kind="", widths=None):
    sizes = "(max-width: 880px) 100vw, 66vw" if kind in ("is-wide", "is-big") else "(max-width: 880px) 100vw, 33vw"
    return f'<figure{(" class=\"" + kind + "\"") if kind else ""}>{img(path, alt, widths, sizes)}{("<figcaption>" + cap + "</figcaption>") if cap else ""}</figure>'

# ---------------------------------------------------------------------- společné bloky
def head(C, title, desc, og, theme="#000000", extra_css="", extra_head=""):
    rel = C.rel
    url = f"{SITE_URL}/{C.prefix}{page_path(C.lang, C.key)}"
    alts = "\n".join(f'  <link rel="alternate" hreflang="{l}" href="{SITE_URL}/{LANG_META[l]["prefix"]}{page_path(l, C.key)}">' for l in LANGS)
    alts += f'\n  <link rel="alternate" hreflang="x-default" href="{SITE_URL}/{page_path("cs", C.key)}">'
    return f"""<!doctype html>
<html lang="{C.lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="{theme}">
  <meta name="color-scheme" content="light">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="{LANG_META[C.lang]['locale']}">
  <meta property="og:site_name" content="Nico &amp; Kai Development">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{SITE_URL}/assets/img/{og}">
  <meta property="og:url" content="{url}">
  <link rel="canonical" href="{url}">
{alts}
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="{rel}assets/img/icons/favicon.ico" sizes="48x48">
  <link rel="icon" href="{rel}assets/img/logo/nk-ikona-cerna.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="{rel}assets/img/icons/apple-touch-icon.png">
  <link rel="preload" href="{rel}assets/fonts/Manrope-Variable.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{rel}assets/css/styles.css">
  <link rel="stylesheet" href="{rel}assets/css/explorer.css">
  <link rel="stylesheet" href="{rel}assets/css/site.css">{extra_css}
  <script>document.documentElement.classList.add('js')</script>{extra_head}
</head>
<body>
  <a class="skip" href="#obsah">{C.T['skip']}</a>
  <div class="progress" aria-hidden="true"></div>
"""

def lang_switch(C, cls="lang"):
    links = "".join(f'<a href="{C.alt(l)}" hreflang="{l}" lang="{l}"{" class=\"is-active\" aria-current=\"page\"" if l == C.lang else ""}>{LANG_META[l]["short"]}</a>' for l in LANGS)
    return f'<nav class="{cls}" aria-label="{C.T["lang_aria"]}">{links}</nav>'

def header(C, nav, cta_href, cta_label, menu=None):
    T, rel = C.T, C.rel
    menu = menu or nav
    navh = "\n".join(f'        <a href="{h}" data-nav="{h.lstrip("#").split("/")[0] or "home"}">{t}</a>' for h, t in nav)
    menuh = "\n".join(f'      <a href="{h}"><small>{i+1:02d}</small>{t}</a>' for i, (h, t) in enumerate(menu))
    return f"""  <header class="site-header" id="header">
    <div class="wrap site-header__in">
      <a class="brand" href="{C.home or './'}" aria-label="{T['brand_aria']}">
        <img class="brand__light" src="{rel}assets/img/logo/nk-logo-horizontalni-cerne.svg" alt="Nico &amp; Kai Development" width="168" height="30">
        <img class="brand__dark" src="{rel}assets/img/logo/nk-logo-horizontalni-bile.svg" alt="" width="168" height="30" aria-hidden="true">
      </a>
      <nav class="nav" aria-label="{T['nav_main']}">
{navh}
      </nav>
      {lang_switch(C)}
      <a class="btn btn--sm header-cta" href="{cta_href}"><span>{cta_label}</span></a>
      <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">
        <span class="menu-btn__label">{T['menu']}</span>
        <span class="menu-btn__icon" aria-hidden="true"><i></i><i></i></span>
      </button>
    </div>
  </header>

  <div class="menu" id="menu" hidden>
    <nav class="wrap menu__nav" aria-label="{T['nav_mobile']}">
{menuh}
    </nav>
    <div class="wrap">{lang_switch(C, "lang lang--menu")}</div>
  </div>

  <main id="obsah">
"""

def footer(C, legal_prefix="company", extra_note=""):
    T, rel = C.T, C.rel
    return f"""  </main>

  <footer class="footer dark">
    <div class="wrap">
      <div class="footer__top">
        <a class="brand" href="{C.home or './'}" aria-label="{T['brand_aria']}">
          <img src="{rel}assets/img/logo/nk-logo-horizontalni-bile.svg" alt="Nico &amp; Kai Development" width="168" height="30">
        </a>
        <nav class="footer__nav" aria-label="{T['nav_footer']}">
          <a href="{C.home}ke-schodum/">{T['ks']}</a>
          <a href="{C.home}do-ctvrti/">{T['dc']}</a>
          <a href="{C.home}apartmany-vysoke/">{T['vy']}</a>
          <a href="{C.home}rezidence-vlnita/">{T['vl']}</a>
          <a href="{C.privacy}">{T['privacy']}</a>
        </nav>
      </div>

      <div class="partners">
        <div class="partners__item"><small>{T['partners_arch']}</small><img src="{rel}assets/img/partners/ja-architekti.svg" alt="JA Architekti" style="height:1.6rem;width:auto;filter:invert(1)"></div>
      </div>

      <ul class="legal-list" data-cfg-group>
        <li data-cfg-wrap="{legal_prefix}.legalName"><span>{T['legal_company']}</span><span data-cfg="{legal_prefix}.legalName"></span></li>
        <li data-cfg-wrap="{legal_prefix}.ico"><span>{T['legal_ico']}</span><span data-cfg="{legal_prefix}.ico"></span></li>
        <li data-cfg-wrap="{legal_prefix}.dic"><span>{T['legal_dic']}</span><span data-cfg="{legal_prefix}.dic"></span></li>
        <li data-cfg-wrap="{legal_prefix}.address"><span>{T['legal_addr']}</span><span data-cfg="{legal_prefix}.address"></span></li>
        <li data-cfg-wrap="company.email"><span>{T['legal_email']}</span><a data-cfg="company.email" data-cfg-href="mailto:"></a></li>
        <li data-cfg-wrap="company.phone"><span>{T['legal_phone']}</span><a data-cfg="company.phone" data-cfg-href="tel:"></a></li>
      </ul>

      <p class="footer__note">
        {T['footer_note']}{extra_note}
      </p>
      <p class="footer__copy">© <span data-year>2026</span> Nico &amp; Kai Development · {lang_switch(C, "lang lang--inline")}</p>
    </div>
    <img class="footer__mark" src="{rel}assets/img/logo/nk-monogram-bile.svg" alt="" aria-hidden="true">
  </footer>
"""

def scripts(C, data=(), explorer=False):
    rel = C.rel
    s = f'  <script src="{rel}assets/js/config.js"></script>\n'
    if C.lang != "cs": s += f'  <script src="{rel}assets/i18n/{C.lang}.js"></script>\n'
    for d in data: s += f'  <script src="{rel}assets/data/{d}.js"></script>\n'
    s += f'  <script src="{rel}assets/js/main.js"></script>\n'
    if explorer: s += f'  <script src="{rel}assets/js/explorer.js"></script>\n'
    s += f'  <script src="{rel}assets/js/site.js"></script>\n  <script src="{rel}assets/js/atmo.js" defer></script>\n</body>\n</html>\n'
    return s

def form(C, project, with_unit=True, extras=True, title=("", ""), lead="", how=(), submit="", eyebrow=("05", "")):
    T = C.T
    unit = f"""            <div class="field field--select">
              <span>{T['f_unit']}</span>
              <select name="unit" aria-label="{T['f_unit']}"><option value="">{T['f_unit_default']}</option></select>
            </div>
""" if with_unit else ""
    ex = f"""            <div class="extras">
              <label class="check"><input type="checkbox" name="parking"><span class="check__box" aria-hidden="true"></span><span class="check__text">{T['f_parking']}</span></label>
              <label class="check"><input type="checkbox" name="cellar"><span class="check__box" aria-hidden="true"></span><span class="check__text">{T['f_cellar']}</span></label>
            </div>
""" if extras else ""
    howh = ("<ol class=\"how\" data-reveal>" + "".join(f"<li>{h}</li>" for h in how) + "</ol>") if how else ""
    return f"""    <section class="section contact reserve" id="rezervace" aria-labelledby="reserve-title">
      <div class="wrap">
        <p class="eyebrow" data-reveal><span>{eyebrow[0]}</span> {eyebrow[1]}</p>
        <div class="contact__grid">
          <div class="contact__copy">
            <h2 class="display display--md" id="reserve-title">
              <span class="mask"><span class="mask__in" data-in>{title[0]}</span></span>
              <span class="mask light"><span class="mask__in" data-in style="--d:.12s">{title[1]}</span></span>
            </h2>
            <p class="lead" data-reveal>{lead}</p>
            {howh}
            <ul class="contact-list" data-reveal>
              <li data-cfg-wrap="company.email"><span>{T['legal_email']}</span><a data-cfg="company.email" data-cfg-href="mailto:"></a></li>
              <li data-cfg-wrap="company.phone"><span>{T['legal_phone']}</span><a data-cfg="company.phone" data-cfg-href="tel:"></a></li>
            </ul>
          </div>
          <form class="form js-lead-form" id="contact-form" data-project="{project}" novalidate data-reveal>
{unit}{ex}            <div class="field"><input id="f-name" name="name" type="text" autocomplete="name" placeholder=" " required><label for="f-name">{T['f_name']}</label></div>
            <div class="field"><input id="f-email" name="email" type="email" autocomplete="email" placeholder=" " required><label for="f-email">{T['f_email']}</label></div>
            <div class="field"><input id="f-phone" name="phone" type="tel" autocomplete="tel" placeholder=" "><label for="f-phone">{T['f_phone']} <span>{T['f_optional']}</span></label></div>
            <div class="field"><textarea id="f-msg" name="message" rows="3" placeholder=" "></textarea><label for="f-msg">{T['f_msg']} <span>{T['f_optional']}</span></label></div>
            <div class="hp" aria-hidden="true"><label>{T['f_hp']} <input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
            <label class="check">
              <input type="checkbox" name="consent" required>
              <span class="check__box" aria-hidden="true"></span>
              <span class="check__text">{T['f_consent_a']} <a href="{C.privacy}" target="_blank" rel="noopener">{T['f_consent_link']}</a> {T['f_consent_b']}</span>
            </label>
            <div class="form__actions">
              <button class="btn" type="submit"><span>{submit}</span><i class="arrow" aria-hidden="true">→</i></button>
              <p class="form__status" role="status" aria-live="polite"></p>
            </div>
          </form>
        </div>
      </div>
    </section>
"""

def explorer_block(C, plan_note, cad_note):
    T = C.T
    ths = "".join(f'<th scope="col">{h}</th>' for h in T['th'][:-1]) + f'<th scope="col"><span class="sr-only">{T["th"][-1]}</span></th>'
    return f"""        <div class="ex" data-reveal>
          <div class="ex__stack">
            <svg id="ex-stack" role="group" aria-label="{T['ex_stack_aria']}"></svg>
            <ul class="ex__floors" id="ex-floors" role="tablist" aria-label="{T['ex_floors_aria']}"></ul>
          </div>
          <div class="ex__main">
            <div class="ex__plan">
              <div class="ex__planhead">
                <h3 id="ex-floor-title">{T['ex_floor']}</h3>
                <button class="link" type="button" id="ex-cad">{T['ex_cad']}</button>
              </div>
              <div class="ex__planbox"><svg id="ex-plan" role="group"></svg></div>
              <p class="ex__note" id="ex-note">{plan_note}</p>
            </div>
            <aside class="ex__detail" id="ex-detail" aria-live="polite"></aside>
          </div>
        </div>

        <div class="units-wrap" data-reveal>
          <h3>{T['ex_overview']}</h3>
          <table id="ex-table">
            <thead><tr>{ths}</tr></thead>
            <tbody></tbody>
          </table>
          <p class="units-note" id="ex-areanote"></p>
        </div>

        <dialog class="dialog" id="ex-dialog" aria-labelledby="ex-dialog-title">
          <div class="dialog__bar">
            <strong class="dialog__title" id="ex-dialog-title">{T['ex_dialog']}</strong>
            <button class="link" type="button" data-dialog-close>{T['close']}</button>
          </div>
          <div class="dialog__body"><img alt="" src=""></div>
          <p class="dialog__note">{cad_note}</p>
        </dialog>
"""

# ======================================================================
# PROJEKTOVÉ STRÁNKY (Ke Schodům, Do Čtvrti)
# ======================================================================
def project_page(C, c):
    T, rel = C.T, C.rel; I = lambda n: f"{rel}assets/img/{c['slug']}/{n}.webp"
    nav = [("#dum", T['p_dum']), ("#galerie", T['p_galerie']), ("#byty", T['p_byty']), ("#cenik", T['p_cenik']), ("#rezervace", T['p_rezervace'])]
    gal = "".join(fig(I(n), a, cap, k) for n, a, cap, k in c["gallery"])
    splits = ""
    for i, (n, a, h3, txt) in enumerate(c["splits"]):
        flip = " split--flip" if i % 2 else ""
        splits += f"""        <div class="split{flip}" data-reveal>
          <div class="split__media">{img(I(n), a, sizes="(max-width: 880px) 100vw, 58vw")}</div>
          <div class="split__copy"><h3>{h3}</h3>{txt}</div>
        </div>
"""
    tech = "".join(f'<article class="tech__col" data-reveal style="--d:.{i}s"><h3>{h}</h3><ul>{"".join(f"<li>{x}</li>" for x in items)}</ul></article>' for i, (h, items) in enumerate(c["tech"]))
    steps = "".join(f'<li{" class=\"is-now\"" if now else ""} data-reveal style="--d:.{i}s"><small>{s}</small><strong>{t}</strong><p>{d}</p></li>' for i, (s, t, d, now) in enumerate(c["steps"]))
    addr = "".join(f"<div><span>{k}</span><strong>{v}</strong></div>" for k, v in c["addr"])
    numbers = "".join(f'<div data-reveal style="--d:.{i}s"><strong><span data-count="{n}">{n}</span>{("<small>" + u + "</small>") if u else ""}</strong><span>{l}</span></div>' for i, ((n, u), l) in enumerate(zip(c['numbers_n'], c['numbers_l'])))
    terms = "".join(f"<li><strong>{a}</strong><p>{b}</p></li>" for a, b in T['terms'])
    html = head(C, c["title"], c["desc"], c["og"], extra_head=f"""
  <script type="application/ld+json">
  {{"@context": "https://schema.org", "@type": "ApartmentComplex", "name": "{c['name']}", "description": "{c['desc']}",
   "numberOfAccommodationUnits": {c['units']}, "address": {{"@type": "PostalAddress", "streetAddress": "{c['street']}", "addressLocality": "Praha", "postalCode": "143 00", "addressCountry": "CZ"}}}}
  </script>""")
    html += header(C, nav, "#byty", T['choose_unit'], nav + [(C.home or "./", T['all_projects'])])
    html += f"""
    <!-- ============ HERO ============ -->
    <section class="hero-media dark" id="top" data-atmo="mist">
      <div class="hero-media__bg">{img(I(c['hero']), c['hero_alt'], sizes="100vw", lazy=False)}{video(rel, c['video']) if c.get('video') else ''}</div>
      <canvas class="hero-media__atmo" aria-hidden="true"></canvas>
      <div class="wrap hero-media__body">
        <p class="chip" data-reveal><i aria-hidden="true"></i>{c['stage']} · {T['chip_suffix']}</p>
        <h1 class="display">
          <span class="mask"><span class="mask__in" style="--d:.05s">{c['h1a']}</span></span>
          <span class="mask light"><span class="mask__in" style="--d:.17s">{c['h1b']}</span></span>
        </h1>
        <p class="lead" data-reveal style="--d:.35s">{c['lead']}</p>
        <div class="hero__cta" data-reveal style="--d:.45s">
          <a class="btn" href="#byty"><span>{T['cta_units']}</span><i class="arrow" aria-hidden="true">→</i></a>
          <a class="btn btn--ghost" href="#cenik"><span>{T['cta_pricing']}</span></a>
        </div>
      </div>
      <div class="wrap hero-media__meta">
        <dl class="meta">{"".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in c['meta'])}</dl>
        <a class="scroll-cue" href="#dum"><span>{T['down']}</span><i aria-hidden="true"></i></a>
      </div>
      <p class="hero-media__credit">{T['credit']}</p>
    </section>

    <!-- ============ DŮM ============ -->
    <section class="section" id="dum" aria-labelledby="dum-title">
      <div class="wrap">
        <p class="eyebrow" data-reveal><span>01</span> {T['sec_house']}</p>
        <h2 class="manifest" id="dum-title" data-reveal>{c['manifest']}</h2>
        <div class="numbers">{numbers}</div>
      </div>
    </section>

    <!-- ============ GALERIE ============ -->
    <section class="section section--tight" id="galerie" aria-labelledby="gal-title" style="padding-top:0">
      <div class="wrap">
        <div class="section-head" data-reveal>
          <h2 class="display display--md" id="gal-title"><span class="mask"><span class="mask__in" data-in>{c['gal_h'][0]}</span></span><span class="mask light"><span class="mask__in" data-in style="--d:.12s">{c['gal_h'][1]}</span></span></h2>
          <p>{c['gal_p']}</p>
        </div>
        <div class="gallery" aria-label="{T['gallery_aria']}">{gal}</div>
        <p class="note" style="margin-top:1rem">{T['gallery_note']}</p>
      </div>
    </section>

    <!-- ============ PŘÍBĚH ============ -->
    <section class="section dark" id="pribeh">
      <div class="wrap" style="display:grid;gap:clamp(3rem,8vw,7rem)">
{splits}      </div>
    </section>

    <!-- ============ BYTY ============ -->
    <section class="section explorer" id="byty" aria-labelledby="byty-title" data-explorer="{c['slug']}" data-img-base="{rel}assets/img/{c['slug']}/">
      <div class="wrap">
        <p class="eyebrow" data-reveal><span>02</span> {T['sec_units']}</p>
        <div class="explorer__head">
          <h2 class="display display--md" id="byty-title">
            <span class="mask"><span class="mask__in" data-in>{T['units_h'][0]}</span></span>
            <span class="mask light"><span class="mask__in" data-in style="--d:.12s">{T['units_h'][1]}</span></span>
          </h2>
          <p class="legend" aria-label="{T['legend_aria']}">
            <span><i class="lg-available"></i>{T['legend_av']}</span>
            <span><i class="lg-reserved"></i>{T['legend_re']}</span>
            <span><i class="lg-sold"></i>{T['legend_so']}</span>
          </p>
        </div>

        <div class="facade" data-facade="{c['slug']}" data-reveal>
          <img class="facade__img" src="{I(c['facade'])[:-5]}-2400.webp" srcset="{I(c['facade'])[:-5]}-1200.webp 1200w, {I(c['facade'])[:-5]}-2400.webp 2400w" sizes="(max-width: 1520px) 100vw, 1520px" width="2400" height="1610" alt="{c['facade_alt']}">
          <span class="facade__hint">{T['facade_hint']}</span>
        </div>
        <p class="facade__legend" data-reveal><span class="lg-available"><i></i>{T['legend_av']}</span><span class="lg-reserved"><i></i>{T['legend_re']}</span><span class="lg-sold"><i></i>{T['legend_so']}</span><span>{T['facade_click']}</span></p>

{explorer_block(C, c['plan_note'], c['cad_note'])}
      </div>
    </section>

    <!-- ============ CENÍK A REZERVACE ============ -->
    <section class="section dark" id="cenik" aria-labelledby="cenik-title">
      <div class="wrap">
        <p class="eyebrow" data-reveal><span>03</span> {T['sec_pricing']}</p>
        <div class="reserve-head">
          <div>
            <h2 class="display display--md" id="cenik-title">
              <span class="mask"><span class="mask__in" data-in>{T['pricing_h'][0]}</span></span>
              <span class="mask light"><span class="mask__in" data-in style="--d:.12s">{T['pricing_h'][1]}</span></span>
            </h2>
          </div>
          <div><p class="lead" data-reveal>{T['pricing_lead']}</p></div>
        </div>

        <dl class="price-extras" data-extras="{c['slug']}" data-reveal></dl>

        <div class="reserve-table-wrap" data-reservation="{c['slug']}" data-reveal></div>
        <p class="note" style="margin-top:1rem"><span data-if-prices>{T['note_prices']}</span><span data-if-no-prices>{T['note_noprices']}</span>{c['price_note']}</p>

        <ol class="reserve-terms" data-reveal>{terms}</ol>
        <div data-reveal style="margin-top:2.5rem"><a class="btn btn--light" href="#rezervace"><span>{T['reserve_btn']}</span><i class="arrow" aria-hidden="true">→</i></a></div>
      </div>
    </section>

    <!-- ============ TECHNOLOGIE ============ -->
    <section class="section" id="technologie" aria-labelledby="tech-title">
      <div class="wrap">
        <p class="eyebrow" data-reveal><span>04</span> {T['sec_standard']}</p>
        <h2 class="display display--md" id="tech-title">
          <span class="mask"><span class="mask__in" data-in>{c['tech_h'][0]}</span></span>
          <span class="mask light"><span class="mask__in" data-in style="--d:.12s">{c['tech_h'][1]}</span></span>
        </h2>
        <div class="tech__grid tech__grid--light">{tech}</div>
        <p class="tech__note" data-reveal>{c['tech_note']}</p>
      </div>
    </section>

    <!-- ============ LOKALITA + HARMONOGRAM ============ -->
    <section class="section dark" id="lokalita" aria-labelledby="lok-title">
      <div class="wrap">
        <p class="eyebrow" data-reveal><span>05</span> {T['sec_location']}</p>
        <div class="addr">
          <div class="addr__copy">
            <h2 class="display display--md" id="lok-title"><span class="mask"><span class="mask__in" data-in>{c['lok_h'][0]}</span></span><span class="mask light"><span class="mask__in" data-in style="--d:.12s">{c['lok_h'][1]}</span></span></h2>
            <p class="lead" data-reveal>{c['lok_p']}</p>
          </div>
          <div class="addr__list" data-reveal>{addr}</div>
        </div>
        <ol class="steps-t steps-t--4" style="margin-top:clamp(3rem,7vw,6rem)">{steps}</ol>
      </div>
    </section>

{form(C, c['name'], True, True, T['form_h'], T['form_lead'], T['form_how'], T['form_submit'], eyebrow=("06", T['sec_reserve']))}
"""
    html += footer(C, f"projects.{c['slug']}.seller", c.get("footnote", "")) + scripts(C, (c["slug"],), explorer=True)
    return html

# ======================================================================
# APARTMÁNY VYSOKÉ
# ======================================================================
def vysoke_page(C):
    T, rel, V = C.T, C.rel, VYSOKE[C.lang]; I = lambda n: f"{rel}assets/img/vysoke/{n}.webp"
    gal = "".join(fig(I(n), a, cap, k) for n, a, cap, k in V['gallery'])
    numbers = "".join(f'<div data-reveal style="--d:.{i}s"><strong><span data-count="{n}">{n}</span>{("<small>" + u + "</small>") if u else ""}</strong><span>{l}</span></div>' for i, (n, u, l) in enumerate(V['numbers']))
    html = head(C, V['title'], V['desc'], "og-vysoke.jpg")
    html += header(C, V['nav'], "#kontakt", V['cta_header'], V['nav'] + [(C.home or "./", T['all_projects'])])
    html += f"""
    <section class="hero-media dark" id="top" data-atmo="snow">
      <div class="hero-media__bg">{img(I('k01'), V['hero_alt'], sizes='100vw', lazy=False)}</div>
      <canvas class="hero-media__atmo" aria-hidden="true"></canvas>
      <div class="wrap hero-media__body">
        <p class="chip" data-reveal><i aria-hidden="true"></i>{V['chip']}</p>
        <h1 class="display">
          <span class="mask"><span class="mask__in" style="--d:.05s">{V['h1a']}</span></span>
          <span class="mask light"><span class="mask__in" style="--d:.17s">{V['h1b']}</span></span>
        </h1>
        <p class="lead" data-reveal style="--d:.35s">{V['lead']}</p>
        <div class="hero__cta" data-reveal style="--d:.45s">
          <a class="btn" href="#jednotky"><span>{V['cta1']}</span><i class="arrow" aria-hidden="true">→</i></a>
          <a class="btn btn--ghost" href="#galerie"><span>{V['cta2']}</span></a>
        </div>
      </div>
      <div class="wrap hero-media__meta">
        <dl class="meta">{"".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in V['meta'])}</dl>
        <a class="scroll-cue" href="#pribeh"><span>{T['down']}</span><i aria-hidden="true"></i></a>
      </div>
    </section>

    <section class="section" id="pribeh" aria-labelledby="pribeh-title">
      <div class="wrap">
        <p class="eyebrow" data-reveal><span>01</span> {V['s1']}</p>
        <h2 class="manifest" id="pribeh-title" data-reveal>{V['manifest']}</h2>
        <div class="numbers">{numbers}</div>
      </div>
    </section>

    <section class="section dark" id="jednotky" aria-labelledby="jed-title">
      <div class="wrap">
        <p class="eyebrow" data-reveal><span>02</span> {V['s2']}</p>
        <div class="section-head" data-reveal>
          <h2 class="display display--md" id="jed-title"><span class="mask"><span class="mask__in" data-in>{V['units_h'][0]}</span></span><span class="mask light"><span class="mask__in" data-in style="--d:.12s">{V['units_h'][1]}</span></span></h2>
          <p>{V['units_p']}</p>
        </div>
        <div class="ucards" data-units-cards="vysoke"></div>
        <div class="agent" data-reveal>
          <div class="agent__mono" aria-hidden="true">S&amp;W</div>
          <div>
            <strong>Jana Kocianová · Svoboda &amp; Williams</strong>
            <span>{V['agent_line']} <a href="https://www.svoboda-williams.com/" rel="noopener" target="_blank">svoboda-williams.com ↗</a></span>
            <span data-cfg-wrap="projects.vysoke.agent.phone"><a data-cfg="projects.vysoke.agent.phone" data-cfg-href="tel:"></a></span>
            <span data-cfg-wrap="projects.vysoke.agent.email"><a data-cfg="projects.vysoke.agent.email" data-cfg-href="mailto:"></a></span>
          </div>
        </div>
      </div>
    </section>

    <section class="section" id="galerie" aria-labelledby="gal-title">
      <div class="wrap">
        <p class="eyebrow" data-reveal><span>03</span> {V['s3']}</p>
        <div class="section-head" data-reveal>
          <h2 class="display display--md" id="gal-title"><span class="mask"><span class="mask__in" data-in>{V['gal_h'][0]}</span></span><span class="mask light"><span class="mask__in" data-in style="--d:.12s">{V['gal_h'][1]}</span></span></h2>
          <p>{V['gal_p']}</p>
        </div>
        <div class="gallery" aria-label="{T['photos_aria']}">{gal}</div>
        <p class="note" style="margin-top:1rem">{V['gal_note']}</p>
      </div>
    </section>

    <section class="section dark" id="lokalita" aria-labelledby="lok-title">
      <div class="wrap">
        <p class="eyebrow" data-reveal><span>04</span> {V['s4']}</p>
        <div class="addr">
          <div class="addr__copy">
            <h2 class="display display--md" id="lok-title"><span class="mask"><span class="mask__in" data-in>{V['lok_h'][0]}</span></span><span class="mask light"><span class="mask__in" data-in style="--d:.12s">{V['lok_h'][1]}</span></span></h2>
            <p class="lead" data-reveal>{V['lok_p']}</p>
          </div>
          <div class="addr__list" data-reveal>{"".join(f"<div><span>{k}</span><strong>{v}</strong></div>" for k, v in V['addr'])}</div>
        </div>
        <figure class="pano" data-reveal>{img(I('k11'), V['pano_alt'], sizes='(max-width: 880px) 240vw, 150vw')}</figure>
      </div>
    </section>

{form(C, "Apartmány Vysoké", False, False, V['form_h'], V['form_lead'], (), T['send'], eyebrow=("05", V['s5'])).replace('id="rezervace"', 'id="kontakt"')}
"""
    html += footer(C, "company") + scripts(C, ("vysoke",))
    return html

# ======================================================================
# REZIDENCE VLNITÁ
# ======================================================================
def vlnita_page(C):
    T, rel, V = C.T, C.rel, VLNITA[C.lang]; I = lambda n: f"{rel}assets/img/vlnita/{n}.webp"
    nav = [(h.replace("HOME", C.home), t) for h, t in V['nav']]
    gal = "".join(fig(I(n), a, cap, k, widths=(600, 1200, 1800)) for n, a, cap, k in V['gallery'])
    html = head(C, V['title'], V['desc'], "og-vlnita.jpg", theme="#ffffff")
    html += header(C, nav, C.home + "#projekty", V['cta_header'], nav)
    html += f"""
    <section class="hero" id="top">
      <div class="wrap hero__grid">
        <div class="hero__copy">
          <p class="sold-banner" data-reveal><i aria-hidden="true"></i>{V['banner']}</p>
          <h1 class="display">
            <span class="mask"><span class="mask__in" style="--d:.05s">{V['h1a']}</span></span>
            <span class="mask light"><span class="mask__in" style="--d:.17s">{V['h1b']}</span></span>
          </h1>
          <p class="lead" data-reveal style="--d:.35s">{V['lead']}</p>
          <div class="hero__cta" data-reveal style="--d:.45s">
            <a class="btn" href="{C.home}ke-schodum/"><span>{T['ks']}</span><i class="arrow" aria-hidden="true">→</i></a>
            <a class="btn btn--ghost" href="{C.home}do-ctvrti/"><span>{T['dc']}</span></a>
          </div>
        </div>
        <div class="hero__art" style="margin-right:0">{img(I('foto-02'), V['hero_alt'], widths=(600, 1200, 1800), sizes='(max-width: 880px) 100vw, 55vw', lazy=False)}</div>
      </div>
      <div class="wrap hero__meta">
        <dl class="meta">{"".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in V['meta'])}</dl>
        <a class="scroll-cue" href="#pribeh"><span>{T['down']}</span><i aria-hidden="true"></i></a>
      </div>
    </section>

    <section class="section dark" id="pribeh" aria-labelledby="pribeh-title">
      <div class="wrap">
        <p class="eyebrow" data-reveal><span>01</span> {V['s1']}</p>
        <h2 class="manifest" id="pribeh-title" data-reveal>{V['manifest']}</h2>
        <div class="split" style="margin-top:clamp(3rem,7vw,6rem)" data-reveal>
          <div class="split__media">{img(I('foto-13'), V['split_alt'], widths=(600, 1200, 1800), sizes='(max-width: 880px) 100vw, 58vw')}</div>
          <div class="split__copy"><h3>{V['split_h']}</h3><p>{V['split_p']}</p></div>
        </div>
      </div>
    </section>

    <section class="section" id="galerie" aria-labelledby="gal-title">
      <div class="wrap">
        <p class="eyebrow" data-reveal><span>02</span> {V['s2']}</p>
        <div class="gallery" aria-label="{T['photos_aria']}">{gal}</div>
        <p class="note" style="margin-top:1rem">{V['gal_note']}</p>
        <div data-reveal style="margin-top:clamp(2rem,5vw,4rem);display:flex;gap:.75rem;flex-wrap:wrap">
          <a class="btn" href="{C.home}ke-schodum/"><span>{V['cta_now']}</span><i class="arrow" aria-hidden="true">→</i></a>
          <a class="btn btn--ghost" href="{C.home}do-ctvrti/"><span>{V['cta_dc']}</span></a>
        </div>
      </div>
    </section>
"""
    html += footer(C, "company") + scripts(C, ("vlnita",))
    return html

# ======================================================================
# OCHRANA OSOBNÍCH ÚDAJŮ
# ======================================================================
def legal_page(C):
    T, V = C.T, LEGAL[C.lang]
    nav = [(h.replace("HOME", C.home), t) for h, t in V['nav']]
    html = head(C, V['title'], V['desc'], "og.jpg", theme="#ffffff", extra_head='\n  <meta name="robots" content="noindex, follow">')
    html += header(C, nav, C.home + "#kontakt", V['cta_header'], nav)
    html += f"""
    <section class="section legal" id="top">
      <div class="wrap">
        <p class="eyebrow" data-reveal>{V['eyebrow']}</p>
        <h1 class="display display--md"><span class="mask"><span class="mask__in" data-in>{V['h'][0]}</span></span><span class="mask light"><span class="mask__in" data-in style="--d:.12s">{V['h'][1]}</span></span></h1>
        <div class="legal__body" data-reveal>
          <p class="lead">{V['lead']}</p>
{V['body']}
        </div>
      </div>
    </section>
"""
    html += footer(C, "company") + scripts(C, ())
    return html

# ======================================================================
# 404 (GitHub Pages ji použije pro každou neexistující adresu; cesty se dopočítají v JS)
# ======================================================================
def notfound_page():
    with open(os.path.join(ROOT, "assets/img/logo/nk-logo-nad-sebou-bile.svg"), encoding="utf-8") as f:
        logo = f.read().replace('width="297.85" height="249.3"', 'width="140" height="117"')
    N = NOTFOUND
    return f"""<!doctype html>
<html lang="cs">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{N['cs']['title']}</title>
  <meta name="robots" content="noindex">
  <style>
    html{{background:#000;color:#fff}}
    body{{margin:0;min-height:100svh;display:grid;place-items:center;font-family:Manrope,system-ui,-apple-system,"Segoe UI",sans-serif;-webkit-font-smoothing:antialiased}}
    main{{text-align:center;padding:2rem 1rem;max-width:36rem}}
    svg{{margin-bottom:2.5rem}}
    h1{{font-size:clamp(2.2rem,7vw,4.5rem);font-weight:800;letter-spacing:-.04em;line-height:.95;margin:0 0 1rem}}
    h1 span{{display:block;font-weight:300}}
    p{{color:#bdbdb8;font-size:1.05rem;line-height:1.55;margin:0 0 .5rem}}
    p.alt{{font-size:.9rem;color:#8a8a85}}
    nav{{margin-top:2rem}}
    a{{display:inline-block;color:#000;background:#fff;text-decoration:none;font-weight:800;padding:.95rem 1.6rem;letter-spacing:-.01em}}
    a+a{{background:transparent;color:#fff;border:1px solid #fff;margin-left:.5rem}}
  </style>
</head>
<body>
  <main>
    {logo}
    <h1>{N['cs']['h1']}<span>{N['cs']['h2']}</span></h1>
    <p>{N['cs']['p']}</p>
    <p class="alt" lang="en">{N['en']['h1']} {N['en']['h2']} {N['en']['p']}</p>
    <p class="alt" lang="de">{N['de']['h1']} {N['de']['h2']} {N['de']['p']}</p>
    <nav><a id="home" href="/">{N['cs']['home']}</a><a id="ks" href="/ke-schodum/">{N['cs']['ks']}</a></nav>
  </main>
  <script>
    (function(){{var r=location.pathname.indexOf('/nicoandkai-web/')===0?'/nicoandkai-web/':'/';var l=/^\\/(nicoandkai-web\\/)?(en|de)\\//.exec(location.pathname);var h=r+(l?l[2]+'/':'');document.getElementById('home').href=h;document.getElementById('ks').href=h+'ke-schodum/';
    var s=document.createElement('style');s.textContent='@font-face{{font-family:Manrope;src:url('+r+'assets/fonts/Manrope-Variable.woff2) format("woff2");font-weight:200 800;font-display:swap}}';document.head.appendChild(s);}})();
  </script>
</body>
</html>
"""

def sitemap_xml():
    pri = {"home": "1.0", "ke-schodum": "0.9", "do-ctvrti": "0.9", "vysoke": "0.7", "vlnita": "0.4"}
    out = ""
    for key in ["home", "ke-schodum", "do-ctvrti", "vysoke", "vlnita"]:
        for lang in LANGS:
            loc = f"{SITE_URL}/{LANG_META[lang]['prefix']}{page_path(lang, key)}"
            alts = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{SITE_URL}/{LANG_META[l]["prefix"]}{page_path(l, key)}"/>' for l in LANGS)
            out += f"  <url><loc>{loc}</loc>{alts}<changefreq>weekly</changefreq><priority>{pri[key] if lang == 'cs' else str(round(float(pri[key]) - 0.1, 1))}</priority></url>\n"
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n{out}</urlset>\n'

# ======================================================================
# ÚVOD
# ======================================================================
def home_page(C):
    T, rel, H = C.T, C.rel, HOME[C.lang]; I = lambda p: f"{rel}assets/img/{p}.webp"
    def card(href, image, alt, badge, live, title_a, title_b, meta, text, cta, sold=False, widths=None):
        return f"""          <a class="pcard2{' pcard2--sold' if sold else ''}" href="{C.home}{href}" data-reveal>
            <div class="pcard2__media"><span class="pcard2__badge{' is-live' if live else ''}{' is-sold' if sold else ''}"><i aria-hidden="true"></i>{badge}</span>{img(I(image), alt, widths, '(max-width: 880px) 100vw, 50vw')}</div>
            <div class="pcard2__body">
              <h3 class="pcard2__title">{title_a} <span class="light">{title_b}</span></h3>
              <p class="pcard2__meta">{"".join(f"<span>{m}</span>" for m in meta)}</p>
              <p class="pcard2__text">{text}</p>
              <span class="pcard2__cta">{cta} <i aria-hidden="true">→</i></span>
            </div>
          </a>
"""
    cards = "".join(card(h, im, a, b, live, ta, tb, m, t, cta, sold) for h, im, a, b, live, ta, tb, m, t, cta, sold in H['cards'])
    numbers = "".join(f'<div data-reveal style="--d:.{i}s"><strong><span data-count="{n}">{n}</span>{("<small>" + u + "</small>") if u else ""}</strong><span>{l}</span></div>' for i, (n, u, l) in enumerate(H['numbers']))
    hows = ""
    for i, (im, a, h3, p) in enumerate(H['how']):
        hows += f"""        <div class="split{' split--flip' if i % 2 else ''}" data-reveal>
          <div class="split__media">{img(I(im), a, sizes='(max-width: 880px) 100vw, 58vw')}</div>
          <div class="split__copy"><h3>{h3}</h3><p>{p}</p></div>
        </div>
"""
    refs = ""
    for i, (href, im, a, ta, tb, text, cta, sold) in enumerate(H['ref_cards']):
        refs += f"""          <a class="pcard2{' pcard2--sold' if sold else ''}" href="{C.home}{href}" data-reveal{' style="--d:.1s"' if i else ''}>
            <div class="pcard2__media">{img(I(im), a, None, '(max-width: 880px) 100vw, 50vw')}</div>
            <div class="pcard2__body"><h3 class="pcard2__title">{ta} <span class="light">{tb}</span></h3><p class="pcard2__text">{text}</p><span class="pcard2__cta">{cta} <i aria-hidden="true">→</i></span></div>
          </a>
"""
    html = head(C, H['title'], H['desc'], "og.jpg", extra_head=f"""
  <script type="application/ld+json">
  {{"@context": "https://schema.org", "@type": "Organization", "name": "Nico & Kai Development", "description": "{H['org_desc']}", "areaServed": "Česká republika", "url": "{SITE_URL}/"}}
  </script>""")
    html += f"""  <div class="splash" aria-hidden="true"><img src="{rel}assets/img/logo/nk-logo-nad-sebou-bile.svg" alt=""><div class="splash__bar"><i></i></div></div>
"""
    html += header(C, H['nav'], C.home + "ke-schodum/", H['cta_header'], H['nav'])
    html += f"""
    <!-- ============ HERO ============ -->
    <section class="hero-media dark" id="top" data-atmo="mist">
      <div class="hero-media__bg is-slides">
        {img(I('do-ctvrti/bddc_01a'), 'Rezidence Do Čtvrti', sizes='100vw', lazy=False)}
        {img(I('ke-schodum/bdks_19'), 'Rezidence ke Schodům', sizes='100vw')}
        {video(rel, 'do-ctvrti')}{video(rel, 'ke-schodum')}
      </div>
      <canvas class="hero-media__atmo" aria-hidden="true"></canvas>
      <div class="wrap hero-media__body">
        <p class="eyebrow" data-reveal>{H['eyebrow']}</p>
        <h1 class="display">
          <span class="mask"><span class="mask__in" style="--d:.05s">{H['h1a']}</span></span>
          <span class="mask light"><span class="mask__in" style="--d:.17s">{H['h1b']}</span></span>
        </h1>
        <p class="lead" data-reveal style="--d:.35s">{H['lead']}</p>
        <div class="hero__cta" data-reveal style="--d:.45s">
          <a class="btn" href="#projekty"><span>{H['cta1']}</span><i class="arrow" aria-hidden="true">→</i></a>
          <a class="btn btn--ghost" href="{C.home}ke-schodum/"><span>{H['cta2']}</span></a>
        </div>
      </div>
      <div class="wrap hero-media__meta">
        <dl class="meta">{"".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in H['meta'])}</dl>
        <a class="scroll-cue" href="#manifest"><span>{T['down']}</span><i aria-hidden="true"></i></a>
      </div>
    </section>

    <!-- ============ MANIFEST ============ -->
    <section class="section" id="manifest" aria-labelledby="manifest-title">
      <div class="wrap">
        <p class="eyebrow" data-reveal><span>01</span> {H['s1']}</p>
        <h2 class="manifest" id="manifest-title" data-reveal>{H['manifest']}</h2>
        <div class="numbers">{numbers}</div>
      </div>
    </section>

    <!-- ============ PROJEKTY ============ -->
    <section class="section dark" id="projekty" aria-labelledby="projects-title">
      <div class="wrap">
        <p class="eyebrow" data-reveal><span>02</span> {H['s2']}</p>
        <div class="section-head" data-reveal>
          <h2 class="display display--md" id="projects-title"><span class="mask"><span class="mask__in" data-in>{H['projects_h'][0]}</span></span><span class="mask light"><span class="mask__in" data-in style="--d:.12s">{H['projects_h'][1]}</span></span></h2>
          <p>{H['projects_p']}</p>
        </div>
        <div class="pgrid">
{cards}        </div>
      </div>
    </section>

    <!-- ============ JAK STAVÍME ============ -->
    <section class="section" id="pristup" aria-labelledby="pristup-title">
      <div class="wrap" style="display:grid;gap:clamp(3rem,8vw,7rem)">
        <div>
          <p class="eyebrow" data-reveal><span>03</span> {H['s3']}</p>
          <h2 class="display display--md" id="pristup-title"><span class="mask"><span class="mask__in" data-in>{H['how_h'][0]}</span></span><span class="mask light"><span class="mask__in" data-in style="--d:.12s">{H['how_h'][1]}</span></span></h2>
        </div>
{hows}      </div>
    </section>

    <!-- ============ REFERENCE + PARTNEŘI ============ -->
    <section class="section dark" id="reference" aria-labelledby="ref-title">
      <div class="wrap">
        <p class="eyebrow" data-reveal><span>04</span> {H['s4']}</p>
        <h2 class="manifest" id="ref-title" data-reveal>{H['ref_manifest']}</h2>
        <div class="partners" data-reveal>
          <div class="partners__item"><small>{H['partner_arch']}</small><img src="{rel}assets/img/partners/ja-architekti.svg" alt="JA Architekti" style="height:2rem;width:auto;filter:invert(1)"></div>
          <div class="partners__item"><small>{H['partner_sales']}</small><strong>Svoboda <span>&amp;</span> Williams</strong></div>
        </div>
        <div class="pgrid" style="margin-top:clamp(2.5rem,5vw,4rem)">
{refs}        </div>
      </div>
    </section>

{form(C, "Nico & Kai Development", False, False, H['form_h'], H['form_lead'], (), T['send'], eyebrow=("05", H['s5'])).replace('id="rezervace"', 'id="kontakt"')}
"""
    html += footer(C, "company") + scripts(C, ())
    return html

# ======================================================================
# VÝSTUP
# ======================================================================
pages = {"404.html": notfound_page(), "sitemap.xml": sitemap_xml(), "robots.txt": f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n"}
for lang in LANGS:
    pre = LANG_META[lang]["prefix"]
    pages[f"{pre}index.html"] = home_page(Ctx(lang, "home"))
    pages[f"{pre}ke-schodum/index.html"] = project_page(Ctx(lang, "ke-schodum"), PROJECTS[lang]["ks"])
    pages[f"{pre}do-ctvrti/index.html"] = project_page(Ctx(lang, "do-ctvrti"), PROJECTS[lang]["dc"])
    pages[f"{pre}apartmany-vysoke/index.html"] = vysoke_page(Ctx(lang, "vysoke"))
    pages[f"{pre}rezidence-vlnita/index.html"] = vlnita_page(Ctx(lang, "vlnita"))
    pages[f"{pre}{LANG_META[lang]['privacy']}/index.html"] = legal_page(Ctx(lang, "privacy"))
for rel, html in pages.items():
    path = os.path.join(ROOT, rel); os.makedirs(os.path.dirname(path) or ROOT, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f: f.write(html)
    print("wrote", rel, len(html))
