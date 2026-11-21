# -*- coding: utf-8 -*-
"""Generátor stránek webu Nico & Kai Development. Spuštění: python3 tools/build-pages.py
Zapisuje index.html, ke-schodum/index.html, do-ctvrti/index.html, apartmany-vysoke/index.html, rezidence-vlnita/index.html."""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_URL = "https://nicoandkai.com"   # ostrá doména (canonical, og:url, sitemap)
PATHS = {"home": "", "ke-schodum": "ke-schodum/", "do-ctvrti": "do-ctvrti/", "vysoke": "apartmany-vysoke/", "vlnita": "rezidence-vlnita/", "gdpr": "ochrana-osobnich-udaju/"}

def img(path, alt, widths=(600, 1200, 2400), sizes="100vw", cls="", lazy=True, extra=""):
    base = path.rsplit(".", 1)[0]
    srcset = ", ".join(f"{base}-{w}.webp {w}w" for w in widths)
    mid = widths[min(1, len(widths) - 1)]
    return (f'<img{(" class=\"" + cls + "\"") if cls else ""} src="{base}-{mid}.webp" srcset="{srcset}" sizes="{sizes}" '
            f'data-full="{base}-{widths[-1]}.webp" alt="{alt}"{" loading=\"lazy\"" if lazy else " fetchpriority=\"high\""}{extra}>')

def fig(path, alt, cap="", kind="", widths=(600, 1200, 2400)):
    sizes = "(max-width: 880px) 100vw, 66vw" if kind in ("is-wide", "is-big") else "(max-width: 880px) 100vw, 33vw"
    return f'<figure{(" class=\"" + kind + "\"") if kind else ""}>{img(path, alt, widths, sizes)}{("<figcaption>" + cap + "</figcaption>") if cap else ""}</figure>'

def head(title, desc, og, rel, canonical_slug, theme="#000000", extra_css="", extra_head=""):
    return f"""<!doctype html>
<html lang="cs">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="{theme}">
  <meta name="color-scheme" content="light">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="cs_CZ">
  <meta property="og:site_name" content="Nico &amp; Kai Development">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{SITE_URL}/assets/img/{og}">
  <meta property="og:url" content="{SITE_URL}/{PATHS.get(canonical_slug, "")}">
  <link rel="canonical" href="{SITE_URL}/{PATHS.get(canonical_slug, "")}">
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
  <a class="skip" href="#obsah">Přeskočit na obsah</a>
  <div class="progress" aria-hidden="true"></div>
"""

def header(rel, nav, cta_href, cta_label, menu=None):
    menu = menu or nav
    navh = "\n".join(f'        <a href="{h}" data-nav="{h.lstrip("#").split("/")[0] or "home"}">{t}</a>' for h, t in nav)
    menuh = "\n".join(f'      <a href="{h}"><small>{i+1:02d}</small>{t}</a>' for i, (h, t) in enumerate(menu))
    return f"""  <header class="site-header" id="header">
    <div class="wrap site-header__in">
      <a class="brand" href="{rel or './'}" aria-label="Nico &amp; Kai Development – úvodní stránka">
        <img class="brand__light" src="{rel}assets/img/logo/nk-logo-horizontalni-cerne.svg" alt="Nico &amp; Kai Development" width="168" height="30">
        <img class="brand__dark" src="{rel}assets/img/logo/nk-logo-horizontalni-bile.svg" alt="" width="168" height="30" aria-hidden="true">
      </a>
      <nav class="nav" aria-label="Hlavní navigace">
{navh}
      </nav>
      <a class="btn btn--sm header-cta" href="{cta_href}"><span>{cta_label}</span></a>
      <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">
        <span class="menu-btn__label">Menu</span>
        <span class="menu-btn__icon" aria-hidden="true"><i></i><i></i></span>
      </button>
    </div>
  </header>

  <div class="menu" id="menu" hidden>
    <nav class="wrap menu__nav" aria-label="Mobilní navigace">
{menuh}
    </nav>
  </div>

  <main id="obsah">
"""

def footer(rel, legal_prefix="company", extra_note=""):
    return f"""  </main>

  <footer class="footer dark">
    <div class="wrap">
      <div class="footer__top">
        <a class="brand" href="{rel or './'}" aria-label="Nico &amp; Kai Development – úvodní stránka">
          <img src="{rel}assets/img/logo/nk-logo-horizontalni-bile.svg" alt="Nico &amp; Kai Development" width="168" height="30">
        </a>
        <nav class="footer__nav" aria-label="Patička">
          <a href="{rel}ke-schodum/">Rezidence ke Schodům</a>
          <a href="{rel}do-ctvrti/">Rezidence Do Čtvrti</a>
          <a href="{rel}apartmany-vysoke/">Apartmány Vysoké</a>
          <a href="{rel}rezidence-vlnita/">Rezidence Vlnitá</a>
          <a href="{rel}ochrana-osobnich-udaju/">Ochrana osobních údajů</a>
        </nav>
      </div>

      <div class="partners">
        <div class="partners__item"><small>Architektura</small><img src="{rel}assets/img/partners/ja-architekti.svg" alt="JA Architekti" style="height:1.6rem;width:auto;filter:invert(1)"></div>
      </div>

      <ul class="legal-list" data-cfg-group>
        <li data-cfg-wrap="{legal_prefix}.legalName"><span>Společnost</span><span data-cfg="{legal_prefix}.legalName"></span></li>
        <li data-cfg-wrap="{legal_prefix}.ico"><span>IČO</span><span data-cfg="{legal_prefix}.ico"></span></li>
        <li data-cfg-wrap="{legal_prefix}.dic"><span>DIČ</span><span data-cfg="{legal_prefix}.dic"></span></li>
        <li data-cfg-wrap="{legal_prefix}.address"><span>Sídlo</span><span data-cfg="{legal_prefix}.address"></span></li>
        <li data-cfg-wrap="company.email"><span>E-mail</span><a data-cfg="company.email" data-cfg-href="mailto:"></a></li>
        <li data-cfg-wrap="company.phone"><span>Telefon</span><a data-cfg="company.phone" data-cfg-href="tel:"></a></li>
      </ul>

      <p class="footer__note">
        Informace na&nbsp;tomto webu mají informativní charakter a&nbsp;nejsou návrhem na&nbsp;uzavření smlouvy ve&nbsp;smyslu § 1732 občanského zákoníku. Vizualizace jsou ilustrativní, plochy jsou uvedeny dle projektové dokumentace a&nbsp;mohou se změnit.{extra_note}
      </p>
      <p class="footer__copy">© <span data-year>2026</span> Nico &amp; Kai Development</p>
    </div>
    <img class="footer__mark" src="{rel}assets/img/logo/nk-monogram-bile.svg" alt="" aria-hidden="true">
  </footer>
"""

def scripts(rel, data=(), explorer=False):
    s = f'  <script src="{rel}assets/js/config.js"></script>\n'
    for d in data: s += f'  <script src="{rel}assets/data/{d}.js"></script>\n'
    s += f'  <script src="{rel}assets/js/main.js"></script>\n'
    if explorer: s += f'  <script src="{rel}assets/js/explorer.js"></script>\n'
    s += f'  <script src="{rel}assets/js/site.js"></script>\n</body>\n</html>\n'
    return s

