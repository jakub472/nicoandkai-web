// Rezidence Do Čtvrti – data pro výběr bytů.
//
// Zdroj: Dokumentace pro povolení stavby JA ARCHITEKTI (08/2026), tabulky místností 1.NP–3.NP, 2.PP,
// a souhlasné vyjádření IPR Praha č. j. IPR 12986/2026 (19. 10. 2026): 3 NP, 2 PP, 6 bytů, 7 stání.
// Web ukazuje jedno podzemní podlaží (1. PP: garáž a sklepy).
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
    '1pp': 'plan-1pp.webp', '1np': 'plan-1np.webp', '2np': 'plan-2np.webp', '3np': 'plan-3np.webp',
  },

  floors: [
    { id: '3np', label: '3. NP', long: '3. nadzemní podlaží', z: 21 },
    { id: '2np', label: '2. NP', long: '2. nadzemní podlaží', z: 14 },
    { id: '1np', label: '1. NP', long: '1. nadzemní podlaží', z: 7 },
    {
      id: '1pp', label: '1. PP', long: '1. podzemní podlaží (garáž a sklepy)', z: 0, type: 'basement',
      meta: '7 stání · 6 sklepů',
      title: 'Garáž a sklepy',
      stats: [['Garážová stání', '7'], ['Sklepy', '6']],
      text: 'Garáž a sklepní kóje v podzemním podlaží se sjezdem z ulice Do čtvrti. Výtah je propojuje se všemi podlažími domu.',
      priceNote: ['Cena stání a sklepů', 'na vyžádání'],
      cta: 'Mám zájem o stání / sklep',
    },
  ],

  // ---- interaktivní fasáda (vizualizace BDDČ_17, jižní/zahradní průčelí, souřadnice v px obrázku 2400 × 1610) ----
  // Pohled od jihu: vlevo západ (A, C, E), vpravo východ (B, D, F).
  facade: {
    image: 'bddc_17', size: [2400, 1610], alt: 'Zahradní průčelí Rezidence Do Čtvrti za soumraku',
    zones: {
      E: [[190, 330], [580, 330], [580, 150], [1235, 150], [1235, 520], [190, 520]],
      F: [[1235, 150], [1870, 150], [1870, 330], [2110, 330], [2110, 520], [1235, 520]],
      C: [[380, 520], [1235, 520], [1235, 960], [190, 960], [190, 770], [380, 770]],
      D: [[1235, 520], [2110, 520], [2110, 770], [2180, 770], [2180, 960], [1235, 960]],
      A: [[300, 960], [1235, 960], [1235, 1340], [300, 1340]],
      B: [[1235, 960], [2110, 960], [2110, 1340], [1235, 1340]],
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

  // 7 stání a 6 sklepů v 1. PP
  parking: Array.from({ length: 7 }, (_, i) => ({ id: i + 1, status: 'available', price: null })),
  cellars: [5.79, 5.79, 5.79, 6.51, 6.51, 6.51].map((area, i) => ({ id: i + 1, area, status: 'available', price: null })),

  // ---- skutečné půdorysy: obrázek + zóny bytů v pixelech obrázku (1750 × 1519) ----
  // Půdorys je symetrický podle středové zdi (x ≈ 938), pravý byt je zrcadlem levého.
  planNote: 'Půdorys z projektové dokumentace (08/2026). Plochy dle projektu, závazné jsou údaje z kolaudace.',
  plans: {
    '3np': { image: 'plan-3np.webp', size: [1750, 1519], scale: 82.5, origin: [245, 240], outline: [[245,240],[1631,240],[1631,1280],[245,1280]], common: [[[705,365],[1171,365],[1171,545],[705,545]]], terraces: [[[245,240],[385,240],[385,1280],[245,1280]], [[1491,240],[1631,240],[1631,1280],[1491,1280]], [[385,1130],[1491,1130],[1491,1280],[385,1280]], [[385,240],[1491,240],[1491,365],[385,365]]],
      zones: { E: [[385, 365], [705, 365], [705, 545], [925, 545], [925, 1130], [385, 1130]], F: [[1491, 365], [1171, 365], [1171, 545], [951, 545], [951, 1130], [1491, 1130]] },
      anchors: { E: [560, 800], F: [1316, 800] } },
    '2np': { image: 'plan-2np.webp', size: [1750, 1519], scale: 82.5, origin: [245, 240], outline: [[245,240],[1631,240],[1631,1280],[245,1280]], common: [[[705,240],[1171,240],[1171,545],[705,545]]],
      zones: { C: [[245, 240], [705, 240], [705, 545], [925, 545], [925, 1280], [245, 1280]], D: [[1631, 240], [1171, 240], [1171, 545], [951, 545], [951, 1280], [1631, 1280]] },
      anchors: { C: [470, 700], D: [1406, 700] } },
    '1np': { image: 'plan-1np.webp', size: [1750, 1519], scale: 82.5, origin: [245, 240], outline: [[245,240],[1631,240],[1631,1280],[245,1280]], common: [[[705,240],[1171,240],[1171,545],[705,545]]],
      zones: { A: [[245, 240], [705, 240], [705, 545], [925, 545], [925, 1280], [245, 1280]], B: [[1631, 240], [1171, 240], [1171, 545], [951, 545], [951, 1280], [1631, 1280]] },
      anchors: { A: [470, 700], B: [1406, 700] } },
    '1pp': { image: 'plan-1pp.webp', size: [1750, 1519], zones: {}, anchors: {} },
  },

  facts: { units: 6, floorsAbove: 3, floorsBelow: 1 },
};
