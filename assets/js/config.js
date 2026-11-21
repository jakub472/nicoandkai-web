// Jediné místo, kam se doplňují údaje o společnosti a napojení formuláře.
// Prázdné hodnoty se na webu automaticky skryjí.
window.NK_CONFIG = {
  company: {
    legalName: '',   // např. "Nico & Kai Development s.r.o."
    ico: '',
    dic: '',
    address: '',     // sídlo / kontaktní adresa
    email: '',       // veřejný kontaktní e-mail
    phone: '',
  },

  // Prodávající u jednotlivých projektů (patička stránky projektu).
  // Rezidence ke Schodům: údaje ze stavebního povolení (stavebník).
  projects: {
    'ke-schodum': {
      seller: {
        legalName: 'Rezidence Ke schodům s.r.o.',
        ico: '23662956',
        address: 'Ke schodům 1465/14, Modřany, 143 00 Praha 12',
      },
    },
    // Do Čtvrti: prodávající zatím není určen (stavebník v řízení je Andima Estates s.r.o.) – nechte prázdné,
    // dokud nebude jasné, kdo bude prodávat a kdo přijímá rezervace.
    'do-ctvrti': {
      seller: { legalName: '', ico: '', address: '' },
    },
    // Apartmány Vysoké: kontakt na makléřku (zobrazí se na stránce projektu, jakmile ho doplníte)
    vysoke: {
      agent: { phone: '', email: '' },
    },
  },

  // Zobrazení cen bytů:
  //   'public'    – cena bytu i Kč/m²
  //   'total'     – jen cena bytu (bez Kč/m²)
  //   'onRequest' – "Cena na vyžádání" (ceník po registraci e-mailem)
  // Ceny se zadávají v assets/data/ke-schodum.js (price). Když je price null, zobrazí se "Cena na vyžádání".
  priceMode: 'onRequest',

  // Formulář: URL endpointu, který přijme POST (např. Formspree, Basin, vlastní API).
  // Když je prázdné, ale je vyplněn company.email, formulář otevře e-mailového klienta (mailto:).
  formEndpoint: '',
};
