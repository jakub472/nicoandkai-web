# -*- coding: utf-8 -*-
"""Texty webu ve třech jazycích (cs = originál, en, de). Používá tools/build-pages.py.
Struktura: UI[lang] = společné prvky (hlavička, patička, formulář, výběr bytů, sekce projektu),
PROJECTS[lang]['ks'|'dc'], HOME[lang], VYSOKE[lang], VLNITA[lang], LEGAL[lang], NOTFOUND[lang]."""

LANGS = ["cs", "en", "de"]
LANG_META = {
    "cs": {"prefix": "", "locale": "cs_CZ", "name": "Čeština", "short": "CS", "privacy": "ochrana-osobnich-udaju"},
    "en": {"prefix": "en/", "locale": "en_GB", "name": "English", "short": "EN", "privacy": "privacy"},
    "de": {"prefix": "de/", "locale": "de_DE", "name": "Deutsch", "short": "DE", "privacy": "datenschutz"},
}

# ======================================================================
# SPOLEČNÉ PRVKY
# ======================================================================
UI = {
"cs": dict(
    skip="Přeskočit na obsah", brand_aria="Nico &amp; Kai Development – úvodní stránka", menu="Menu", lang_aria="Jazyk",
    nav_main="Hlavní navigace", nav_mobile="Mobilní navigace", nav_footer="Patička",
    all_projects="Všechny projekty", choose_unit="Vybrat byt",
    p_dum="Dům", p_galerie="Galerie", p_byty="Byty", p_cenik="Ceník", p_rezervace="Rezervace",
    ks="Rezidence ke Schodům", dc="Rezidence Do Čtvrti", vy="Apartmány Vysoké", vl="Rezidence Vlnitá", privacy="Ochrana osobních údajů",
    partners_arch="Architektura", legal_company="Společnost", legal_ico="IČO", legal_dic="DIČ", legal_addr="Sídlo", legal_email="E-mail", legal_phone="Telefon",
    footer_note="Informace na&nbsp;tomto webu mají informativní charakter a&nbsp;nejsou návrhem na&nbsp;uzavření smlouvy ve&nbsp;smyslu § 1732 občanského zákoníku. Vizualizace jsou ilustrativní, plochy jsou uvedeny dle projektové dokumentace a&nbsp;mohou se změnit.",
    # formulář
    f_unit="Byt", f_unit_default="Zatím nevím / obecný dotaz", f_parking="Mám zájem o garážové stání", f_cellar="Mám zájem o sklep",
    f_name="Jméno a&nbsp;příjmení", f_email="E-mail", f_phone="Telefon", f_optional="(volitelné)", f_msg="Zpráva", f_hp="Nevyplňujte",
    f_consent_a="Souhlasím se", f_consent_link="zpracováním osobních údajů", f_consent_b="za&nbsp;účelem odpovědi na&nbsp;můj dotaz a&nbsp;zasílání informací o&nbsp;projektu.",
    # výběr bytů
    ex_floor="Podlaží", ex_cad="Půdorys z&nbsp;projektu ↗", ex_overview="Přehled bytů",
    th=["Byt", "Podlaží", "Dispozice", "Plocha", "Terasa", "Celkem", "Cena", "Stav", "Detail"], ex_dialog="Půdorys", close="Zavřít ✕",
    ex_stack_aria="Dům po podlažích – vyberte patro", ex_floors_aria="Podlaží",
    legend_av="Volný", legend_re="Rezervovaný", legend_so="Prodaný", facade_hint="Najeďte myší na byt", facade_click="Kliknutím otevřete detail bytu a půdorys",
    gallery_aria="Galerie vizualizací", photos_aria="Galerie fotografií", legend_aria="Legenda",
    # stránka projektu
    chip_suffix="stavební řízení zahájeno", credit="Vizualizace · JA Architekti", down="Dolů", cta_units="Vybrat byt", cta_pricing="Ceník a rezervace",
    sec_house="Dům", sec_gallery="Galerie", sec_units="Byty", sec_pricing="Ceník", sec_standard="Standard", sec_location="Lokalita", sec_reserve="Rezervace",
    gallery_note="Vizualizace JA Architekti. Zařízení interiéru je ilustrativní.",
    units_h=("Vyberte si", "svůj byt."),
    pricing_h=("Rezervace", "s výhodou."),
    pricing_lead="Byty prodáváme v&nbsp;průběhu stavebního řízení. Kdo se rozhodne teď, získá slevu z&nbsp;ceny bytu podle výše složené zálohy. Záloha se započítává do kupní ceny.",
    note_prices="Ceny bytů jsou uvedeny bez garážového stání a&nbsp;sklepu, které lze přikoupit. Cena po slevě se zaokrouhluje na tisíce Kč. ",
    note_noprices="Ceník bytů, garážových stání a&nbsp;sklepů vám pošleme na vyžádání, stačí vyplnit formulář níže. Sleva se počítá z&nbsp;ceny bytu. ",
    terms=[("Vyberete byt a&nbsp;složíte zálohu", "3, 4 nebo 5&nbsp;mil.&nbsp;Kč podle toho, jakou slevu chcete získat. Záloha je součástí kupní ceny."),
           ("Sleva je sjednaná ve smlouvě", "Sleva 3, 4 nebo 5&nbsp;% z&nbsp;ceny bytu se promítne do rezervační a&nbsp;následně kupní smlouvy."),
           ("Jistota vrácení zálohy", "Pokud stavební povolení nenabude právní moci do <strong data-reservation-deadline>31. 10. 2028</strong>, vrátíme vám zálohu v&nbsp;plné výši. Způsob uložení zálohy upravuje rezervační smlouva.")],
    reserve_btn="Rezervovat byt",
    form_h=("Rezervujte si", "svůj byt."), form_lead="Vyplňte krátký formulář. Ozveme se vám, projdeme detaily a&nbsp;připravíme rezervační smlouvu.",
    form_how=("Vyberete byt a&nbsp;odešlete nezávaznou žádost.", "Ozveme se vám, projdeme podmínky a&nbsp;výši zálohy.", "Po podpisu rezervační smlouvy je byt váš."),
    form_submit="Odeslat žádost o rezervaci", send="Odeslat",
),
"en": dict(
    skip="Skip to content", brand_aria="Nico &amp; Kai Development – home page", menu="Menu", lang_aria="Language",
    nav_main="Main navigation", nav_mobile="Mobile navigation", nav_footer="Footer",
    all_projects="All projects", choose_unit="Choose an apartment",
    p_dum="The house", p_galerie="Gallery", p_byty="Apartments", p_cenik="Pricing", p_rezervace="Reservation",
    ks="Rezidence ke Schodům", dc="Rezidence Do Čtvrti", vy="Apartmány Vysoké", vl="Rezidence Vlnitá", privacy="Privacy policy",
    partners_arch="Architecture", legal_company="Company", legal_ico="Company ID", legal_dic="VAT ID", legal_addr="Registered office", legal_email="E-mail", legal_phone="Phone",
    footer_note="The information on this website is for information only and does not constitute an offer to conclude a contract within the meaning of Section 1732 of the Czech Civil Code. Visualisations are illustrative; areas follow the design documentation and may change.",
    f_unit="Apartment", f_unit_default="Not sure yet / general enquiry", f_parking="I am interested in a garage space", f_cellar="I am interested in a cellar",
    f_name="Full name", f_email="E-mail", f_phone="Phone", f_optional="(optional)", f_msg="Message", f_hp="Leave empty",
    f_consent_a="I agree to the", f_consent_link="processing of my personal data", f_consent_b="for the purpose of answering my enquiry and sending information about the project.",
    ex_floor="Floor", ex_cad="Plan from the design ↗", ex_overview="Apartment overview",
    th=["Apt.", "Floor", "Layout", "Area", "Terrace", "Total", "Price", "Status", "Detail"], ex_dialog="Floor plan", close="Close ✕",
    ex_stack_aria="The house floor by floor – choose a level", ex_floors_aria="Floors",
    legend_av="Available", legend_re="Reserved", legend_so="Sold", facade_hint="Hover over an apartment", facade_click="Click to open the apartment detail and floor plan",
    gallery_aria="Gallery of visualisations", photos_aria="Photo gallery", legend_aria="Legend",
    chip_suffix="building permit applied for", credit="Visualisation · JA Architekti", down="Down", cta_units="Choose an apartment", cta_pricing="Pricing and reservation",
    sec_house="The house", sec_gallery="Gallery", sec_units="Apartments", sec_pricing="Pricing", sec_standard="Standard", sec_location="Location", sec_reserve="Reservation",
    gallery_note="Visualisations by JA Architekti. Interior furnishings are illustrative.",
    units_h=("Choose", "your apartment."),
    pricing_h=("Reserve", "with an advantage."),
    pricing_lead="We sell the apartments during the building permit procedure. Decide now and you get a discount on the apartment price according to the size of your deposit. The deposit counts towards the purchase price.",
    note_prices="Apartment prices exclude the garage space and cellar, which can be purchased separately. Discounted prices are rounded to thousands of CZK. ",
    note_noprices="We will send you the price list of apartments, garage spaces and cellars on request, just fill in the form below. The discount is calculated from the apartment price. ",
    terms=[("You choose an apartment and pay a deposit", "CZK 3, 4 or 5 million, depending on the discount you want. The deposit is part of the purchase price."),
           ("The discount is fixed in the contract", "A discount of 3, 4 or 5&nbsp;% of the apartment price is written into the reservation agreement and then the purchase agreement."),
           ("Your deposit is safe", "If the building permit does not become final by <strong data-reservation-deadline>31 October 2028</strong>, we refund your deposit in full. How the deposit is held is set out in the reservation agreement.")],
    reserve_btn="Reserve an apartment",
    form_h=("Reserve", "your apartment."), form_lead="Fill in the short form. We will get back to you, go through the details and prepare the reservation agreement.",
    form_how=("Choose an apartment and send a non-binding request.", "We contact you and go through the terms and the deposit.", "Once the reservation agreement is signed, the apartment is yours."),
    form_submit="Send reservation request", send="Send",
),
"de": dict(
    skip="Zum Inhalt springen", brand_aria="Nico &amp; Kai Development – Startseite", menu="Menü", lang_aria="Sprache",
    nav_main="Hauptnavigation", nav_mobile="Mobile Navigation", nav_footer="Fußzeile",
    all_projects="Alle Projekte", choose_unit="Wohnung wählen",
    p_dum="Das Haus", p_galerie="Galerie", p_byty="Wohnungen", p_cenik="Preise", p_rezervace="Reservierung",
    ks="Rezidence ke Schodům", dc="Rezidence Do Čtvrti", vy="Apartmány Vysoké", vl="Rezidence Vlnitá", privacy="Datenschutz",
    partners_arch="Architektur", legal_company="Gesellschaft", legal_ico="Firmen-ID (IČO)", legal_dic="USt-IdNr.", legal_addr="Sitz", legal_email="E-Mail", legal_phone="Telefon",
    footer_note="Die Angaben auf dieser Website dienen nur der Information und stellen kein Angebot zum Vertragsabschluss im Sinne von § 1732 des tschechischen Bürgerlichen Gesetzbuchs dar. Visualisierungen sind unverbindlich; Flächen entsprechen der Projektplanung und können sich ändern.",
    f_unit="Wohnung", f_unit_default="Noch unklar / allgemeine Anfrage", f_parking="Ich interessiere mich für einen Garagenstellplatz", f_cellar="Ich interessiere mich für einen Keller",
    f_name="Vor- und Nachname", f_email="E-Mail", f_phone="Telefon", f_optional="(optional)", f_msg="Nachricht", f_hp="Nicht ausfüllen",
    f_consent_a="Ich stimme der", f_consent_link="Verarbeitung meiner personenbezogenen Daten", f_consent_b="zur Beantwortung meiner Anfrage und zum Versand von Informationen über das Projekt zu.",
    ex_floor="Geschoss", ex_cad="Grundriss aus dem Projekt ↗", ex_overview="Wohnungsübersicht",
    th=["Whg.", "Geschoss", "Grundriss", "Fläche", "Terrasse", "Gesamt", "Preis", "Status", "Detail"], ex_dialog="Grundriss", close="Schließen ✕",
    ex_stack_aria="Das Haus nach Geschossen – wählen Sie eine Etage", ex_floors_aria="Geschosse",
    legend_av="Frei", legend_re="Reserviert", legend_so="Verkauft", facade_hint="Fahren Sie mit der Maus über eine Wohnung", facade_click="Klicken Sie für Wohnungsdetail und Grundriss",
    gallery_aria="Galerie der Visualisierungen", photos_aria="Fotogalerie", legend_aria="Legende",
    chip_suffix="Baugenehmigung beantragt", credit="Visualisierung · JA Architekti", down="Nach unten", cta_units="Wohnung wählen", cta_pricing="Preise und Reservierung",
    sec_house="Das Haus", sec_gallery="Galerie", sec_units="Wohnungen", sec_pricing="Preise", sec_standard="Ausstattung", sec_location="Lage", sec_reserve="Reservierung",
    gallery_note="Visualisierungen JA Architekti. Die Inneneinrichtung ist unverbindlich.",
    units_h=("Wählen Sie", "Ihre Wohnung."),
    pricing_h=("Reservieren", "mit Vorteil."),
    pricing_lead="Wir verkaufen die Wohnungen während des Genehmigungsverfahrens. Wer sich jetzt entscheidet, erhält je nach Höhe der Anzahlung einen Rabatt auf den Wohnungspreis. Die Anzahlung wird auf den Kaufpreis angerechnet.",
    note_prices="Die Wohnungspreise verstehen sich ohne Garagenstellplatz und Keller, die hinzugekauft werden können. Rabattierte Preise werden auf Tausend CZK gerundet. ",
    note_noprices="Die Preisliste für Wohnungen, Garagenstellplätze und Keller senden wir Ihnen auf Anfrage, füllen Sie einfach das Formular unten aus. Der Rabatt wird vom Wohnungspreis berechnet. ",
    terms=[("Sie wählen eine Wohnung und leisten eine Anzahlung", "3, 4 oder 5&nbsp;Mio.&nbsp;CZK, je nachdem, welchen Rabatt Sie erhalten möchten. Die Anzahlung ist Teil des Kaufpreises."),
           ("Der Rabatt wird vertraglich vereinbart", "Ein Rabatt von 3, 4 oder 5&nbsp;% des Wohnungspreises wird in den Reservierungs- und anschließend in den Kaufvertrag aufgenommen."),
           ("Sicherheit der Anzahlung", "Wird die Baugenehmigung nicht bis zum <strong data-reservation-deadline>31. Oktober 2028</strong> rechtskräftig, erstatten wir Ihnen die Anzahlung in voller Höhe. Die Verwahrung der Anzahlung regelt der Reservierungsvertrag.")],
    reserve_btn="Wohnung reservieren",
    form_h=("Reservieren Sie", "Ihre Wohnung."), form_lead="Füllen Sie das kurze Formular aus. Wir melden uns, besprechen die Details und bereiten den Reservierungsvertrag vor.",
    form_how=("Sie wählen eine Wohnung und senden eine unverbindliche Anfrage.", "Wir melden uns und besprechen Bedingungen und Anzahlung.", "Nach Unterzeichnung des Reservierungsvertrags gehört die Wohnung Ihnen."),
    form_submit="Reservierungsanfrage senden", send="Senden",
),
}

