"""
Generates the full German /de/ version of the SunWave Switzerland website.
- Creates website/de/ with German translations of all pages
- Adjusts all asset paths for the de/ subfolder
- Adds EN|DE language switcher to all pages (English + German)
- Adds hreflang tags to all pages
"""

import os, re, glob, shutil

BASE_EN = 'https://sunwaveswitzerland.com'
BASE_DE = 'https://sunwaveswitzerland.com/de'

os.makedirs('de', exist_ok=True)
os.makedirs('de/blog', exist_ok=True)

# ── Language switcher HTML ────────────────────────────────────────────────────
SWITCHER_CSS = """
  <style>
    .nav__lang{display:flex;align-items:center;gap:2px;margin-left:10px}
    .nav__lang-btn{font-size:.68rem;font-weight:700;letter-spacing:.06em;color:rgba(255,255,255,.45);text-decoration:none;padding:3px 7px;border-radius:3px;border:1px solid rgba(255,255,255,.18);transition:all .2s}
    .nav__lang-btn:hover,.nav__lang-btn.lang-active{color:var(--gold);border-color:var(--gold);background:rgba(245,197,24,.08)}
    .nav__lang-sep{color:rgba(255,255,255,.2);font-size:.7rem}
  </style>"""

def lang_switcher_en(slug):
    """Language switcher for English pages — EN active, DE links to /de/"""
    de_link = f'de/{slug}'
    return f"""<div class="nav__lang">
      <span class="nav__lang-btn lang-active">EN</span>
      <span class="nav__lang-sep">|</span>
      <a href="{de_link}" class="nav__lang-btn">DE</a>
    </div>"""

def lang_switcher_de(slug):
    """Language switcher for German pages — DE active, EN links back to root"""
    en_link = f'../{slug}'
    return f"""<div class="nav__lang">
      <a href="{en_link}" class="nav__lang-btn">EN</a>
      <span class="nav__lang-sep">|</span>
      <span class="nav__lang-btn lang-active">DE</span>
    </div>"""

