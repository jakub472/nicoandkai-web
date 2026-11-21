// Apartmány Vysoké – Vysoké nad Jizerou. Dokončený projekt, poslední tři apartmány v prodeji.
//
// Zdroj: apartmanyvysoke.cz (B2: 5+kk, 193,1 m²) a zadání (A2, B2, B1 jsou poslední volné, prodej Svoboda & Williams, Jana Kocianová).
// !!! K DOPLNĚNÍ: dispozice a plochy A2 a B1, ceny, kontakt (telefon, e-mail) na makléřku.

window.NK_PROJECTS = window.NK_PROJECTS || {};
window.NK_PROJECTS['vysoke'] = {
  slug: 'vysoke',
  name: 'Apartmány Vysoké',
  place: 'Vysoké nad Jizerou',
  address: 'K. Havlíčka Borovského 442/443, 512 11 Vysoké nad Jizerou',
  stage: { label: 'Dokončeno · poslední 3 apartmány', permitShort: 'zkolaudováno' },
  units: [
    { id: 'A2', house: 'Dům A', disposition: null, area: null, status: 'available', price: null, note: 'Dispozici a plochu doplníme.' },
    { id: 'B1', house: 'Dům B', disposition: null, area: null, status: 'available', price: null, note: 'Dispozici a plochu doplníme.' },
    { id: 'B2', house: 'Dům B', disposition: '5+kk', area: 193.1, status: 'available', price: null, note: 'Prostorný apartmán přes dvě podlaží s vlastní terasou.' },
  ],
  agent: {
    company: 'Svoboda & Williams',
    name: 'Jana Kocianová',
    phone: '',   // doplnit
    email: '',   // doplnit
    url: 'https://www.svoboda-williams.com/',
  },
  external: 'https://www.apartmanyvysoke.cz/',
};