# ======================================================================
# PROJEKTY: KE SCHODŮM (ks) A DO ČTVRTI (dc)
# ======================================================================
KS_COMMON = dict(slug="ke-schodum", name="Rezidence ke Schodům", street="Ke Schodům", units=8, og="og-ke-schodum.jpg",
                 hero="bdks_22", video="ke-schodum", facade="bdks_02", canonical="ke-schodum", numbers_n=[("8", ""), ("104", "m²"), ("16", ""), ("2028", "")])
DC_COMMON = dict(slug="do-ctvrti", name="Rezidence Do Čtvrti", street="Do čtvrti 1145/20", units=6, og="og-do-ctvrti.jpg",
                 hero="bddc_01a", video="do-ctvrti", facade="bddc_17", canonical="do-ctvrti", numbers_n=[("6", ""), ("2", ""), ("7", ""), ("91", "m²")])

PROJECTS = {
"cs": {
"ks": dict(KS_COMMON,
    title="Rezidence ke Schodům | Nico &amp; Kai Development",
    desc="Osm bytů s velkými terasami a zahradami v Praze-Modřanech. Pohledový beton, dřevo, tepelná čerpadla a fotovoltaika. Předprodej zahájen.",
    hero_alt="Rezidence ke Schodům – zahradní průčelí za soumraku", stage="Předprodej zahájen",
    h1a="Rezidence", h1b="ke&nbsp;Schodům",
    lead="Osm bytů, osm teras a&nbsp;zahrad. Dům v&nbsp;klidné části Modřan, kde se bydlí uvnitř i&nbsp;venku.",
    meta=[("Lokalita", "Praha-Modřany"), ("Byty", "8 · 2+kk a 3+kk"), ("Terasy", "19–104&nbsp;m²"), ("Dokončení", "2. čtvrtletí 2028")],
    manifest="Každý byt má svou <strong>zahradu nebo terasu</strong>. Materiály, které stárnou krásně: <strong>pohledový beton, dřevo a&nbsp;sklo</strong>. A&nbsp;dům, který si energii vyrábí sám.",
    numbers_l=["bytů 2+kk a 3+kk", "největší terasa", "garážových stání", "dokončení stavby"],
    gal_h=("Dům, který", "chcete vidět zblízka."),
    gal_p="Tři nadzemní podlaží s&nbsp;ustupujícími terasami, vegetační střechy a&nbsp;fasáda z&nbsp;patinovaného plechu, která mění barvu se světlem.",
    gallery=[("bdks_13", "Rezidence ke Schodům z ulice", "Pohled z ulice", "is-big"), ("bdks_18", "Detail fasády a velkoformátových oken", "Detail fasády", ""), ("bdks_10", "Zahradní strana domu se zelení", "Zahrada", ""),
             ("bdks_07", "Nároží domu se stromy", "Nároží", ""), ("bdks_19", "Dům za soumraku", "Soumrak", "is-wide"), ("bdks_09", "Dům v zimě", "Zima", ""),
             ("bdks_03", "Vstup do domu", "Vstup", ""), ("bdks_20", "Severní strana s pavlačí", "Pavlač a vstupy do bytů", "is-wide"), ("bdks_08", "Večerní pohled na roh domu", "Večer", "")],
    splits=[("bdks_10", "Terasy a zahrady Rezidence ke Schodům", "Terasa jako další pokoj.", "<p>Byty v&nbsp;přízemí mají vlastní zahradu, byty v&nbsp;patrech terasy od 25 do 104&nbsp;m². Dřevěná paluba, zeleň na střechách a&nbsp;skleněné zábradlí. Venku strávíte víc času, než jste čekali.</p>"),
            ("bdks_18", "Detail fasády z patinovaného plechu", "Materiály, které stárnou krásně.", "<p>Fasáda z&nbsp;plechových panelů s&nbsp;přiznanými spárami mění barvu během dne. Uvnitř pohledový beton, třívrstvé dřevěné podlahy a&nbsp;minerální stěrky. Nic, co by se za pár let muselo předělávat.</p>"),
            ("bdks_20", "Pavlač na severní straně domu", "Soukromí na prvním místě.", "<p>Do bytů se vchází z&nbsp;otevřených pavlačí na severní straně. Obytné místnosti a&nbsp;terasy míří na jih, do zahrady. Mezi byty je železobetonová stěna, sousedy neuslyšíte.</p>")],
    facade_alt="Jižní průčelí Rezidence ke Schodům – vyberte byt najetím myší",
    plan_note="Půdorys z projektové dokumentace (12/2025). Plochy a&nbsp;dispozice dle projektu, závazné jsou údaje z&nbsp;prohlášení vlastníka.",
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
),
"dc": dict(DC_COMMON,
    title="Rezidence Do Čtvrti | Nico &amp; Kai Development",
    desc="Šest bytů v nárožním domě v Praze-Modřanech. Zahrady, balkony a střešní terasy, garáž a sklepy. Předprodej zahájen.",
    hero_alt="Rezidence Do Čtvrti – nárožní dům za soumraku", stage="Předprodej zahájen",
    h1a="Rezidence", h1b="Do&nbsp;Čtvrti",
    lead="Šest bytů v&nbsp;domě se zaoblenými rohy a&nbsp;fasádou z&nbsp;perforovaného zdiva. Vždy jen dva byty na podlaží.",
    meta=[("Lokalita", "Praha-Modřany"), ("Byty", "6 · 2+kk a 3+kk"), ("Venkovní prostory", "zahrady, balkony, terasy"), ("Souhlas IPR", "19. 10. 2026")],
    manifest="Dům pro <strong>šest domácností</strong>. Přízemí se zahradou, patro s&nbsp;balkony, střecha s&nbsp;terasami. <strong>Vlastní výtah</strong> až do garáže a&nbsp;sousedé, které znáte jménem.",
    numbers_l=["bytů 2+kk a 3+kk", "byty na každém podlaží", "garážových stání", "největší zahrada"],
    gal_h=("Jemné křivky,", "pevný charakter."),
    gal_p="Nároží ulic Do čtvrti a&nbsp;Malá Tyršovka. Ustupující poslední podlaží, zaoblené rohy a&nbsp;zábradlí z&nbsp;perforovaných cihel, které propouští světlo i&nbsp;soukromí.",
    gallery=[("bddc_03", "Rezidence Do Čtvrti – nároží za dne", "Nároží", "is-big"), ("bddc_int_01", "Obývací pokoj s kuchyní", "Obývací pokoj", ""), ("bddc_int_02", "Ložnice", "Ložnice", ""),
             ("bddc_05a", "Vstupní průčelí ze severu při západu slunce", "Vstup z ulice", ""), ("bddc_16", "Zahradní průčelí zblízka", "Zahrada", "is-wide"), ("bddc_int_04", "Koupelna", "Koupelna", ""),
             ("bddc_09", "Dům z nadhledu za soumraku", "Z nadhledu", ""), ("bddc_int_05", "Jídelna s terasou", "Jídelna", "is-wide"), ("bddc_12b", "Zimní pohled s vjezdem do garáže", "Zima", "")],
    splits=[("bddc_17", "Zahradní průčelí za soumraku", "Zahrada za domem, ne za městem.", "<p>Byty v&nbsp;přízemí mají vlastní zahradu o&nbsp;84 a&nbsp;91&nbsp;m², patro balkony a&nbsp;horní byty střešní terasy přes 40&nbsp;m². Obytné místnosti jsou otočené k&nbsp;jihu, do zeleně.</p>"),
            ("bddc_int_07", "Vstupní hala s perforovanou stěnou", "Světlo skrz cihlu.", "<p>Perforované zdivo na zábradlích a&nbsp;ve vstupní hale propouští světlo a&nbsp;zároveň chrání soukromí. Uvnitř omítky v&nbsp;teplých tónech, dřevo a&nbsp;kámen.</p>"),
            ("bddc_rez", "Řez domem", "Dům v&nbsp;řezu.", "<p>Tři nadzemní podlaží, pod nimi garáž se sedmi stáními a&nbsp;ještě níž sklepy a&nbsp;technika. Výtah jezdí ze sklepa až ke dveřím bytu.</p>")],
    facade_alt="Zahradní průčelí Rezidence Do Čtvrti – vyberte byt najetím myší",
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
),
},
"en": {
"ks": dict(KS_COMMON,
    title="Rezidence ke Schodům | Nico &amp; Kai Development",
    desc="Eight apartments with large terraces and gardens in Prague-Modřany. Exposed concrete, wood, heat pumps and photovoltaics. Pre-sale open.",
    hero_alt="Rezidence ke Schodům – garden facade at dusk", stage="Pre-sale open",
    h1a="Rezidence", h1b="ke&nbsp;Schodům",
    lead="Eight apartments, eight terraces and gardens. A house in a quiet part of Modřany where life happens inside and out.",
    meta=[("Location", "Prague-Modřany"), ("Apartments", "8 · 2+kk and 3+kk"), ("Terraces", "19–104&nbsp;m²"), ("Completion", "Q2 2028")],
    manifest="Every apartment has its own <strong>garden or terrace</strong>. Materials that age beautifully: <strong>exposed concrete, wood and glass</strong>. And a house that makes its own energy.",
    numbers_l=["apartments, 2+kk and 3+kk", "largest terrace", "garage spaces", "completion of construction"],
    gal_h=("A house you want", "to see up close."),
    gal_p="Three storeys with stepped terraces, green roofs and a patinated metal facade that changes colour with the light.",
    gallery=[("bdks_13", "Rezidence ke Schodům from the street", "Street view", "is-big"), ("bdks_18", "Facade detail and large-format windows", "Facade detail", ""), ("bdks_10", "Garden side of the house with greenery", "Garden", ""),
             ("bdks_07", "Corner of the house with trees", "Corner", ""), ("bdks_19", "The house at dusk", "Dusk", "is-wide"), ("bdks_09", "The house in winter", "Winter", ""),
             ("bdks_03", "Entrance to the house", "Entrance", ""), ("bdks_20", "North side with the access gallery", "Access gallery and apartment entrances", "is-wide"), ("bdks_08", "Evening view of the corner of the house", "Evening", "")],
    splits=[("bdks_10", "Terraces and gardens of Rezidence ke Schodům", "The terrace as another room.", "<p>Ground-floor apartments have their own garden, upper floors have terraces from 25 to 104&nbsp;m². Timber decking, green roofs and glass balustrades. You will spend more time outside than you expected.</p>"),
            ("bdks_18", "Detail of the patinated metal facade", "Materials that age beautifully.", "<p>A facade of metal panels with exposed joints changes colour over the day. Inside: exposed concrete, three-layer wooden floors and mineral plasters. Nothing that would need redoing in a few years.</p>"),
            ("bdks_20", "Access gallery on the north side", "Privacy first.", "<p>Apartments are entered from open galleries on the north side. Living rooms and terraces face south, into the garden. A reinforced-concrete wall between apartments means you will not hear the neighbours.</p>")],
    facade_alt="South facade of Rezidence ke Schodům – hover to choose an apartment",
    plan_note="Floor plan from the design documentation (12/2025). Areas and layouts per the design; the binding figures will be stated in the declaration of the owner.",
    cad_note="Floor plan from the building permit documentation (12/2025). Furnishings and equipment are illustrative.",
    price_note="The apartment area is an estimate of the floor area under Czech Government Regulation No. 366/2013 Coll.; the binding figure will be stated in the declaration of the owner.",
    tech_h=("A house that", "saves energy."),
    tech=[("Energy", ["Cascade of air-to-water heat pumps", "Rooftop photovoltaic plant with battery storage", "Underfloor heating and cooling", "No gas connection"]),
          ("Structure and interior", ["Reinforced-concrete structure, exposed concrete", "Three-layer wooden floors, mineral plasters", "Large-format glazing, aluminium windows", "Party walls Rw 57–58&nbsp;dB"]),
          ("The house", ["Lift from the garage to every floor", "16 garage spaces, 8 cellars", "Green roofs and a shared roof terrace", "Pre-wired for electric-car charging"])],
    tech_note="Based on the building permit documentation (12/2025). Final execution, layouts and areas may change.",
    lok_h=("Modřany,", "calm by the Vltava."),
    lok_p="A villa district above the Vltava. Five minutes to the river and the cycle path, the woods of Modřanská rokle around the corner and a direct tram to the centre.",
    addr=[("Address", "Ke Schodům street, Prague 12 – Modřany"), ("Cadastre", "Modřany, plot no. 1505/1"), ("Transport", "tram and bus within walking distance"), ("Nature", "Vltava river, Modřanská rokle"), ("Architect", "JA Architekti, Ing. arch. Andrea Jašková")],
    steps=[("12/2025", "Building permit application", "Building permit documentation submitted.", False), ("Now", "Pre-sale", "Reserve with a discount of up to 5&nbsp;%.", True), ("Q1 2027", "Start of construction", "Expected start of works.", False), ("Q2 2028", "Completion", "Expected handover of apartments.", False)],
),
"dc": dict(DC_COMMON,
    title="Rezidence Do Čtvrti | Nico &amp; Kai Development",
    desc="Six apartments in a corner house in Prague-Modřany. Gardens, balconies and roof terraces, garage and cellars. Pre-sale open.",
    hero_alt="Rezidence Do Čtvrti – corner house at dusk", stage="Pre-sale open",
    h1a="Rezidence", h1b="Do&nbsp;Čtvrti",
    lead="Six apartments in a house with rounded corners and a facade of perforated brickwork. Only two apartments per floor.",
    meta=[("Location", "Prague-Modřany"), ("Apartments", "6 · 2+kk and 3+kk"), ("Outdoor spaces", "gardens, balconies, terraces"), ("IPR approval", "19 Oct 2026")],
    manifest="A house for <strong>six households</strong>. Ground floor with gardens, first floor with balconies, roof with terraces. <strong>Your own lift</strong> down to the garage and neighbours you know by name.",
    numbers_l=["apartments, 2+kk and 3+kk", "apartments per floor", "garage spaces", "largest garden"],
    gal_h=("Soft curves,", "strong character."),
    gal_p="The corner of Do čtvrti and Malá Tyršovka streets. A set-back top floor, rounded corners and balustrades of perforated brick that let in light while keeping privacy.",
    gallery=[("bddc_03", "Rezidence Do Čtvrti – the corner by day", "Corner", "is-big"), ("bddc_int_01", "Living room with kitchen", "Living room", ""), ("bddc_int_02", "Bedroom", "Bedroom", ""),
             ("bddc_05a", "Entrance facade from the north at sunset", "Street entrance", ""), ("bddc_16", "Garden facade up close", "Garden", "is-wide"), ("bddc_int_04", "Bathroom", "Bathroom", ""),
             ("bddc_09", "The house from above at dusk", "From above", ""), ("bddc_int_05", "Dining room with terrace", "Dining room", "is-wide"), ("bddc_12b", "Winter view with the garage entrance", "Winter", "")],
    splits=[("bddc_17", "Garden facade at dusk", "A garden behind the house, not behind the city.", "<p>Ground-floor apartments have their own gardens of 84 and 91&nbsp;m², the first floor has balconies and the top apartments roof terraces of over 40&nbsp;m². Living rooms face south, into the greenery.</p>"),
            ("bddc_int_07", "Entrance hall with the perforated wall", "Light through brick.", "<p>Perforated brickwork on the balustrades and in the entrance hall lets light through while protecting privacy. Inside: warm-toned plasters, wood and stone.</p>"),
            ("bddc_rez", "Section through the house", "The house in section.", "<p>Three storeys, a garage with seven spaces beneath them and cellars and utilities further down. The lift runs from the cellar right to your apartment door.</p>")],
    facade_alt="Garden facade of Rezidence Do Čtvrti – hover to choose an apartment",
    plan_note="Floor plan from the design documentation (08/2026). Apartment area indicative per Regulation 366/2013. Binding figures will be stated in the declaration of the owner.",
    cad_note="Floor plan from the building permit documentation (08/2026). Furnishings and equipment are illustrative.",
    price_note="The apartment area is the floor area under Czech Government Regulation No. 366/2013 Coll. (an indicative estimate from the plans); the binding figure will be stated in the declaration of the owner.",
    tech_h=("An efficient house", "with its own energy."),
    tech=[("Energy", ["Air-to-water heat pumps", "Rooftop photovoltaic plant", "Underfloor heating", "No gas connection"]),
          ("Structure", ["Monolithic reinforced-concrete structure", "Flat green roof", "Aluminium windows", "Perforated brick balustrades"]),
          ("The house", ["Lift from the cellar to the roof terraces", "7 garage spaces, 6 cellars", "Pre-wired for electric-car charging", "Quiet villa district"])],
    tech_note="Based on the building permit documentation (08/2026). The permit procedure is under way; the final design, layouts and areas may change.",
    lok_h=("Tyršova čtvrť,", "Modřany."),
    lok_p="A corner plot in a quiet villa district of family houses. Woods within reach, the Vltava below the hill, the centre by tram.",
    addr=[("Address", "Do čtvrti 1145/20 and Malá Tyršovka, Prague 12 – Modřany"), ("Plot", "516&nbsp;m², plots no. 1540, 1539/1, 1539/2"), ("Zoning", "OB – purely residential, approved by IPR Prague"), ("Nature", "woods above Modřany, Vltava river"), ("Architect", "JA Architekti, Ing. arch. Andrea Jašková")],
    steps=[("08/2026", "Building permit application", "Documentation submitted, IPR Prague approval 19 Oct 2026.", False), ("Now", "Pre-sale", "Reserve with a discount of up to 5&nbsp;%.", True), ("2027", "Building permit", "Expected to become final.", False), ("2029", "Completion", "Expected handover of apartments.", False)],
),
},
"de": {
"ks": dict(KS_COMMON,
    title="Rezidence ke Schodům | Nico &amp; Kai Development",
    desc="Acht Wohnungen mit großen Terrassen und Gärten in Prag-Modřany. Sichtbeton, Holz, Wärmepumpen und Photovoltaik. Vorverkauf gestartet.",
    hero_alt="Rezidence ke Schodům – Gartenfassade in der Abenddämmerung", stage="Vorverkauf gestartet",
    h1a="Rezidence", h1b="ke&nbsp;Schodům",
    lead="Acht Wohnungen, acht Terrassen und Gärten. Ein Haus in einem ruhigen Teil von Modřany, in dem man drinnen wie draußen lebt.",
    meta=[("Lage", "Prag-Modřany"), ("Wohnungen", "8 · 2+kk und 3+kk"), ("Terrassen", "19–104&nbsp;m²"), ("Fertigstellung", "2. Quartal 2028")],
    manifest="Jede Wohnung hat ihren eigenen <strong>Garten oder ihre Terrasse</strong>. Materialien, die schön altern: <strong>Sichtbeton, Holz und Glas</strong>. Und ein Haus, das seine Energie selbst erzeugt.",
    numbers_l=["Wohnungen 2+kk und 3+kk", "größte Terrasse", "Garagenstellplätze", "Fertigstellung"],
    gal_h=("Ein Haus, das man", "aus der Nähe sehen will."),
    gal_p="Drei Geschosse mit zurückgestaffelten Terrassen, begrünte Dächer und eine Fassade aus patiniertem Blech, die ihre Farbe mit dem Licht wechselt.",
    gallery=[("bdks_13", "Rezidence ke Schodům von der Straße", "Blick von der Straße", "is-big"), ("bdks_18", "Fassadendetail und großformatige Fenster", "Fassadendetail", ""), ("bdks_10", "Gartenseite des Hauses mit Grün", "Garten", ""),
             ("bdks_07", "Hausecke mit Bäumen", "Ecke", ""), ("bdks_19", "Das Haus in der Abenddämmerung", "Abenddämmerung", "is-wide"), ("bdks_09", "Das Haus im Winter", "Winter", ""),
             ("bdks_03", "Hauseingang", "Eingang", ""), ("bdks_20", "Nordseite mit Laubengang", "Laubengang und Wohnungseingänge", "is-wide"), ("bdks_08", "Abendlicher Blick auf die Hausecke", "Abend", "")],
    splits=[("bdks_10", "Terrassen und Gärten der Rezidence ke Schodům", "Die Terrasse als weiteres Zimmer.", "<p>Die Erdgeschosswohnungen haben einen eigenen Garten, die oberen Geschosse Terrassen von 25 bis 104&nbsp;m². Holzdeck, begrünte Dächer und Glasbrüstungen. Sie werden mehr Zeit draußen verbringen, als Sie dachten.</p>"),
            ("bdks_18", "Detail der Fassade aus patiniertem Blech", "Materialien, die schön altern.", "<p>Die Fassade aus Blechpaneelen mit sichtbaren Fugen wechselt im Lauf des Tages die Farbe. Innen Sichtbeton, dreischichtige Holzböden und Mineralspachtel. Nichts, was man in ein paar Jahren erneuern müsste.</p>"),
            ("bdks_20", "Laubengang auf der Nordseite", "Privatsphäre zuerst.", "<p>Die Wohnungen werden über offene Laubengänge auf der Nordseite erschlossen. Wohnräume und Terrassen sind nach Süden, zum Garten, ausgerichtet. Zwischen den Wohnungen liegt eine Stahlbetonwand, die Nachbarn hört man nicht.</p>")],
    facade_alt="Südfassade der Rezidence ke Schodům – Wohnung per Mauszeiger wählen",
    plan_note="Grundriss aus der Projektplanung (12/2025). Flächen und Grundrisse laut Projekt; verbindlich sind die Angaben der Teilungserklärung.",
    cad_note="Grundriss aus der Baugenehmigungsplanung (12/2025). Möblierung und Ausstattung sind unverbindlich.",
    price_note="Die Wohnfläche ist eine Schätzung der Bodenfläche gemäß tschechischer Regierungsverordnung Nr. 366/2013 Slg.; verbindlich ist die Angabe in der Teilungserklärung.",
    tech_h=("Ein Haus, das", "Energie spart."),
    tech=[("Energie", ["Kaskade von Luft-Wasser-Wärmepumpen", "Photovoltaikanlage auf dem Dach mit Batteriespeicher", "Fußbodenheizung und -kühlung", "Kein Gasanschluss"]),
          ("Konstruktion und Interieur", ["Stahlbetonkonstruktion, Sichtbeton", "Dreischichtige Holzböden, Mineralspachtel", "Großformatige Verglasung, Aluminiumfenster", "Wohnungstrennwände Rw 57–58&nbsp;dB"]),
          ("Das Haus", ["Aufzug von der Garage in alle Geschosse", "16 Garagenstellplätze, 8 Keller", "Begrünte Dächer und gemeinsame Dachterrasse", "Vorbereitung für E-Auto-Ladestationen"])],
    tech_note="Angaben auf Basis der Baugenehmigungsplanung (12/2025). Endgültige Ausführung, Grundrisse und Flächen können sich ändern.",
    lok_h=("Modřany,", "Ruhe an der Moldau."),
    lok_p="Ein Villenviertel über der Moldau. Fünf Minuten zum Fluss und zum Radweg, der Wald der Modřanská rokle um die Ecke und mit der Straßenbahn ohne Umsteigen ins Zentrum.",
    addr=[("Adresse", "Straße Ke Schodům, Prag 12 – Modřany"), ("Kataster", "Modřany, Parz. Nr. 1505/1"), ("Verkehr", "Straßenbahn und Bus in Gehweite"), ("Natur", "Moldau, Modřanská rokle"), ("Architekt", "JA Architekti, Ing. arch. Andrea Jašková")],
    steps=[("12/2025", "Antrag auf Baugenehmigung", "Baugenehmigungsplanung eingereicht.", False), ("Jetzt", "Vorverkauf", "Reservierung mit bis zu 5&nbsp;% Rabatt.", True), ("1. Quartal 2027", "Baubeginn", "Voraussichtlicher Baubeginn.", False), ("2. Quartal 2028", "Fertigstellung", "Voraussichtliche Übergabe der Wohnungen.", False)],
),
"dc": dict(DC_COMMON,
    title="Rezidence Do Čtvrti | Nico &amp; Kai Development",
    desc="Sechs Wohnungen in einem Eckhaus in Prag-Modřany. Gärten, Balkone und Dachterrassen, Garage und Keller. Vorverkauf gestartet.",
    hero_alt="Rezidence Do Čtvrti – Eckhaus in der Abenddämmerung", stage="Vorverkauf gestartet",
    h1a="Rezidence", h1b="Do&nbsp;Čtvrti",
    lead="Sechs Wohnungen in einem Haus mit abgerundeten Ecken und einer Fassade aus perforiertem Mauerwerk. Nur zwei Wohnungen pro Geschoss.",
    meta=[("Lage", "Prag-Modřany"), ("Wohnungen", "6 · 2+kk und 3+kk"), ("Außenbereiche", "Gärten, Balkone, Terrassen"), ("Zustimmung IPR", "19. 10. 2026")],
    manifest="Ein Haus für <strong>sechs Haushalte</strong>. Erdgeschoss mit Garten, Obergeschoss mit Balkonen, Dach mit Terrassen. <strong>Eigener Aufzug</strong> bis in die Garage und Nachbarn, die man beim Namen kennt.",
    numbers_l=["Wohnungen 2+kk und 3+kk", "Wohnungen pro Geschoss", "Garagenstellplätze", "größter Garten"],
    gal_h=("Sanfte Kurven,", "fester Charakter."),
    gal_p="Die Ecke der Straßen Do čtvrti und Malá Tyršovka. Zurückgesetztes oberstes Geschoss, abgerundete Ecken und Brüstungen aus perforierten Ziegeln, die Licht und Privatsphäre zugleich bieten.",
    gallery=[("bddc_03", "Rezidence Do Čtvrti – die Ecke bei Tag", "Ecke", "is-big"), ("bddc_int_01", "Wohnzimmer mit Küche", "Wohnzimmer", ""), ("bddc_int_02", "Schlafzimmer", "Schlafzimmer", ""),
             ("bddc_05a", "Eingangsfassade von Norden bei Sonnenuntergang", "Eingang von der Straße", ""), ("bddc_16", "Gartenfassade aus der Nähe", "Garten", "is-wide"), ("bddc_int_04", "Bad", "Bad", ""),
             ("bddc_09", "Das Haus von oben in der Abenddämmerung", "Von oben", ""), ("bddc_int_05", "Esszimmer mit Terrasse", "Esszimmer", "is-wide"), ("bddc_12b", "Winteransicht mit Garageneinfahrt", "Winter", "")],
    splits=[("bddc_17", "Gartenfassade in der Abenddämmerung", "Ein Garten hinter dem Haus, nicht hinter der Stadt.", "<p>Die Erdgeschosswohnungen haben eigene Gärten mit 84 und 91&nbsp;m², das Obergeschoss Balkone und die oberen Wohnungen Dachterrassen mit über 40&nbsp;m². Die Wohnräume sind nach Süden, ins Grüne, ausgerichtet.</p>"),
            ("bddc_int_07", "Eingangshalle mit perforierter Wand", "Licht durch den Ziegel.", "<p>Perforiertes Mauerwerk an den Brüstungen und in der Eingangshalle lässt Licht herein und schützt zugleich die Privatsphäre. Innen Putze in warmen Tönen, Holz und Stein.</p>"),
            ("bddc_rez", "Schnitt durch das Haus", "Das Haus im Schnitt.", "<p>Drei Geschosse, darunter eine Garage mit sieben Stellplätzen und noch tiefer Keller und Haustechnik. Der Aufzug fährt vom Keller bis vor die Wohnungstür.</p>")],
    facade_alt="Gartenfassade der Rezidence Do Čtvrti – Wohnung per Mauszeiger wählen",
    plan_note="Grundriss aus der Projektplanung (08/2026). Wohnfläche orientierend gemäß VO 366/2013. Verbindliche Angaben stehen in der Teilungserklärung.",
    cad_note="Grundriss aus der Baugenehmigungsplanung (08/2026). Möblierung und Ausstattung sind unverbindlich.",
    price_note="Die Wohnfläche ist die Bodenfläche gemäß tschechischer Regierungsverordnung Nr. 366/2013 Slg. (Richtwert aus den Grundrissen); verbindlich ist die Angabe in der Teilungserklärung.",
    tech_h=("Ein sparsames Haus", "mit eigener Energie."),
    tech=[("Energie", ["Luft-Wasser-Wärmepumpen", "Photovoltaikanlage auf dem Dach", "Fußbodenheizung", "Kein Gasanschluss"]),
          ("Konstruktion", ["Monolithische Stahlbetonkonstruktion", "Begrüntes Flachdach", "Aluminiumfenster", "Brüstungen aus perforierten Ziegeln"]),
          ("Das Haus", ["Aufzug vom Keller bis zu den Dachterrassen", "7 Garagenstellplätze, 6 Keller", "Vorbereitung für E-Auto-Ladestationen", "Ruhiges Villenviertel"])],
    tech_note="Angaben auf Basis der Baugenehmigungsplanung (08/2026). Das Genehmigungsverfahren läuft; endgültige Lösung, Grundrisse und Flächen können sich ändern.",
    lok_h=("Tyršova čtvrť,", "Modřany."),
    lok_p="Eckgrundstück in einem ruhigen Villenviertel mit Einfamilienhäusern. Wald in Reichweite, die Moldau unterhalb des Hügels, das Zentrum mit der Straßenbahn.",
    addr=[("Adresse", "Do čtvrti 1145/20 und Malá Tyršovka, Prag 12 – Modřany"), ("Grundstück", "516&nbsp;m², Parz. Nr. 1540, 1539/1, 1539/2"), ("Flächennutzung", "OB – reines Wohngebiet, Zustimmung IPR Prag"), ("Natur", "Wälder über Modřany, Moldau"), ("Architekt", "JA Architekti, Ing. arch. Andrea Jašková")],
    steps=[("08/2026", "Antrag auf Baugenehmigung", "Planung eingereicht, Zustimmung IPR Prag am 19. 10. 2026.", False), ("Jetzt", "Vorverkauf", "Reservierung mit bis zu 5&nbsp;% Rabatt.", True), ("2027", "Baugenehmigung", "Voraussichtliche Rechtskraft.", False), ("2029", "Fertigstellung", "Voraussichtliche Übergabe der Wohnungen.", False)],
),
},
}