def form(project, with_unit=True, extras=True, title=("Zarezervujte si", "svůj byt."), lead="", how=(), submit="Odeslat žádost o rezervaci", eyebrow=("05", "Rezervace"), rel="../"):
    unit = """            <div class="field field--select">
              <span>Byt</span>
              <select name="unit" aria-label="Byt"><option value="">Zatím nevím / obecný dotaz</option></select>
            </div>
""" if with_unit else ""
    ex = """            <div class="extras">
              <label class="check"><input type="checkbox" name="parking"><span class="check__box" aria-hidden="true"></span><span class="check__text">Mám zájem o garážové stání</span></label>
              <label class="check"><input type="checkbox" name="cellar"><span class="check__box" aria-hidden="true"></span><span class="check__text">Mám zájem o sklep</span></label>
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
              <li data-cfg-wrap="company.email"><span>E-mail</span><a data-cfg="company.email" data-cfg-href="mailto:"></a></li>
              <li data-cfg-wrap="company.phone"><span>Telefon</span><a data-cfg="company.phone" data-cfg-href="tel:"></a></li>
            </ul>
          </div>
          <form class="form js-lead-form" id="contact-form" data-project="{project}" novalidate data-reveal>
{unit}{ex}            <div class="field"><input id="f-name" name="name" type="text" autocomplete="name" placeholder=" " required><label for="f-name">Jméno a&nbsp;příjmení</label></div>
            <div class="field"><input id="f-email" name="email" type="email" autocomplete="email" placeholder=" " required><label for="f-email">E-mail</label></div>
            <div class="field"><input id="f-phone" name="phone" type="tel" autocomplete="tel" placeholder=" "><label for="f-phone">Telefon <span>(volitelné)</span></label></div>
            <div class="field"><textarea id="f-msg" name="message" rows="3" placeholder=" "></textarea><label for="f-msg">Zpráva <span>(volitelné)</span></label></div>
            <div class="hp" aria-hidden="true"><label>Nevyplňujte <input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
            <label class="check">
              <input type="checkbox" name="consent" required>
              <span class="check__box" aria-hidden="true"></span>
              <span class="check__text">Souhlasím se <a href="{rel}ochrana-osobnich-udaju/" target="_blank" rel="noopener">zpracováním osobních údajů</a> za&nbsp;účelem odpovědi na&nbsp;můj dotaz a&nbsp;zasílání informací o&nbsp;projektu.</span>
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

def explorer_block(slug, plan_note, cad_note):
    return f"""        <div class="ex" data-reveal>
          <div class="ex__stack">
            <svg id="ex-stack" role="group" aria-label="Dům po podlažích – vyberte patro"></svg>
            <ul class="ex__floors" id="ex-floors" role="tablist" aria-label="Podlaží"></ul>
          </div>
          <div class="ex__main">
            <div class="ex__plan">
              <div class="ex__planhead">
                <h3 id="ex-floor-title">Podlaží</h3>
                <button class="link" type="button" id="ex-cad">Půdorys z&nbsp;projektu ↗</button>
              </div>
              <div class="ex__planbox"><svg id="ex-plan" role="group"></svg></div>
              <p class="ex__note" id="ex-note">{plan_note}</p>
            </div>
            <aside class="ex__detail" id="ex-detail" aria-live="polite"></aside>
          </div>
        </div>

        <div class="units-wrap" data-reveal>
          <h3>Přehled bytů</h3>
          <table id="ex-table">
            <thead><tr><th scope="col">Byt</th><th scope="col">Podlaží</th><th scope="col">Dispozice</th><th scope="col">Plocha</th><th scope="col">Terasa</th><th scope="col">Celkem</th><th scope="col">Cena</th><th scope="col">Stav</th><th scope="col"><span class="sr-only">Detail</span></th></tr></thead>
            <tbody></tbody>
          </table>
          <p class="units-note" id="ex-areanote"></p>
        </div>

        <dialog class="dialog" id="ex-dialog" aria-labelledby="ex-dialog-title">
          <div class="dialog__bar">
            <strong class="dialog__title" id="ex-dialog-title">Půdorys</strong>
            <button class="link" type="button" data-dialog-close>Zavřít ✕</button>
          </div>
          <div class="dialog__body"><img alt="" src=""></div>
          <p class="dialog__note">{cad_note}</p>
        </dialog>
"""

# ======================================================================
# PROJEKTOVÉ STRÁNKY (Ke Schodům, Do Čtvrti)
# ======================================================================
def project_page(c):
    rel = "../"; I = lambda n: f"{rel}assets/img/{c['slug']}/{n}.webp"
    nav = [("#dum", "Dům"), ("#galerie", "Galerie"), ("#byty", "Byty"), ("#cenik", "Ceník"), ("#rezervace", "Rezervace")]
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
    html = head(c["title"], c["desc"], c["og"], rel, c["slug"], extra_head=f"""
  <script type="application/ld+json">
  {{"@context": "https://schema.org", "@type": "ApartmentComplex", "name": "{c['name']}", "description": "{c['desc']}",
   "numberOfAccommodationUnits": {c['units']}, "address": {{"@type": "PostalAddress", "streetAddress": "{c['street']}", "addressLocality": "Praha", "postalCode": "143 00", "addressCountry": "CZ"}}}}
  </script>""")
    html += header(rel, nav, "#byty", "Vybrat byt", nav + [(rel, "Všechny projekty")])
    html += f"""
    <!-- ============ HERO ============ -->
    <section class="hero-media dark" id="top">
      <div class="hero-media__bg">{img(I(c['hero']), c['hero_alt'], sizes="100vw", lazy=False)}</div>
      <div class="wrap hero-media__body">
        <p class="chip" data-reveal><i aria-hidden="true"></i>{c['stage']} · stavební řízení zahájeno</p>
        <h1 class="display">
          <span class="mask"><span class="mask__in" style="--d:.05s">{c['h1a']}</span></span>
          <span class="mask light"><span class="mask__in" style="--d:.17s">{c['h1b']}</span></span>
        </h1>
        <p class="lead" data-reveal style="--d:.35s">{c['lead']}</p>
        <div class="hero__cta" data-reveal style="--d:.45s">
          <a class="btn" href="#byty"><span>Vybrat byt</span><i class="arrow" aria-hidden="true">→</i></a>
          <a class="btn btn--ghost" href="#cenik"><span>Ceník a rezervace</span></a>
        </div>
      </div>
      <div class="wrap hero-media__meta">
        <dl class="meta">{"".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in c['meta'])}</dl>
        <a class="scroll-cue" href="#dum"><span>Dolů</span><i aria-hidden="true"></i></a>
      </div>
      <p class="hero-media__credit">Vizualizace · JA Architekti</p>
    </section>

    <!-- ============ DŮM ============ -->
    <section class="section" id="dum" aria-labelledby="dum-title">
      <div class="wrap">
        <p class="eyebrow" data-reveal><span>01</span> Dům</p>
        <h2 class="manifest" id="dum-title" data-reveal>{c['manifest']}</h2>
        <div class="numbers">{"".join(f'<div data-reveal style="--d:.{i}s"><strong><span data-count="{n}">{n}</span>{("<small>" + u + "</small>") if u else ""}</strong><span>{l}</span></div>' for i, (n, u, l) in enumerate(c['numbers']))}</div>
      </div>
    </section>

    <!-- ============ GALERIE ============ -->
    <section class="section section--tight" id="galerie" aria-labelledby="gal-title" style="padding-top:0">
      <div class="wrap">
        <div class="section-head" data-reveal>
          <h2 class="display display--md" id="gal-title"><span class="mask"><span class="mask__in" data-in>{c['gal_h'][0]}</span></span><span class="mask light"><span class="mask__in" data-in style="--d:.12s">{c['gal_h'][1]}</span></span></h2>
          <p>{c['gal_p']}</p>
        </div>
        <div class="gallery" aria-label="Galerie vizualizací">{gal}</div>
        <p class="note" style="margin-top:1rem">Vizualizace JA Architekti. Zařízení interiéru je ilustrativní.</p>
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
        <p class="eyebrow" data-reveal><span>02</span> Byty</p>
        <div class="explorer__head">
          <h2 class="display display--md" id="byty-title">
            <span class="mask"><span class="mask__in" data-in>Vyberte si</span></span>
            <span class="mask light"><span class="mask__in" data-in style="--d:.12s">svůj byt.</span></span>
          </h2>
          <p class="legend" aria-label="Legenda">
            <span><i class="lg-available"></i>Volný</span>
            <span><i class="lg-reserved"></i>Rezervovaný</span>
            <span><i class="lg-sold"></i>Prodaný</span>
          </p>
        </div>

        <div class="facade" data-facade="{c['slug']}" data-reveal>
          <img class="facade__img" src="{I(c['facade'])[:-5]}-2400.webp" srcset="{I(c['facade'])[:-5]}-1200.webp 1200w, {I(c['facade'])[:-5]}-2400.webp 2400w" sizes="(max-width: 1520px) 100vw, 1520px" width="2528" height="1696" alt="{c['facade_alt']}">
          <span class="facade__hint">Najeďte myší na byt</span>
        </div>
        <p class="facade__legend" data-reveal><span class="lg-available"><i></i>Volný</span><span class="lg-reserved"><i></i>Rezervovaný</span><span class="lg-sold"><i></i>Prodaný</span><span>Kliknutím otevřete detail bytu a půdorys</span></p>

