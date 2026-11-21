// Rezidence Do Čtvrti – data pro výběr bytů.
//
// Zdroj: Dokumentace pro povolení stavby JA ARCHITEKTI (08/2026), tabulky místností 1.NP–3.NP, 2.PP,
// a souhlasné vyjádření IPR Praha č. j. IPR 12986/2026 (19. 10. 2026): 3 NP, 2 PP, 6 bytů, 7 stání.
// area = součet místností (studie 05/2026); areaNV = podlahová plocha dle NV 366/2013 Sb., odhad změřený z půdorysů studie (±0,5 m²),
// soubor BD_Do_ctvrti_plochy_NV366.xlsx. Závazná plocha bude v prohlášení vlastníka.
//
// !!! K DOPLNĚNÍ:
//   - status: 'available' | 'reserved' | 'sold'
//   - price: cena v Kč včetně DPH, nebo null = "cena na vyžádání"
//   - terrace / total: zahrada, balkon, terasa (orientační měření z půdorysů a situace, ±1 m²) a součet s plochou dle NV

window.NK_PROJECTS = window.NK_PROJECTS || {};
window.NK_PROJECTS['do-ctvrti'] = {
  slug: 'do-ctvrti',
  name: 'Rezidence Do Čtvrti',
  place: 'Praha-Modřany',
  planImages: {
    '2pp': 'plan-2pp.webp', '1pp': 'plan-1pp.webp', '1np': 'plan-1np.webp', '2np': 'plan-2np.webp', '3np': 'plan-3np.webp',
  },

  floors: [
    { id: '3np', label: '3. NP', long: '3. nadzemní podlaží', z: 28 },
    { id: '2np', label: '2. NP', long: '2. nadzemní podlaží', z: 21 },
    { id: '1np', label: '1. NP', long: '1. nadzemní podlaží', z: 14 },
    {
      id: '1pp', label: '1. PP', long: '1. podzemní podlaží (garáž)', z: 7, type: 'basement',
      meta: '7 garážových stání',
      title: 'Garáž',
      stats: [['Garážová stání', '7'], ['Plocha garáže', '224,6 m²']],
      text: 'Garáž v 1. podzemním podlaží se sjezdem z ulice Do čtvrti. Výtah propojuje garáž i všechna podlaží domu.',
      priceNote: ['Cena stání', 'na vyžádání'],
      cta: 'Mám zájem o stání',
    },
    {
      id: '2pp', label: '2. PP', long: '2. podzemní podlaží (sklepy a technika)', z: 0, type: 'basement',
      meta: '6 sklepů',
      title: 'Sklepy a technika',
      stats: [['Sklepy', '6'], ['Plocha sklepů', '5,8 – 6,5 m²']],
      text: 'Sklepní kóje a technické zázemí domu ve 2. podzemním podlaží. Výtah sem sjíždí z&nbsp;celého domu.',
      priceNote: ['Cena sklepů', 'na vyžádání'],
      cta: 'Mám zájem o sklep',
    },
  ],

  // ---- interaktivní fasáda (vizualizace BDDČ_17, jižní/zahradní průčelí, 2528 × 1696 px): zóny bytů v pixelech ----
  // Pohled od jihu: vlevo západ (A, C, E), vpravo východ (B, D, F).
  facade: {
    image: 'bddc_17', size: [2528, 1696], alt: 'Zahradní průčelí Rezidence Do Čtvrti za soumraku',
    zones: {
      E: [[203, 353], [606, 353], [606, 169], [1285, 169], [1285, 540], [203, 540]],
      F: [[1285, 169], [1963, 169], [1963, 353], [2205, 353], [2205, 540], [1285, 540]],
      C: [[203, 540], [1210, 540], [1210, 1000], [203, 1000]],
      D: [[1210, 540], [2205, 540], [2205, 848], [2308, 848], [2308, 951], [2205, 951], [2205, 1000], [1210, 1000]],
      A: [[215, 1000], [1210, 1000], [1210, 1420], [215, 1420]],
      B: [[1210, 1000], [2205, 1000], [2205, 1420], [1210, 1420]],
    },
  },

  pricing: {
    note: 'Ceny zatím nezveřejňujeme (price: null). Ceník je v neveřejném souboru mimo web.',
    parking: { count: 7, price: null, label: 'Garážové stání' },
    cellarPerM2: null,
  },
  reservation: {
    title: 'Rezervace v průběhu stavebního řízení',
    tiers: [[3000000, 0.03], [4000000, 0.04], [5000000, 0.05]],
    deadline: '2028-10-31',
    refund: 'Pokud do tohoto data nenabude stavební povolení právní moci, záloha se vrací v plné výši.',
  },
  stage: { label: 'Předprodej zahájen', permit: 'Žádost o povolení stavby podána 26. 8. 2026, souhlas IPR Praha 19. 10. 2026', permitShort: 'stavební řízení zahájeno' },

  cta: { unit: 'Rezervovat byt' },
  outdoorHeader: 'Zahrada / balkon / terasa',
  accessoriesNote: '',

  units: [
    {
      id: 'E', floor: '3np', disposition: '2+kk', status: 'available', price: null,
      area: 43.0, areaNV: 44.67, terrace: 41.5, total: 86.17, outdoorLabel: 'Terasa', outdoor: 'střešní terasa', terraceNote: 'střešní terasa',
      rooms: [['Chodba', 5.03], ['WC', 1.62], ['Koupelna', 3.52], ['Ložnice', 9.81], ['Obývací pokoj', 14.82], ['Kuchyně', 8.2]],
    },
    {
      id: 'F', floor: '3np', disposition: '2+kk', status: 'available', price: null,
      area: 43.0, areaNV: 44.66, terrace: 41.9, total: 86.56, outdoorLabel: 'Terasa', outdoor: 'střešní terasa', terraceNote: 'střešní terasa',
      rooms: [['Chodba', 5.03], ['WC', 1.62], ['Koupelna', 3.52], ['Ložnice', 9.81], ['Obývací pokoj', 14.82], ['Kuchyně', 8.2]],
    },
    {
      id: 'C', floor: '2np', disposition: '3+kk', status: 'available', price: null,
      area: 78.27, areaNV: 82.01, terrace: 14.3, total: 96.31, outdoorLabel: 'Balkon', outdoor: 'balkon', terraceNote: 'balkon',
      rooms: [['Vstup', 7.43], ['Šatna', 2.43], ['WC', 1.62], ['Koupelna', 6.47], ['Obývací část', 33.85], ['Pokoj', 10.75], ['Ložnice', 15.72]],
    },
    {
      id: 'D', floor: '2np', disposition: '3+kk', status: 'available', price: null,
      area: 78.22, areaNV: 81.96, terrace: 7.8, total: 89.76, outdoorLabel: 'Balkon', outdoor: 'balkon', terraceNote: 'balkon',
      rooms: [['Chodba', 7.43], ['Šatna', 2.43], ['WC', 1.62], ['Koupelna', 6.47], ['Obývací část', 33.85], ['Pokoj', 10.75], ['Ložnice', 15.67]],
    },
    {
      id: 'A', floor: '1np', disposition: '3+kk', status: 'available', price: null,
      area: 78.54, areaNV: 82.32, terrace: 84.0, total: 166.32, outdoorLabel: 'Zahrada', outdoor: 'soukromá zahrada', terraceNote: 'soukromá zahrada',
      rooms: [['Chodba', 7.43], ['Šatna', 2.43], ['WC', 1.62], ['Koupelna', 6.47], ['Obývací část', 34.35], ['Pokoj', 10.75], ['Ložnice', 15.49]],
    },
    {
      id: 'B', floor: '1np', disposition: '3+kk', status: 'available', price: null,
      area: 78.54, areaNV: 82.32, terrace: 91.5, total: 173.82, outdoorLabel: 'Zahrada', outdoor: 'soukromá zahrada', terraceNote: 'soukromá zahrada',
      rooms: [['Chodba', 7.43], ['Šatna', 2.43], ['WC', 1.62], ['Koupelna', 6.47], ['Obývací část', 34.35], ['Pokoj', 10.75], ['Ložnice', 15.49]],
    },
  ],

  // 7 stání (1.PP), 6 sklepů (2.PP, místnosti 004–009)
  parking: Array.from({ length: 7 }, (_, i) => ({ id: i + 1, status: 'available', price: null })),
  cellars: [5.79, 5.79, 5.79, 6.51, 6.51, 6.51].map((area, i) => ({ id: i + 1, area, status: 'available', price: null })),

  // ---- skutečné půdorysy: obrázek + zóny bytů v pixelech obrázku (1750 × 1519) ----
  // Půdorys je symetrický podle středové zdi (x ≈ 938), pravý byt je zrcadlem levého.
  planNote: 'Půdorys z projektové dokumentace (08/2026). Plochy dle projektu, závazné jsou údaje z kolaudace.',
  plans: {
    '3np': { image: 'plan-3np.webp', size: [1750, 1519],
      zones: { E: [[385, 365], [705, 365], [705, 545], [925, 545], [925, 1130], [385, 1130]], F: [[1491, 365], [1171, 365], [1171, 545], [951, 545], [951, 1130], [1491, 1130]] },
      anchors: { E: [560, 800], F: [1316, 800] } },
    '2np': { image: 'plan-2np.webp', size: [1750, 1519],
      zones: { C: [[245, 240], [705, 240], [705, 545], [925, 545], [925, 1280], [245, 1280]], D: [[1631, 240], [1171, 240], [1171, 545], [951, 545], [951, 1280], [1631, 1280]] },
      anchors: { C: [470, 700], D: [1406, 700] } },
    '1np': { image: 'plan-1np.webp', size: [1750, 1519],
      zones: { A: [[245, 240], [705, 240], [705, 545], [925, 545], [925, 1280], [245, 1280]], B: [[1631, 240], [1171, 240], [1171, 545], [951, 545], [951, 1280], [1631, 1280]] },
      anchors: { A: [470, 700], B: [1406, 700] } },
    '1pp': { image: 'plan-1pp.webp', size: [1750, 1519], zones: {}, anchors: {} },
    '2pp': { image: 'plan-2pp.webp', size: [1750, 1519], zones: {}, anchors: {} },
  },

  // ---- schematická geometrie pro axonometrii (metry; x = východ, y = jih). Půdorys domu cca 16,8 × 12,45 m ----
  geometry: {
    '3np': {
      outline: [-1.8, 0, 18.6, 14.0],
      common: [{ x: 5.9, y: 0, w: 5.0, d: 4.2, label: 'schodiště · výtah' }],
      units: {
        E: { body: { x: 0.9, y: 4.2, w: 7.3, d: 6.5 }, terraces: [{ x: -1.5, y: 10.7, w: 9.7, d: 3.0 }] },
        F: { body: { x: 8.6, y: 4.2, w: 7.3, d: 6.5 }, terraces: [{ x: 8.6, y: 10.7, w: 9.7, d: 3.0 }] },
      },
    },
    '2np': {
      outline: [-0.6, 0, 17.4, 13.4],
      common: [{ x: 5.9, y: 0, w: 5.0, d: 4.2, label: 'schodiště · výtah' }],
      units: {
        C: { body: { x: 0, y: 3.9, w: 8.2, d: 7.6 }, terraces: [{ x: -0.6, y: 11.5, w: 8.8, d: 1.7 }] },
        D: { body: { x: 8.6, y: 3.9, w: 8.2, d: 7.6 }, terraces: [{ x: 8.6, y: 11.5, w: 8.8, d: 1.7 }] },
      },
    },
    '1np': {
      outline: [-1.6, 0, 18.4, 14.2],
      common: [{ x: 5.9, y: 0, w: 5.0, d: 4.4, label: 'hala · výtah' }],
      units: {
        A: { body: { x: 0, y: 3.9, w: 8.2, d: 7.6 }, terraces: [{ x: -1.5, y: 3.9, w: 1.5, d: 9.9 }, { x: 0, y: 11.5, w: 8.2, d: 2.3 }] },
        B: { body: { x: 8.6, y: 3.9, w: 8.2, d: 7.6 }, terraces: [{ x: 16.8, y: 3.9, w: 1.5, d: 9.9 }, { x: 8.6, y: 11.5, w: 8.2, d: 2.3 }] },
      },
    },
    '1pp': {
      outline: [0, 0, 16.8, 13.4],
      garage: { x: 0, y: 0, w: 16.8, d: 13.4 },
      common: [{ x: 11.4, y: 0.4, w: 5.0, d: 3.2, label: 'schodiště · výtah' }],
      lane: [8.4, 6.7],
      stalls: [[0.8, 1.2], [3.6, 1.2], [6.4, 1.2], [9.2, 4.4], [1.6, 7.4], [4.8, 7.4], [8.0, 7.4]].map(([x, y]) => ({ x, y, w: 2.5, d: 5.0 })),
    },
    '2pp': {
      outline: [0, 0, 16.8, 8.2],
      common: [
        { x: 0.4, y: 4.2, w: 5.0, d: 3.6, label: 'sklad · chodba' },
        { x: 5.8, y: 4.2, w: 5.2, d: 3.6, label: 'schodiště · výtah' },
        { x: 11.4, y: 4.2, w: 5.0, d: 3.6, label: 'technika' },
      ],
      cellars: Array.from({ length: 6 }, (_, i) => ({ x: 0.4 + i * 2.7, y: 0.4, w: 2.4, d: 3.4 })),
    },
  },

  facts: { units: 6, floorsAbove: 3, floorsBelow: 2 },
};