# ======================================================================
# ÚVOD
# ======================================================================
HOME = {
"cs": dict(
    title="Nico &amp; Kai Development | Rezidenční projekty v Praze a v horách",
    desc="Nico & Kai Development staví domy, ve kterých se dobře žije. Rezidence ke Schodům a Do Čtvrti v Praze-Modřanech v předprodeji, Apartmány Vysoké a Rezidence Vlnitá dokončeny.",
    org_desc="Rezidenční development v Praze a v horách.",
    nav=[("#projekty", "Projekty"), ("#pristup", "Jak stavíme"), ("#reference", "Reference"), ("#kontakt", "Kontakt")],
    cta_header="Vybrat byt", eyebrow="Nico &amp; Kai Development",
    h1a="Domov,", h1b="na který se těšíte.",
    lead="Stavíme domy pro skutečný život. Ne metry čtvereční, ale místa, kam se chcete vracet. V&nbsp;Praze i&nbsp;v&nbsp;horách.",
    cta1="Naše projekty", cta2="Předprodej: Ke Schodům",
    meta=[("V předprodeji", "Rezidence ke&nbsp;Schodům · Do&nbsp;Čtvrti"), ("V nabídce", "Apartmány Vysoké"), ("Dokončeno", "Rezidence Vlnitá")],
    s1="Kdo jsme", manifest="Neprodáváme byty. <strong>Vytváříme místa, kde se žije dobře.</strong> Promyšlená architektura, poctivé materiály a&nbsp;otevřená komunikace od první schůzky po předání klíčů.",
    numbers=[("4", "", "rezidenční projekty"), ("2", "", "dokončené a předané"), ("17", "", "bytů v aktuální nabídce"), ("100", "%", "projektů s vlastní zahradou nebo terasou")],
    s2="Projekty", projects_h=("Naše", "domy."),
    projects_p="Dva domy v&nbsp;Praze-Modřanech právě v&nbsp;předprodeji, horské apartmány s&nbsp;posledními třemi jednotkami a&nbsp;dokončená rezidence, která je naší vizitkou.",
    cards=[("ke-schodum/", "ke-schodum/bdks_13", "Rezidence ke Schodům", "Předprodej zahájen", True, "Rezidence", "ke&nbsp;Schodům", ["Praha-Modřany", "8 bytů · 2+kk a 3+kk", "terasy až 104 m²"], "Osm bytů s&nbsp;terasami a&nbsp;zahradami, pohledový beton a&nbsp;dům, který si vyrábí energii. Rezervace se slevou až 5&nbsp;%.", "Vybrat byt", False),
           ("do-ctvrti/", "do-ctvrti/bddc_03", "Rezidence Do Čtvrti", "Předprodej zahájen", True, "Rezidence", "Do&nbsp;Čtvrti", ["Praha-Modřany", "6 bytů · 2+kk a 3+kk", "zahrady a střešní terasy"], "Nárožní dům se zaoblenými rohy a&nbsp;perforovanou cihlou. Jen dva byty na podlaží. Rezervace se slevou až 5&nbsp;%.", "Vybrat byt", False),
           ("apartmany-vysoke/", "vysoke/e01", "Apartmány Vysoké", "Poslední 3 apartmány", False, "Apartmány", "Vysoké", ["Vysoké nad Jizerou", "A2 · B1 · B2", "dokončeno"], "Horské apartmány s&nbsp;terasami, společnou zahradou a&nbsp;jezírkem. Prodej posledních jednotek zajišťuje Svoboda &amp; Williams.", "Volné apartmány", False),
           ("rezidence-vlnita/", "vlnita/foto-02", "Rezidence Vlnitá", "Prodáno", False, "Rezidence", "Vlnitá", ["Praha", "dokončeno", "všechny byty prodány"], "Dokončený dům, který nám ukázal, že detail rozhoduje. Zůstává jako naše vizitka.", "Prohlédnout", True)],
    s3="Jak stavíme", how_h=("Jednoduše,", "poctivě, natrvalo."),
    how=[("ke-schodum/bdks_10", "Zahrada Rezidence ke Schodům", "Každý byt má kus nebe.", "Zahrada, terasa nebo balkon. Nestavíme dům, kde se venku jen parkuje. Obytné místnosti míří na jih, do zeleně, a&nbsp;venkovní prostor počítáme jako další pokoj."),
         ("do-ctvrti/bddc_int_01", "Interiér Rezidence Do Čtvrti", "Materiály, které stárnou krásně.", "Pohledový beton, dřevo, omítky v&nbsp;teplých tónech, cihla a&nbsp;sklo. Méně prvků, zato lepších. Nic, co se za pár let musí vyměnit."),
         ("ke-schodum/bdks_18", "Detail fasády Rezidence ke Schodům", "Důvěra se staví stejně jako dům.", "Srozumitelné informace, jasné termíny a&nbsp;přímý kontakt na lidi, kteří za projektem stojí. Když se něco změní, dozvíte se to od nás jako první.")],
    s4="Reference a partneři",
    ref_manifest="Dva domy jsme už <strong>dokončili a&nbsp;předali</strong>. Dva další navrhujeme s&nbsp;ateliérem <strong>JA Architekti</strong>, který má za sebou desítky realizací.",
    partner_arch="Architektura obou pražských projektů", partner_sales="Prodej Apartmánů Vysoké",
    ref_cards=[("apartmany-vysoke/", "vysoke/e03w", "Apartmány Vysoké v zimě", "Apartmány", "Vysoké", "Dokončeno. Dva horské domy, zahrada s&nbsp;jezírkem, výhled na Krkonoše.", "Prohlédnout", False),
               ("rezidence-vlnita/", "vlnita/foto-13", "Obývací pokoj Rezidence Vlnitá", "Rezidence", "Vlnitá", "Dokončeno a&nbsp;prodáno. Čisté linie, tmavé dřevo a&nbsp;světlo.", "Prohlédnout", True)],
    s5="Kontakt", form_h=("Chcete vědět", "jako první?"),
    form_lead="Zanechte nám kontakt. Ozveme se, jakmile budeme mít k&nbsp;projektům další informace, a&nbsp;rádi vás provedeme výběrem bytu.",
),
"en": dict(
    title="Nico &amp; Kai Development | Residential projects in Prague and the mountains",
    desc="Nico & Kai Development builds houses that are good to live in. Rezidence ke Schodům and Do Čtvrti in Prague-Modřany in pre-sale, Apartmány Vysoké and Rezidence Vlnitá completed.",
    org_desc="Residential development in Prague and the mountains.",
    nav=[("#projekty", "Projects"), ("#pristup", "How we build"), ("#reference", "References"), ("#kontakt", "Contact")],
    cta_header="Choose an apartment", eyebrow="Nico &amp; Kai Development",
    h1a="A home", h1b="to look forward to.",
    lead="We build houses for real life. Not square metres, but places you want to come back to. In Prague and in the mountains.",
    cta1="Our projects", cta2="Pre-sale: Ke Schodům",
    meta=[("In pre-sale", "Rezidence ke&nbsp;Schodům · Do&nbsp;Čtvrti"), ("On offer", "Apartmány Vysoké"), ("Completed", "Rezidence Vlnitá")],
    s1="Who we are", manifest="We do not sell apartments. <strong>We create places where life is good.</strong> Considered architecture, honest materials and open communication from the first meeting to the handover of keys.",
    numbers=[("4", "", "residential projects"), ("2", "", "completed and handed over"), ("17", "", "apartments currently on offer"), ("100", "%", "of projects with a private garden or terrace")],
    s2="Projects", projects_h=("Our", "houses."),
    projects_p="Two houses in Prague-Modřany now in pre-sale, mountain apartments with the last three units and a completed residence that is our calling card.",
    cards=[("ke-schodum/", "ke-schodum/bdks_13", "Rezidence ke Schodům", "Pre-sale open", True, "Rezidence", "ke&nbsp;Schodům", ["Prague-Modřany", "8 apartments · 2+kk and 3+kk", "terraces up to 104 m²"], "Eight apartments with terraces and gardens, exposed concrete and a house that makes its own energy. Reserve with a discount of up to 5&nbsp;%.", "Choose an apartment", False),
           ("do-ctvrti/", "do-ctvrti/bddc_03", "Rezidence Do Čtvrti", "Pre-sale open", True, "Rezidence", "Do&nbsp;Čtvrti", ["Prague-Modřany", "6 apartments · 2+kk and 3+kk", "gardens and roof terraces"], "A corner house with rounded corners and perforated brick. Only two apartments per floor. Reserve with a discount of up to 5&nbsp;%.", "Choose an apartment", False),
           ("apartmany-vysoke/", "vysoke/e01", "Apartmány Vysoké", "Last 3 apartments", False, "Apartmány", "Vysoké", ["Vysoké nad Jizerou", "A2 · B1 · B2", "completed"], "Mountain apartments with terraces, a shared garden and a pond. The last units are sold by Svoboda &amp; Williams.", "Available apartments", False),
           ("rezidence-vlnita/", "vlnita/foto-02", "Rezidence Vlnitá", "Sold out", False, "Rezidence", "Vlnitá", ["Prague", "completed", "all apartments sold"], "A completed house that showed us that detail decides. It remains our calling card.", "View", True)],
    s3="How we build", how_h=("Simply,", "honestly, to last."),
    how=[("ke-schodum/bdks_10", "Garden of Rezidence ke Schodům", "Every apartment gets a piece of sky.", "A garden, a terrace or a balcony. We do not build houses where the outdoors is just for parking. Living rooms face south, into the greenery, and we count the outdoor space as another room."),
         ("do-ctvrti/bddc_int_01", "Interior of Rezidence Do Čtvrti", "Materials that age beautifully.", "Exposed concrete, wood, warm-toned plasters, brick and glass. Fewer elements, but better ones. Nothing that has to be replaced in a few years."),
         ("ke-schodum/bdks_18", "Facade detail of Rezidence ke Schodům", "Trust is built like a house.", "Clear information, clear dates and direct contact with the people behind the project. If something changes, you hear it from us first.")],
    s4="References and partners",
    ref_manifest="We have already <strong>completed and handed over</strong> two houses. We are designing two more with the studio <strong>JA Architekti</strong>, which has dozens of built projects behind it.",
    partner_arch="Architecture of both Prague projects", partner_sales="Sales of Apartmány Vysoké",
    ref_cards=[("apartmany-vysoke/", "vysoke/e03w", "Apartmány Vysoké in winter", "Apartmány", "Vysoké", "Completed. Two mountain houses, a garden with a pond, views of the Giant Mountains.", "View", False),
               ("rezidence-vlnita/", "vlnita/foto-13", "Living room of Rezidence Vlnitá", "Rezidence", "Vlnitá", "Completed and sold. Clean lines, dark wood and light.", "View", True)],
    s5="Contact", form_h=("Want to be", "the first to know?"),
    form_lead="Leave us your contact details. We will get in touch as soon as we have more information about the projects and will gladly guide you through choosing an apartment.",
),
"de": dict(
    title="Nico &amp; Kai Development | Wohnprojekte in Prag und in den Bergen",
    desc="Nico & Kai Development baut Häuser, in denen man gut lebt. Rezidence ke Schodům und Do Čtvrti in Prag-Modřany im Vorverkauf, Apartmány Vysoké und Rezidence Vlnitá fertiggestellt.",
    org_desc="Wohnungsbau in Prag und in den Bergen.",
    nav=[("#projekty", "Projekte"), ("#pristup", "Wie wir bauen"), ("#reference", "Referenzen"), ("#kontakt", "Kontakt")],
    cta_header="Wohnung wählen", eyebrow="Nico &amp; Kai Development",
    h1a="Ein Zuhause,", h1b="auf das Sie sich freuen.",
    lead="Wir bauen Häuser für das echte Leben. Keine Quadratmeter, sondern Orte, an die man zurückkehren möchte. In Prag und in den Bergen.",
    cta1="Unsere Projekte", cta2="Vorverkauf: Ke Schodům",
    meta=[("Im Vorverkauf", "Rezidence ke&nbsp;Schodům · Do&nbsp;Čtvrti"), ("Im Angebot", "Apartmány Vysoké"), ("Fertiggestellt", "Rezidence Vlnitá")],
    s1="Wer wir sind", manifest="Wir verkaufen keine Wohnungen. <strong>Wir schaffen Orte, an denen man gut lebt.</strong> Durchdachte Architektur, ehrliche Materialien und offene Kommunikation vom ersten Gespräch bis zur Schlüsselübergabe.",
    numbers=[("4", "", "Wohnprojekte"), ("2", "", "fertiggestellt und übergeben"), ("17", "", "Wohnungen im aktuellen Angebot"), ("100", "%", "der Projekte mit eigenem Garten oder Terrasse")],
    s2="Projekte", projects_h=("Unsere", "Häuser."),
    projects_p="Zwei Häuser in Prag-Modřany gerade im Vorverkauf, Bergapartments mit den letzten drei Einheiten und eine fertiggestellte Residenz, die unsere Visitenkarte ist.",
    cards=[("ke-schodum/", "ke-schodum/bdks_13", "Rezidence ke Schodům", "Vorverkauf gestartet", True, "Rezidence", "ke&nbsp;Schodům", ["Prag-Modřany", "8 Wohnungen · 2+kk und 3+kk", "Terrassen bis 104 m²"], "Acht Wohnungen mit Terrassen und Gärten, Sichtbeton und ein Haus, das seine Energie selbst erzeugt. Reservierung mit bis zu 5&nbsp;% Rabatt.", "Wohnung wählen", False),
           ("do-ctvrti/", "do-ctvrti/bddc_03", "Rezidence Do Čtvrti", "Vorverkauf gestartet", True, "Rezidence", "Do&nbsp;Čtvrti", ["Prag-Modřany", "6 Wohnungen · 2+kk und 3+kk", "Gärten und Dachterrassen"], "Ein Eckhaus mit abgerundeten Ecken und perforiertem Ziegel. Nur zwei Wohnungen pro Geschoss. Reservierung mit bis zu 5&nbsp;% Rabatt.", "Wohnung wählen", False),
           ("apartmany-vysoke/", "vysoke/e01", "Apartmány Vysoké", "Letzte 3 Apartments", False, "Apartmány", "Vysoké", ["Vysoké nad Jizerou", "A2 · B1 · B2", "fertiggestellt"], "Bergapartments mit Terrassen, gemeinsamem Garten und Teich. Die letzten Einheiten verkauft Svoboda &amp; Williams.", "Freie Apartments", False),
           ("rezidence-vlnita/", "vlnita/foto-02", "Rezidence Vlnitá", "Verkauft", False, "Rezidence", "Vlnitá", ["Prag", "fertiggestellt", "alle Wohnungen verkauft"], "Ein fertiggestelltes Haus, das uns gezeigt hat, dass das Detail entscheidet. Es bleibt unsere Visitenkarte.", "Ansehen", True)],
    s3="Wie wir bauen", how_h=("Einfach,", "ehrlich, dauerhaft."),
    how=[("ke-schodum/bdks_10", "Garten der Rezidence ke Schodům", "Jede Wohnung hat ein Stück Himmel.", "Garten, Terrasse oder Balkon. Wir bauen keine Häuser, in denen draußen nur geparkt wird. Die Wohnräume sind nach Süden ins Grüne ausgerichtet, und den Außenbereich zählen wir als weiteres Zimmer."),
         ("do-ctvrti/bddc_int_01", "Interieur der Rezidence Do Čtvrti", "Materialien, die schön altern.", "Sichtbeton, Holz, Putze in warmen Tönen, Ziegel und Glas. Weniger Elemente, dafür bessere. Nichts, was man in ein paar Jahren austauschen muss."),
         ("ke-schodum/bdks_18", "Fassadendetail der Rezidence ke Schodům", "Vertrauen baut man wie ein Haus.", "Verständliche Informationen, klare Termine und direkter Kontakt zu den Menschen hinter dem Projekt. Wenn sich etwas ändert, erfahren Sie es von uns zuerst.")],
    s4="Referenzen und Partner",
    ref_manifest="Zwei Häuser haben wir bereits <strong>fertiggestellt und übergeben</strong>. Zwei weitere planen wir mit dem Büro <strong>JA Architekti</strong>, das Dutzende Realisierungen vorweisen kann.",
    partner_arch="Architektur beider Prager Projekte", partner_sales="Verkauf der Apartmány Vysoké",
    ref_cards=[("apartmany-vysoke/", "vysoke/e03w", "Apartmány Vysoké im Winter", "Apartmány", "Vysoké", "Fertiggestellt. Zwei Berghäuser, ein Garten mit Teich, Blick auf das Riesengebirge.", "Ansehen", False),
               ("rezidence-vlnita/", "vlnita/foto-13", "Wohnzimmer der Rezidence Vlnitá", "Rezidence", "Vlnitá", "Fertiggestellt und verkauft. Klare Linien, dunkles Holz und Licht.", "Ansehen", True)],
    s5="Kontakt", form_h=("Möchten Sie es", "als Erste erfahren?"),
    form_lead="Hinterlassen Sie uns Ihren Kontakt. Wir melden uns, sobald wir weitere Informationen zu den Projekten haben, und begleiten Sie gern bei der Wahl Ihrer Wohnung.",
),
}