{explorer_block(c['slug'], c['plan_note'], c['cad_note'])}
      </div>
    </section>

    <!-- ============ CENÍK A REZERVACE ============ -->
    <section class="section dark" id="cenik" aria-labelledby="cenik-title">
      <div class="wrap">
        <p class="eyebrow" data-reveal><span>03</span> Ceník</p>
        <div class="reserve-head">
          <div>
            <h2 class="display display--md" id="cenik-title">
              <span class="mask"><span class="mask__in" data-in>Rezervace</span></span>
              <span class="mask light"><span class="mask__in" data-in style="--d:.12s">s výhodou.</span></span>
            </h2>
          </div>
          <div><p class="lead" data-reveal>Byty prodáváme v&nbsp;průběhu stavebního řízení. Kdo se rozhodne teď, získá slevu z&nbsp;ceny bytu podle výše složené zálohy. Záloha se započítává do kupní ceny.</p></div>
        </div>

        <dl class="price-extras" data-extras="{c['slug']}" data-reveal></dl>

        <div class="reserve-table-wrap" data-reservation="{c['slug']}" data-reveal></div>
        <p class="note" style="margin-top:1rem"><span data-if-prices>Ceny bytů jsou uvedeny bez garážového stání a&nbsp;sklepu, které lze přikoupit. Cena po slevě se zaokrouhluje na tisíce Kč. </span><span data-if-no-prices>Ceník bytů, garážových stání a&nbsp;sklepů vám pošleme na vyžádání, stačí vyplnit formulář níže. Sleva se počítá z&nbsp;ceny bytu. </span>{c['price_note']}</p>

        <ol class="reserve-terms" data-reveal>
          <li><strong>Vyberete byt a&nbsp;složíte zálohu</strong><p>3, 4 nebo 5&nbsp;mil.&nbsp;Kč podle toho, jakou slevu chcete získat. Záloha je součástí kupní ceny.</p></li>
          <li><strong>Sleva je sjednaná ve smlouvě</strong><p>Sleva 3, 4 nebo 5&nbsp;% z&nbsp;ceny bytu se promítne do rezervační a&nbsp;následně kupní smlouvy.</p></li>
          <li><strong>Jistota vrácení zálohy</strong><p>Pokud stavební povolení nenabude právní moci do <strong data-reservation-deadline>31. 10. 2028</strong>, vrátíme vám zálohu v&nbsp;plné výši. Způsob uložení zálohy upravuje rezervační smlouva.</p></li>
        </ol>
        <div data-reveal style="margin-top:2.5rem"><a class="btn btn--light" href="#rezervace"><span>Rezervovat byt</span><i class="arrow" aria-hidden="true">→</i></a></div>
      </div>
    </section>

    <!-- ============ TECHNOLOGIE ============ -->
    <section class="section" id="technologie" aria-labelledby="tech-title">
      <div class="wrap">
        <p class="eyebrow" data-reveal><span>04</span> Standard</p>
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
        <p class="eyebrow" data-reveal><span>05</span> Lokalita</p>
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

