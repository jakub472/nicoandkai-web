// Rezidence ke Schodům – data pro výběr bytů.
//
// Plochy a místnosti: Dokumentace pro povolení stavby (DSP 12/2025), tabulky místností 1.NP–3.NP.
// Garáž a sklepy: 1.PP téhož projektu. Plochy jsou projektové, závazné jsou až údaje z kolaudace
// / prohlášení vlastníka.
//
// !!! K DOPLNĚNÍ (tady a jinde se nic neodesílá bez vašeho vědomí):
//   - status  každého bytu: 'available' | 'reserved' | 'sold'   (3 byty rezervované, 1 prodaný – které? zatím vše 'available')
//   - price   cena bytu v Kč, nebo null = „Cena na vyžádání“ (ceny zatím nezveřejňujeme; návrh cen je v neveřejném souboru mimo web)
//   - areaNV  odhad plochy dle NV 366/2013 (+4,5 % u 3+kk, +4 % u 2+kk oproti součtu místností; závazný výpočet dodá architekt)
//   - u stání a sklepů: price, případně status a unit (ke kterému bytu patří)
//

window.NK_PROJECTS = window.NK_PROJECTS || {};
window.NK_PROJECTS['ke-schodum'] = {
  slug: 'ke-schodum',
  name: 'Rezidence ke Schodům',
  place: 'Praha-Modřany',
  planImages: {
    '1pp': 'plan-1pp.webp', '1np': 'plan-1np.webp', '2np': 'plan-2np.webp', '3np': 'plan-3np.webp',
  },

  // ---- skutečné půdorysy (DSP 12/2025): obrázek + obrysy bytů v pixelech obrázku ----
  // zones = celý byt včetně terasy (klik/hover), bodies = uzavřená část (axonometrie), terraces/common = terasy a jádro,
  // scale/origin = převod pixelů na metry pro axonometrii (82 px/m, SZ roh domu).
  planNote: 'Půdorys z dokumentace pro povolení stavby (12/2025). Plochy dle projektu, závazné jsou údaje z prohlášení vlastníka.',
  plans: {
    '3np': { image: 'plan-3np.webp', size: [2439, 1840], scale: 82, origin: [30, 274],
      outline: [[30,503],[549,503],[549,274],[2393,274],[2393,1341],[30,1341]],
      common: [[[915,274],[1524,274],[1524,503],[915,503]]],
      terraces: [[[30,274],[503,274],[503,1067],[823,1067],[823,1341],[30,1341]], [[823,1067],[1296,1067],[1296,1341],[823,1341]], [[2043,274],[2393,274],[2393,1341],[1616,1341],[1616,1067],[2043,1067]]],
      zones: { '3A': [[30,274],[503,274],[503,503],[1296,503],[1296,1341],[30,1341]], '3B': [[1296,503],[2043,503],[2043,274],[2393,274],[2393,1341],[1296,1341]] },
      bodies: { '3A': [[503,503],[1296,503],[1296,1067],[503,1067]], '3B': [[1296,503],[2043,503],[2043,1128],[1296,1128]] },
      anchors: { '3A': [854,915], '3B': [1829,793] } },
    '2np': { image: 'plan-2np.webp', size: [2439, 1840], scale: 82, origin: [30, 274],
      outline: [[30,503],[549,503],[549,274],[2393,274],[2393,1357],[30,1357]],
      common: [[[915,274],[1524,274],[1524,503],[915,503]]],
      terraces: [[[30,1357],[503,1357],[503,1524],[30,1524]], [[854,1357],[1280,1357],[1280,1524],[854,1524]], [[1616,1357],[1982,1357],[1982,1524],[1616,1524]]],
      zones: { '2A': [[30,503],[549,503],[549,274],[831,274],[831,1357],[503,1357],[503,1524],[30,1524]], '2B': [[831,503],[1616,503],[1616,1357],[1280,1357],[1280,1524],[854,1524],[854,1357],[831,1357]], '2C': [[1616,503],[1905,503],[1905,274],[2393,274],[2393,1357],[1982,1357],[1982,1524],[1616,1524]] },
      bodies: { '2A': [[30,503],[549,503],[549,274],[831,274],[831,1357],[30,1357]], '2B': [[831,503],[1616,503],[1616,1357],[831,1357]], '2C': [[1616,503],[1905,503],[1905,274],[2393,274],[2393,1357],[1616,1357]] },
      anchors: { '2A': [305,915], '2B': [1143,915], '2C': [1844,915] } },
    '1np': { image: 'plan-1np.webp', size: [2439, 1840], scale: 82, origin: [30, 274],
      outline: [[30,503],[549,503],[549,274],[2393,274],[2393,1357],[30,1357]],
      common: [[[915,274],[1524,274],[1524,503],[915,503]]],
      terraces: [[[30,1357],[503,1357],[503,1524],[30,1524]], [[854,1357],[1280,1357],[1280,1524],[854,1524]], [[1616,1357],[1982,1357],[1982,1524],[1616,1524]]],
      zones: { '1A': [[30,503],[549,503],[549,274],[831,274],[831,1357],[503,1357],[503,1524],[30,1524]], '1B': [[831,503],[1616,503],[1616,1357],[1280,1357],[1280,1524],[854,1524],[854,1357],[831,1357]], '1C': [[1616,503],[1905,503],[1905,274],[2393,274],[2393,1357],[1982,1357],[1982,1524],[1616,1524]] },
      bodies: { '1A': [[30,503],[549,503],[549,274],[831,274],[831,1357],[30,1357]], '1B': [[831,503],[1616,503],[1616,1357],[831,1357]], '1C': [[1616,503],[1905,503],[1905,274],[2393,274],[2393,1357],[1616,1357]] },
      anchors: { '1A': [305,915], '1B': [1143,915], '1C': [1844,915] } },
    '1pp': { image: 'plan-1pp.webp', size: [2495, 2146], zones: {}, anchors: {} },
  },

  floors: [
    { id: '3np', label: '3. NP', long: '3. nadzemní podlaží', z: 21 },
    { id: '2np', label: '2. NP', long: '2. nadzemní podlaží', z: 14 },
    { id: '1np', label: '1. NP', long: '1. nadzemní podlaží', z: 7 },
    {
      id: '1pp', label: '1. PP', long: '1. podzemní podlaží (garáž a sklepy)', z: 0, type: 'basement',
      meta: '16 stání · 8 sklepů',
      title: 'Garáž a sklepy',
      stats: [['Garážová stání', '16'], ['Sklepy', '8'], ['Plocha sklepů', '1,9 – 5,1 m²']],
      text: 'Garáž je propojená výtahem se všemi podlažími. Stání č.&nbsp;6 je vyhrazené pro osoby s omezenou schopností pohybu. Garážové stání i sklep lze k bytu přikoupit samostatně.',
      priceNote: ['Cena stání a sklepů', 'na vyžádání'],
      cta: 'Mám zájem o stání / sklep',
    },
  ],

  // ---- interaktivní fasáda (vizualizace BDKS_02, jižní průčelí, souřadnice v px obrázku 2400 × 1610) ----
  // Pohled od jihu: vlevo západ (A), uprostřed B, vpravo východ (C). Obývací pokoj bytu A je mimo záběr vlevo za břízou.
  facade: {
    image: 'bdks_02', size: [2400, 1610], alt: 'Jižní průčelí Rezidence ke Schodům za soumraku',
    zones: {
      '3A': [[0, 400], [300, 400], [300, 290], [1230, 290], [1230, 620], [0, 620]],
      '3B': [[1230, 290], [2020, 290], [2020, 400], [2400, 400], [2400, 620], [1230, 620]],
      '2A': [[0, 620], [700, 620], [700, 960], [0, 960]],
      '2B': [[700, 620], [1600, 620], [1600, 960], [700, 960]],
      '2C': [[1600, 620], [2400, 620], [2400, 960], [1600, 960]],
      '1A': [[0, 960], [700, 960], [700, 1290], [0, 1290]],
      '1B': [[700, 960], [1600, 960], [1600, 1290], [700, 1290]],
      '1C': [[1600, 960], [2400, 960], [2400, 1290], [1600, 1290]],
    },
  },

  // ---- ceník a rezervace ----
  pricing: {
    note: 'Ceny zatím nezveřejňujeme (price: null). Zobrazení cen řídí NK_CONFIG.priceMode.',
    parking: { count: 16, price: null, label: 'Garážové stání' },
    cellarPerM2: null,
  },
  reservation: {
    title: 'Rezervace v průběhu stavebního řízení',
    tiers: [[3000000, 0.03], [4000000, 0.04], [5000000, 0.05]],
    deadline: '2028-10-31',
    refund: 'Pokud do tohoto data nenabude stavební povolení právní moci, záloha se vrací v plné výši.',
  },
  stage: { label: 'Předprodej zahájen', permit: 'Žádost o stavební povolení podána 12/2025', permitShort: 'stavební řízení zahájeno' },

  cta: { unit: 'Rezervovat byt' },
  accessoriesNote: 'Ke každému bytu lze přikoupit garážové stání a sklep.',

  units: [
    {
      id: '3A', floor: '3np', disposition: '2+kk', status: 'available', price: null,
      area: 67.8, areaNV: 70.5, terrace: 104.2, total: 172.0,
      terraceNote: 'dvě střešní terasy (81,3 + 22,9 m²)',
      rooms: [['Zádveří', 3.66], ['Koupelna + WC', 4.47], ['Obývací pokoj + kuchyň', 46.24], ['Ložnice', 13.47]],
    },
    {
      id: '3B', floor: '3np', disposition: '2+kk', status: 'available', price: null,
      area: 75.2, areaNV: 78.2, terrace: 72.35, total: 147.6,
      terraceNote: 'střešní terasa',
      rooms: [['Zádveří', 7.39], ['WC', 2.16], ['Obývací pokoj + kuchyň', 38.30], ['Ložnice', 13.70], ['Koupelna + WC', 13.70]],
    },
    {
      id: '2A', floor: '2np', disposition: '3+kk', status: 'available', price: null,
      area: 89.9, areaNV: 93.9, terrace: 27.11, total: 117.0, terraceNote: 'terasa',
      rooms: [['Zádveří', 7.63], ['Chodba', 5.43], ['Pokoj', 13.36], ['WC', 1.93], ['Koupelna + WC', 4.84], ['Prádelna', 2.72], ['Ložnice', 12.77], ['Obývací pokoj + kuchyň', 41.25]],
    },
    {
      id: '2B', floor: '2np', disposition: '3+kk', status: 'available', price: null,
      area: 81.8, areaNV: 85.5, terrace: 29.76, total: 111.5, terraceNote: 'terasa',
      rooms: [['Zádveří', 5.58], ['Chodba', 4.05], ['Pokoj', 9.80], ['WC', 1.94], ['Koupelna + WC', 5.25], ['Ložnice', 12.54], ['Obývací pokoj + kuchyň', 42.61]],
    },
    {
      id: '2C', floor: '2np', disposition: '3+kk', status: 'available', price: null,
      area: 90.1, areaNV: 94.2, terrace: 25.33, total: 115.4, terraceNote: 'terasa',
      rooms: [['Zádveří', 7.62], ['Chodba', 5.43], ['Pokoj', 13.43], ['WC', 1.94], ['Koupelna + WC', 5.08], ['Prádelna', 2.74], ['Ložnice', 12.83], ['Obývací pokoj + kuchyň', 41.00]],
    },
    {
      id: '1A', floor: '1np', disposition: '3+kk', status: 'available', price: null,
      area: 108.5, areaNV: 113.4, terrace: 22.04, total: 130.6, terraceNote: 'terasa se zahradou',
      rooms: [['Zádveří', 7.63], ['Chodba', 7.42], ['Pokoj', 13.28], ['WC', 1.90], ['Koupelna + WC', 6.53], ['Prádelna', 5.30], ['Ložnice', 13.05], ['Obývací pokoj + kuchyň', 53.45]],
    },
    {
      id: '1B', floor: '1np', disposition: '3+kk', status: 'available', price: null,
      area: 100.6, areaNV: 105.1, terrace: 20.82, total: 121.4, terraceNote: 'terasa se zahradou',
      rooms: [['Zádveří', 5.58], ['Chodba', 5.42], ['Pokoj', 9.70], ['WC', 1.89], ['Koupelna', 7.89], ['Ložnice', 14.70], ['Obývací pokoj + kuchyň', 55.40]],
    },
    {
      id: '1C', floor: '1np', disposition: '3+kk', status: 'available', price: null,
      area: 108.8, areaNV: 113.7, terrace: 19.26, total: 128.1, terraceNote: 'terasa se zahradou',
      rooms: [['Zádveří', 7.62], ['Chodba', 7.42], ['Pokoj', 13.35], ['WC', 1.91], ['Koupelna + WC', 6.59], ['Prádelna', 5.35], ['Ložnice', 13.41], ['Obývací pokoj + kuchyň', 53.17]],
    },
  ],

  // Garážová stání (1.PP) – 16 míst, č. 6 je vyhrazené pro osoby s omezenou schopností pohybu.
  parking: Array.from({ length: 16 }, (_, i) => ({
    id: i + 1, status: 'available', price: null, accessible: i + 1 === 6,
  })),

  // Sklepy (1.PP) – místnosti 006–013 v tabulce místností.
  cellars: [5.11, 5.11, 5.01, 4.42, 4.42, 1.90, 4.35, 4.35].map((area, i) => ({
    id: i + 1, area, status: 'available', price: null,
  })),

  // Technické údaje z DSP (A.3 TEA, D.1.1.1 TZ)
  facts: {
    units: 8,
    floorsAbove: 3,
    floorsBelow: 1,
    start: '1. čtvrtletí 2027',
    finish: '2. čtvrtletí 2028',
  },
};