# ======================================================================
# APARTMÁNY VYSOKÉ
# ======================================================================
VYSOKE = {
"cs": dict(
    title="Apartmány Vysoké | Nico &amp; Kai Development",
    desc="Apartmány Vysoké nad Jizerou: dokončené horské apartmány s terasami, zahradou a jezírkem. Poslední tři jednotky A2, B1 a B2 v prodeji.",
    nav=[("#pribeh", "Apartmány"), ("#jednotky", "Volné jednotky"), ("#galerie", "Galerie"), ("#lokalita", "Lokalita"), ("#kontakt", "Kontakt")],
    cta_header="Mám zájem", hero_alt="Zimní ráno s inverzí v Pasekách nad Jizerou", chip="Dokončeno · poslední 3 apartmány",
    h1a="Apartmány", h1b="Vysoké",
    lead="Dva horské domy na kraji Vysokého nad Jizerou. Vlastní terasa, společná zahrada s&nbsp;přírodním jezírkem a&nbsp;Krkonoše na dohled.",
    cta1="Volné apartmány", cta2="Galerie",
    meta=[("Lokalita", "Vysoké nad Jizerou"), ("Stav", "Zkolaudováno"), ("V nabídce", "A2 · B1 · B2"), ("Prodej", "Svoboda &amp; Williams")],
    s1="Apartmány", manifest="Místo, kam se <strong>jezdí odpočívat</strong>. Dřevo, trámy a&nbsp;střešní okna, pod nimiž se spí jinak. V&nbsp;zimě běžky od dveří, v&nbsp;létě jezírko na zahradě.",
    numbers=[("2", "", "apartmánové domy"), ("3", "", "poslední volné jednotky"), ("193", "m²", "apartmán B2, 5+kk"), ("700", "m n. m.", "Vysoké nad Jizerou")],
    s2="Volné jednotky", units_h=("Poslední", "tři apartmány."),
    units_p="Ostatní jednotky už mají své majitele. Prodej posledních tří zajišťuje realitní kancelář Svoboda &amp; Williams.",
    agent_line="Prodej apartmánů A2, B1 a&nbsp;B2.",
    s3="Galerie", gal_h=("Hory", "za oknem."), gal_p="Fotografie z&nbsp;dokončených apartmánů a&nbsp;z&nbsp;okolí Vysokého nad Jizerou.",
    gallery=[("e01", "Apartmánový dům ze zahrady v podvečer", "Dům ze zahrady", "is-big"),
             ("e03", "Apartmánový dům v zimním podvečeru", "Zimní večer", "is-tall"),
             ("k03", "Běžkař v zasněženém lese", "Běžecká stopa", "is-tall"),
             ("a01", "Obývací pokoj s krbem a kuchyní", "Obývací pokoj", "is-big"),
             ("a03", "Kuchyně s tmavou linkou", "Kuchyně", ""),
             ("a04", "Ložnice s dřevěným trámem", "Ložnice", ""),
             ("a05", "Koupelna s vanou a sprchovým koutem", "Koupelna", ""),
             ("e02", "Apartmánové domy z příjezdové cesty", "Oba domy", "is-wide"),
             ("a07", "Podkroví s trámy", "Podkroví", ""),
             ("a09", "Výhled ze střešního okna na hory", "Výhled z okna", ""),
             ("k05", "Zasněžený hřeben Krkonoš", "Hřeben Krkonoš", "is-wide"),
             ("k06", "Pastviny s kravami a výhledem na hory", "Léto", ""),
             ("k07", "Podzimní alej", "Podzim", ""),
             ("k08", "Říčka Kamenice mezi balvany", "Kamenice", ""),
             ("k02", "Sjezdovka a hřebeny v ranním oparu, Paseky nad Jizerou", "Paseky nad Jizerou", "is-wide"),
             ("k09", "Rozhledna Maják Járy Cimrmana za svítání", "Rozhledna", "")],
    gal_note="Krajinné fotografie: Jiří Smejkal. Fotografie apartmánu a domu: Svoboda &amp; Williams. Snímky exteriéru jsou retušované a ilustrační: zahrada je zobrazena po dokončení úprav, hranice pozemku nejsou vyznačeny.", pano_alt="Letní krajina v okolí Vysokého nad Jizerou",
    s4="Lokalita", lok_h=("Vysoké", "nad Jizerou."),
    lok_p="Jedno z&nbsp;nejvýše položených měst v&nbsp;Česku na pomezí Krkonoš a&nbsp;Jizerských hor. Běžecké tratě, cyklotrasy, lyžařské vleky Šachty a&nbsp;Krakonošovo divadlo. Rokytnice a&nbsp;Harrachov za pár minut autem.",
    addr=[("Adresa", "K. Havlíčka Borovského 442/443, 512 11 Vysoké nad Jizerou"), ("Nadmořská výška", "cca 700 m n. m."), ("Zima", "běžecké tratě, vleky Šachty, Rokytnice, Harrachov"), ("Léto", "cyklotrasy, turistika, jezírko na zahradě"), ("Ve městě", "škola, nemocnice, pekárna, restaurace, divadlo")],
    s5="Kontakt", form_h=("Chci vědět", "víc."), form_lead="Napište nám, kterého apartmánu se váš zájem týká. Předáme ho makléřce a&nbsp;ozveme se vám.",
),
"en": dict(
    title="Apartmány Vysoké | Nico &amp; Kai Development",
    desc="Apartmány Vysoké nad Jizerou: completed mountain apartments with terraces, a garden and a pond. The last three units A2, B1 and B2 for sale.",
    nav=[("#pribeh", "Apartments"), ("#jednotky", "Available units"), ("#galerie", "Gallery"), ("#lokalita", "Location"), ("#kontakt", "Contact")],
    cta_header="I am interested", hero_alt="Winter morning with a temperature inversion at Paseky nad Jizerou", chip="Completed · last 3 apartments",
    h1a="Apartmány", h1b="Vysoké",
    lead="Two mountain houses on the edge of Vysoké nad Jizerou. A private terrace, a shared garden with a natural pond and the Giant Mountains in view.",
    cta1="Available apartments", cta2="Gallery",
    meta=[("Location", "Vysoké nad Jizerou"), ("Status", "Final inspection passed"), ("On offer", "A2 · B1 · B2"), ("Sales", "Svoboda &amp; Williams")],
    s1="Apartments", manifest="A place people <strong>come to rest</strong>. Wood, beams and roof windows under which you sleep differently. Cross-country skiing from the door in winter, the garden pond in summer.",
    numbers=[("2", "", "apartment houses"), ("3", "", "last available units"), ("193", "m²", "apartment B2, 5+kk"), ("700", "m a.s.l.", "Vysoké nad Jizerou")],
    s2="Available units", units_h=("The last", "three apartments."),
    units_p="The other units already have their owners. The last three are sold by the estate agency Svoboda &amp; Williams.",
    agent_line="Sales of apartments A2, B1 and B2.",
    s3="Gallery", gal_h=("Mountains", "outside the window."), gal_p="Photographs of the completed apartments and the surroundings of Vysoké nad Jizerou.",
    gallery=[("e01", "The apartment house from the garden at dusk", "From the garden", "is-big"),
             ("e03", "The apartment house on a winter evening", "Winter evening", "is-tall"),
             ("k03", "Cross-country skier in a snowy forest", "Cross-country trail", "is-tall"),
             ("a01", "Living room with fireplace and kitchen", "Living room", "is-big"),
             ("a03", "Kitchen with dark cabinets", "Kitchen", ""),
             ("a04", "Bedroom with a timber beam", "Bedroom", ""),
             ("a05", "Bathroom with bath and walk-in shower", "Bathroom", ""),
             ("e02", "The apartment houses from the driveway", "Both houses", "is-wide"),
             ("a07", "Attic with timber beams", "Attic", ""),
             ("a09", "View of the mountains from the roof window", "View from the window", ""),
             ("k05", "Snow-covered ridge of the Giant Mountains", "Giant Mountains ridge", "is-wide"),
             ("k06", "Pastures with cows and mountain views", "Summer", ""),
             ("k07", "Autumn tree-lined lane", "Autumn", ""),
             ("k08", "The Kamenice stream among boulders", "Kamenice", ""),
             ("k02", "Ski slope and ridges in the morning haze, Paseky nad Jizerou", "Paseky nad Jizerou", "is-wide"),
             ("k09", "The Jára Cimrman Lighthouse lookout tower at dawn", "Lookout tower", "")],
    gal_note="Landscape photography: Jiří Smejkal. Photographs of the apartment and house: Svoboda &amp; Williams. Exterior photographs are retouched and illustrative: the garden is shown after landscaping, plot boundaries are not marked.", pano_alt="Summer landscape around Vysoké nad Jizerou",
    s4="Location", lok_h=("Vysoké", "nad Jizerou."),
    lok_p="One of the highest-lying towns in the Czech Republic, between the Giant Mountains and the Jizera Mountains. Cross-country trails, cycle routes, the Šachty ski lifts and the Krakonoš theatre. Rokytnice and Harrachov a few minutes by car.",
    addr=[("Address", "K. Havlíčka Borovského 442/443, 512 11 Vysoké nad Jizerou"), ("Altitude", "approx. 700 m a.s.l."), ("Winter", "cross-country trails, Šachty lifts, Rokytnice, Harrachov"), ("Summer", "cycle routes, hiking, the garden pond"), ("In town", "school, hospital, bakery, restaurants, theatre")],
    s5="Contact", form_h=("I want to", "know more."), form_lead="Tell us which apartment you are interested in. We will pass it on to the agent and get back to you.",
),
"de": dict(
    title="Apartmány Vysoké | Nico &amp; Kai Development",
    desc="Apartmány Vysoké nad Jizerou: fertiggestellte Bergapartments mit Terrassen, Garten und Teich. Die letzten drei Einheiten A2, B1 und B2 zum Verkauf.",
    nav=[("#pribeh", "Apartments"), ("#jednotky", "Freie Einheiten"), ("#galerie", "Galerie"), ("#lokalita", "Lage"), ("#kontakt", "Kontakt")],
    cta_header="Ich habe Interesse", hero_alt="Wintermorgen mit Inversion in Paseky nad Jizerou", chip="Fertiggestellt · letzte 3 Apartments",
    h1a="Apartmány", h1b="Vysoké",
    lead="Zwei Berghäuser am Rand von Vysoké nad Jizerou. Eigene Terrasse, gemeinsamer Garten mit Naturteich und das Riesengebirge in Sichtweite.",
    cta1="Freie Apartments", cta2="Galerie",
    meta=[("Lage", "Vysoké nad Jizerou"), ("Status", "Abgenommen"), ("Im Angebot", "A2 · B1 · B2"), ("Verkauf", "Svoboda &amp; Williams")],
    s1="Apartments", manifest="Ein Ort, an den man <strong>zum Ausruhen fährt</strong>. Holz, Balken und Dachfenster, unter denen man anders schläft. Im Winter Langlauf ab Haustür, im Sommer der Teich im Garten.",
    numbers=[("2", "", "Apartmenthäuser"), ("3", "", "letzte freie Einheiten"), ("193", "m²", "Apartment B2, 5+kk"), ("700", "m ü. M.", "Vysoké nad Jizerou")],
    s2="Freie Einheiten", units_h=("Die letzten", "drei Apartments."),
    units_p="Die übrigen Einheiten haben bereits ihre Eigentümer. Den Verkauf der letzten drei übernimmt das Maklerbüro Svoboda &amp; Williams.",
    agent_line="Verkauf der Apartments A2, B1 und B2.",
    s3="Galerie", gal_h=("Berge", "vor dem Fenster."), gal_p="Fotografien der fertiggestellten Apartments und der Umgebung von Vysoké nad Jizerou.",
    gallery=[("e01", "Das Apartmenthaus vom Garten in der Abenddämmerung", "Vom Garten", "is-big"),
             ("e03", "Das Apartmenthaus an einem Winterabend", "Winterabend", "is-tall"),
             ("k03", "Langläufer im verschneiten Wald", "Loipe", "is-tall"),
             ("a01", "Wohnzimmer mit Kamin und Küche", "Wohnzimmer", "is-big"),
             ("a03", "Küche mit dunkler Zeile", "Küche", ""),
             ("a04", "Schlafzimmer mit Holzbalken", "Schlafzimmer", ""),
             ("a05", "Bad mit Wanne und Dusche", "Bad", ""),
             ("e02", "Die Apartmenthäuser von der Zufahrt", "Beide Häuser", "is-wide"),
             ("a07", "Dachgeschoss mit Balken", "Dachgeschoss", ""),
             ("a09", "Blick aus dem Dachfenster auf die Berge", "Blick aus dem Fenster", ""),
             ("k05", "Verschneiter Kamm des Riesengebirges", "Riesengebirgskamm", "is-wide"),
             ("k06", "Weiden mit Kühen und Bergblick", "Sommer", ""),
             ("k07", "Herbstliche Allee", "Herbst", ""),
             ("k08", "Der Fluss Kamenice zwischen Felsblöcken", "Kamenice", ""),
             ("k02", "Skipiste und Bergkämme im Morgendunst, Paseky nad Jizerou", "Paseky nad Jizerou", "is-wide"),
             ("k09", "Aussichtsturm „Leuchtturm von Jára Cimrman“ in der Morgendämmerung", "Aussichtsturm", "")],
    gal_note="Landschaftsfotografie: Jiří Smejkal. Fotos des Apartments und des Hauses: Svoboda &amp; Williams. Die Außenaufnahmen sind retuschiert und illustrativ: der Garten ist nach Fertigstellung dargestellt, Grundstücksgrenzen sind nicht eingezeichnet.", pano_alt="Sommerliche Landschaft rund um Vysoké nad Jizerou",
    s4="Lage", lok_h=("Vysoké", "nad Jizerou."),
    lok_p="Eine der höchstgelegenen Städte Tschechiens an der Grenze zwischen Riesengebirge und Isergebirge. Loipen, Radwege, die Skilifte Šachty und das Krakonoš-Theater. Rokytnice und Harrachov in wenigen Autominuten.",
    addr=[("Adresse", "K. Havlíčka Borovského 442/443, 512 11 Vysoké nad Jizerou"), ("Höhe", "ca. 700 m ü. M."), ("Winter", "Loipen, Lifte Šachty, Rokytnice, Harrachov"), ("Sommer", "Radwege, Wandern, Teich im Garten"), ("In der Stadt", "Schule, Krankenhaus, Bäckerei, Restaurants, Theater")],
    s5="Kontakt", form_h=("Ich möchte", "mehr wissen."), form_lead="Schreiben Sie uns, welches Apartment Sie interessiert. Wir leiten es an die Maklerin weiter und melden uns bei Ihnen.",
),
}

