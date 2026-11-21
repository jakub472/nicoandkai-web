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
// Schematická geometrie (geometry) slouží jen pro kresbu půdorysů na webu. Není to výkres.

window.NK_PROJECTS = window.NK_PROJECTS || {};
window.NK_PROJECTS['ke-schodum'] = {
  slug: 'ke-schodum',
  name: 'Rezidence ke Schodům',
  place: 'Praha-Modřany',
  planImages: {
    '1pp': 'plan-1pp.webp', '1np': 'plan-1np.webp', '2np': 'plan-2np.webp', '3np': 'plan-3np.webp',
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

  // ---- interaktivní fasáda (vizualizace BDKS_02, jižní průčelí, 2528 × 1696 px): zóny bytů v pixelech ----
  facade: {
    image: 'bdks_02', size: [2528, 1696], alt: 'Jižní průčelí Rezidence ke Schodům za soumraku',
    zones: {
      '3A': [[60, 330], [300, 330], [300, 190], [720, 190], [720, 330], [1220, 330], [1220, 560], [60, 560]],
      '3B': [[1220, 330], [1220, 190], [2010, 190], [2010, 220], [2460, 220], [2460, 560], [1220, 560]],
      '2A': [[160, 560], [625, 560], [625, 1000], [160, 1000]],
      '2B': [[625, 560], [1360, 560], [1360, 1000], [625, 1000]],
      '2C': [[1360, 560], [2420, 560], [2420, 1000], [1360, 1000]],
      '1A': [[160, 1000], [625, 1000], [625, 1420], [160, 1420]],
      '1B': [[625, 1000], [1360, 1000], [1360, 1420], [625, 1420]],
      '1C': [[1360, 1000], [2420, 1000], [2420, 1420], [1360, 1420]],
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

  // ---- schematická geometrie pro kresbu (metry; x = východ, y = jih) ----
  geometry: {
    '3np': {
      outline: [-6.2, 0, 31.6, 15.2],
      common: [{ x: 4.2, y: 0, w: 8.8, d: 3.4, label: 'schodiště · výtah' }],
      units: {
        '3A': { body: { x: 0, y: 3.6, w: 10.0, d: 6.9 }, terraces: [{ x: -6.0, y: 0.8, w: 6.0, d: 13.6 }, { x: 4.2, y: 10.5, w: 5.8, d: 3.9 }] },
        '3B': { body: { x: 10.0, y: 3.6, w: 9.9, d: 7.6 }, terraces: [{ x: 19.9, y: 0.8, w: 5.3, d: 13.6 }, { x: 10.0, y: 11.2, w: 9.9, d: 3.2 }] },
      },
    },
    '2np': {
      outline: [0, 0, 29.4, 15.9],
      common: [{ x: 0, y: 0, w: 29.4, d: 2.0, label: 'pavlač' }, { x: 10.2, y: 0, w: 6.2, d: 4.6, label: 'schodiště · výtah' }],
      units: {
        '2A': { body: { x: 0, y: 2.2, w: 9.5, d: 10.85 }, terraces: [{ x: 0, y: 13.05, w: 9.5, d: 2.85 }] },
        '2B': { body: { x: 9.5, y: 4.6, w: 9.9, d: 8.3 }, terraces: [{ x: 9.5, y: 12.9, w: 9.9, d: 3.0 }] },
        '2C': { body: { x: 19.4, y: 2.2, w: 10.0, d: 11.17 }, terraces: [{ x: 19.4, y: 13.37, w: 10.0, d: 2.53 }] },
      },
    },
    '1np': {
      outline: [0, 0, 29.4, 15.9],
      common: [{ x: 0, y: 0, w: 29.4, d: 2.0, label: 'vstup · pavlač' }, { x: 10.2, y: 0, w: 6.2, d: 4.6, label: 'schodiště · výtah' }],
      units: {
        '1A': { body: { x: 0, y: 2.2, w: 9.5, d: 11.4 }, terraces: [{ x: 0, y: 13.6, w: 9.5, d: 2.3 }] },
        '1B': { body: { x: 9.5, y: 4.6, w: 9.9, d: 9.2 }, terraces: [{ x: 9.5, y: 13.8, w: 9.9, d: 2.1 }] },
        '1C': { body: { x: 19.4, y: 2.2, w: 10.0, d: 11.8 }, terraces: [{ x: 19.4, y: 14.0, w: 10.0, d: 1.9 }] },
      },
    },
    '1pp': {
      outline: [0, 0, 29.4, 15.5],
      common: [{ x: 12.0, y: 0.2, w: 5.0, d: 2.6, label: 'schodiště · výtah' }],
      garage: { x: 0, y: 0, w: 29.4, d: 15.5 },
      lane: [14.7, 8.9],
      cellars: [
        { x: 0.4, y: 0.3, w: 2.3, d: 2.3 }, { x: 2.9, y: 0.3, w: 2.3, d: 2.3 }, { x: 5.4, y: 0.3, w: 2.3, d: 2.3 },
        { x: 7.9, y: 0.3, w: 2.1, d: 2.3 }, { x: 10.1, y: 0.3, w: 1.4, d: 2.3 },
        { x: 17.4, y: 0.3, w: 1.2, d: 1.6 }, { x: 24.4, y: 0.3, w: 2.2, d: 2.3 }, { x: 26.8, y: 0.3, w: 2.2, d: 2.3 },
      ],
      stalls: [
        // horní řada (1–7)
        [2.3, 3.2], [4.9, 3.2], [8.4, 3.2], [11.0, 3.2], [13.6, 3.2], [18.4, 3.2], [24.9, 3.2],
        // dolní řada (8–16)
        [2.0, 10.3], [4.8, 10.3], [8.3, 10.3], [11.6, 10.3], [14.8, 10.3], [18.3, 10.3], [21.3, 10.3], [23.9, 10.3], [26.7, 10.3],
      ].map(([x, y]) => ({ x, y, w: 2.5, d: 5.0 })),
    },
  },

  // Technické údaje z DSP (A.3 TEA, D.1.1.1 TZ)
  facts: {
    units: 8,
    floorsAbove: 3,
    floorsBelow: 1,
    start: '1. čtvrtletí 2027',
    finish: '2. čtvrtletí 2028',
  },
};