{form(c['name'], True, True, ("Rezervujte si", "svůj byt."), "Vyplňte krátký formulář. Ozveme se vám, projdeme detaily a&nbsp;připravíme rezervační smlouvu.", ("Vyberete byt a&nbsp;odešlete nezávaznou žádost.", "Ozveme se vám, projdeme podmínky a&nbsp;výši zálohy.", "Po podpisu rezervační smlouvy je byt váš."), eyebrow=("06", "Rezervace"))}
"""
    html += footer(rel, f"projects.{c['slug']}.seller", c.get("footnote", "")) + scripts(rel, (c["slug"],), explorer=True)
    return html

KS = dict(
    slug="ke-schodum", name="Rezidence ke Schodům", street="Ke Schodům", units=8,
    title="Rezidence ke Schodům | Nico &amp; Kai Development", og="og-ke-schodum.jpg",
    desc="Osm bytů s velkými terasami a zahradami v Praze-Modřanech. Pohledový beton, dřevo, tepelná čerpadla a fotovoltaika. Předprodej zahájen.",
    hero="bdks_22", hero_alt="Rezidence ke Schodům – zahradní průčelí za soumraku", stage="Předprodej zahájen",
    h1a="Rezidence", h1b="ke&nbsp;Schodům",
    lead="Osm bytů, osm teras a&nbsp;zahrad. Dům v&nbsp;klidné části Modřan, kde se bydlí uvnitř i&nbsp;venku.",
    meta=[("Lokalita", "Praha-Modřany"), ("Byty", "8 · 2+kk a 3+kk"), ("Terasy", "19–104&nbsp;m²"), ("Dokončení", "2. čtvrtletí 2028")],
    manifest="Každý byt má svou <strong>zahradu nebo terasu</strong>. Materiály, které stárnou krásně: <strong>pohledový beton, dřevo a&nbsp;sklo</strong>. A&nbsp;dům, který si energii vyrábí sám.",
    numbers=[("8", "", "bytů 2+kk a 3+kk"), ("104", "m²", "největší terasa"), ("16", "", "garážových stání"), ("2028", "", "dokončení stavby")],
    gal_h=("Dům, který", "chcete vidět zblízka."),
    gal_p="Tři nadzemní podlaží s&nbsp;ustupujícími terasami, vegetační střechy a&nbsp;fasáda z&nbsp;patinovaného plechu, která mění barvu se světlem.",
    gallery=[("bdks_13", "Rezidence ke Schodům z ulice", "Pohled z ulice", "is-big"), ("bdks_18", "Detail fasády a velkoformátových oken", "Detail fasády", ""), ("bdks_10", "Zahradní strana domu se zelení", "Zahrada", ""),
             ("bdks_07", "Nároží domu se stromy", "Nároží", ""), ("bdks_19", "Dům za soumraku", "Soumrak", "is-wide"), ("bdks_09", "Dům v zimě", "Zima", ""),
             ("bdks_03", "Vstup do domu", "Vstup", ""), ("bdks_20", "Severní strana s pavlačí", "Pavlač a vstupy do bytů", "is-wide"), ("bdks_08", "Večerní pohled na roh domu", "Večer", "")],
    splits=[("bdks_10", "Terasy a zahrady Rezidence ke Schodům", "Terasa jako další pokoj.", "<p>Byty v&nbsp;přízemí mají vlastní zahradu, byty v&nbsp;patrech terasy od 25 do 104&nbsp;m². Dřevěná paluba, zeleň na střechách a&nbsp;skleněné zábradlí. Venku strávíte víc času, než jste čekali.</p>"),
            ("bdks_18", "Detail fasády z patinovaného plechu", "Materiály, které stárnou krásně.", "<p>Fasáda z&nbsp;plechových panelů s&nbsp;přiznanými spárami mění barvu během dne. Uvnitř pohledový beton, třívrstvé dřevěné podlahy a&nbsp;minerální stěrky. Nic, co by se za pár let muselo předělávat.</p>"),
            ("bdks_20", "Pavlač na severní straně domu", "Soukromí na prvním místě.", "<p>Do bytů se vchází z&nbsp;otevřených pavlačí na severní straně. Obytné místnosti a&nbsp;terasy míří na jih, do zahrady. Mezi byty je železobetonová stěna, sousedy neuslyšíte.</p>")],
    facade="bdks_02", facade_alt="Jižní průčelí Rezidence ke Schodům – vyberte byt najetím myší",
    plan_note="Schematický půdorys. Plochy a&nbsp;dispozice dle projektové dokumentace (12/2025), závazné jsou údaje z&nbsp;prohlášení vlastníka.",
    cad_note="Půdorys z projektové dokumentace pro povolení stavby (12/2025). Vybavení a zařízení je ilustrativní.",
    price_note="Plocha bytu je uvedena jako odhad podlahové plochy dle nařízení vlády č. 366/2013 Sb., závazná bude v&nbsp;prohlášení vlastníka.",
    tech_h=("Dům, který", "šetří energii."),
    tech=[("Energie", ["Kaskáda tepelných čerpadel vzduch–voda", "Fotovoltaická elektrárna na střeše, bateriové úložiště", "Podlahové vytápění a&nbsp;chlazení", "Bez plynové přípojky"]),
          ("Konstrukce a&nbsp;interiér", ["Železobetonová konstrukce, pohledový beton", "Třívrstvé dřevěné podlahy, minerální stěrky", "Velkoformátové zasklení, hliníková okna", "Stěny mezi byty Rw 57–58&nbsp;dB"]),
          ("Dům", ["Výtah z&nbsp;garáže do všech podlaží", "16 garážových stání, 8 sklepů", "Vegetační střechy a&nbsp;společná střešní terasa", "Příprava na nabíjení elektromobilů"])],
    tech_note="Údaje vycházejí z&nbsp;projektové dokumentace pro povolení stavby (12/2025). Finální provedení, dispozice a&nbsp;plochy se mohou změnit.",
    lok_h=("Modřany,", "klid u Vltavy."),
    lok_p="Vilová čtvrť nad Vltavou. Pět minut k&nbsp;řece a&nbsp;na cyklostezku, les v&nbsp;Modřanské rokli za rohem a&nbsp;tramvají do centra bez přestupu.",
    addr=[("Adresa", "ulice Ke Schodům, Praha 12 – Modřany"), ("Katastr", "Modřany, parc. č. 1505/1"), ("Doprava", "tramvaj a&nbsp;autobus v&nbsp;docházkové vzdálenosti"), ("Příroda", "Vltava, Modřanská rokle"), ("Projektant", "JA Architekti, Ing. arch. Andrea Jašková")],
    steps=[("12/2025", "Žádost o&nbsp;stavební povolení", "Dokumentace pro povolení stavby podána.", False), ("Nyní", "Předprodej", "Rezervace se slevou až 5&nbsp;%.", True), ("1. čtvrtletí 2027", "Zahájení výstavby", "Předpokládaný začátek stavby.", False), ("2. čtvrtletí 2028", "Dokončení", "Předpokládané předání bytů.", False)],
)

DC = dict(
    slug="do-ctvrti", name="Rezidence Do Čtvrti", street="Do čtvrti 1145/20", units=6,
    title="Rezidence Do Čtvrti | Nico &amp; Kai Development", og="og-do-ctvrti.jpg",
    desc="Šest bytů v nárožním domě v Praze-Modřanech. Zahrady, balkony a střešní terasy, garáž a sklepy. Předprodej zahájen.",
    hero="bddc_01a", hero_alt="Rezidence Do Čtvrti – nárožní dům za soumraku", stage="Předprodej zahájen",
    h1a="Rezidence", h1b="Do&nbsp;Čtvrti",
    lead="Šest bytů v&nbsp;domě se zaoblenými rohy a&nbsp;fasádou z&nbsp;perforovaného zdiva. Vždy jen dva byty na podlaží.",
    meta=[("Lokalita", "Praha-Modřany"), ("Byty", "6 · 2+kk a 3+kk"), ("Venkovní prostory", "zahrady, balkony, terasy"), ("Souhlas IPR", "19. 10. 2026")],
    manifest="Dům pro <strong>šest domácností</strong>. Přízemí se zahradou, patro s&nbsp;balkony, střecha s&nbsp;terasami. <strong>Vlastní výtah</strong> až do garáže a&nbsp;sousedé, které znáte jménem.",
    numbers=[("6", "", "bytů 2+kk a 3+kk"), ("2", "", "byty na každém podlaží"), ("7", "", "garážových stání"), ("91", "m²", "největší zahrada")],
    gal_h=("Jemné křivky,", "pevný charakter."),
    gal_p="Nároží ulic Do čtvrti a&nbsp;Malá Tyršovka. Ustupující poslední podlaží, zaoblené rohy a&nbsp;zábradlí z&nbsp;perforovaných cihel, které propouští světlo i&nbsp;soukromí.",
    gallery=[("bddc_03", "Rezidence Do Čtvrti – nároží za dne", "Nároží", "is-big"), ("bddc_int_01", "Obývací pokoj s kuchyní", "Obývací pokoj", ""), ("bddc_int_02", "Ložnice", "Ložnice", ""),
             ("bddc_05a", "Vstupní průčelí ze severu při západu slunce", "Vstup z ulice", ""), ("bddc_16", "Zahradní průčelí zblízka", "Zahrada", "is-wide"), ("bddc_int_04", "Koupelna", "Koupelna", ""),
             ("bddc_09", "Dům z nadhledu za soumraku", "Z nadhledu", ""), ("bddc_int_05", "Jídelna s terasou", "Jídelna", "is-wide"), ("bddc_12b", "Zimní pohled s vjezdem do garáže", "Zima", "")],
    splits=[("bddc_17", "Zahradní průčelí za soumraku", "Zahrada za domem, ne za městem.", "<p>Byty v&nbsp;přízemí mají vlastní zahradu o&nbsp;84 a&nbsp;91&nbsp;m², patro balkony a&nbsp;horní byty střešní terasy přes 40&nbsp;m². Obytné místnosti jsou otočené k&nbsp;jihu, do zeleně.</p>"),
            ("bddc_int_07", "Vstupní hala s perforovanou stěnou", "Světlo skrz cihlu.", "<p>Perforované zdivo na zábradlích a&nbsp;ve vstupní hale propouští světlo a&nbsp;zároveň chrání soukromí. Uvnitř omítky v&nbsp;teplých tónech, dřevo a&nbsp;kámen.</p>"),
            ("bddc_rez", "Řez domem", "Dům v&nbsp;řezu.", "<p>Tři nadzemní podlaží, pod nimi garáž se sedmi stáními a&nbsp;ještě níž sklepy a&nbsp;technika. Výtah jezdí ze sklepa až ke dveřím bytu.</p>")],
    facade="bddc_17", facade_alt="Zahradní průčelí Rezidence Do Čtvrti – vyberte byt najetím myší",
    plan_note="Půdorys z projektové dokumentace (08/2026). Plocha bytu orientačně dle NV 366/2013 Sb. Závazné údaje budou v&nbsp;prohlášení vlastníka.",
    cad_note="Půdorys z projektové dokumentace pro povolení stavby (08/2026). Vybavení a zařízení je ilustrativní.",
    price_note="Plocha bytu je uvedena jako podlahová plocha dle nařízení vlády č. 366/2013 Sb. (orientační odhad z&nbsp;půdorysů), závazná bude v&nbsp;prohlášení vlastníka.",
    tech_h=("Šetrný dům", "s vlastní energií."),
    tech=[("Energie", ["Tepelná čerpadla vzduch–voda", "Fotovoltaická elektrárna na střeše", "Podlahové vytápění", "Bez plynové přípojky"]),
          ("Konstrukce", ["Monolitická železobetonová konstrukce", "Plochá vegetační střecha", "Hliníková okna", "Perforované cihelné zábradlí"]),
          ("Dům", ["Výtah od sklepa po střešní terasy", "7 garážových stání, 6 sklepů", "Příprava na nabíjení elektromobilů", "Klidná vilová čtvrť"])],
    tech_note="Údaje vycházejí z&nbsp;projektové dokumentace pro povolení stavby (08/2026). Stavební řízení probíhá, finální řešení, dispozice a&nbsp;plochy se mohou změnit.",
    lok_h=("Tyršova čtvrť,", "Modřany."),
    lok_p="Nárožní parcela v&nbsp;klidné vilové zástavbě s&nbsp;rodinnými domy. Les na dosah, Vltava pod kopcem, centrum tramvají.",
    addr=[("Adresa", "Do čtvrti 1145/20 a&nbsp;Malá Tyršovka, Praha 12 – Modřany"), ("Pozemek", "516&nbsp;m², parc. č. 1540, 1539/1, 1539/2"), ("Územní plán", "OB – čistě obytné, souhlas IPR Praha"), ("Příroda", "lesy nad Modřany, Vltava"), ("Projektant", "JA Architekti, Ing. arch. Andrea Jašková")],
    steps=[("08/2026", "Žádost o&nbsp;povolení stavby", "Dokumentace podána, souhlas IPR Praha 19. 10. 2026.", False), ("Nyní", "Předprodej", "Rezervace se slevou až 5&nbsp;%.", True), ("2027", "Stavební povolení", "Předpokládané nabytí právní moci.", False), ("2029", "Dokončení", "Předpokládané předání bytů.", False)],
)

# ======================================================================
# APARTMÁNY VYSOKÉ
# ======================================================================
def vysoke_page():
    rel = "../"; I = lambda n: f"{rel}assets/img/vysoke/{n}.webp"
    nav = [("#pribeh", "Apartmány"), ("#jednotky", "Volné jednotky"), ("#galerie", "Galerie"), ("#lokalita", "Lokalita"), ("#kontakt", "Kontakt")]
    gal = "".join(fig(I(n), a, cap, k, widths=w) for n, a, cap, k, w in [
        ("foto-14", "Apartmánové domy ve Vysokém nad Jizerou v zimě", "Domy v zimě", "is-big", (600, 1200, 1800)),
        ("foto-07", "Koupelna s vanou pod střešním oknem", "Koupelna", "is-tall", (600, 1200, 1800)),
        ("foto-11", "Dětský pokoj v podkroví", "Podkroví", "", (600, 1200, 1800)),
        ("foto-08", "Ložnice s trámy", "Ložnice", "", (600, 1200, 1800)),
        ("l11", "Pastviny nad Vysokým s výhledem na Krkonoše", "Výhled na Krkonoše", "is-wide", (600, 1200, 2400)),
        ("foto-09", "Koupelna se sprchou", "Koupelna", "", (600, 1200, 1800)),
        ("foto-06", "Dubové dveře a koupelna", "Detail", "", (600, 1200, 1800)),
        ("l03", "Zimní západ slunce nad krajinou", "Zimní večer", "is-wide", (600, 1200, 2400)),
        ("foto-01", "Kuchyně", "Kuchyně", "", (600, 1200, 1800)),
        ("foto-12", "Schodiště do podkroví", "Schodiště", "", (600, 1200, 1800)),
        ("l06", "Zasněžený les u Vysokého", "Zima v lese", "", (600, 1200, 2400)),
        ("l07", "Rozhledna při západu slunce", "Rozhledna", "", (600, 1200, 2400)),
    ])
    html = head("Apartmány Vysoké | Nico &amp; Kai Development", "Apartmány Vysoké nad Jizerou: dokončené horské apartmány s terasami, zahradou a jezírkem. Poslední tři jednotky A2, B1 a B2 v prodeji.", "og-vysoke.jpg", rel, "vysoke")
    html += header(rel, nav, "#kontakt", "Mám zájem", nav + [(rel, "Všechny projekty")])
    html += f"""
    <section class="hero-media dark" id="top">
      <div class="hero-media__bg">{img(I('l03'), 'Zimní západ slunce nad Vysokým nad Jizerou', sizes='100vw', lazy=False)}</div>
      <div class="wrap hero-media__body">
        <p class="chip" data-reveal><i aria-hidden="true"></i>Dokončeno · poslední 3 apartmány</p>
        <h1 class="display">
          <span class="mask"><span class="mask__in" style="--d:.05s">Apartmány</span></span>
          <span class="mask light"><span class="mask__in" style="--d:.17s">Vysoké</span></span>
        </h1>
        <p class="lead" data-reveal style="--d:.35s">Dva horské domy na kraji Vysokého nad Jizerou. Vlastní terasa, společná zahrada s&nbsp;přírodním jezírkem a&nbsp;Krkonoše na dohled.</p>
        <div class="hero__cta" data-reveal style="--d:.45s">
          <a class="btn" href="#jednotky"><span>Volné apartmány</span><i class="arrow" aria-hidden="true">→</i></a>
          <a class="btn btn--ghost" href="#galerie"><span>Galerie</span></a>
        </div>
      </div>
      <div class="wrap hero-media__meta">
        <dl class="meta"><div><dt>Lokalita</dt><dd>Vysoké nad Jizerou</dd></div><div><dt>Stav</dt><dd>Zkolaudováno</dd></div><div><dt>V nabídce</dt><dd>A2 · B1 · B2</dd></div><div><dt>Prodej</dt><dd>Svoboda &amp; Williams</dd></div></dl>
        <a class="scroll-cue" href="#pribeh"><span>Dolů</span><i aria-hidden="true"></i></a>
      </div>
    </section>

    <section class="section" id="pribeh" aria-labelledby="pribeh-title">
      <div class="wrap">
        <p class="eyebrow" data-reveal><span>01</span> Apartmány</p>
        <h2 class="manifest" id="pribeh-title" data-reveal>Místo, kam se <strong>jezdí odpočívat</strong>. Dřevo, trámy a&nbsp;střešní okna, pod nimiž se spí jinak. V&nbsp;zimě běžky od dveří, v&nbsp;létě jezírko na zahradě.</h2>
        <div class="numbers">
          <div data-reveal><strong><span data-count="2">2</span></strong><span>apartmánové domy</span></div>
          <div data-reveal style="--d:.1s"><strong><span data-count="3">3</span></strong><span>poslední volné jednotky</span></div>
          <div data-reveal style="--d:.2s"><strong><span data-count="193">193</span><small>m²</small></strong><span>apartmán B2, 5+kk</span></div>
          <div data-reveal style="--d:.3s"><strong><span data-count="700">700</span><small>m n. m.</small></strong><span>Vysoké nad Jizerou</span></div>
        </div>
      </div>
    </section>

    <section class="section dark" id="jednotky" aria-labelledby="jed-title">
      <div class="wrap">
        <p class="eyebrow" data-reveal><span>02</span> Volné jednotky</p>
        <div class="section-head" data-reveal>
          <h2 class="display display--md" id="jed-title"><span class="mask"><span class="mask__in" data-in>Poslední</span></span><span class="mask light"><span class="mask__in" data-in style="--d:.12s">tři apartmány.</span></span></h2>
          <p>Ostatní jednotky už mají své majitele. Prodej posledních tří zajišťuje realitní kancelář Svoboda &amp; Williams.</p>
        </div>
        <div class="ucards" data-units-cards="vysoke"></div>
        <div class="agent" data-reveal>
          <div class="agent__mono" aria-hidden="true">S&amp;W</div>
          <div>
            <strong>Jana Kocianová · Svoboda &amp; Williams</strong>
            <span>Prodej apartmánů A2, B1 a&nbsp;B2. <a href="https://www.svoboda-williams.com/" rel="noopener" target="_blank">svoboda-williams.com ↗</a></span>
            <span data-cfg-wrap="projects.vysoke.agent.phone"><a data-cfg="projects.vysoke.agent.phone" data-cfg-href="tel:"></a></span>
            <span data-cfg-wrap="projects.vysoke.agent.email"><a data-cfg="projects.vysoke.agent.email" data-cfg-href="mailto:"></a></span>
          </div>
        </div>
      </div>
    </section>

    <section class="section" id="galerie" aria-labelledby="gal-title">
      <div class="wrap">
        <p class="eyebrow" data-reveal><span>03</span> Galerie</p>
        <div class="section-head" data-reveal>
          <h2 class="display display--md" id="gal-title"><span class="mask"><span class="mask__in" data-in>Hory</span></span><span class="mask light"><span class="mask__in" data-in style="--d:.12s">za oknem.</span></span></h2>
          <p>Fotografie z&nbsp;dokončených apartmánů a&nbsp;z&nbsp;okolí Vysokého nad Jizerou.</p>
        </div>
        <div class="gallery" aria-label="Galerie fotografií">{gal}</div>
      </div>
    </section>

    <section class="section dark" id="lokalita" aria-labelledby="lok-title">
      <div class="wrap">
        <p class="eyebrow" data-reveal><span>04</span> Lokalita</p>
        <div class="addr">
          <div class="addr__copy">
            <h2 class="display display--md" id="lok-title"><span class="mask"><span class="mask__in" data-in>Vysoké</span></span><span class="mask light"><span class="mask__in" data-in style="--d:.12s">nad Jizerou.</span></span></h2>
            <p class="lead" data-reveal>Jedno z&nbsp;nejvýše položených měst v&nbsp;Česku na pomezí Krkonoš a&nbsp;Jizerských hor. Běžecké tratě, cyklotrasy, lyžařské vleky Šachty a&nbsp;Krakonošovo divadlo. Rokytnice a&nbsp;Harrachov za pár minut autem.</p>
          </div>
          <div class="addr__list" data-reveal>
            <div><span>Adresa</span><strong>K. Havlíčka Borovského 442/443, 512 11 Vysoké nad Jizerou</strong></div>
            <div><span>Nadmořská výška</span><strong>cca 700 m n. m.</strong></div>
            <div><span>Zima</span><strong>běžecké tratě, vleky Šachty, Rokytnice, Harrachov</strong></div>
            <div><span>Léto</span><strong>cyklotrasy, turistika, jezírko na zahradě</strong></div>
            <div><span>Ve městě</span><strong>škola, nemocnice, pekárna, restaurace, divadlo</strong></div>
          </div>
        </div>
      </div>
    </section>