# ── Translation dictionary ────────────────────────────────────────────────────
# Order matters — longer strings first to avoid partial matches
TRANSLATIONS = [
    # Meta / titles handled separately per page

    # Navigation
    ('Hotels &amp; Hospitality', 'Hotels &amp; Gastronomie'),
    ('Offices &amp; Commercial', 'Büro &amp; Gewerbe'),
    ('Swiss Homes', 'Schweizer Haushalte'),
    ('Solar Installers', 'Solar-Installateure'),
    ('>The Panel<', '>Das Paneel<'),
    ('>Research<', '>Forschung<'),
    ('>Calculator<', '>Rechner<'),
    ('>Contact<', '>Kontakt<'),
    ('>Order Now<', '>Jetzt bestellen<'),
    ('class="nav__mobile-order">Order Now<', 'class="nav__mobile-order">Jetzt bestellen<'),
    ('class="nav__order-btn">Order Now<', 'class="nav__order-btn">Jetzt bestellen<'),

    # Hero — homepage
    ('Ceramic Infrared Heating — Switzerland', 'Keramik-Infrarotheizung — Schweiz'),
    ("Among Switzerland's most\n        independently tested\n      \n      infrared heating panels.", 'Eines der meistgeprüften\n        Infrarotheizpaneele\n      \n      der Schweiz.'),
    ('Ceramic infrared heating. Silent. Zero emissions. Up to 80% less energy than A+++ convectors. BSRIA tested. MuKEn compliant.', 'Keramik-Infrarotheizung. Geräuschlos. Null Emissionen. Bis zu 80% weniger Energie als A+++ Konvektoren. BSRIA-getestet. MuKEn-konform.'),
    ('View the Panel', 'Das Paneel ansehen'),
    ('Calculate Savings', 'Einsparungen berechnen'),

    # Stats strip
    ('less consumption vs A+++', 'weniger Verbrauch vs. A+++'),
    ('confirmed by BSRIA', 'bestätigt von BSRIA'),
    ('independent\nproduct lab tests', 'unabhängige\nLaborprüfungen'),
    ('manufacturer\nwarranty', 'Herstellergarantie'),
    ('per panel incl. thermostat,', 'pro Paneel inkl. Thermostat,'),
    ('per panel incl. thermostat', 'pro Paneel inkl. Thermostat'),
    ('12–15 m² per panel', '12–15 m² pro Paneel'),

    # Evidence strip
    ('Independently tested by', 'Unabhängig getestet von'),

    # Product showcase
    ('A panel that heats\nyour home — not the air.', 'Ein Paneel, das Ihr Zuhause wärmt\n— nicht die Luft.'),
    ('SunWave Ceramica. 60 × 120 cm. 650 W. Nine surface finishes in 6 mm fine porcelain stoneware. The same technology across every finish — change the look, not the performance.', 'SunWave Ceramica. 60 × 120 cm. 650 W. Neun Oberflächendesigns in 6 mm feinem Feinsteinzeug. Dieselbe Technologie in jeder Ausführung — ändern Sie das Design, nicht die Leistung.'),
    ('per panel · incl. VAT · WiFi thermostat required &amp; included · CHF 35 delivery', 'pro Paneel · inkl. MwSt. · WLAN-Thermostat erforderlich &amp; enthalten · CHF 35 Lieferung'),
    ('>Order Now<', '>Jetzt bestellen<'),
    ('Full Specifications', 'Vollständige Spezifikationen'),
    ('5-year warranty', '5 Jahre Garantie'),
    ('Ships in 3–5 days', 'Lieferung in 3–5 Tagen'),
    ('30-day returns', '30 Tage Rückgabe'),
    ('Class II certified', 'Klasse II zertifiziert'),

    # Segment cards
    ('Who it\'s for', 'Für wen'),
    ('Built for Swiss professionals\nand homeowners', 'Für Schweizer Fachleute\nund Hausbesitzer'),
    ('Pair infrared heating with your solar PV installations. Clients charge panels by day, heat rooms in thermal mass — perfect MuKEn-compliant package.', 'Kombinieren Sie Infrarotheizung mit Ihrer Solar-PV-Anlage. Kunden laden Paneele tagsüber, heizen Räume thermisch — das perfekte MuKEn-konforme Paket.'),
    ('Silent operation. No dust. No maintenance. Individual room control. Premium tile aesthetic. Perfect for 4- and 5-star properties across Switzerland.', 'Geräuschloser Betrieb. Kein Staub. Keine Wartung. Individuelle Raumsteuerung. Premium-Kachel-Ästhetik. Perfekt für 4- und 5-Sterne-Häuser in der Schweiz.'),
    ('MuKEn-compliant boiler replacement from CHF 490. No plumber. No planning permission. CHF 35 delivery, 3–5 days. Works in apartments and owned properties.', 'MuKEn-konformer Heizungsersatz ab CHF 490. Kein Klempner. Keine Baugenehmigung. CHF 35 Lieferung, 3–5 Tage. Für Miet- und Eigentumswohnungen.'),
    ('Zone heating — heat only occupied areas. Silent (no fan). Lower CO₂ reporting. Payback in under 3 years against gas. Minimal installation disruption.', 'Zonenheizung — nur bewohnte Bereiche beheizen. Geräuschlos (kein Ventilator). Niedrigere CO₂-Bilanz. Amortisation in unter 3 Jahren vs. Gas. Minimale Installationsunterbrechung.'),
    ('>Learn more →<', '>Mehr erfahren →<'),

    # Science section
    ('The science', 'Die Wissenschaft'),
    ('Why radiant heat\noutperforms convection', 'Warum Strahlungswärme\nKonvektion übertrifft'),
    ('Conventional electric heaters warm the air. Warm air rises. Your feet stay cold while the thermostat is satisfied. Every time a window opens or a door closes, the heated air escapes and must be replaced.', 'Herkömmliche Elektroheizungen erwärmen die Luft. Warme Luft steigt auf. Ihre Füße bleiben kalt, während der Thermostat zufrieden ist. Jedes Mal, wenn ein Fenster oder eine Tür geöffnet wird, entweicht die erwärmte Luft.'),
    ('SunWave Ceramica panels emit long-wave infrared (8–14 µm) — the same wavelength that building materials, floors, walls, and people absorb most efficiently. Surfaces warm up. Walls store heat and release it slowly. The room is comfortable at 1–2°C lower thermostat setting.', 'SunWave Ceramica Paneele emittieren langwelliges Infrarot (8–14 µm) — dieselbe Wellenlänge, die Baumaterialien, Böden, Wände und Menschen am effizientesten absorbieren. Oberflächen erwärmen sich. Wände speichern Wärme und geben sie langsam ab. Der Raum ist bei 1–2°C niedrigerer Thermostateinstellung komfortabel.'),
    ('No stratification', 'Keine Luftschichtung'),
    ('Uniform floor-to-ceiling temperature. No warm-ceiling, cold-floor effect.', 'Gleichmäßige Temperatur vom Boden bis zur Decke. Kein Warm-Decke-Kalt-Boden-Effekt.'),
    ('Charges thermal mass', 'Thermische Masse aufgeladen'),
    ('Walls and floors absorb and slowly re-radiate heat. Room stays warm after panel switches off.', 'Wände und Böden absorbieren und geben Wärme langsam wieder ab. Der Raum bleibt warm, nachdem das Paneel abschaltet.'),
    ('No dust circulation', 'Keine Staubzirkulation'),
    ('No convective air currents means settled allergens stay settled. No recirculation.', 'Keine Konvektionsluftströme bedeutet: abgesetzte Allergene bleiben abgesetzt. Keine Rezirkulation.'),
    ('Completely silent', 'Vollständig geräuschlos'),
    ('No fan. No pump. No combustion. No moving parts. Absolute silence in operation.', 'Kein Ventilator. Keine Pumpe. Keine Verbrennung. Keine beweglichen Teile. Absolute Stille im Betrieb.'),
    ('The physics in depth →', 'Die Physik im Detail →'),
    ('Energy use per m²/year', 'Energieverbrauch pro m²/Jahr'),
    ('Gas condensing boiler', 'Gas-Brennwertkessel'),
    ('Gas central heating', 'Gas-Zentralheizung'),
    ('SunWave Ceramica (infrared)', 'SunWave Ceramica (Infrarot)'),
    ('Source: Independent academic research on ceramic infrared heating technology (Dr.-Ing. Peter Kosack, 2008–2009). Figures apply to infrared heating as a technology category.', 'Quelle: Unabhängige akademische Forschung zur keramischen Infrarotheizungstechnologie (Dr.-Ing. Peter Kosack, 2008–2009).'),

    # Evidence section
    ('Independent evidence', 'Unabhängige Belege'),
    ('4 laboratories.\n4 independent tests.', '4 Laboratorien.\n4 unabhängige Tests.'),
    ('Every claim on this website is grounded in a named study with a report number. Not marketing. Not manufacturer data. Independent labs.', 'Jede Aussage auf dieser Website basiert auf einer namentlich genannten Studie mit Berichtsnummer. Kein Marketing. Keine Herstellerdaten. Unabhängige Laboratorien.'),
    ('98-Day Continuous Performance Test', '98-tägiger Dauerleistungstest'),
    ('Approved by Mark Roper, Head of Laboratory &amp; Test, BSRIA', 'Genehmigt von Mark Roper, Leiter Labor &amp; Test, BSRIA'),
    ('Indoor Air Quality — AgBB Assessment', 'Innenraumluftqualität — AgBB-Bewertung'),
    ('Radiation Efficiency Measurement', 'Messung des Strahlungswirkungsgrads'),
    ('Full Electrical Safety Test', 'Vollständige Elektrosicherheitsprüfung'),
    ('Most recent test', 'Neuester Test'),
    ('All applicable clauses', 'Alle anwendbaren Klauseln'),
    ('Full test data available', 'Alle Testdaten verfügbar'),
    ('All four reports documented with methodology, raw data, and conclusions.', 'Alle vier Berichte mit Methodik, Rohdaten und Schlussfolgerungen dokumentiert.'),
    ('Read all research →', 'Alle Forschungsdaten lesen →'),

    # MuKEn section
    ('Swiss market', 'Schweizer Markt'),
    ("MuKEn is phasing out\nyour boiler. We're ready.", 'MuKEn verdrängt\nIhre Heizung. Wir sind bereit.'),
    ('SunWave Ceramica panels are fully electric with zero on-site emissions. They qualify as a compliant replacement in all cantons that have adopted the fossil fuel phase-out provision — without planning permission, without a plumber, and deliverable within 3–5 days.', 'SunWave Ceramica Paneele sind vollständig elektrisch mit null Emissionen vor Ort. Sie qualifizieren sich als konformer Ersatz in allen Kantonen, die die Fossile-Brennstoffe-Ausstiegsregelung übernommen haben — ohne Baugenehmigung, ohne Klempner, lieferbar innerhalb von 3–5 Tagen.'),
    ('No fossil fuel combustion — zero on-site CO₂', 'Keine Verbrennung fossiler Brennstoffe — null CO₂ vor Ort'),
    ("Compatible with Switzerland's ~90% low-carbon grid", 'Kompatibel mit dem ~90% kohlenstoffarmen Schweizer Stromnetz'),
    ('No building permit required in most cantons', 'In den meisten Kantonen keine Baugenehmigung erforderlich'),
    ('Can be installed within days of boiler failure', 'Kann innerhalb von Tagen nach Heizungsausfall installiert werden'),
    ('MuKEn Compliance Guide →', 'MuKEn-Konformitätsleitfaden →'),
    ('Annual cost — 80m² apartment, Zurich', 'Jährliche Kosten — 80m² Wohnung, Zürich'),
    ('+CHF 400 annual service', '+CHF 400 jährlicher Service'),
    ('No service required', 'Kein Service erforderlich'),
    ('Annual saving', 'Jährliche Ersparnis'),
    ('Panel payback: 2–3 years', 'Paneel-Amortisation: 2–3 Jahre'),
    ('Based on academic research on ceramic infrared heating technology, CHF 0.29/kWh electricity (Swiss 2026 avg), CHF 0.13/kWh gas. Individual results vary.', 'Basierend auf akademischer Forschung, CHF 0,29/kWh Strom (Schweizer Durchschnitt 2026), CHF 0,13/kWh Gas. Individuelle Ergebnisse variieren.'),

    # Calculator
    ('Savings calculator', 'Sparrechner'),
    ('Calculate your switch', 'Berechnen Sie Ihren Wechsel'),
    ('Floor area to heat (m²)', 'Zu beheizende Fläche (m²)'),
    ('Current heating system', 'Aktuelles Heizsystem'),
    ('Electricity price (CHF/kWh)', 'Strompreis (CHF/kWh)'),
    ('Gas price (CHF/kWh)', 'Gaspreis (CHF/kWh)'),
    ('Building insulation', 'Gebäudedämmung'),
    ('Results update automatically as you adjust the inputs above. Based on Swiss 2026 average energy prices.', 'Ergebnisse werden automatisch aktualisiert. Basierend auf Schweizer Durchschnitts-Energiepreisen 2026.'),
    ('Annual saving (CHF)', 'Jährliche Ersparnis (CHF)'),
    ('Panel payback period', 'Amortisierungsdauer'),
    ('CO₂ saved per year', 'Jährlich eingesparte CO₂'),
    ('Gas central heating', 'Gas-Zentralheizung'),
    ('Oil boiler', 'Ölheizung'),
    ('Electric heating (storage or panel)', 'Elektrische Heizung (Speicher oder Paneel)'),
    ('Heat pump', 'Wärmepumpe'),
    ('District heating', 'Fernwärme'),
    ('No heating (new build)', 'Keine Heizung (Neubau)'),
    ('Poor (before 1960)', 'Schlecht (vor 1960)'),
    ('Average (1960–1980)', 'Durchschnittlich (1960–1980)'),
    ('Good (1980–2000)', 'Gut (1980–2000)'),
    ('Excellent (after 2000)', 'Ausgezeichnet (nach 2000)'),
    ('Energy data: Independent academic research', 'Energiedaten: Unabhängige akademische Forschung'),

    # FAQ
    ('>FAQ<', '>FAQ<'),
    ('Common questions', 'Häufig gestellte Fragen'),
    ('Is infrared heating MuKEn-compliant in Switzerland?', 'Ist eine Infrarotheizung MuKEn-konform in der Schweiz?'),
    ('How quickly can my boiler be replaced with infrared panels?', 'Wie schnell kann meine Heizung durch Infrarotpaneele ersetzt werden?'),
    ('What is the warranty?', 'Wie lange ist die Garantie?'),
    ('Can I use infrared panels in a rented apartment?', 'Kann ich Infrarotpaneele in einer Mietwohnung nutzen?'),
    ('Are the panels safe for children and allergy sufferers?', 'Sind die Paneele sicher für Kinder und Allergiker?'),

    # CTA section
    ('Ready to switch to clean,\nsilent infrared heat?', 'Bereit für saubere,\ngeräuschlose Infrarotwärme?'),
    ('CHF 490 per panel. A thermostat is required — included with every order. CHF 35 delivery across Switzerland. 5-year warranty. 3–5 day delivery.', 'CHF 490 pro Paneel. Ein Thermostat ist erforderlich — bei jeder Bestellung enthalten. CHF 35 Lieferung in die ganze Schweiz. 5 Jahre Garantie. 3–5 Tage Lieferzeit.'),
    ('Order the Panel →', 'Das Paneel bestellen →'),
    ('Ask a Question', 'Frage stellen'),

    # Footer
    ('Swiss distributor of SunWave Ceramica ceramic infrared heating panels. MuKEn-compliant. BSRIA-tested. Fraunhofer-certified.<br>Delivering to all Swiss cantons.', 'Schweizer Distributor von SunWave Ceramica Keramik-Infrarotheizpaneelen. MuKEn-konform. BSRIA-getestet. Fraunhofer-zertifiziert.<br>Lieferung in alle Schweizer Kantone.'),
    ('<h4>Product</h4>', '<h4>Produkt</h4>'),
    ('<h4>Learn</h4>', '<h4>Wissen</h4>'),
    ('<h4>For</h4>', '<h4>Für</h4>'),
    ('<h4>Legal</h4>', '<h4>Rechtliches</h4>'),
    ('>Design Variants<', '>Design-Varianten<'),
    ('>Full Specifications<', '>Vollständige Spezifikationen<'),
    ('>Research &amp; Evidence<', '>Forschung &amp; Belege<'),
    ('>MuKEn Guide<', '>MuKEn-Leitfaden<'),
    ('>How Infrared Works<', '>Wie Infrarot funktioniert<'),
    ('>Savings Calculator<', '>Sparrechner<'),
    ('>Swiss Homes<', '>Schweizer Haushalte<'),
    ('>Offices<', '>Büro<'),
    ('>Blog<', '>Blog<'),
    ('>Legal Notice<', '>Impressum<'),
    ('>Terms &amp; Conditions<', '>AGB<'),
    ('>Returns Policy<', '>Rückgabebedingungen<'),
    ('>Shipping<', '>Lieferung<'),
    ('>Privacy Policy<', '>Datenschutz<'),

    # Product page specific
    ('A panel that heats\nyour home — not the air.', 'Ein Paneel, das Ihr Zuhause wärmt\n— nicht die Luft.'),
    ('Technical Specifications', 'Technische Spezifikationen'),
    ('Performance Data', 'Leistungsdaten'),
    ('4 Independent Laboratory Tests', '4 Unabhängige Laborprüfungen'),
    ('Configure Your Order', 'Bestellung konfigurieren'),
    ('Product Questions', 'Produktfragen'),
    ('Electrical', 'Elektrisch'),
    ('Physical', 'Physisch'),
    ('Thermal Performance', 'Thermische Leistung'),
    ('Installation', 'Installation'),
    ("What's in the box", 'Lieferumfang'),
    ('Delivery &amp; shipping', 'Lieferung &amp; Versand'),
    ('Guarantee &amp; returns', 'Garantie &amp; Rückgabe'),
    ('Need more than 5 panels?', 'Mehr als 5 Paneele benötigt?'),
    ('Choose your finish', 'Wählen Sie Ihr Design'),
    ('Select canton...', 'Kanton auswählen...'),
    ('Homeowner / apartment tenant', 'Hausbesitzer / Mieter'),
    ('Solar / PV installer', 'Solar- / PV-Installateur'),
    ('Hotel or hospitality operator', 'Hotel- oder Gastronomiebetreiber'),
    ('Office / commercial property manager', 'Büro- / Gewerbeobjektverwalter'),
    ('Architect or interior designer', 'Architekt oder Innenarchitekt'),
    ('Electrician / installer', 'Elektriker / Installateur'),

    # Research page
    ('4 Laboratory Tests. Every Claim Verified.', '4 Laborprüfungen. Jede Aussage verifiziert.'),
    ('Independent Test Reports', 'Unabhängige Prüfberichte'),
    ('Certifications &amp; Standards', 'Zertifizierungen &amp; Normen'),
    ('The Physics Behind the Performance', 'Die Physik hinter der Leistung'),

    # Segment pages H1s
    ('Infrared Heating for Swiss Homes', 'Infrarotheizung für Schweizer Haushalte'),
    ('Infrared Heating for Swiss Hotels', 'Infrarotheizung für Schweizer Hotels'),
    ('Infrared Heating for Swiss Offices', 'Infrarotheizung für Schweizer Büros'),
    ('Infrared Heating for Solar Installers', 'Infrarotheizung für Solar-Installateure'),

    # Contact page
    ('Get a Free Quote', 'Kostenloses Angebot erhalten'),
    ('Request a Quote', 'Angebot anfragen'),
    ('We reply within 24 hours, typically much sooner.', 'Wir antworten innerhalb von 24 Stunden, meist deutlich früher.'),
    ('Your name', 'Ihr Name'),
    ('Name', 'Name'),
    ('Email', 'E-Mail'),
    ('Phone', 'Telefon'),
    ('Canton', 'Kanton'),
    ('Floor area (m²)', 'Wohnfläche (m²)'),
    ('Message / questions', 'Nachricht / Fragen'),
    ('Send Quote Request', 'Angebotsanfrage senden'),
    ('No spam. We use this information only to prepare your personalised quote.', 'Kein Spam. Wir verwenden diese Informationen nur zur Erstellung Ihres persönlichen Angebots.'),
    ('Quote request sent!', 'Angebotsanfrage gesendet!'),
    ('In the meantime, you can', 'In der Zwischenzeit können Sie'),
    ('use our savings calculator', 'unseren Sparrechner nutzen'),
    ('read the independent test reports', 'die unabhängigen Prüfberichte lesen'),
    ('Tell us about your space and we\'ll send back a personalised panel count, capital cost, annual saving estimate, and payback period within 24 hours.', 'Beschreiben Sie Ihren Raum und wir senden Ihnen innerhalb von 24 Stunden eine personalisierte Paneel-Anzahl, Kapitalkosten, Jahresersparnisschätzung und Amortisierungsdauer.'),

    # For-homes page
    ("Stop Paying for Gas You Don't Need", 'Schluss mit unnötigen Gaskosten'),
    ('Why Swiss Homeowners Are Switching', 'Warum Schweizer Hausbesitzer wechseln'),
    ('From Decision to Warm Rooms in a Day', 'Von der Entscheidung bis zum warmen Zimmer in einem Tag'),
    ('Find out exactly how much you\'ll save', 'Erfahren Sie genau, wie viel Sie sparen'),
    ('MuKEn-compliant boiler replacement', 'MuKEn-konformer Heizungsersatz'),
    ('Get a Quote', 'Angebot anfordern'),
    ('Calculate My Savings', 'Meine Einsparungen berechnen'),
    ('See the Panel', 'Das Paneel ansehen'),
    ('The MuKEn 2014 deadline', 'Die MuKEn 2014 Frist'),
    ('The energy case for infrared', 'Die Energieargumente für Infrarot'),
    ('Health advantages in Swiss homes', 'Gesundheitsvorteile in Schweizer Haushalten'),
    ('80m² Apartment — Energy Comparison', '80m² Wohnung — Energievergleich'),
    ('Calculate your panel count', 'Ihre Paneel-Anzahl berechnen'),

    # For-hotels page
    ('Heating That Matches Your Guest Experience', 'Heizung, die zu Ihrem Gästeerlebnis passt'),
    ('Why Hotels Are Switching to Infrared', 'Warum Hotels auf Infrarot umsteigen'),

    # For-offices page
    ('Heating Only the Zones People Actually Use', 'Nur die genutzten Zonen beheizen'),
    ('Why Offices Choose Infrared', 'Warum Büros Infrarot wählen'),

    # For-solar page
    ('The Perfect Load for Your Solar Customers', 'Die perfekte Last für Ihre Solar-Kunden'),
    ('Why Solar Installers Add Infrared', 'Warum Solar-Installateure Infrarot ergänzen'),
    ('Pair infrared heating with your solar PV', 'Kombinieren Sie Infrarotheizung mit Ihrer Solar-PV'),

    # Blog
    ('Infrared Heating Insights', 'Infrarotheizung — Wissen'),
    ('SunWave Knowledge Base', 'SunWave Wissensbasis'),
    ('Swiss Regulation', 'Schweizer Vorschriften'),
    ('Energy Savings', 'Energieeinsparung'),
    ('Product Science', 'Produktwissenschaft'),
    ('Cost Analysis', 'Kostenanalyse'),
    ('Read article →', 'Artikel lesen →'),
    ('min read', 'Min. Lesezeit'),

    # Legal pages
    ('Legal Notice', 'Impressum'),
    ('Terms &amp; Conditions', 'AGB'),
    ('Returns &amp; Cancellations', 'Rückgabe &amp; Stornierung'),
    ('Shipping &amp; Delivery', 'Versand &amp; Lieferung'),
    ('Privacy Policy', 'Datenschutzerklärung'),
    ('Impressum — Company information as required by Swiss law', 'Impressum — Pflichtangaben gemäß Schweizer Recht'),
    ('Last updated: June 2026', 'Zuletzt aktualisiert: Juni 2026'),
    ('General Terms and Conditions of Sale', 'Allgemeine Verkaufsbedingungen'),
    ('30-day returns — no questions asked on undamaged, uninstalled panels', '30 Tage Rückgabe — kein Kommentar nötig bei unbeschädigten, nicht installierten Paneelen'),
    ('CHF 35 flat rate — all Swiss cantons — 3 to 5 working days', 'CHF 35 Pauschale — alle Schweizer Kantone — 3 bis 5 Werktage'),
    ('How we collect, use, and protect your personal data — in accordance with Swiss nDSG', 'Wie wir Ihre personenbezogenen Daten erheben, nutzen und schützen — gemäß Schweizer nDSG'),
]

