# Nico & Kai Development – web

Statický web bez build kroku (HTML + CSS + JS). Stránky se generují skriptem `tools/build-pages.py`
(společná hlavička, patička, formuláře, GDPR, 404, sitemap) – po úpravě textů ho spusťte znovu:

```bash
python3 tools/build-pages.py
```

Skript přidává k odkazům na CSS a JS otisk obsahu (`?v=…`), takže po úpravě stylů nebo skriptů je potřeba stránky
přegenerovat – jinak by prohlížeče (hlavně telefony) dál načítaly starou verzi z cache.

Odhalování při scrollu (`main.js`): sleduje se maska nadpisu, ne posunutý řádek, s prahem 0 – jinak se na telefonu
zalomené nadpisy a vysoké bloky neodhalí. Prvky s `data-reveal` doplněné skriptem (karty jednotek) hlídá MutationObserver.

```
index.html                       úvod: hero, manifest, 4 projekty, jak stavíme, reference + partneři, kontakt
ke-schodum/index.html            Rezidence ke Schodům – předprodej (fasáda s výběrem bytů, půdorysy, rezervace)
do-ctvrti/index.html             Rezidence Do Čtvrti – předprodej (totéž)
apartmany-vysoke/index.html      Apartmány Vysoké – dokončeno, poslední 3 jednotky (A2, B1, B2), prodej Svoboda & Williams
rezidence-vlnita/index.html      Rezidence Vlnitá – dokončeno, prodáno
ochrana-osobnich-udaju/          zásady zpracování osobních údajů (odkaz ze souhlasu ve formuláři a z patičky)
404.html, sitemap.xml, robots.txt
assets/data/*.js                 DATA: byty, plochy, ceny (nyní null), stavy, zóny na fasádě, rezervační klíč
assets/js/config.js              kontakty, prodávající, režim cen (priceMode), napojení formuláře
assets/js/site.js                splash, hero (obrázky / video), galerie + lightbox, interaktivní fasáda (reflektor), ceník/rezervace
assets/js/explorer.js            výběr bytu po patrech (axonometrie z obrysů půdorysů, půdorys se zónami, detail, tabulka)
assets/js/atmo.js                atmosféra v hero: mlha (Praha) / sníh (Vysoké) na canvasu; vypnuto při prefers-reduced-motion
assets/video/                    hero videa (Veo 3.1 přes Figma Weave): <projekt>.mp4 1080p a <projekt>-720.mp4; src/ = výchozí snímky 16:9
assets/css/site.css              komponenty webu; styles.css = základ a typografie; explorer.css = výběr bytů
assets/img/<projekt>/            vizualizace a fotky ve 3 šířkách (600/1200/1800–2400 px, WebP)
```

## Jazyky (CS / EN / DE)

Čeština je v kořeni, angličtina v `en/`, němčina v `de/` (stejné adresy stránek; GDPR je `en/privacy/` a `de/datenschutz/`).
Všechny texty stránek jsou v `tools/i18n.py` (UI, projekty, úvod, Vysoké, Vlnitá, GDPR); texty vykreslované skriptem
(stavy, patra, místnosti, ceník, formulář) překládají slovníky `assets/i18n/en.js` a `de.js` s českými originály jako klíči.
Nový text v datech (`assets/data/*.js`) stačí přidat do obou slovníků, jinak zůstane česky. Přepínač jazyků je v hlavičce,
v mobilním menu a v patičce; každá stránka má `hreflang` odkazy a sitemap obsahuje všechny jazyky.

## Nasazení (GitHub Pages, doména nicoandkai.com)

Repozitář: `jakub472/nicoandkai-web` (větev `main`, kořen = tato složka). Každý push na `main` web během minuty nasadí.
Doména se nastavuje souborem `CNAME` (obsah `nicoandkai.com`) a DNS záznamy u registrátora (Websupport / Active24):

```
A     @    185.199.108.153
A     @    185.199.109.153
A     @    185.199.110.153
A     @    185.199.111.153
CNAME www  jakub472.github.io
```

## Ceny