{form("Apartmány Vysoké", False, False, ("Chci vědět", "víc."), "Napište nám, kterého apartmánu se váš zájem týká. Předáme ho makléřce a&nbsp;ozveme se vám.", (), "Odeslat", eyebrow=("05", "Kontakt")).replace('id="rezervace"', 'id="kontakt"')}
"""
    html += footer(rel, "company") + scripts(rel, ("vysoke",))
    return html

# ======================================================================
# REZIDENCE VLNITÁ
# ======================================================================
def vlnita_page():
    rel = "../"; I = lambda n: f"{rel}assets/img/vlnita/{n}.webp"
    nav = [("#pribeh", "O domě"), ("#galerie", "Galerie"), (rel + "#projekty", "Aktuální projekty")]
    gal = "".join(fig(I(n), a, cap, k, widths=(600, 1200, 1800)) for n, a, cap, k in [
        ("foto-02", "Rezidence Vlnitá z ulice při západu slunce", "Z ulice", "is-big"), ("foto-04", "Kuchyně s dřevěnou dýhou", "Kuchyně", "is-tall"),
        ("foto-13", "Obývací pokoj s krbem", "Obývací pokoj", "is-tall"), ("foto-05", "Kuchyně a dubové dveře", "Detail", ""), ("foto-03", "Průčelí domu", "Průčelí", "")])
    html = head("Rezidence Vlnitá | Nico &amp; Kai Development", "Rezidence Vlnitá: dokončený rezidenční projekt Nico & Kai Development v Praze. Všechny byty prodány.", "og-vlnita.jpg", rel, "vlnita", theme="#ffffff")
    html += header(rel, nav, rel + "#projekty", "Aktuální projekty", nav)
    html += f"""
    <section class="hero" id="top">
      <div class="wrap hero__grid">
        <div class="hero__copy">
          <p class="sold-banner" data-reveal><i aria-hidden="true"></i>Prodáno · dokončeno</p>
          <h1 class="display">
            <span class="mask"><span class="mask__in" style="--d:.05s">Rezidence</span></span>
            <span class="mask light"><span class="mask__in" style="--d:.17s">Vlnitá</span></span>
          </h1>
          <p class="lead" data-reveal style="--d:.35s">Dokončený dům v&nbsp;Praze. Všechny byty mají své majitele. Zůstává jako ukázka toho, jak stavíme.</p>
          <div class="hero__cta" data-reveal style="--d:.45s">
            <a class="btn" href="{rel}ke-schodum/"><span>Rezidence ke Schodům</span><i class="arrow" aria-hidden="true">→</i></a>
            <a class="btn btn--ghost" href="{rel}do-ctvrti/"><span>Rezidence Do Čtvrti</span></a>
          </div>
        </div>
        <div class="hero__art" style="margin-right:0">{img(I('foto-02'), 'Rezidence Vlnitá z ulice', widths=(600, 1200, 1800), sizes='(max-width: 880px) 100vw, 55vw', lazy=False)}</div>
      </div>
      <div class="wrap hero__meta">
        <dl class="meta"><div><dt>Lokalita</dt><dd>Praha</dd></div><div><dt>Stav</dt><dd>Prodáno, dokončeno</dd></div><div><dt>Typ</dt><dd>Rezidenční dům</dd></div></dl>
        <a class="scroll-cue" href="#pribeh"><span>Dolů</span><i aria-hidden="true"></i></a>
      </div>
    </section>

    <section class="section dark" id="pribeh" aria-labelledby="pribeh-title">
      <div class="wrap">
        <p class="eyebrow" data-reveal><span>01</span> O domě</p>
        <h2 class="manifest" id="pribeh-title" data-reveal>Čisté linie, <strong>tmavé dřevo a&nbsp;světlo</strong>. Dům, u&nbsp;kterého jsme si ověřili, že <strong>detail rozhoduje</strong>: od dubových dveří po kování.</h2>
        <div class="split" style="margin-top:clamp(3rem,7vw,6rem)" data-reveal>
          <div class="split__media">{img(I('foto-13'), 'Obývací pokoj s krbem', widths=(600, 1200, 1800), sizes='(max-width: 880px) 100vw, 58vw')}</div>
          <div class="split__copy"><h3>Co jsme si odnesli.</h3><p>Velká okna, krb a&nbsp;jeden materiál na podlaze v&nbsp;celém bytě. Méně prvků, zato lepších. Stejný přístup dnes vedeme do Rezidence ke Schodům a&nbsp;Do Čtvrti.</p></div>
        </div>
      </div>
    </section>

    <section class="section" id="galerie" aria-labelledby="gal-title">
      <div class="wrap">
        <p class="eyebrow" data-reveal><span>02</span> Galerie</p>
        <div class="gallery" aria-label="Galerie fotografií">{gal}</div>
        <p class="note" style="margin-top:1rem">Fotografie dokončeného domu.</p>
        <div data-reveal style="margin-top:clamp(2rem,5vw,4rem);display:flex;gap:.75rem;flex-wrap:wrap">
          <a class="btn" href="{rel}ke-schodum/"><span>Aktuálně v prodeji: Ke Schodům</span><i class="arrow" aria-hidden="true">→</i></a>
          <a class="btn btn--ghost" href="{rel}do-ctvrti/"><span>Do Čtvrti</span></a>
        </div>
      </div>
    </section>