# ======================================================================
# REZIDENCE VLNITÁ
# ======================================================================
VLNITA = {
"cs": dict(
    title="Rezidence Vlnitá | Nico &amp; Kai Development", desc="Rezidence Vlnitá: dokončený rezidenční projekt Nico & Kai Development v Praze. Všechny byty prodány.",
    nav=[("#pribeh", "O domě"), ("#galerie", "Galerie"), ("HOME#projekty", "Aktuální projekty")], cta_header="Aktuální projekty",
    banner="Prodáno · dokončeno", h1a="Rezidence", h1b="Vlnitá",
    lead="Dokončený dům v&nbsp;Praze. Všechny byty mají své majitele. Zůstává jako ukázka toho, jak stavíme.",
    hero_alt="Rezidence Vlnitá z ulice",
    meta=[("Lokalita", "Praha"), ("Stav", "Prodáno, dokončeno"), ("Typ", "Rezidenční dům")],
    s1="O domě", manifest="Čisté linie, <strong>tmavé dřevo a&nbsp;světlo</strong>. Dům, u&nbsp;kterého jsme si ověřili, že <strong>detail rozhoduje</strong>: od dubových dveří po kování.",
    split_alt="Obývací pokoj s krbem", split_h="Co jsme si odnesli.", split_p="Velká okna, krb a&nbsp;jeden materiál na podlaze v&nbsp;celém bytě. Méně prvků, zato lepších. Stejný přístup dnes vedeme do Rezidence ke Schodům a&nbsp;Do Čtvrti.",
    s2="Galerie", gallery=[("foto-02", "Rezidence Vlnitá z ulice při západu slunce", "Z ulice", "is-big"),
             ("foto-24", "Rezidence Vlnitá z ulice ve dne", "Dům z ulice", "is-tall"),
             ("foto-23", "Sprchový kout s velkoformátovým obkladem", "Koupelna", "is-tall"),
             ("foto-21", "Dům a zahrada z nadhledu, v pozadí Praha", "Dům a zahrada", "is-big"),
             ("foto-04", "Kuchyně s dřevěnou dýhou", "Kuchyně", "is-tall"),
             ("foto-13", "Obývací pokoj s krbem", "Obývací pokoj", "is-tall"),
             ("foto-22", "Kuchyně se světlou linkou", "Kuchyně", ""),
             ("foto-05", "Kuchyně a dubové dveře", "Detail", ""),
             ("foto-03", "Průčelí domu", "Průčelí", "is-wide"),
             ("foto-25", "Koupelna s dubovou deskou umyvadla", "Detail koupelny", "")],
    gal_note="Fotografie dokončeného domu, retušované (světlo, obloha, odstraněná zaparkovaná auta).", cta_now="Aktuálně v prodeji: Ke Schodům", cta_dc="Do Čtvrti",
),
"en": dict(
    title="Rezidence Vlnitá | Nico &amp; Kai Development", desc="Rezidence Vlnitá: a completed residential project by Nico & Kai Development in Prague. All apartments sold.",
    nav=[("#pribeh", "About the house"), ("#galerie", "Gallery"), ("HOME#projekty", "Current projects")], cta_header="Current projects",
    banner="Sold out · completed", h1a="Rezidence", h1b="Vlnitá",
    lead="A completed house in Prague. All apartments have their owners. It remains as an example of how we build.",
    hero_alt="Rezidence Vlnitá from the street",
    meta=[("Location", "Prague"), ("Status", "Sold out, completed"), ("Type", "Residential house")],
    s1="About the house", manifest="Clean lines, <strong>dark wood and light</strong>. The house where we confirmed that <strong>detail decides</strong>: from the oak doors to the fittings.",
    split_alt="Living room with fireplace", split_h="What we took with us.", split_p="Large windows, a fireplace and one floor material throughout the apartment. Fewer elements, but better ones. We bring the same approach to Rezidence ke Schodům and Do Čtvrti today.",
    s2="Gallery", gallery=[("foto-02", "Rezidence Vlnitá from the street at sunset", "From the street", "is-big"),
             ("foto-24", "Rezidence Vlnitá from the street by day", "The house from the street", "is-tall"),
             ("foto-23", "Walk-in shower with large-format tiles", "Bathroom", "is-tall"),
             ("foto-21", "The house and garden from above, Prague in the background", "House and garden", "is-big"),
             ("foto-04", "Kitchen with wood veneer", "Kitchen", "is-tall"),
             ("foto-13", "Living room with fireplace", "Living room", "is-tall"),
             ("foto-22", "Kitchen with light cabinets", "Kitchen", ""),
             ("foto-05", "Kitchen and oak doors", "Detail", ""),
             ("foto-03", "Facade of the house", "Facade", "is-wide"),
             ("foto-25", "Bathroom with an oak washbasin top", "Bathroom detail", "")],
    gal_note="Photographs of the completed house, retouched (light, sky, parked cars removed).", cta_now="Now selling: Ke Schodům", cta_dc="Do Čtvrti",
),
"de": dict(
    title="Rezidence Vlnitá | Nico &amp; Kai Development", desc="Rezidence Vlnitá: ein fertiggestelltes Wohnprojekt von Nico & Kai Development in Prag. Alle Wohnungen verkauft.",
    nav=[("#pribeh", "Über das Haus"), ("#galerie", "Galerie"), ("HOME#projekty", "Aktuelle Projekte")], cta_header="Aktuelle Projekte",
    banner="Verkauft · fertiggestellt", h1a="Rezidence", h1b="Vlnitá",
    lead="Ein fertiggestelltes Haus in Prag. Alle Wohnungen haben ihre Eigentümer. Es bleibt als Beispiel dafür, wie wir bauen.",
    hero_alt="Rezidence Vlnitá von der Straße",
    meta=[("Lage", "Prag"), ("Status", "Verkauft, fertiggestellt"), ("Typ", "Wohnhaus")],
    s1="Über das Haus", manifest="Klare Linien, <strong>dunkles Holz und Licht</strong>. Das Haus, bei dem wir bestätigt bekamen, dass <strong>das Detail entscheidet</strong>: von den Eichentüren bis zu den Beschlägen.",
    split_alt="Wohnzimmer mit Kamin", split_h="Was wir mitgenommen haben.", split_p="Große Fenster, ein Kamin und ein Bodenmaterial in der ganzen Wohnung. Weniger Elemente, dafür bessere. Denselben Ansatz bringen wir heute in die Rezidence ke Schodům und Do Čtvrti.",
    s2="Galerie", gallery=[("foto-02", "Rezidence Vlnitá von der Straße bei Sonnenuntergang", "Von der Straße", "is-big"),
             ("foto-24", "Rezidence Vlnitá von der Straße bei Tag", "Das Haus von der Straße", "is-tall"),
             ("foto-23", "Bodengleiche Dusche mit großformatigen Fliesen", "Bad", "is-tall"),
             ("foto-21", "Haus und Garten von oben, im Hintergrund Prag", "Haus und Garten", "is-big"),
             ("foto-04", "Küche mit Holzfurnier", "Küche", "is-tall"),
             ("foto-13", "Wohnzimmer mit Kamin", "Wohnzimmer", "is-tall"),
             ("foto-22", "Küche mit heller Zeile", "Küche", ""),
             ("foto-05", "Küche und Eichentüren", "Detail", ""),
             ("foto-03", "Fassade des Hauses", "Fassade", "is-wide"),
             ("foto-25", "Bad mit Eichenplatte am Waschbecken", "Bad-Detail", "")],
    gal_note="Fotografien des fertiggestellten Hauses, retuschiert (Licht, Himmel, parkende Autos entfernt).", cta_now="Aktuell im Verkauf: Ke Schodům", cta_dc="Do Čtvrti",
),
}