Ceny se zatím nezveřejňují: `config.js` → `priceMode: 'onRequest'` a v datech je `price: null`.
Web pak zobrazuje „Cena na vyžádání“, rezervační klíč (záloha → sleva) a odkaz „Vyžádat ceník“ na formulář.
Návrh cen je v neveřejném souboru mimo web (`nico-kai-ceny-navrh.md` o úroveň výš). Až ceny zveřejníte:
doplňte `price` u bytů, `pricing.parking.price`, `cellarPerM2` a přepněte `priceMode` na `'total'`.

## Jak upravit stav bytu

`assets/data/ke-schodum.js` / `do-ctvrti.js`, u každého bytu:
- `status`: `'available'` | `'reserved'` | `'sold'`  (promítne se do fasády, půdorysů, tabulek i formuláře)
- `areaNV`: plocha dle NV 366/2013; `terrace`/`total`: venkovní plocha a součet

Rezervační klíč: `reservation.tiers` (záloha → sleva) a `reservation.deadline` (datum pro vrácení zálohy).
Zóny bytů na fasádě (`facade.zones`) jsou v pixelech vizualizace 2528 × 1696 px.

## CO ZKONTROLOVAT / DOPLNIT

1. **Ke Schodům: 3 byty rezervované + 1 prodaný – které?** V datech jsou všechny `available`.
2. **Plochy dle NV u Ke Schodům jsou odhad** (+4,5 % / +4 % k součtu místností). Do Čtvrti má odhad z Archicad zón (±0,5 m²).
3. **Zahrady, balkony a terasy Do Čtvrti** jsou měření z půdorysů a situace (±1 m²), zahrady nejsou vymezené oplocením.
4. **Rezervace:** klíč 3/4/5 mil. → 3/4/5 %, vrácení zálohy při nenabytí právní moci povolení do 31. 10. 2028 (návrh data).
   Smlouvu a způsob úschovy zálohy ověřte s právníkem.
5. **Apartmány Vysoké:** A2 a B1 bez dispozice/plochy; kontakt na Janu Kocianovou (Svoboda & Williams) doplňte v `config.js`.
6. **Rezidence Vlnitá:** doplnit lokalitu, rok, počet bytů a profesionální fotky (`assets/data/vlnita.js`, `assets/img/vlnita/`).
7. **Formulář** nic neodesílá, dokud nenastavíte `formEndpoint` (Formspree apod.) nebo `company.email` v `config.js`.
8. **Údaje společnosti** (název, IČO, sídlo, e-mail, telefon) v `config.js` – zobrazí se v patičce i v zásadách GDPR.
9. Logo JA Architekti je vektor z projektové dokumentace; před spuštěním si vyžádejte jejich souhlas s užitím.

## Zdroje
- Ke Schodům: DSP 12/2025 (JA Architekti / Jakub Killnar), vizualizace JA Architekti (BDKS_*).
- Do Čtvrti: DPZ 08/2026, studie 05/2026, souhlas IPR č. j. 12986/2026; vizualizace JA Architekti (BDDČ_*).
- Vysoké: krajinné fotografie Jiří Smejkal (koupené, originály v iCloud Drive › Downloads › „Claude foto Vysoke“; na webu `k01`–`k11`),
  interiéry a dům z nabídky Svoboda & Williams č. 115557 (svoboda-williams.com, apartmán A2; na webu `a01`–`a09`), dům v zimě z vlastního
  prodejního podkladu (`d01`, `d02`). Pod galerií je uveden autor fotografií. Staré soubory `l*` a `foto-*` už web nepoužívá.
  Exteriéry domu na webu jsou retušované verze (`e01` zahrada v podvečer, `e02` oba domy z příjezdu, `e03`/`e03w` zima v podvečer):
  Figma Weave, Nano Banana Pro, 23. 11. 2026; měnila se obloha a světlo, zmizela hromada hlíny a kostek, dům je beze změny.
  U `e02` je dlažba z původní fotky (model ji nahradil štěrkem, proto složeno ručně). Původní `a08`, `d01`, `d02` web nepoužívá.
- Vlnitá: fotografie od zadavatele (`foto-21`–`foto-25` z 23. 11. 2026; na `foto-24` je auto přebarvené na bílou a bez polepů).