# ── Meta tags per page (German) ───────────────────────────────────────────────
PAGE_META = {
    'index.html': {
        'title': 'SunWave Switzerland — Keramik-Infrarotheizung für die Schweiz',
        'desc':  'Eines der meistgeprüften Keramik-Infrarotheizpaneele der Schweiz. BSRIA, Fraunhofer WKI, TU Dresden und Labor S.A. zertifiziert. MuKEn-konform. CHF 35 Lieferung.',
        'url':   BASE_DE + '/',
        'og_image': BASE_EN + '/images/hero-banner-1.webp',
    },
    'product.html': {
        'title': 'SunWave Ceramica Infrarotheizpaneel | SunWave Switzerland',
        'desc':  'SunWave Ceramica: 650W Keramik-Infrarotheizpaneel. BSRIA, TU Dresden, Fraunhofer WKI und Labor S.A. geprüft. Neun Schweizer Design-Varianten. CHF 490 inkl. Thermostat. Lieferung in 3–5 Tagen.',
        'url':   BASE_DE + '/product.html',
        'og_image': BASE_EN + '/images/panel-imperial-marble.webp',
    },
    'research.html': {
        'title': 'Unabhängige Prüfberichte | SunWave Ceramica',
        'desc':  '4 unabhängige Laborprüfungen: BSRIA Report 105350/1, TU Dresden DIN EN IEC 60675-3, Fraunhofer WKI MAIC-2022-2428 und Labor S.A. EN 60335-2-30. Jede Aussage unabhängig verifiziert.',
        'url':   BASE_DE + '/research.html',
        'og_image': BASE_EN + '/images/logo-bsria.webp',
    },
    'contact.html': {
        'title': 'Kontakt SunWave Switzerland — Kostenloses Angebot',
        'desc':  'Fordern Sie ein persönliches Infrarotheizungs-Angebot für Ihr Schweizer Zuhause, Hotel oder Büro an. Paneel-Anzahl, Jahresersparnis und Amortisierungsdauer — innerhalb von 24 Stunden.',
        'url':   BASE_DE + '/contact.html',
        'og_image': BASE_EN + '/images/hero-banner-1.webp',
    },
    'for-homes.html': {
        'title': 'Infrarotheizung für Schweizer Haushalte | SunWave Switzerland',
        'desc':  'Ersetzen Sie Ihre Gasheizung durch SunWave Ceramica Infrarotpaneele. MuKEn 2014-konform, 66% weniger Energie als Gas, null Wartung, 30 Jahre Lebensdauer. Kostenloses Angebot.',
        'url':   BASE_DE + '/for-homes.html',
        'og_image': BASE_EN + '/images/homes-family-comfort.webp',
    },
    'for-hotels.html': {
        'title': 'Infrarotheizung für Hotels | SunWave Switzerland',
        'desc':  'Geräuschlose Keramik-Infrarotheizung für Schweizer Hotels und Chalets. Kein Lüftergeräusch, kein Staub, individuelle Raumsteuerung, neun Designer-Varianten. Bis zu 66% weniger Energie.',
        'url':   BASE_DE + '/for-hotels.html',
        'og_image': BASE_EN + '/images/hotels-luxury-suite.webp',
    },
    'for-offices.html': {
        'title': 'Infrarotheizung für Schweizer Büros | SunWave Switzerland',
        'desc':  'Zonenheizung für Schweizer Büros und Gewerbeflächen. Nur bewohnte Bereiche beheizen, null Staubzirkulation, 66% weniger Energie vs. Gas, keine Kesselwartung. Amortisation unter 3 Jahren.',
        'url':   BASE_DE + '/for-offices.html',
        'og_image': BASE_EN + '/images/offices-open-plan.webp',
    },
    'for-solar.html': {
        'title': 'Infrarotheizung für Solar-Installateure | SunWave Switzerland',
        'desc':  'Kombinieren Sie SunWave Ceramica Infrarotpaneele mit Ihren PV-Anlagen. 650W Last, thermische Massenspeicherung, 66% weniger Energie vs. Gas. MuKEn-konformes Solar-Wärme-Paket.',
        'url':   BASE_DE + '/for-solar.html',
        'og_image': BASE_EN + '/images/solar-rooftop-swiss.webp',
    },
    'legal.html': {
        'title': 'Impressum | SunWave Switzerland — Lumia Technologies GmbH',
        'desc':  'Impressum für SunWave Switzerland, betrieben von Lumia Technologies GmbH, Glaserbergstrasse 27, 4056 Basel. UID CHE-204.700.764. Schweizer Recht. Gerichtsstand: Basel-Stadt.',
        'url':   BASE_DE + '/legal.html',
        'og_image': BASE_EN + '/images/logo.webp',
    },
    'terms.html': {
        'title': 'AGB | SunWave Switzerland',
        'desc':  'Allgemeine Verkaufsbedingungen für SunWave Ceramica Infrarotheizpaneele. 30 Tage Rückgabe, 5 Jahre Garantie, CHF 35 Schweizer Lieferung, 3–5 Tage Versand. Schweizer Recht.',
        'url':   BASE_DE + '/terms.html',
        'og_image': BASE_EN + '/images/logo.webp',
    },
    'returns.html': {
        'title': 'Rückgabebedingungen | SunWave Switzerland',
        'desc':  '30 Tage Rückgaberecht für SunWave Ceramica Paneele. Kostenlose Rückgabe bei fehlerhaften Artikeln. Vollständige Rückerstattung innerhalb von 14 Tagen. Paneele müssen uninstalliert sein.',
        'url':   BASE_DE + '/returns.html',
        'og_image': BASE_EN + '/images/logo.webp',
    },
    'shipping.html': {
        'title': 'Versand & Lieferung | SunWave Switzerland',
        'desc':  'CHF 35 Pauschale in alle Schweizer Kantone. SunWave Ceramica Paneele werden innerhalb von 1–2 Werktagen versandt, Lieferung in 3–5 Werktagen. Sendungsverfolgung. Transportschäden gedeckt.',
        'url':   BASE_DE + '/shipping.html',
        'og_image': BASE_EN + '/images/logo.webp',
    },
    'privacy.html': {
        'title': 'Datenschutzerklärung | SunWave Switzerland',
        'desc':  'Datenschutzerklärung für sunwaveswitzerland.com. Wie Lumia Technologies GmbH Ihre Daten gemäß Schweizer nDSG erhebt und schützt. Keine Tracking-Cookies. Keine Datenweitergabe.',
        'url':   BASE_DE + '/privacy.html',
        'og_image': BASE_EN + '/images/logo.webp',
    },
    'blog/index.html': {
        'title': 'Infrarotheizung Blog | SunWave Switzerland',
        'desc':  'Expertenbeiträge zur Infrarotheizung in der Schweiz: MuKEn 2014-Konformität, Solar-PV-Kombination, unabhängige Labortestergebnisse und Gas vs. Infrarot Kostenvergleiche.',
        'url':   BASE_DE + '/blog/',
        'og_image': BASE_EN + '/images/hero-banner-2.webp',
    },
    'blog/muken-2014-boiler-replacement-switzerland.html': {
        'title': 'MuKEn 2014: Gasheizung ersetzen Schweiz | SunWave',
        'desc':  'MuKEn 2014 Artikel 4.1 verlangt, dass Gasheizungen am Lebensende durch erneuerbare Heizsysteme ersetzt werden. Welche Kantone die Regel anwenden und warum Infrarotpaneele qualifizieren.',
        'url':   BASE_DE + '/blog/muken-2014-boiler-replacement-switzerland.html',
        'og_image': BASE_EN + '/images/hero-banner-3.webp',
    },
    'blog/solar-infrared-heating-switzerland.html': {
        'title': 'Solar + Infrarotheizung Schweiz | SunWave Switzerland',
        'desc':  'Warum Schweizer Solar-Installateure SunWave Ceramica Infrarotpaneele mit PV-Anlagen kombinieren. Lastanpassung, Eigenverbrauchserhöhung und thermische Masse erklärt.',
        'url':   BASE_DE + '/blog/solar-infrared-heating-switzerland.html',
        'og_image': BASE_EN + '/images/solar-rooftop-swiss.webp',
    },
    'blog/tu-dresden-infrared-test-results.html': {
        'title': 'TU Dresden DIN EN IEC 60675-3 Infrarot Testergebnisse | SunWave',
        'desc':  'TU Dresden testete SunWave Ceramica nach DIN EN IEC 60675-3 — dem europäischen Infrarotheizungsstandard. Strahlungswirkungsgrad, Spitzenwellenlänge 8,52μm und Bedeutung für Ihre Heizung.',
        'url':   BASE_DE + '/blog/tu-dresden-infrared-test-results.html',
        'og_image': BASE_EN + '/images/logo-tu-dresden.webp',
    },
    'blog/ceramic-vs-aluminium-infrared-panels.html': {
        'title': 'Keramik vs. Aluminium Infrarotheizung | SunWave Switzerland',
        'desc':  'Fraunhofer WKI testete Keramik-Infrarotpaneele: 0,043 mg/m³ TVOC — 23× unter dem Grenzwert. Warum Keramik Aluminium bei Innenraumluftqualität, thermischer Masse und Langlebigkeit übertrifft.',
        'url':   BASE_DE + '/blog/ceramic-vs-aluminium-infrared-panels.html',
        'og_image': BASE_EN + '/images/logo-fraunhofer.webp',
    },
    'blog/gas-vs-infrared-heating-cost-switzerland.html': {
        'title': 'Gas vs. Infrarotheizung Kosten Schweiz 2026 | SunWave',
        'desc':  'Vollständiger Kostenvergleich: Gasheizung vs. SunWave Ceramica Infrarot in der Schweiz. Kapitalkosten, Betriebskosten und Amortisation basierend auf unabhängiger Forschung und Schweizer Energiepreisen 2026.',
        'url':   BASE_DE + '/blog/gas-vs-infrared-heating-cost-switzerland.html',
        'og_image': BASE_EN + '/images/hero-banner-1.webp',
    },
}