"""
    html += footer(rel, "company") + scripts(rel, ("vlnita",))
    return html


# ======================================================================
# OCHRANA OSOBNÍCH ÚDAJŮ
# ======================================================================
def legal_page():
    rel = "../"
    nav = [(rel + "#projekty", "Projekty"), (rel + "ke-schodum/", "Ke Schodům"), (rel + "do-ctvrti/", "Do Čtvrti"), (rel + "#kontakt", "Kontakt")]
    html = head("Ochrana osobních údajů | Nico &amp; Kai Development", "Zásady zpracování osobních údajů na webu Nico & Kai Development.", "og.jpg", rel, "gdpr", theme="#ffffff", extra_head='\n  <meta name="robots" content="noindex, follow">')
    html += header(rel, nav, rel + "#kontakt", "Kontakt", nav)
    html += f"""
    <section class="section legal" id="top">
      <div class="wrap">
        <p class="eyebrow" data-reveal>Právní informace</p>
        <h1 class="display display--md"><span class="mask"><span class="mask__in" data-in>Ochrana</span></span><span class="mask light"><span class="mask__in" data-in style="--d:.12s">osobních údajů.</span></span></h1>
        <div class="legal__body" data-reveal>
          <p class="lead">Vážíme si vašeho zájmu o&nbsp;naše domy a&nbsp;stejně tak vašeho soukromí. Tady najdete, jaké údaje zpracováváme, proč a&nbsp;jaká máte práva.</p>

          <h2>1. Kdo údaje zpracovává</h2>
          <p>Správcem osobních údajů je <strong><span data-cfg="company.legalName">Nico &amp; Kai Development</span></strong><span data-cfg-wrap="company.ico">, IČO <span data-cfg="company.ico"></span></span><span data-cfg-wrap="company.address">, se sídlem <span data-cfg="company.address"></span></span> (dále „my“). U&nbsp;Rezidence ke Schodům je prodávajícím společnost Rezidence Ke schodům s.r.o., IČO 23662956, Ke schodům 1465/14, 143&nbsp;00 Praha 12 – Modřany, které vaši poptávku předáme.</p>
          <p data-cfg-wrap="company.email">Kontakt ve věcech osobních údajů: <a data-cfg="company.email" data-cfg-href="mailto:"></a>.</p>

          <h2>2. Jaké údaje zpracováváme</h2>
          <ul>
            <li><strong>Údaje z&nbsp;formuláře:</strong> jméno a&nbsp;příjmení, e-mail, telefon (pokud ho uvedete), text zprávy, vybraný byt a&nbsp;zájem o&nbsp;garážové stání nebo sklep.</li>
            <li><strong>Technické údaje:</strong> při načtení webu zpracovává poskytovatel hostingu IP adresu a&nbsp;údaje o&nbsp;prohlížeči v&nbsp;provozních záznamech serveru.</li>
          </ul>
          <p>Web nepoužívá sledovací cookies ani analytické nástroje třetích stran. Prohlížeč si pouze po dobu návštěvy pamatuje, že jste už viděli úvodní animaci (technická nezbytnost, žádné osobní údaje).</p>

          <h2>3. Proč údaje zpracováváme a&nbsp;na jakém základě</h2>
          <ul>
            <li><strong>Odpověď na váš dotaz a&nbsp;jednání o&nbsp;rezervaci bytu</strong> – jednání o&nbsp;uzavření smlouvy na vaši žádost (čl. 6 odst. 1 písm. b) nařízení GDPR).</li>
            <li><strong>Zasílání informací o&nbsp;projektu</strong>, o&nbsp;který jste projevili zájem (novinky o&nbsp;stavbě, ceník, termíny) – na základě vašeho souhlasu (čl. 6 odst. 1 písm. a) GDPR). Souhlas můžete kdykoli odvolat.</li>
            <li><strong>Provoz a&nbsp;zabezpečení webu</strong> – náš oprávněný zájem (čl. 6 odst. 1 písm. f) GDPR).</li>
          </ul>

          <h2>4. Jak dlouho údaje uchováváme</h2>
          <p>Po dobu jednání o&nbsp;rezervaci a&nbsp;koupi bytu a&nbsp;dále nejdéle 3&nbsp;roky od posledního kontaktu, nebo do odvolání souhlasu, podle toho, co nastane dříve. Údaje, které jsou součástí smlouvy, uchováváme po dobu stanovenou právními předpisy.</p>

          <h2>5. Komu údaje předáváme</h2>
          <ul>
            <li>Prodávajícímu daného projektu (viz bod 1), aby mohl s&nbsp;vámi jednat o&nbsp;rezervaci.</li>
            <li>U&nbsp;Apartmánů Vysoké realitní kanceláři Svoboda &amp; Williams, která zajišťuje prodej posledních jednotek.</li>
            <li>Poskytovateli hostingu webu (GitHub, Inc., USA – provozní záznamy serveru; předání je zajištěno standardními smluvními doložkami EU) a&nbsp;poskytovateli e-mailové služby.</li>
          </ul>
          <p>Údaje nikomu neprodáváme ani nepředáváme pro marketing třetích stran.</p>

          <h2>6. Vaše práva</h2>
          <p>Máte právo na přístup ke svým údajům, jejich opravu nebo výmaz, omezení zpracování, přenositelnost, právo vznést námitku a&nbsp;právo kdykoli odvolat souhlas (odvoláním není dotčena zákonnost zpracování před odvoláním). Stačí nám napsat. Pokud se domníváte, že údaje zpracováváme v&nbsp;rozporu s&nbsp;právem, můžete podat stížnost u&nbsp;Úřadu pro ochranu osobních údajů, Pplk. Sochora 27, 170&nbsp;00 Praha 7, <a href="https://uoou.gov.cz" rel="noopener" target="_blank">uoou.gov.cz</a>.</p>

          <h2>7. Změny těchto zásad</h2>
          <p>Zásady můžeme upravit, například při změně hostingu nebo nástrojů. Aktuální znění je vždy na této stránce.</p>
          <p class="legal__date">Účinnost od 21. 11. 2026.</p>
        </div>
      </div>
    </section>