# ======================================================================
# OCHRANA OSOBNÍCH ÚDAJŮ
# ======================================================================
LEGAL = {
"cs": dict(
    title="Ochrana osobních údajů | Nico &amp; Kai Development", desc="Zásady zpracování osobních údajů na webu Nico & Kai Development.",
    nav=[("HOME#projekty", "Projekty"), ("HOMEke-schodum/", "Ke Schodům"), ("HOMEdo-ctvrti/", "Do Čtvrti"), ("HOME#kontakt", "Kontakt")], cta_header="Kontakt",
    eyebrow="Právní informace", h=("Ochrana", "osobních údajů."),
    lead="Vážíme si vašeho zájmu o&nbsp;naše domy a&nbsp;stejně tak vašeho soukromí. Tady najdete, jaké údaje zpracováváme, proč a&nbsp;jaká máte práva.",
    body="""
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
          <p class="legal__date">Účinnost od 21. 11. 2026.</p>""",
),
"en": dict(
    title="Privacy policy | Nico &amp; Kai Development", desc="Personal data processing policy of the Nico & Kai Development website.",
    nav=[("HOME#projekty", "Projects"), ("HOMEke-schodum/", "Ke Schodům"), ("HOMEdo-ctvrti/", "Do Čtvrti"), ("HOME#kontakt", "Contact")], cta_header="Contact",
    eyebrow="Legal information", h=("Privacy", "policy."),
    lead="We appreciate your interest in our houses and value your privacy just as much. Here you can find what data we process, why, and what your rights are.",
    body="""
          <h2>1. Who processes your data</h2>
          <p>The controller of personal data is <strong><span data-cfg="company.legalName">Nico &amp; Kai Development</span></strong><span data-cfg-wrap="company.ico">, Company ID <span data-cfg="company.ico"></span></span><span data-cfg-wrap="company.address">, registered office <span data-cfg="company.address"></span></span> (“we”). For Rezidence ke Schodům the seller is Rezidence Ke schodům s.r.o., Company ID 23662956, Ke schodům 1465/14, 143&nbsp;00 Prague 12 – Modřany, to whom we pass on your enquiry.</p>
          <p data-cfg-wrap="company.email">Contact for personal data matters: <a data-cfg="company.email" data-cfg-href="mailto:"></a>.</p>
          <h2>2. What data we process</h2>
          <ul>
            <li><strong>Form data:</strong> name and surname, e-mail, phone (if you provide it), the text of your message, the selected apartment and interest in a garage space or cellar.</li>
            <li><strong>Technical data:</strong> when the website loads, the hosting provider processes your IP address and browser details in the server logs.</li>
          </ul>
          <p>The website uses no tracking cookies or third-party analytics. Your browser only remembers for the duration of your visit that you have seen the intro animation (a technical necessity, no personal data).</p>
          <h2>3. Why we process data and on what basis</h2>
          <ul>
            <li><strong>Answering your enquiry and negotiating an apartment reservation</strong> – steps prior to entering into a contract at your request (Art. 6(1)(b) GDPR).</li>
            <li><strong>Sending information about the project</strong> you are interested in (construction news, price list, dates) – based on your consent (Art. 6(1)(a) GDPR). You may withdraw consent at any time.</li>
            <li><strong>Operation and security of the website</strong> – our legitimate interest (Art. 6(1)(f) GDPR).</li>
          </ul>
          <h2>4. How long we keep data</h2>
          <p>For the duration of negotiations about the reservation and purchase of an apartment and then for no longer than 3&nbsp;years after the last contact, or until consent is withdrawn, whichever comes first. Data that forms part of a contract is kept for the period required by law.</p>
          <h2>5. Who we share data with</h2>
          <ul>
            <li>The seller of the given project (see point 1), so that it can negotiate the reservation with you.</li>
            <li>For Apartmány Vysoké, the estate agency Svoboda &amp; Williams, which sells the last units.</li>
            <li>The website hosting provider (GitHub, Inc., USA – server logs; the transfer is covered by EU standard contractual clauses) and the e-mail service provider.</li>
          </ul>
          <p>We never sell data or pass it on for third-party marketing.</p>
          <h2>6. Your rights</h2>
          <p>You have the right to access your data, to have it rectified or erased, to restrict processing, to data portability, to object, and to withdraw consent at any time (withdrawal does not affect the lawfulness of processing before withdrawal). Just write to us. If you believe we process your data unlawfully, you may lodge a complaint with the Czech Office for Personal Data Protection, Pplk. Sochora 27, 170&nbsp;00 Prague 7, <a href="https://uoou.gov.cz" rel="noopener" target="_blank">uoou.gov.cz</a>.</p>
          <h2>7. Changes to this policy</h2>
          <p>We may update this policy, for example when hosting or tools change. The current version is always on this page.</p>
          <p class="legal__date">Effective from 21 November 2026.</p>""",
),
"de": dict(
    title="Datenschutz | Nico &amp; Kai Development", desc="Grundsätze der Verarbeitung personenbezogener Daten auf der Website von Nico & Kai Development.",
    nav=[("HOME#projekty", "Projekte"), ("HOMEke-schodum/", "Ke Schodům"), ("HOMEdo-ctvrti/", "Do Čtvrti"), ("HOME#kontakt", "Kontakt")], cta_header="Kontakt",
    eyebrow="Rechtliche Informationen", h=("Datenschutz-", "erklärung."),
    lead="Wir schätzen Ihr Interesse an unseren Häusern ebenso wie Ihre Privatsphäre. Hier erfahren Sie, welche Daten wir verarbeiten, warum und welche Rechte Sie haben.",
    body="""
          <h2>1. Wer die Daten verarbeitet</h2>
          <p>Verantwortlicher für die personenbezogenen Daten ist <strong><span data-cfg="company.legalName">Nico &amp; Kai Development</span></strong><span data-cfg-wrap="company.ico">, IČO <span data-cfg="company.ico"></span></span><span data-cfg-wrap="company.address">, mit Sitz <span data-cfg="company.address"></span></span> („wir“). Bei der Rezidence ke Schodům ist die Verkäuferin die Gesellschaft Rezidence Ke schodům s.r.o., IČO 23662956, Ke schodům 1465/14, 143&nbsp;00 Prag 12 – Modřany, an die wir Ihre Anfrage weiterleiten.</p>
          <p data-cfg-wrap="company.email">Kontakt in Datenschutzfragen: <a data-cfg="company.email" data-cfg-href="mailto:"></a>.</p>
          <h2>2. Welche Daten wir verarbeiten</h2>
          <ul>
            <li><strong>Formulardaten:</strong> Vor- und Nachname, E-Mail, Telefon (falls angegeben), Nachrichtentext, gewählte Wohnung und Interesse an Garagenstellplatz oder Keller.</li>
            <li><strong>Technische Daten:</strong> beim Laden der Website verarbeitet der Hosting-Anbieter Ihre IP-Adresse und Browserdaten in den Server-Logs.</li>
          </ul>
          <p>Die Website verwendet keine Tracking-Cookies und keine Analysetools Dritter. Ihr Browser merkt sich nur für die Dauer des Besuchs, dass Sie die Startanimation bereits gesehen haben (technisch notwendig, keine personenbezogenen Daten).</p>
          <h2>3. Warum wir Daten verarbeiten und auf welcher Grundlage</h2>
          <ul>
            <li><strong>Beantwortung Ihrer Anfrage und Verhandlung über die Reservierung einer Wohnung</strong> – vorvertragliche Maßnahmen auf Ihre Anfrage (Art. 6 Abs. 1 lit. b DSGVO).</li>
            <li><strong>Versand von Informationen über das Projekt</strong>, für das Sie sich interessieren (Bauneuigkeiten, Preisliste, Termine) – auf Grundlage Ihrer Einwilligung (Art. 6 Abs. 1 lit. a DSGVO). Die Einwilligung können Sie jederzeit widerrufen.</li>
            <li><strong>Betrieb und Sicherheit der Website</strong> – unser berechtigtes Interesse (Art. 6 Abs. 1 lit. f DSGVO).</li>
          </ul>
          <h2>4. Wie lange wir Daten aufbewahren</h2>
          <p>Für die Dauer der Verhandlungen über Reservierung und Kauf einer Wohnung und danach höchstens 3&nbsp;Jahre ab dem letzten Kontakt bzw. bis zum Widerruf der Einwilligung, je nachdem, was früher eintritt. Daten, die Bestandteil eines Vertrags sind, bewahren wir für die gesetzlich vorgeschriebene Dauer auf.</p>
          <h2>5. An wen wir Daten weitergeben</h2>
          <ul>
            <li>An den Verkäufer des jeweiligen Projekts (siehe Punkt 1), damit er mit Ihnen über die Reservierung verhandeln kann.</li>
            <li>Bei den Apartmány Vysoké an das Maklerbüro Svoboda &amp; Williams, das die letzten Einheiten verkauft.</li>
            <li>An den Hosting-Anbieter der Website (GitHub, Inc., USA – Server-Logs; die Übermittlung ist durch EU-Standardvertragsklauseln abgesichert) und an den E-Mail-Dienstleister.</li>
          </ul>
          <p>Wir verkaufen keine Daten und geben sie nicht für Marketing Dritter weiter.</p>
          <h2>6. Ihre Rechte</h2>
          <p>Sie haben das Recht auf Auskunft, Berichtigung oder Löschung Ihrer Daten, auf Einschränkung der Verarbeitung, auf Datenübertragbarkeit, auf Widerspruch sowie das Recht, die Einwilligung jederzeit zu widerrufen (der Widerruf berührt nicht die Rechtmäßigkeit der bis dahin erfolgten Verarbeitung). Schreiben Sie uns einfach. Wenn Sie der Ansicht sind, dass wir Ihre Daten rechtswidrig verarbeiten, können Sie sich bei der tschechischen Datenschutzbehörde beschweren: Úřad pro ochranu osobních údajů, Pplk. Sochora 27, 170&nbsp;00 Prag 7, <a href="https://uoou.gov.cz" rel="noopener" target="_blank">uoou.gov.cz</a>.</p>
          <h2>7. Änderungen dieser Erklärung</h2>
          <p>Wir können diese Erklärung anpassen, etwa bei einem Wechsel des Hostings oder der Tools. Die aktuelle Fassung finden Sie stets auf dieser Seite.</p>
          <p class="legal__date">Gültig ab 21. 11. 2026.</p>""",
),
}

NOTFOUND = {
    "cs": dict(title="Stránka nenalezena | Nico &amp; Kai Development", h1="Tady nic nestojí.", h2="Zatím.", p="Stránka, kterou hledáte, neexistuje nebo se přestěhovala.", home="Úvodní stránka", ks="Rezidence ke Schodům"),
    "en": dict(title="Page not found | Nico &amp; Kai Development", h1="Nothing built here.", h2="Yet.", p="The page you are looking for does not exist or has moved.", home="Home page", ks="Rezidence ke Schodům"),
    "de": dict(title="Seite nicht gefunden | Nico &amp; Kai Development", h1="Hier steht nichts.", h2="Noch nicht.", p="Die gesuchte Seite existiert nicht oder ist umgezogen.", home="Startseite", ks="Rezidence ke Schodům"),
}