# ── Core transform function ───────────────────────────────────────────────────
def transform_to_german(content, slug, is_blog=False):
    prefix = '../' if is_blog else ''

    # 1. Set lang to de
    content = content.replace('<html lang="en">', '<html lang="de">')

    # 2. Fix asset paths for de/ subfolder
    content = content.replace('href="css/style.css"', f'href="{prefix}../css/style.css"')
    content = content.replace('src="js/main.js"', f'src="{prefix}../js/main.js"')
    content = re.sub(r'src="(images/[^"]+)"', lambda m: f'src="{prefix}../{m.group(1)}"', content)
    content = re.sub(r'href="(images/[^"]+)"', lambda m: f'href="{prefix}../{m.group(1)}"', content)

    # 3. Fix internal navigation links
    nav_pages = ['index.html','product.html','research.html','contact.html',
                 'for-solar.html','for-hotels.html','for-homes.html','for-offices.html',
                 'legal.html','terms.html','returns.html','shipping.html','privacy.html']

    if is_blog:
        # From blog/: ../page.html stays, blog/index.html becomes index.html
        for page in nav_pages:
            content = content.replace(f'href="../{page}"', f'href="../{page}"')  # already correct
        content = content.replace('href="../blog/index.html"', 'href="index.html"')
        content = content.replace('href="../index.html#calculator"', 'href="../index.html#calculator"')
    else:
        # From root de/: page.html links stay relative within de/
        # blog links need to point to blog/ (which exists in de/ too if needed, else parent)
        content = content.replace('href="blog/index.html"', 'href="blog/index.html"')
        content = content.replace('href="index.html#calculator"', 'href="index.html#calculator"')

    # 4. Fix send-mail.php path
    content = content.replace("fetch('send-mail.php'", f"fetch('{prefix}../send-mail.php'")

    # 5. Update meta title, description, canonical, og tags
    meta = PAGE_META.get(slug, {})
    if meta:
        content = re.sub(r'<title>.*?</title>', f'<title>{meta["title"]}</title>', content)
        content = re.sub(r'<meta name="description"\s+content="[^"]*">',
                        f'<meta name="description" content="{meta["desc"]}">', content)
        content = re.sub(r'<link rel="canonical"\s+href="[^"]*">',
                        f'<link rel="canonical" href="{meta["url"]}">', content)
        content = re.sub(r'<meta property="og:title"\s+content="[^"]*">',
                        f'<meta property="og:title" content="{meta["title"]}">', content)
        content = re.sub(r'<meta property="og:description"\s+content="[^"]*">',
                        f'<meta property="og:description" content="{meta["desc"]}">', content)
        content = re.sub(r'<meta property="og:url"\s+content="[^"]*">',
                        f'<meta property="og:url" content="{meta["url"]}">', content)
        content = re.sub(r'<meta name="twitter:title"\s+content="[^"]*">',
                        f'<meta name="twitter:title" content="{meta["title"]}">', content)
        content = re.sub(r'<meta name="twitter:description"\s+content="[^"]*">',
                        f'<meta name="twitter:description" content="{meta["desc"]}">', content)

    # 6. Add hreflang
    base_slug = slug.replace('blog/', '')
    if slug.startswith('blog/'):
        en_url = f'{BASE_EN}/blog/{base_slug}'
        de_url = f'{BASE_DE}/blog/{base_slug}'
    elif slug == 'index.html':
        en_url = BASE_EN + '/'
        de_url = BASE_DE + '/'
    else:
        en_url = f'{BASE_EN}/{slug}'
        de_url = f'{BASE_DE}/{slug}'

    hreflang = f'''  <link rel="alternate" hreflang="en" href="{en_url}">
  <link rel="alternate" hreflang="de" href="{de_url}">
  <link rel="alternate" hreflang="x-default" href="{en_url}">'''
    content = content.replace('</head>', hreflang + '\n</head>')

    # 7. Add language switcher CSS
    content = content.replace('</head>', SWITCHER_CSS + '\n</head>')

    # 8. Inject DE language switcher into nav (replace EN switcher or add after order button)
    switcher_html = lang_switcher_de(slug if not is_blog else slug)
    # Remove any existing lang switcher and add new one
    content = re.sub(r'<div class="nav__lang">.*?</div>', '', content, flags=re.DOTALL)
    content = content.replace(
        'class="nav__order-btn">Jetzt bestellen</a>',
        f'class="nav__order-btn">Jetzt bestellen</a>\n      {switcher_html}'
    )
    content = content.replace(
        'class="nav__order-btn">Order Now</a>',
        f'class="nav__order-btn">Order Now</a>\n      {switcher_html}'
    )

    # 9. Apply text translations
    for en, de in TRANSLATIONS:
        content = content.replace(en, de)

    return content