"""
    html += footer(rel, "company") + scripts(rel, ())
    return html

# ======================================================================
# 404 (GitHub Pages ji použije pro každou neexistující adresu; cesty se dopočítají v JS)
# ======================================================================
def notfound_page():
    with open(os.path.join(ROOT, "assets/img/logo/nk-logo-nad-sebou-bile.svg"), encoding="utf-8") as f:
        logo = f.read().replace('width="297.85" height="249.3"', 'width="140" height="117"')
    return f"""<!doctype html>
<html lang="cs">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Stránka nenalezena | Nico &amp; Kai Development</title>
  <meta name="robots" content="noindex">
  <style>
    html{{background:#000;color:#fff}}
    body{{margin:0;min-height:100svh;display:grid;place-items:center;font-family:Manrope,system-ui,-apple-system,"Segoe UI",sans-serif;-webkit-font-smoothing:antialiased}}
    main{{text-align:center;padding:2rem 1rem;max-width:36rem}}
    svg{{margin-bottom:2.5rem}}
    h1{{font-size:clamp(2.2rem,7vw,4.5rem);font-weight:800;letter-spacing:-.04em;line-height:.95;margin:0 0 1rem}}
    h1 span{{display:block;font-weight:300}}
    p{{color:#bdbdb8;font-size:1.05rem;line-height:1.55;margin:0 0 2rem}}
    a{{display:inline-block;color:#000;background:#fff;text-decoration:none;font-weight:800;padding:.95rem 1.6rem;letter-spacing:-.01em}}
    a+a{{background:transparent;color:#fff;border:1px solid #fff;margin-left:.5rem}}
  </style>
</head>
<body>
  <main>
    {logo}
    <h1>Tady nic nestojí.<span>Zatím.</span></h1>
    <p>Stránka, kterou hledáte, neexistuje nebo se přestěhovala.</p>
    <nav><a id="home" href="/">Úvodní stránka</a><a id="ks" href="/ke-schodum/">Rezidence ke Schodům</a></nav>
  </main>
  <script>
    (function(){{var r=location.pathname.indexOf('/nicoandkai-web/')===0?'/nicoandkai-web/':'/';document.getElementById('home').href=r;document.getElementById('ks').href=r+'ke-schodum/';
    var s=document.createElement('style');s.textContent='@font-face{{font-family:Manrope;src:url('+r+'assets/fonts/Manrope-Variable.woff2) format("woff2");font-weight:200 800;font-display:swap}}';document.head.appendChild(s);}})();
  </script>
</body>
</html>
"""

def sitemap_xml():
    urls = "".join(f"  <url><loc>{SITE_URL}/{p}</loc><changefreq>weekly</changefreq><priority>{pr}</priority></url>\n"
                   for p, pr in [("", "1.0"), ("ke-schodum/", "0.9"), ("do-ctvrti/", "0.9"), ("apartmany-vysoke/", "0.7"), ("rezidence-vlnita/", "0.4")])
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n'

# ======================================================================
# ÚVOD
# ======================================================================
def home_page():
    rel = ""; I = lambda p: f"assets/img/{p}.webp"
    nav = [("#projekty", "Projekty"), ("#pristup", "Jak stavíme"), ("#reference", "Reference"), ("#kontakt", "Kontakt")]
    def card(href, image, alt, badge, live, title_a, title_b, meta, text, cta, sold=False, widths=(600, 1200, 2400)):
        return f"""          <a class="pcard2{' pcard2--sold' if sold else ''}" href="{href}" data-reveal>
            <div class="pcard2__media"><span class="pcard2__badge{' is-live' if live else ''}{' is-sold' if sold else ''}"><i aria-hidden="true"></i>{badge}</span>{img(I(image), alt, widths, '(max-width: 880px) 100vw, 50vw')}</div>
            <div class="pcard2__body">
              <h3 class="pcard2__title">{title_a} <span class="light">{title_b}</span></h3>
              <p class="pcard2__meta">{"".join(f"<span>{m}</span>" for m in meta)}</p>
              <p class="pcard2__text">{text}</p>
              <span class="pcard2__cta">{cta} <i aria-hidden="true">→</i></span>
            </div>
          </a>
"""
    html = head("Nico &amp; Kai Development | Rezidenční projekty v Praze a v horách", "Nico & Kai Development staví domy, ve kterých se dobře žije. Rezidence ke Schodům a Do Čtvrti v Praze-Modřanech v předprodeji, Apartmány Vysoké a Rezidence Vlnitá dokončeny.", "og.jpg", rel, "home", extra_head="""
  <script type="application/ld+json">
  {"@context": "https://schema.org", "@type": "Organization", "name": "Nico & Kai Development", "description": "Rezidenční development v Praze a v horách.", "areaServed": "Česká republika"}
  </script>""")
    html += """  <div class="splash" aria-hidden="true"><img src="assets/img/logo/nk-logo-nad-sebou-bile.svg" alt=""><div class="splash__bar"><i></i></div></div>
"""
    html += header(rel, nav, "ke-schodum/", "Vybrat byt", nav)
    html += f"""
    <!-- ============ HERO ============ -->
    <section class="hero-media dark" id="top">
      <div class="hero-media__bg is-slides">
        {img(I('ke-schodum/bdks_19'), 'Rezidence ke Schodům za soumraku', sizes='100vw', lazy=False)}
        {img(I('do-ctvrti/bddc_01a'), 'Rezidence Do Čtvrti za soumraku', sizes='100vw')}
      </div>
      <div class="wrap hero-media__body">
        <p class="eyebrow" data-reveal>Nico &amp; Kai Development</p>
        <h1 class="display">
          <span class="mask"><span class="mask__in" style="--d:.05s">Domov,</span></span>
          <span class="mask light"><span class="mask__in" style="--d:.17s">na který se těšíte.</span></span>
        </h1>
        <p class="lead" data-reveal style="--d:.35s">Stavíme domy pro skutečný život. Ne metry čtvereční, ale místa, kam se chcete vracet. V&nbsp;Praze i&nbsp;v&nbsp;horách.</p>
        <div class="hero__cta" data-reveal style="--d:.45s">
          <a class="btn" href="#projekty"><span>Naše projekty</span><i class="arrow" aria-hidden="true">→</i></a>
          <a class="btn btn--ghost" href="ke-schodum/"><span>Předprodej: Ke Schodům</span></a>
        </div>
      </div>
      <div class="wrap hero-media__meta">
        <dl class="meta"><div><dt>V předprodeji</dt><dd>Rezidence ke&nbsp;Schodům · Do&nbsp;Čtvrti</dd></div><div><dt>V nabídce</dt><dd>Apartmány Vysoké</dd></div><div><dt>Dokončeno</dt><dd>Rezidence Vlnitá</dd></div></dl>
        <a class="scroll-cue" href="#manifest"><span>Dolů</span><i aria-hidden="true"></i></a>
      </div>
    </section>

    <!-- ============ MANIFEST ============ -->
    <section class="section" id="manifest" aria-labelledby="manifest-title">
      <div class="wrap">
        <p class="eyebrow" data-reveal><span>01</span> Kdo jsme</p>
        <h2 class="manifest" id="manifest-title" data-reveal>Neprodáváme byty. <strong>Vytváříme místa, kde se žije dobře.</strong> Promyšlená architektura, poctivé materiály a&nbsp;otevřená komunikace od první schůzky po předání klíčů.</h2>
        <div class="numbers">
          <div data-reveal><strong><span data-count="4">4</span></strong><span>rezidenční projekty</span></div>
          <div data-reveal style="--d:.1s"><strong><span data-count="2">2</span></strong><span>dokončené a předané</span></div>
          <div data-reveal style="--d:.2s"><strong><span data-count="17">17</span></strong><span>bytů v aktuální nabídce</span></div>
          <div data-reveal style="--d:.3s"><strong><span data-count="100">100</span><small>%</small></strong><span>projektů s vlastní zahradou nebo terasou</span></div>
        </div>
      </div>
    </section>

    <!-- ============ PROJEKTY ============ -->
    <section class="section dark" id="projekty" aria-labelledby="projects-title">
      <div class="wrap">
        <p class="eyebrow" data-reveal><span>02</span> Projekty</p>
        <div class="section-head" data-reveal>
          <h2 class="display display--md" id="projects-title"><span class="mask"><span class="mask__in" data-in>Naše</span></span><span class="mask light"><span class="mask__in" data-in style="--d:.12s">domy.</span></span></h2>
          <p>Dva domy v&nbsp;Praze-Modřanech právě v&nbsp;předprodeji, horské apartmány s&nbsp;posledními třemi jednotkami a&nbsp;dokončená rezidence, která je naší vizitkou.</p>
        </div>
        <div class="pgrid">
{card("ke-schodum/", "ke-schodum/bdks_13", "Rezidence ke Schodům", "Předprodej zahájen", True, "Rezidence", "ke&nbsp;Schodům", ["Praha-Modřany", "8 bytů · 2+kk a 3+kk", "terasy až 104 m²"], "Osm bytů s&nbsp;terasami a&nbsp;zahradami, pohledový beton a&nbsp;dům, který si vyrábí energii. Rezervace se slevou až 5&nbsp;%.", "Vybrat byt")}
{card("do-ctvrti/", "do-ctvrti/bddc_03", "Rezidence Do Čtvrti", "Předprodej zahájen", True, "Rezidence", "Do&nbsp;Čtvrti", ["Praha-Modřany", "6 bytů · 2+kk a 3+kk", "zahrady a střešní terasy"], "Nárožní dům se zaoblenými rohy a&nbsp;perforovanou cihlou. Jen dva byty na podlaží. Rezervace se slevou až 5&nbsp;%.", "Vybrat byt")}
{card("apartmany-vysoke/", "vysoke/l03", "Apartmány Vysoké", "Poslední 3 apartmány", False, "Apartmány", "Vysoké", ["Vysoké nad Jizerou", "A2 · B1 · B2", "dokončeno"], "Horské apartmány s&nbsp;terasami, společnou zahradou a&nbsp;jezírkem. Prodej posledních jednotek zajišťuje Svoboda &amp; Williams.", "Volné apartmány")}
{card("rezidence-vlnita/", "vlnita/foto-02", "Rezidence Vlnitá", "Prodáno", False, "Rezidence", "Vlnitá", ["Praha", "dokončeno", "všechny byty prodány"], "Dokončený dům, který nám ukázal, že detail rozhoduje. Zůstává jako naše vizitka.", "Prohlédnout", sold=True, widths=(600, 1200, 1800))}
        </div>
      </div>
    </section>

    <!-- ============ JAK STAVÍME ============ -->
    <section class="section" id="pristup" aria-labelledby="pristup-title">
      <div class="wrap" style="display:grid;gap:clamp(3rem,8vw,7rem)">
        <div>
          <p class="eyebrow" data-reveal><span>03</span> Jak stavíme</p>
          <h2 class="display display--md" id="pristup-title"><span class="mask"><span class="mask__in" data-in>Jednoduše,</span></span><span class="mask light"><span class="mask__in" data-in style="--d:.12s">poctivě, natrvalo.</span></span></h2>
        </div>
        <div class="split" data-reveal>
          <div class="split__media">{img(I('ke-schodum/bdks_10'), 'Zahrada Rezidence ke Schodům', sizes='(max-width: 880px) 100vw, 58vw')}</div>
          <div class="split__copy"><h3>Každý byt má kus nebe.</h3><p>Zahrada, terasa nebo balkon. Nestavíme dům, kde se venku jen parkuje. Obytné místnosti míří na jih, do zeleně, a&nbsp;venkovní prostor počítáme jako další pokoj.</p></div>
        </div>
        <div class="split split--flip" data-reveal>
          <div class="split__media">{img(I('do-ctvrti/bddc_int_01'), 'Interiér Rezidence Do Čtvrti', sizes='(max-width: 880px) 100vw, 58vw')}</div>
          <div class="split__copy"><h3>Materiály, které stárnou krásně.</h3><p>Pohledový beton, dřevo, omítky v&nbsp;teplých tónech, cihla a&nbsp;sklo. Méně prvků, zato lepších. Nic, co se za pár let musí vyměnit.</p></div>
        </div>
        <div class="split" data-reveal>
          <div class="split__media">{img(I('ke-schodum/bdks_18'), 'Detail fasády Rezidence ke Schodům', sizes='(max-width: 880px) 100vw, 58vw')}</div>
          <div class="split__copy"><h3>Důvěra se staví stejně jako dům.</h3><p>Srozumitelné informace, jasné termíny a&nbsp;přímý kontakt na lidi, kteří za projektem stojí. Když se něco změní, dozvíte se to od nás jako první.</p></div>
        </div>
      </div>
    </section>

    <!-- ============ REFERENCE + PARTNEŘI ============ -->
    <section class="section dark" id="reference" aria-labelledby="ref-title">
      <div class="wrap">
        <p class="eyebrow" data-reveal><span>04</span> Reference a partneři</p>
        <h2 class="manifest" id="ref-title" data-reveal>Dva domy jsme už <strong>dokončili a&nbsp;předali</strong>. Dva další navrhujeme s&nbsp;ateliérem <strong>JA Architekti</strong>, který má za sebou desítky realizací.</h2>
        <div class="partners" data-reveal>
          <div class="partners__item"><small>Architektura obou pražských projektů</small><img src="assets/img/partners/ja-architekti.svg" alt="JA Architekti" style="height:2rem;width:auto;filter:invert(1)"></div>
          <div class="partners__item"><small>Prodej Apartmánů Vysoké</small><strong>Svoboda <span>&amp;</span> Williams</strong></div>
        </div>
        <div class="pgrid" style="margin-top:clamp(2.5rem,5vw,4rem)">
          <a class="pcard2" href="apartmany-vysoke/" data-reveal>
            <div class="pcard2__media">{img(I('vysoke/foto-14'), 'Apartmány Vysoké v zimě', (600, 1200, 1800), '(max-width: 880px) 100vw, 50vw')}</div>
            <div class="pcard2__body"><h3 class="pcard2__title">Apartmány <span class="light">Vysoké</span></h3><p class="pcard2__text">Dokončeno. Dva horské domy, zahrada s&nbsp;jezírkem, výhled na Krkonoše.</p><span class="pcard2__cta">Prohlédnout <i aria-hidden="true">→</i></span></div>
          </a>
          <a class="pcard2 pcard2--sold" href="rezidence-vlnita/" data-reveal style="--d:.1s">
            <div class="pcard2__media">{img(I('vlnita/foto-13'), 'Obývací pokoj Rezidence Vlnitá', (600, 1200, 1800), '(max-width: 880px) 100vw, 50vw')}</div>
            <div class="pcard2__body"><h3 class="pcard2__title">Rezidence <span class="light">Vlnitá</span></h3><p class="pcard2__text">Dokončeno a&nbsp;prodáno. Čisté linie, tmavé dřevo a&nbsp;světlo.</p><span class="pcard2__cta">Prohlédnout <i aria-hidden="true">→</i></span></div>
          </a>
        </div>
      </div>
    </section>

{form("Nico & Kai Development", False, False, ("Chcete vědět", "jako první?"), "Zanechte nám kontakt. Ozveme se, jakmile budeme mít k&nbsp;projektům další informace, a&nbsp;rádi vás provedeme výběrem bytu.", (), "Odeslat", eyebrow=("05", "Kontakt"), rel="").replace('id="rezervace"', 'id="kontakt"')}
"""
    html += footer(rel, "company") + scripts(rel, ())
    return html

pages = {"index.html": home_page(), "ke-schodum/index.html": project_page(KS), "do-ctvrti/index.html": project_page(DC),
         "apartmany-vysoke/index.html": vysoke_page(), "rezidence-vlnita/index.html": vlnita_page(),
         "ochrana-osobnich-udaju/index.html": legal_page(), "404.html": notfound_page(),
         "sitemap.xml": sitemap_xml(), "robots.txt": f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n"}
for rel, html in pages.items():
    path = os.path.join(ROOT, rel); os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f: f.write(html)
    print("wrote", rel, len(html))