# ── Add EN language switcher to all existing English pages ────────────────────
def add_en_switcher(content, slug):
    # Remove any existing lang switcher
    content = re.sub(r'<div class="nav__lang">.*?</div>', '', content, flags=re.DOTALL)
    # Add switcher CSS if not present
    if 'nav__lang' not in content:
        content = content.replace('</head>', SWITCHER_CSS + '\n</head>')
    # Add switcher after Order Now button
    is_blog = slug.startswith('blog/')
    de_slug = f'de/{slug}' if not is_blog else f'../de/{slug}'
    switcher = f"""<div class="nav__lang">
      <span class="nav__lang-btn lang-active">EN</span>
      <span class="nav__lang-sep">|</span>
      <a href="{de_slug}" class="nav__lang-btn">DE</a>
    </div>"""
    content = content.replace(
        'class="nav__order-btn">Order Now</a>',
        f'class="nav__order-btn">Order Now</a>\n      {switcher}'
    )
    return content

# ── Process all files ─────────────────────────────────────────────────────────
all_files = [(f.replace('\\','/'), False) for f in glob.glob('*.html')]
all_files += [(f.replace('\\','/'), True) for f in glob.glob('blog/*.html')]

print('=== Adding EN switcher to English pages ===')
for slug, is_blog in all_files:
    with open(slug,'r',encoding='utf-8') as f: c=f.read()
    new_c = add_en_switcher(c, slug)
    with open(slug,'w',encoding='utf-8') as f: f.write(new_c)
    print(f'EN switcher: {slug}')

print()
print('=== Generating German pages ===')
for slug, is_blog in all_files:
    with open(slug,'r',encoding='utf-8') as f: c=f.read()
    german = transform_to_german(c, slug, is_blog)
    out_path = f'de/{slug}'
    with open(out_path,'w',encoding='utf-8') as f: f.write(german)
    print(f'DE created: {out_path}')

print()
print(f'Done. {len(all_files)} English pages updated + {len(all_files)} German pages created.')
print('Upload: de/ folder to sunwaveswitzerland.com/de/')
print('Upload: all updated English .html files (EN switcher added)')
