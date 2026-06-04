"""
Complete German translation pass — replaces ALL English text in de/ pages.
Uses HTML-aware text node replacement (preserves tags, scripts, styles).
Also rebuilds the language switcher properly including mobile nav.
"""

import re, glob, os

# ── HTML-aware text replacement ───────────────────────────────────────────────
def replace_text_nodes(html, replacements):
    """Split HTML by tags, apply replacements only to text portions."""
    parts = re.split(r'(<[^>]+>)', html)
    in_skip = 0
    skip_tags = {'script', 'style', 'noscript'}
    result = []
    for part in parts:
        if part.startswith('<'):
            tag = re.match(r'</?(\w+)', part)
            if tag:
                t = tag.group(1).lower()
                if t in skip_tags and not part.startswith('</'):
                    in_skip += 1
                elif t in skip_tags and part.startswith('</'):
                    in_skip = max(0, in_skip - 1)
            result.append(part)
        else:
            if in_skip == 0:
                for en, de in replacements:
                    part = part.replace(en, de)
            result.append(part)
    return ''.join(result)

# ── Complete translation dictionary ───────────────────────────────────────────
# Every English text string found on the site, ordered longest first
TRANS = [

    # ── Homepage hero & stats ─────────────────────────────────────────────────
    ("Among Switzerland's most", "Eines der meistgeprüften"),
    ("independently tested", "Infrarotheizpaneele"),
    ("infrared heating panels.", "der Schweiz."),
    ("Ceramic infrared heating. Silent. Zero emissions. Up to 80% less energy than A+++ convectors. BSRIA tested. MuKEn compliant.",
     "Keramik-Infrarotheizung. Geräuschlos. Null Emissionen. Bis zu 80% weniger Energie als A+++ Konvektoren. BSRIA-getestet. MuKEn-konform."),
    ("View the Panel", "Das Paneel ansehen"),
    ("Calculate Savings", "Einsparungen berechnen"),
    ("less consumption vs A+++", "weniger Verbrauch vs. A+++"),
    ("confirmed by BSRIA", "bestätigt von BSRIA"),
    ("independent\nproduct lab tests", "unabhängige\nLaborprüfungen"),
    ("manufacturer\nwarranty", "Herstellergarantie"),
    ("per panel incl. thermostat,\n12–15 m² per panel", "pro Paneel inkl. Thermostat,\n12–15 m² pro Paneel"),
    ("per panel incl. thermostat", "pro Paneel inkl. Thermostat"),
    ("12–15 m² per panel", "12–15 m² pro Paneel"),
    ("Scroll", "Scrollen"),

    # Evidence strip
    ("Independently tested by", "Unabhängig getestet von"),
    ("less consumption vs A+++ convection heaters\n(BSRIA Report 105350/1, 2023)",
     "weniger Verbrauch als A+++ Konvektionsheizungen\n(BSRIA Bericht 105350/1, 2023)"),
    ("Less energy vs gas central heating\n(independent academic research — infrared technology)",
     "Weniger Energie vs. Gaszentralheizung\n(unabhängige akademische Forschung — Infrarottechnologie)"),
    ("below limit\n(Fraunhofer WKI AgBB, Day 7)", "unter Grenzwert\n(Fraunhofer WKI AgBB, Tag 7)"),
    ("Stable surface temp in 32 min\n(BSRIA 98-day continuous test)",
     "Stabile Oberflächentemp. in 32 Min.\n(BSRIA 98-Tage-Dauertest)"),
    ("mg/m³ TVOC — 23× below limit", "mg/m³ TVOC — 23× unter Grenzwert"),
    ("Up to 80%", "Bis zu 80%"),
    ("less consumption vs A+++", "weniger Verbrauch vs. A+++"),
    ("66%", "66%"),
    ("Less energy vs gas central heating", "Weniger Energie vs. Gaszentralheizung"),
    ("(independent academic research — infrared technology)", "(unabhängige akademische Forschung — Infrarottechnologie)"),
    ("0.043", "0,043"),
    ("mg/m³ TVOC — 23× below limit", "mg/m³ TVOC — 23× unter Grenzwert"),
    ("67°C", "67°C"),
    ("Stable surface temp in 32 min", "Stabile Oberflächentemp. in 32 Min."),
    ("(BSRIA 98-day continuous test)", "(BSRIA 98-Tage-Dauertest)"),

    # ── Product showcase ──────────────────────────────────────────────────────
    ("A panel that heats", "Ein Paneel, das wärmt"),
    ("your home — not the air.", "Ihr Zuhause — nicht die Luft."),
    ("SunWave Ceramica. 60 × 120 cm. 650 W. Nine surface finishes in 6 mm fine porcelain stoneware. The same technology across every finish — change the look, not the performance.",
     "SunWave Ceramica. 60 × 120 cm. 650 W. Neun Oberflächendesigns in 6 mm feinem Feinsteinzeug. Dieselbe Technologie in jeder Ausführung — Design ändern, Leistung beibehalten."),
    ("per panel · incl. VAT · WiFi thermostat required & included · CHF 35 delivery",
     "pro Paneel · inkl. MwSt. · WLAN-Thermostat erforderlich & enthalten · CHF 35 Lieferung"),
    ("per panel · incl. VAT · WiFi thermostat required &amp; included · CHF 35 delivery",
     "pro Paneel · inkl. MwSt. · WLAN-Thermostat erforderlich &amp; enthalten · CHF 35 Lieferung"),
    ("✓ 5-year warranty", "✓ 5 Jahre Garantie"),
    ("✓ Ships in 3–5 days", "✓ Lieferung in 3–5 Tagen"),
    ("✓ 30-day returns", "✓ 30 Tage Rückgabe"),
    ("✓ Class II certified", "✓ Klasse II zertifiziert"),

    # ── Segment intro ─────────────────────────────────────────────────────────
    ("Who it's for", "Für wen"),
    ("Built for Swiss professionals\nand homeowners", "Für Schweizer Fachleute\nund Hausbesitzer"),
    ("From solar installers adding a clean-heat product to their portfolio, to hotels eliminating fan noise from guest rooms, to homeowners replacing a failed boiler before winter.",
     "Von Solar-Installateueren, die ihr Portfolio erweitern, bis hin zu Hotels, die Lüfterlärm aus Gästezimmern eliminieren, und Hausbesitzern, die eine defekte Heizung vor dem Winter ersetzen."),

    # Segment card descriptions
    ("Pair infrared heating with your solar PV installations. Clients charge panels by day, heat rooms in thermal mass — perfect MuKEn-compliant package.",
     "Kombinieren Sie Infrarotheizung mit Solar-PV. Kunden laden tagsüber, heizen mittels Wärmespeicherung — das perfekte MuKEn-konforme Paket."),
    ("Silent operation. No dust. No maintenance. Individual room control. Premium tile aesthetic. Perfect for 4- and 5-star properties across Switzerland.",
     "Geräuschloser Betrieb. Kein Staub. Keine Wartung. Individuelle Raumsteuerung. Hochwertige Kachel-Ästhetik. Ideal für 4- und 5-Sterne-Häuser in der Schweiz."),
    ("MuKEn-compliant boiler replacement from CHF 490. No plumber. No planning permission. CHF 35 delivery, 3–5 days. Works in apartments and owned properties.",
     "MuKEn-konformer Heizungsersatz ab CHF 490. Kein Installateur. Keine Baugenehmigung. CHF 35 Lieferung, 3–5 Tage. Für Miet- und Eigentumswohnungen."),
    ("Zone heating — heat only occupied areas. Silent (no fan). Lower CO₂ reporting. Payback in under 3 years against gas. Minimal installation disruption.",
     "Zonenheizung — nur bewohnte Bereiche beheizen. Geräuschlos (kein Ventilator). Niedrigere CO₂-Bilanz. Amortisation in unter 3 Jahren vs. Gas. Minimaler Installationsaufwand."),
    ("Learn more →", "Mehr erfahren →"),

    # ── Science section ───────────────────────────────────────────────────────
    ("The science", "Die Wissenschaft"),
    ("Why radiant heat\noutperforms convection", "Warum Strahlungswärme\nKonvektion übertrifft"),
    ("Conventional electric heaters warm the air. Warm air rises. Your feet stay cold while the thermostat is satisfied. Every time a window opens or a door closes, the heated air escapes and must be replaced.",
     "Herkömmliche Elektroheizungen erwärmen die Luft. Warme Luft steigt auf. Ihre Füße bleiben kalt, während der Thermostat zufrieden ist. Jedes Mal, wenn ein Fenster geöffnet wird, entweicht die erwärmte Luft."),
    ("SunWave Ceramica panels emit long-wave infrared (8–14 µm) — the same wavelength that building materials, floors, walls, and people absorb most efficiently. Surfaces warm up. Walls store heat and release it slowly. The room is comfortable at 1–2°C lower thermostat setting.",
     "SunWave Ceramica Paneele emittieren langwelliges Infrarot (8–14 µm) — dieselbe Wellenlänge, die Baumaterialien, Böden, Wände und Menschen am effizientesten absorbieren. Oberflächen erwärmen sich. Wände speichern Wärme und geben sie langsam ab. Der Raum ist bei 1–2°C niedrigerer Thermostateinstellung komfortabel."),
    ("No stratification", "Keine Luftschichtung"),
    ("Uniform floor-to-ceiling temperature. No warm-ceiling, cold-floor effect.",
     "Gleichmäßige Temperatur vom Boden bis zur Decke. Kein Warm-Decke-Kalt-Boden-Effekt."),
    ("Charges thermal mass", "Thermische Masse aufgeladen"),
    ("Walls and floors absorb and slowly re-radiate heat. Room stays warm after panel switches off.",
     "Wände und Böden absorbieren Wärme und geben sie langsam ab. Der Raum bleibt warm, nachdem das Paneel abschaltet."),
    ("No dust circulation", "Keine Staubzirkulation"),
    ("No convective air currents means settled allergens stay settled. No recirculation.",
     "Keine Konvektionsluftströme: abgesetzte Allergene bleiben abgesetzt. Keine Rezirkulation."),
    ("Completely silent", "Vollständig geräuschlos"),
    ("No fan. No pump. No combustion. No moving parts. Absolute silence in operation.",
     "Kein Ventilator. Keine Pumpe. Keine Verbrennung. Keine beweglichen Teile. Absolute Stille im Betrieb."),
    ("The physics in depth →", "Die Physik im Detail →"),
    ("Energy use per m²/year", "Energieverbrauch pro m²/Jahr"),
    ("Gas central heating", "Gas-Zentralheizung"),
    ("Gas condensing boiler", "Gas-Brennwertkessel"),
    ("SunWave Ceramica (infrared)", "SunWave Ceramica (Infrarot)"),
    ("Source: Independent academic research on ceramic infrared heating technology (Dr.-Ing. Peter Kosack, 2008–2009). Figures apply to infrared heating as a technology category.",
     "Quelle: Unabhängige akademische Forschung zur Keramik-Infrarotheizungstechnologie (Dr.-Ing. Peter Kosack, 2008–2009)."),

    # ── Evidence section ──────────────────────────────────────────────────────
    ("Independent evidence", "Unabhängige Belege"),
    ("4 laboratories.\n4 independent tests.", "4 Laboratorien.\n4 unabhängige Tests."),
    ("Every claim on this website is grounded in a named study with a report number. Not marketing. Not manufacturer data. Independent labs.",
     "Jede Aussage auf dieser Website basiert auf einer namentlich genannten Studie mit Berichtsnummer. Kein Marketing. Keine Herstellerdaten. Unabhängige Labore."),
    ("BSRIA Limited, UK", "BSRIA Limited, UK"),
    ("98-Day Continuous Performance Test", "98-tägiger Dauerleistungstest"),
    ('"Ceramic heaters save up to 80% of the cost vs best-rated triple-A conventional electric heating."',
     '„Keramikheizungen sparen bis zu 80% der Kosten im Vergleich zu den bestbewerteten Triple-A konventionellen Elektroheizungen."'),
    ("vs best-rated triple-A conventional electric heating.", "vs. bestbewerteten Triple-A konventionellen Elektroheizungen."),
    ("Surface temp: 67°C at 32 min. Avg daily cost: £0.91.", "Oberflächentemp.: 67°C in 32 Min. Durchschnittliche Tageskosten: £0,91."),
    ("Approved by Mark Roper, Head of Laboratory & Test, BSRIA",
     "Genehmigt von Mark Roper, Leiter Labor & Test, BSRIA"),
    ("Approved by Mark Roper, Head of Laboratory &amp; Test, BSRIA",
     "Genehmigt von Mark Roper, Leiter Labor &amp; Test, BSRIA"),
    ("Fraunhofer WKI, Germany", "Fraunhofer WKI, Deutschland"),
    ("Indoor Air Quality — AgBB Assessment", "Innenraumluftqualität — AgBB-Bewertung"),
    ("TVOC: 0.043 mg/m³ (limit 1.0). R-value: 0.186 (limit 1.0).\nCarcinogenic VOC: not detected. All AgBB Day 28 requirements met in 7 days.",
     "TVOC: 0,043 mg/m³ (Grenzwert 1,0). R-Wert: 0,186 (Grenzwert 1,0).\nKarzinogene VOC: nicht nachgewiesen. Alle AgBB-Anforderungen in 7 Tagen erfüllt."),
    ("Carcinogenic VOC: not detected. All AgBB Day 28 requirements met in 7 days.",
     "Karzinogene VOC: nicht nachgewiesen. Alle AgBB-Tag-28-Anforderungen in 7 Tagen erfüllt."),
    ("Dr. E. Uhde, Materials Analysis & Indoor Air Chemistry Dept.",
     "Dr. E. Uhde, Abteilung Materialanalyse & Innenraumluftchemie"),
    ("Dr. E. Uhde, Materials Analysis &amp; Indoor Air Chemistry Dept.",
     "Dr. E. Uhde, Abteilung Materialanalyse &amp; Innenraumluftchemie"),
    ("TU Dresden, Germany", "TU Dresden, Deutschland"),
    ("DIN EN IEC 60675-3 · October 2022", "DIN EN IEC 60675-3 · Oktober 2022"),
    ("Radiation Efficiency Measurement", "Messung des Strahlungswirkungsgrads"),
    ("Radiation efficiency of the SunWave Ceramica panel confirmed per DIN EN IEC 60675-3 — the European standard for measuring what proportion of electrical input becomes infrared radiation vs. convective heat output.",
     "Strahlungswirkungsgrad des SunWave Ceramica Paneels bestätigt nach DIN EN IEC 60675-3 — dem europäischen Standard zur Messung des Anteils der elektrischen Eingangsleistung, der zu Infrarotstrahlung wird."),
    ("Technische Universität Dresden, Energy Efficiency Dept.", "Technische Universität Dresden, Fachbereich Energieeffizienz"),
    ("Labor S.A., Greece", "Labor S.A., Griechenland"),
    ("Full EN 60335-2-30 Electrical Safety Test", "Vollständige EN-60335-2-30-Elektrosicherheitsprüfung"),
    ("All clauses PASS. Class II / IP20. Surface temp rise: 71.2K (limit 90K). Leakage current: 0.1mA (limit 0.25mA). Withstood 3000V dielectric test.",
     "Alle Klauseln BESTANDEN. Klasse II / IP20. Oberflächentemperaturanstieg: 71,2K (Grenzwert 90K). Ableitstrom: 0,1mA (Grenzwert 0,25mA). 3000V Dielektrizitätsprüfung bestanden."),
    ("Most recent test · December 23, 2024 · All applicable clauses",
     "Neuester Test · 23. Dezember 2024 · Alle anwendbaren Klauseln"),
    ("Full test data available", "Alle Testdaten verfügbar"),
    ("All four reports documented with methodology, raw data, and conclusions.",
     "Alle vier Berichte mit Methodik, Rohdaten und Schlussfolgerungen dokumentiert."),
    ("Read all research →", "Alle Forschungsdaten lesen →"),

    # ── MuKEn section ────────────────────────────────────────────────────────
    ("Swiss market", "Schweizer Markt"),
    ("MuKEn is phasing out\nyour boiler. We're ready.", "MuKEn verdrängt\nIhre Heizung. Wir sind bereit."),
    ("MuKEn 2014 — the Swiss cantonal model energy regulations — requires that fossil fuel heating systems be replaced with renewable alternatives at end of life. As of 2026, this is in force across most Swiss cantons including Zurich, Bern, Basel, Vaud, and Aargau.",
     "MuKEn 2014 — die Mustervorschriften der Kantone im Energiebereich — schreibt vor, dass fossile Heizsysteme am Lebensende durch erneuerbare Alternativen ersetzt werden müssen. Ab 2026 gilt dies in den meisten Schweizer Kantonen, darunter Zürich, Bern, Basel, Waadt und Aargau."),
    ("SunWave Ceramica panels are fully electric with zero on-site emissions. They qualify as a compliant replacement in all cantons that have adopted the fossil fuel phase-out provision — without planning permission, without a plumber, and deliverable within 3–5 days.",
     "SunWave Ceramica Paneele sind vollständig elektrisch mit null Emissionen vor Ort. Sie qualifizieren sich als konformer Ersatz in allen Kantonen mit Fossile-Brennstoffe-Ausstiegsregelung — ohne Baugenehmigung, ohne Installateur, lieferbar innerhalb von 3–5 Tagen."),
    ("No fossil fuel combustion — zero on-site CO₂", "Keine Verbrennung fossiler Brennstoffe — null CO₂ vor Ort"),
    ("Compatible with Switzerland's ~90% low-carbon grid",
     "Kompatibel mit dem ~90% kohlenstoffarmen Schweizer Stromnetz"),
    ("No building permit required in most cantons", "In den meisten Kantonen keine Baugenehmigung erforderlich"),
    ("Can be installed within days of boiler failure", "Innerhalb von Tagen nach Heizungsausfall installierbar"),
    ("MuKEn Compliance Guide →", "MuKEn-Konformitätsleitfaden →"),
    ("Annual cost — 80m² apartment, Zurich", "Jährliche Kosten — 80m² Wohnung, Zürich"),
    ("+CHF 400 annual service", "+CHF 400 jährlicher Service"),
    ("No service required", "Kein Service erforderlich"),
    ("Annual saving", "Jährliche Ersparnis"),
    ("Panel payback: 2–3 years", "Paneel-Amortisation: 2–3 Jahre"),
    ("Based on academic research on ceramic infrared heating technology, CHF 0.29/kWh electricity (Swiss 2026 avg), CHF 0.13/kWh gas. Individual results vary.",
     "Basierend auf akademischer Forschung, CHF 0,29/kWh Strom (Schweizer Durchschnitt 2026), CHF 0,13/kWh Gas. Individuelle Ergebnisse variieren."),

    # ── Calculator ────────────────────────────────────────────────────────────
    ("Savings calculator", "Sparrechner"),
    ("Calculate your switch", "Berechnen Sie Ihren Wechsel"),
    ("Floor area to heat (m²)", "Zu beheizende Fläche (m²)"),
    ("Current heating system", "Aktuelles Heizsystem"),
    ("Electricity price (CHF/kWh)", "Strompreis (CHF/kWh)"),
    ("Gas price (CHF/kWh)", "Gaspreis (CHF/kWh)"),
    ("Building insulation", "Gebäudedämmung"),
    ("Based on independent research data. Adjust for your building and energy prices.",
     "Basierend auf unabhängigen Forschungsdaten. Für Ihr Gebäude und Ihre Energiepreise anpassen."),
    ("Results update automatically as you adjust the inputs above.",
     "Ergebnisse werden automatisch aktualisiert."),
    ("Based on Swiss 2026 average energy prices.", "Basierend auf Schweizer Durchschnitts-Energiepreisen 2026."),
    ("Annual saving (CHF)", "Jährliche Ersparnis (CHF)"),
    ("Panel payback period", "Amortisierungsdauer"),
    ("CO₂ saved per year", "Jährlich eingesparte CO₂"),
    ("Gas central heating", "Gas-Zentralheizung"),
    ("Gas condensing boiler", "Gas-Brennwertkessel"),
    ("Oil boiler", "Ölheizung"),
    ("Electric heating (storage or panel)", "Elektrische Heizung (Speicher oder Paneel)"),
    ("Heat pump", "Wärmepumpe"),
    ("District heating", "Fernwärme"),
    ("No heating (new build)", "Keine Heizung (Neubau)"),
    ("Poor (before 1960)", "Schlecht (vor 1960)"),
    ("Average (1960–1980)", "Durchschnittlich (1960–1980)"),
    ("Good (1980–2000)", "Gut (1980–2000)"),
    ("Excellent (after 2000)", "Ausgezeichnet (nach 2000)"),
    ("Energy data: Independent academic research on ceramic infrared heating technology (Dr. Kosack, 2008–2009) — 71.21 kWh/m²/yr infrared vs 208.73 kWh/m²/yr gas. Insulation multipliers per SIA 380/1. Default rates: CHF 0.29/kWh electricity, CHF 0.13/kWh gas (Swiss 2026 averages — adjust to your tariff). Panel capital: CHF 490 × panels (12–15 m² each, thermostat included). CO₂: Swiss grid avg 35g/kWh; gas 202g/kWh. Results are indicative — individual buildings vary.",
     "Energiedaten: Unabhängige akademische Forschung (Dr. Kosack, 2008–2009) — 71,21 kWh/m²/Jahr Infrarot vs. 208,73 kWh/m²/Jahr Gas. Dämmungsmultiplikatoren per SIA 380/1. Standardwerte: CHF 0,29/kWh Strom, CHF 0,13/kWh Gas (Schweizer Durchschnitt 2026). Paneel-Kapital: CHF 490 × Paneele (12–15 m² pro Stück, Thermostat enthalten). CO₂: Schweizer Stromnetz-Durchschnitt 35g/kWh; Gas 202g/kWh. Ergebnisse sind Richtwerte."),

    # ── FAQ ───────────────────────────────────────────────────────────────────
    ("FAQ", "Häufige Fragen"),
    ("Common questions", "Häufig gestellte Fragen"),
    ("Is infrared heating MuKEn-compliant in Switzerland?",
     "Ist eine Infrarotheizung MuKEn-konform in der Schweiz?"),
    ("Electric infrared panels produce zero on-site combustion and operate on Switzerland's ~90% low-carbon electricity grid. They qualify as a compliant fossil fuel heating replacement under MuKEn 2014 Article 4.1 in all cantons that have adopted the provision — including Zurich, Bern, Basel, Vaud, and Aargau. No planning permission required in most cases.",
     "Elektrische Infrarotpaneele erzeugen keine Verbrennung vor Ort und betreiben sich mit dem ~90% kohlenstoffarmen Schweizer Stromnetz. Sie qualifizieren sich als konformer Heizungsersatz unter MuKEn 2014 Artikel 4.1 in allen Kantonen mit entsprechender Regelung — inkl. Zürich, Bern, Basel, Waadt und Aargau."),
    ("How quickly can my boiler be replaced with infrared panels?",
     "Wie schnell kann meine Heizung durch Infrarotpaneele ersetzt werden?"),
    ("SunWave Ceramica panels ship to all Swiss cantons with delivery in 3–5 working days. Panels connecting to standard sockets can be installed the same day they arrive — no electrician required for socket-connected panels. Hardwired installation requires a NIV-authorised electrician (typically 1 day).",
     "SunWave Ceramica Paneele werden in alle Schweizer Kantone in 3–5 Werktagen geliefert. Steckdosen-Paneele können am Liefertag installiert werden — kein Elektriker erforderlich. Fest verdrahtete Installation erfordert einen NIV-zugelassenen Elektriker (in der Regel 1 Tag)."),
    ("What is the warranty?", "Wie lange ist die Garantie?"),
    ("5 years full manufacturer's warranty. The ceramic surface does not degrade — there are no moving parts, no filters, no gas components. The BSRIA 98-day continuous test confirmed stable performance with no output degradation throughout.",
     "5 Jahre volle Herstellergarantie. Die Keramikoberfläche degradiert nicht — keine beweglichen Teile, keine Filter, keine Gaskomponenten. Der BSRIA 98-Tage-Dauertest bestätigte stabile Leistung ohne Leistungsabfall."),
    ("Can I use infrared panels in a rented apartment?",
     "Kann ich Infrarotpaneele in einer Mietwohnung nutzen?"),
    ("Yes. Panels connecting to standard sockets do not require modification to the building and typically do not require landlord consent under Swiss tenancy law. They can be removed on departure with no permanent damage — mounting holes only.",
     "Ja. Steckdosen-Paneele erfordern keine baulichen Veränderungen und benötigen in der Regel keine Vermietereinwilligung nach Schweizer Mietrecht. Sie können bei Auszug ohne bleibende Schäden entfernt werden — nur Montagelöcher."),
    ("Are the panels safe for children and allergy sufferers?",
     "Sind die Paneele sicher für Kinder und Allergiker?"),
    ("Fraunhofer WKI certified VOC emissions at 0.043 mg/m³ TVOC — 23× below the limit. No combustion products. No forced air movement (no dust recirculation). The ceramic surface is chemically inert (same material as food-safe floor tiles). Install on the upper wall out of direct reach of small children.",
     "Fraunhofer WKI zertifizierte VOC-Emissionen bei 0,043 mg/m³ TVOC — 23× unter dem Grenzwert. Keine Verbrennungsprodukte. Keine Zwangslüftung (keine Staubrezirkulation). Die Keramikoberfläche ist chemisch inert. An der oberen Wand außerhalb der Reichweite kleiner Kinder montieren."),

    # ── CTA section ───────────────────────────────────────────────────────────
    ("Ready to switch to clean,\nsilent infrared heat?", "Bereit für saubere,\ngeräuschlose Infrarotwärme?"),
    ("Ready to switch to clean,", "Bereit für saubere,"),
    ("silent infrared heat?", "geräuschlose Infrarotwärme?"),
    ("CHF 490 per panel. A thermostat is required — included with every order. CHF 35 delivery across Switzerland. 5-year warranty. 3–5 day delivery.",
     "CHF 490 pro Paneel. Ein Thermostat ist erforderlich — bei jeder Bestellung enthalten. CHF 35 Lieferung in die ganze Schweiz. 5 Jahre Garantie. 3–5 Tage Lieferzeit."),
    ("Order the Panel →", "Das Paneel bestellen →"),
    ("Ask a Question", "Frage stellen"),

    # ── Product page specific ─────────────────────────────────────────────────
    ("Not a binding order — we confirm availability within 24 hours",
     "Keine verbindliche Bestellung — wir bestätigen die Verfügbarkeit innerhalb von 24 Stunden"),
    ("German-patented magnetocaloric paste (carbon nanotube & graphene) — the heart of the technology",
     "Deutsch-patentierte magnetokalorische Paste (Kohlenstoffnanoröhren & Graphen) — das Herzstück der Technologie"),
    ("Confirmed per DIN EN IEC 60675-3", "Bestätigt nach DIN EN IEC 60675-3"),
    ("Wall or ceiling", "Wand oder Decke"),
    ("50 mm from ceiling", "50 mm von der Decke"),
    ("10 mm from wall surface", "10 mm von der Wandoberfläche"),
    ("10 mm from wall", "10 mm von der Wand"),
    ("Zero (no moving parts)", "Null (keine beweglichen Teile)"),
    ("From independent laboratory reports — not manufacturer claims",
     "Aus unabhängigen Laborberichten — keine Herstellerangaben"),
    ("less consumption than A+++ convection heaters", "weniger Verbrauch als A+++ Konvektionsheizungen"),
    ("Less energy vs. gas heating per m²", "Weniger Energie vs. Gasheizung pro m²"),
    ("Labor S.A. Report 2316.001.3.01 — Dec 2024", "Labor S.A. Bericht 2316.001.3.01 — Dez. 2024"),
    ("All EN 60335-2-30 safety clauses passed", "Alle EN-60335-2-30-Sicherheitsklauseln bestanden"),
    ("Every claim on this page is supported by a named test report from an accredited institution",
     "Jede Aussage auf dieser Seite wird durch einen namentlich genannten Prüfbericht einer akkreditierten Institution belegt"),
    ("BSRIA independently measured heat transfer efficiency of the SunWave Ceramica. The panel uses up to 80% less energy than the best-rated A+++ conventional electric heaters.",
     "BSRIA hat die Wärmeübertragungseffizienz des SunWave Ceramica unabhängig gemessen. Das Paneel verbraucht bis zu 80% weniger Energie als die bestbewerteten A+++ konventionellen Elektroheizungen."),
    ("TU Dresden tested the SunWave Ceramica to DIN EN IEC 60675-3 — the European standard that precisely measures what proportion of electrical input is emitted as infrared radiation.",
     "TU Dresden hat das SunWave Ceramica nach DIN EN IEC 60675-3 getestet — dem europäischen Standard, der genau misst, welcher Anteil der elektrischen Eingangsleistung als Infrarotstrahlung emittiert wird."),
    ("Fraunhofer WKI is Europe's leading institute for indoor air quality testing. The SunWave Ceramica was tested at operating temperature for VOC, formaldehyde, and carcinogens.",
     "Fraunhofer WKI ist Europas führendes Institut für Innenraumluftqualitätsprüfung. Das SunWave Ceramica wurde bei Betriebstemperatur auf VOC, Formaldehyd und Karzinogene geprüft."),
    ("No formaldehyde detected", "Kein Formaldehyd nachgewiesen"),
    ("No benzene detected", "Kein Benzol nachgewiesen"),
    ("An independent academic study (TU Kaiserslautern) compared actual energy consumption of flat infrared panels (Knebel brand) with gas central heating over a 9-month winter season.",
     "Eine unabhängige akademische Studie (TU Kaiserslautern) verglich den tatsächlichen Energieverbrauch von flachen Infrarotpaneelen (Marke Knebel) mit Gaszentralheizung über eine 9-monatige Wintersaison."),
    ("66% energy saving vs. gas", "66% Energieeinsparung vs. Gas"),
    ("No temperature stratification", "Keine Temperaturschichtung"),
    ("Category research — not SunWave-specific", "Kategorie-Forschung — nicht SunWave-spezifisch"),
    ("Labor S.A. conducted a comprehensive electrical safety test to EN 60335-2-30 — the international standard for fixed electric space heating appliances.",
     "Labor S.A. führte eine umfassende Elektrosicherheitsprüfung nach EN 60335-2-30 durch — dem internationalen Standard für festverdrahtete elektrische Raumheizgeräte."),
    ("All EN 60335-2-30 clauses PASS", "Alle EN-60335-2-30-Klauseln BESTANDEN"),
    ("All prices in CHF including VAT · CHF 35 shipping within Switzerland",
     "Alle Preise in CHF inkl. MwSt. · CHF 35 Versand innerhalb der Schweiz"),
    ("Submitting a quote request is not a binding order. We'll confirm availability and shipping timeline within 24 hours.",
     "Eine Angebotsanfrage ist keine verbindliche Bestellung. Wir bestätigen Verfügbarkeit und Lieferfrist innerhalb von 24 Stunden."),
    ("Cable with Schuko plug (Type F) — 10 mm exit from wall",
     "Kabel mit Schuko-Stecker (Typ F) — 10 mm Wandaustritt"),
    ("Delivery to all Swiss cantons including Ticino", "Lieferung in alle Schweizer Kantone inkl. Tessin"),
    ("5 Jahre Garantie (parts and labour)", "5 Jahre Garantie (Teile und Arbeit)"),
    ("No questions asked — if unhappy, return for full refund",
     "Keine Fragen — bei Unzufriedenheit vollständige Rückerstattung"),
    ("Panels do not degrade — 30+ year design life", "Paneele degradieren nicht — Auslegungslebensdauer 30+ Jahre"),
    ("Volume pricing available for installers and hotels",
     "Mengenrabatte für Installateure und Hotels verfügbar"),
    ("Contact us to discuss your project", "Kontaktieren Sie uns für Ihr Projekt"),

    # Product FAQ
    ("How many panels do I need for my room?", "Wie viele Paneele benötige ich für meinen Raum?"),
    ("One 650 W SunWave Ceramica panel is designed to heat 12–15 m² effectively. For a 50 m² apartment in good condition, four panels are typically sufficient — one per room or zone. For higher ceilings (above 2.8 m) or older buildings with average insulation, plan closer to one panel per 12 m². Our savings calculator gives a personalised estimate based on your floor area and insulation quality.",
     "Ein 650W SunWave Ceramica Paneel ist für die effektive Beheizung von 12–15 m² ausgelegt. Für eine 80 m² Wohnung in gutem Zustand reichen in der Regel vier Paneele — eines pro Raum oder Zone. Bei höheren Decken (über 2,8 m) oder älteren Gebäuden mit durchschnittlicher Dämmung planen Sie näher an einem Paneel pro 12 m². Unser Sparrechner liefert eine personalisierte Schätzung."),
    ("Can the panels be installed on a ceiling?", "Können die Paneele an der Decke montiert werden?"),
    ("Yes — ceiling mounting is often the most effective position, directing infrared radiation downward onto the occupancy zone. Maintain at least 50 mm clearance from the ceiling surface for airflow around the back of the panel. Standard ceiling mounting hardware is included. For high ceilings (above 3 m), wall mounting at mid-height may be preferable to keep radiation intensity focused on the living zone.",
     "Ja — Deckenmontage ist oft die effektivste Position und richtet die Infrarotstrahlung nach unten in die Aufenthaltszone. Mindestens 50 mm Abstand zur Deckenfläche für die Luftzirkulation einhalten. Standard-Deckenmontagehalterung ist enthalten. Bei hohen Decken (über 3 m) kann Wandmontage auf halber Höhe bevorzugt werden."),
    ("Do I need an electrician to install the panel?", "Benötige ich einen Elektriker für die Installation?"),
    ("Plug-in installation (Schuko plug Type F — use standard Schuko socket or adapter) can be done without an electrician: mount the bracket, hang the panel, plug in. The cable exits 10 mm from the wall for a clean, minimal look. For hardwired installation (fully recessed cable, no visible plug), a certified Swiss electrician is required per NIN 2020 regulations. Most installers complete hardwired installations in under two hours per panel. We can refer you to certified installers in your canton — contact us.",
     "Steckdosen-Installation (Schuko Typ F) ist ohne Elektriker möglich: Halterung montieren, Paneel einhängen, einstecken. Das Kabel tritt 10 mm von der Wand aus. Für Fest-Installation ist ein NIN-2020-zertifizierter Elektriker erforderlich. Die meisten Installateure benötigen unter zwei Stunden pro Paneel."),
    ("Are the panels compatible with solar panels?", "Sind die Paneele mit Solaranlagen kompatibel?"),
    ("Yes — this is one of the most effective pairings in Swiss residential energy. A SunWave Ceramica panel draws 650 W; a standard 400 W rooftop solar panel produces that energy in under 2 hours of good sun. Because infrared heating stores heat in thermal mass (walls, floor, furniture), you can run panels during peak solar generation and coast on stored warmth for hours afterward — dramatically reducing your grid draw. Many Swiss solar installers now package SunWave panels with their PV installs. See our solar installer page for full technical details.",
     "Ja — eine der effektivsten Kombinationen im Schweizer Wohnbereich. Ein SunWave Ceramica Paneel zieht 650W; ein Standard-400W-Solarmodul erzeugt diese Energie in unter 2 Stunden Sonnenschein. Da Infrarotheizung Wärme in der thermischen Masse speichert, können Sie Paneele während der Spitzen-Solarproduktion betreiben und stundenlang von gespeicherter Wärme profitieren — Stromnetzentnahme drastisch reduziert."),
    ("What thermostat should I use?", "Welchen Thermostat soll ich verwenden?"),
    ("Any 230 V thermostat rated for resistive loads (most are) will work. We recommend a smart WiFi thermostat that allows scheduling — heating before you arrive, reducing during the night, and optimising for solar production windows. We offer a compatible smart thermostat as an add-on in the order form above. Third-party options from Nest, Heatmiser, or Swiss-made thermostats all work without any modification.",
     "Jeder 230V-Thermostat für resistive Lasten (die meisten) funktioniert. Wir empfehlen einen smarten WLAN-Thermostat mit Zeitplanung — Heizung vor Ihrer Ankunft, Reduktion nachts, Optimierung für Solarproduktionsfenster. Kompatible Smart-Thermostaten von Nest, Heatmiser oder Schweizer Herstellern funktionieren alle ohne Modifikation."),
    ("Is the surface temperature safe for children and pets?",
     "Ist die Oberflächentemperatur sicher für Kinder und Haustiere?"),
    ("The SunWave Ceramica surface reaches approximately 67°C at typical operating temperature (max 90°C per Labor S.A. certification). This is above the safe-to-touch threshold. The panel should be mounted on the wall or ceiling at a height that prevents direct contact — not placed as a freestanding unit. With standard upper-wall mounting, the panel surface is out of reach.",
     "Die SunWave Ceramica Oberfläche erreicht ca. 67°C bei typischer Betriebstemperatur (max. 90°C per Labor S.A. Zertifizierung). Das liegt über der sicheren Berührungsgrenze. Das Paneel sollte an der Wand oder Decke in einer Höhe montiert werden, die direkten Kontakt verhindert."),

    # Product specs labels
    ("Technical Specifications", "Technische Spezifikationen"),
    ("Performance Data", "Leistungsdaten"),
    ("4 Independent Laboratory Tests", "4 Unabhängige Laborprüfungen"),
    ("Configure Your Order", "Bestellung konfigurieren"),
    ("Product Questions", "Produktfragen"),
    ("Electrical", "Elektrisch"),
    ("Physical", "Physisch"),
    ("Thermal Performance", "Thermische Leistung"),
    ("Installation", "Installation"),
    ("What's in the box", "Lieferumfang"),
    ("Delivery & shipping", "Lieferung & Versand"),
    ("Delivery &amp; shipping", "Lieferung &amp; Versand"),
    ("Guarantee & returns", "Garantie & Rückgabe"),
    ("Guarantee &amp; returns", "Garantie &amp; Rückgabe"),
    ("Need more than 5 panels?", "Mehr als 5 Paneele benötigt?"),
    ("Choose your finish", "Wählen Sie Ihr Design"),

    # ── Research page ─────────────────────────────────────────────────────────
    ("4 Laboratory Tests. Every Claim Verified.", "4 Laborprüfungen. Jede Aussage verifiziert."),
    ("Independent Test Reports", "Unabhängige Prüfberichte"),
    ("Certifications & Standards", "Zertifizierungen & Normen"),
    ("Certifications &amp; Standards", "Zertifizierungen &amp; Normen"),
    ("The Physics Behind the Performance", "Die Physik hinter der Leistung"),
    ("Academic Research", "Akademische Forschung"),
    ("9-Month Infrared vs Gas Energy Study", "9-Monats-Studie: Infrarot vs. Gas-Energieverbrauch"),
    ("EU Declaration of Conformity · CE Marking · 5-Year Warranty",
     "EU-Konformitätserklärung · CE-Kennzeichnung · 5 Jahre Garantie"),

    # ── Contact page ──────────────────────────────────────────────────────────
    ("Get a Free Quote", "Kostenloses Angebot erhalten"),
    ("Tell us about your space and we'll send back a personalised panel count, capital cost, annual saving estimate, and payback period within 24 hours.",
     "Beschreiben Sie Ihren Raum und wir senden Ihnen innerhalb von 24 Stunden eine personalisierte Paneel-Anzahl, Kapitalkosten, Jahresersparnisschätzung und Amortisierungsdauer."),
    ("Request a Quote", "Angebot anfragen"),
    ("We reply within 24 hours, typically much sooner.", "Wir antworten innerhalb von 24 Stunden, meist deutlich früher."),
    ("Your name", "Ihr Name"),
    ("your@email.com", "ihre@email.com"),
    ("+41 79 123 45 67", "+41 79 123 45 67"),
    ("Select canton...", "Kanton auswählen..."),
    ("I am enquiring as a...", "Ich frage an als..."),
    ("Select...", "Auswählen..."),
    ("Homeowner / apartment tenant", "Hausbesitzer / Mieter"),
    ("Solar / PV installer", "Solar- / PV-Installateur"),
    ("Hotel or hospitality operator", "Hotel- oder Gastronomiebetreiber"),
    ("Office / commercial property manager", "Büro- / Gewerbeobjektverwalter"),
    ("Architect or interior designer", "Architekt oder Innenarchitekt"),
    ("Electrician / installer", "Elektriker / Installateur"),
    ("Other", "Sonstiges"),
    ("Floor area (m²)", "Wohnfläche (m²)"),
    ("e.g. 80", "z.B. 80"),
    ("Current heating system", "Aktuelles Heizsystem"),
    ("Message / questions", "Nachricht / Fragen"),
    ("Tell us anything helpful: your insulation quality, whether you have solar panels, specific rooms you want to heat, timeline, etc.",
     "Teilen Sie uns Nützliches mit: Ihre Dämmqualität, ob Sie Solarpaneele haben, bestimmte Räume, die Sie beheizen möchten, Zeitplan usw."),
    ("Send Quote Request", "Angebotsanfrage senden"),
    ("Sending…", "Wird gesendet…"),
    ("No spam. We use this information only to prepare your personalised quote.",
     "Kein Spam. Wir verwenden diese Informationen nur zur Erstellung Ihres persönlichen Angebots."),
    ("Quote request sent!", "Angebotsanfrage gesendet!"),
    ("We'll review your information and send back a personalised panel count, savings estimate, and pricing within 24 hours (usually much sooner).",
     "Wir prüfen Ihre Informationen und senden Ihnen innerhalb von 24 Stunden eine personalisierte Paneel-Anzahl, Sparschätzung und Preisgestaltung (meist deutlich früher)."),
    ("In the meantime, you can", "In der Zwischenzeit können Sie"),
    ("use our savings calculator", "unseren Sparrechner nutzen"),
    ("or", "oder"),
    ("read the independent test reports", "die unabhängigen Prüfberichte lesen"),
    ("Something went wrong. Please email us directly at", "Etwas ist schief gelaufen. Bitte mailen Sie uns direkt an"),

    # ── For-homes page ────────────────────────────────────────────────────────
    ("For Schweizer Haushalte", "Für Schweizer Haushalte"),
    ("Infrared Heating for\n      Swiss Homes", "Infrarotheizung für\n      Schweizer Haushalte"),
    ("The SunWave Ceramica cuts home heating costs by up to 66% compared to gas. No annual boiler service. No gas connection fixed charge. From CHF 490 per panel.",
     "Das SunWave Ceramica senkt die Haushalts-Heizkosten um bis zu 66% im Vergleich zu Gas. Kein jährlicher Kesseldienst. Keine Gasanschluss-Grundgebühr. Ab CHF 490 pro Paneel."),
    ("Less energy than gas (independent academic research — infrared technology)",
     "Weniger Energie als Gas (unabhängige akademische Forschung — Infrarottechnologie)"),
    ("Year lifespan (no moving parts)", "Jahre Lebensdauer (keine beweglichen Teile)"),
    ("Rising gas prices, MuKEn boiler replacement requirements, and Swiss solar incentives are making infrared the obvious choice for Swiss homeowners in 2026.",
     "Steigende Gaspreise, MuKEn-Heizungsersatzpflichten und Schweizer Solar-Anreize machen Infrarot zur offensichtlichen Wahl für Schweizer Hausbesitzer 2026."),
    ("Switzerland's Model Kantonal Energy Regulation (MuKEn 2014) requires that when your gas or oil boiler reaches end-of-life, it must be replaced with a renewable heating source. In most cantons, this is already in force.",
     "Die Mustervorschriften der Kantone (MuKEn 2014) schreiben vor, dass Ihre Gas- oder Ölheizung am Lebensende durch eine erneuerbare Heizquelle ersetzt werden muss. In den meisten Kantonen gilt dies bereits."),
    ("Rather than waiting for the boiler to fail — and scrambling for a replacement mid-winter — many Swiss homeowners are proactively switching.",
     "Anstatt auf den Ausfall der Heizung zu warten — und mitten im Winter nach einem Ersatz zu suchen — wechseln viele Schweizer Hausbesitzer proaktiv."),
    ("A typical Swiss gas-heated apartment (80 m², good insulation) carries significant annual costs — gas energy, annual boiler service, and the gas connection standing charge.",
     "Eine typische Schweizer gasgeheizte Wohnung (80 m², gute Dämmung) trägt erhebliche jährliche Kosten — Gasenergie, jährlicher Kesseldienst und Gasanschluss-Grundgebühr."),
    ("Swiss residential buildings are among the best-sealed in Europe — excellent for energy efficiency, but concentrating any indoor air pollutants. SunWave Ceramica produces no combustion, no VOCs, and no forced air movement.",
     "Schweizer Wohngebäude gehören zu den am besten gedichteten in Europa — ideal für Energieeffizienz, aber konzentrierend für Innenluftschadstoffe. SunWave Ceramica erzeugt keine Verbrennung, keine VOCs und keine Zwangslüftung."),
    ("No annual boiler service contract", "Kein jährlicher Kesseldienst-Vertrag"),
    ("No gas connection fixed charge", "Keine Gasanschluss-Grundgebühr"),
    ("No CO or NO₂ emissions indoors", "Keine CO- oder NO₂-Emissionen in Innenräumen"),
    ("Works with existing Swiss electrical circuits (no rewiring)",
     "Funktioniert mit bestehenden Schweizer Stromkreisen (kein Umverdrahten)"),
    ("Can be paired with solar PV for near-zero heating cost",
     "Kombinierbar mit Solar-PV für nahezu null Heizkosten"),
    ("Consumption figures from independent academic research. Your actual saving depends on current system, insulation, and local energy tariffs. Contact us",
     "Verbrauchszahlen aus unabhängiger akademischer Forschung. Ihre tatsächliche Einsparung hängt von aktuellem System, Dämmung und lokalen Energietarifen ab. Kontaktieren Sie uns"),
    ("for a personalised CHF estimate.", "für eine personalisierte CHF-Schätzung."),
    ("Installing SunWave Ceramica is simpler and faster than replacing a boiler — typically completed in a single day by a certified Swiss electrician.",
     "Die Installation von SunWave Ceramica ist einfacher und schneller als ein Kesselaustausch — in der Regel in einem Tag von einem zertifizierten Schweizer Elektriker abgeschlossen."),
    ("Use our online calculator to determine how many panels your home needs, or contact us and we'll calculate it for you based on your floor plan.",
     "Verwenden Sie unseren Online-Rechner, um zu bestimmen, wie viele Paneele Ihr Zuhause benötigt, oder kontaktieren Sie uns und wir berechnen es für Sie basierend auf Ihrem Grundriss."),
    ("Select from six Swiss-themed ceramic finishes to match your interior. All panels are the same 60×120 cm size with identical performance.",
     "Wählen Sie aus neun keramischen Designs, die zu Ihrem Interieur passen. Alle Paneele sind 60×120 cm groß mit identischer Leistung."),
    ("Order and delivery (3–5 working days)", "Bestellung und Lieferung (3–5 Werktage)"),
    ("Installation (plug-in or hardwired)", "Installation (Steckdose oder fest verdrahtet)"),
    ("Set the thermostat and enjoy", "Thermostat einstellen und genießen"),
    ("Find out exactly how much you'll save", "Erfahren Sie genau, wie viel Sie sparen"),
    ("Calculate My Savings", "Meine Einsparungen berechnen"),
    ("See the Panel", "Das Paneel ansehen"),
    ("Get a Quote", "Angebot anfordern"),

    # ── For-hotels page ───────────────────────────────────────────────────────
    ("Heating That Matches Your Guest Experience", "Heizung, die zu Ihrem Gästeerlebnis passt"),
    ("Infrared Heating for\n      Swiss Hotels", "Infrarotheizung für\n      Schweizer Hotels"),
    ("Why Hotels Are Switching to Infrared", "Warum Hotels auf Infrarot umsteigen"),
    ("Request a Hotel Quote", "Hotel-Angebot anfordern"),
    ("See Technical Specs", "Technische Spezifikationen ansehen"),
    ("Silent. No dust. No maintenance. Individual room control.",
     "Geräuschlos. Kein Staub. Keine Wartung. Individuelle Raumsteuerung."),

    # ── For-offices page ──────────────────────────────────────────────────────
    ("Heating Only the Zones People Actually Use", "Nur die genutzten Zonen beheizen"),
    ("Why Offices Choose Infrared", "Warum Büros Infrarot wählen"),
    ("Zone by zone. Silent. No maintenance.",
     "Zone für Zone. Geräuschlos. Keine Wartung."),

    # ── For-solar page ────────────────────────────────────────────────────────
    ("The Perfect Load for Your Solar Customers", "Die perfekte Last für Ihre Solar-Kunden"),
    ("Why Solar Installers Add Infrared", "Warum Solar-Installateure Infrarot ergänzen"),
    ("Pair infrared heating with your solar PV", "Kombinieren Sie Infrarotheizung mit Solar-PV"),

    # ── Blog ──────────────────────────────────────────────────────────────────
    ("Infrared Heating Insights", "Infrarotheizung — Wissen & Forschung"),
    ("SunWave Knowledge Base", "SunWave Wissensbasis"),
    ("Independent research, Swiss regulations, real energy numbers — everything you need to make an informed heating decision.",
     "Unabhängige Forschung, Schweizer Vorschriften, echte Energiezahlen — alles, was Sie für eine fundierte Heizenentscheidung benötigen."),
    ("Swiss Regulation", "Schweizer Vorschriften"),
    ("Energy Savings", "Energieeinsparung"),
    ("Product Science", "Produktwissenschaft"),
    ("Cost Analysis", "Kostenanalyse"),
    ("Read article →", "Artikel lesen →"),
    ("min read", "Min. Lesezeit"),
    ("May 2025", "Mai 2025"),
    ("April 2025", "April 2025"),
    ("March 2025", "März 2025"),
    ("February 2025", "Februar 2025"),
    ("January 2025", "Januar 2025"),

    # ── Navigation ────────────────────────────────────────────────────────────
    ("Hotels & Hospitality", "Hotels & Gastronomie"),
    ("Hotels &amp; Hospitality", "Hotels &amp; Gastronomie"),
    ("Offices & Commercial", "Büro & Gewerbe"),
    ("Offices &amp; Commercial", "Büro &amp; Gewerbe"),
    ("Swiss Homes", "Schweizer Haushalte"),
    ("Solar Installers", "Solar-Installateure"),
    ("The Panel", "Das Paneel"),
    ("Research", "Forschung"),
    ("Calculator", "Rechner"),
    ("Contact", "Kontakt"),
    ("Order Now", "Jetzt bestellen"),

    # ── Footer ────────────────────────────────────────────────────────────────
    ("Swiss distributor of SunWave Ceramica ceramic infrared heating panels. MuKEn-compliant. BSRIA-tested. Fraunhofer-certified.",
     "Schweizer Distributor von SunWave Ceramica Keramik-Infrarotheizpaneelen. MuKEn-konform. BSRIA-getestet. Fraunhofer-zertifiziert."),
    ("Delivering to all Swiss cantons.", "Lieferung in alle Schweizer Kantone."),
    ("Product", "Produkt"),
    ("Learn", "Wissen"),
    ("For", "Für"),
    ("Legal", "Rechtliches"),
    ("Design Variants", "Design-Varianten"),
    ("Full Specifications", "Vollständige Spezifikationen"),
    ("Research & Evidence", "Forschung & Belege"),
    ("Research &amp; Evidence", "Forschung &amp; Belege"),
    ("MuKEn Guide", "MuKEn-Leitfaden"),
    ("How Infrared Works", "Wie Infrarot funktioniert"),
    ("Savings Calculator", "Sparrechner"),
    ("Hotels", "Hotels"),
    ("Offices", "Büro"),
    ("Legal Notice", "Impressum"),
    ("Terms & Conditions", "AGB"),
    ("Terms &amp; Conditions", "AGB"),
    ("Returns Policy", "Rückgabebedingungen"),
    ("Shipping", "Lieferung"),
    ("Privacy Policy", "Datenschutz"),
    ("Blog", "Blog"),

    # Legal pages
    ("Impressum — Company information as required by Swiss law",
     "Impressum — Pflichtangaben gemäß Schweizer Recht"),
    ("Last updated: June 2026", "Zuletzt aktualisiert: Juni 2026"),
    ("General Terms and Conditions of Sale — Lumia Technologies GmbH",
     "Allgemeine Verkaufsbedingungen — Lumia Technologies GmbH"),
    ("30-day returns — no questions asked on undamaged, uninstalled panels",
     "30 Tage Rückgabe — kein Kommentar nötig bei unbeschädigten, nicht installierten Paneelen"),
    ("CHF 35 flat rate — all Swiss cantons — 3 to 5 working days",
     "CHF 35 Pauschale — alle Schweizer Kantone — 3 bis 5 Werktage"),
    ("How we collect, use, and protect your personal data — in accordance with Swiss nDSG",
     "Wie wir Ihre personenbezogenen Daten erheben, nutzen und schützen — gemäß Schweizer nDSG"),
    ("30-day return window", "30-tägiges Rückgabefenster"),
    ("Return Window", "Rückgabefenster"),
    ("Conditions for Return", "Rückgabebedingungen"),
    ("How to Return", "Rückgabeprozess"),
    ("Return Shipping Costs", "Rücksendekosten"),
    ("Faulty or incorrect item:", "Fehlerhafter oder falscher Artikel:"),
    ("Change of mind:", "Meinungsänderung:"),
    ("SunWave Switzerland covers return shipping costs in full.",
     "SunWave Switzerland übernimmt die Rücksendekosten vollständig."),
    ("Return shipping costs are borne by the customer.",
     "Die Rücksendekosten trägt der Kunde."),
    ("Faulty or Damaged Items", "Fehlerhafte oder beschädigte Artikel"),
    ("Order Cancellation", "Bestellstornierung"),
    ("Delivery cost", "Lieferkosten"),
    ("Delivery time", "Lieferzeit"),
    ("Coverage", "Abdeckung"),
    ("International", "International"),
    ("Dispatch", "Versand"),
    ("Damaged in Transit", "Beim Transport beschädigt"),
    ("Delays", "Verzögerungen"),
    ("Large & Multi-Panel Orders", "Große & Mehrpaneel-Bestellungen"),
    ("Large &amp; Multi-Panel Orders", "Große &amp; Mehrpaneel-Bestellungen"),
    ("Controller", "Verantwortlicher"),
    ("Legal Basis", "Rechtsgrundlage"),
    ("Data We Collect", "Erhobene Daten"),
    ("Purpose & Use of Data", "Zweck & Verwendung der Daten"),
    ("Purpose &amp; Use of Data", "Zweck &amp; Verwendung der Daten"),
    ("Google Fonts", "Google Fonts"),
    ("Data Retention", "Datenspeicherung"),
    ("Data Security", "Datensicherheit"),
    ("Your Rights", "Ihre Rechte"),
    ("Complaints", "Beschwerden"),
    ("Changes to this Policy", "Änderungen dieser Richtlinie"),

    # ── Cert tags ─────────────────────────────────────────────────────────────
    ("BSRIA Tested", "BSRIA Getestet"),
    ("MuKEn Ready", "MuKEn Konform"),
]

# ── Rebuild language switcher (proper mobile + desktop) ───────────────────────
SWITCHER_CSS = """<style>
    .nav__lang{display:flex;align-items:center;gap:2px;margin-left:10px}
    .nav__lang-btn{font-size:.68rem;font-weight:700;letter-spacing:.06em;color:rgba(255,255,255,.45);text-decoration:none;padding:3px 7px;border-radius:3px;border:1px solid rgba(255,255,255,.18);transition:all .2s;cursor:default}
    a.nav__lang-btn{cursor:pointer}
    .nav__lang-btn:hover,.nav__lang-btn.lang-active{color:var(--gold);border-color:var(--gold);background:rgba(245,197,24,.08)}
    .nav__lang-sep{color:rgba(255,255,255,.2);font-size:.7rem;padding:0 1px}
    .mobile-lang{display:flex;align-items:center;gap:6px;padding:12px 24px;border-top:1px solid rgba(255,255,255,.08);margin-top:8px}
    .mobile-lang a,.mobile-lang span{font-size:.8rem;font-weight:700;color:rgba(255,255,255,.5);text-decoration:none;padding:4px 10px;border-radius:4px;border:1px solid rgba(255,255,255,.15)}
    .mobile-lang a:hover,.mobile-lang .lang-active{color:var(--gold);border-color:var(--gold)}
  </style>"""

def build_switcher_de(slug, is_blog=False):
    """Desktop + mobile switcher for German pages."""
    if is_blog:
        en_href = f'../../blog/{slug}'
    elif slug == 'index.html':
        en_href = '../../index.html' if is_blog else '../index.html'
    else:
        en_href = f'../{slug}'

    desktop = f'''<div class="nav__lang">
      <a href="{en_href}" class="nav__lang-btn">EN</a>
      <span class="nav__lang-sep">|</span>
      <span class="nav__lang-btn lang-active">DE</span>
    </div>'''
    mobile = f'''<div class="mobile-lang">
      <a href="{en_href}">EN</a>
      <span class="lang-active">DE</span>
    </div>'''
    return desktop, mobile

def build_switcher_en(slug, is_blog=False):
    """Desktop + mobile switcher for English pages."""
    if is_blog:
        de_href = f'../de/blog/{slug}'
    else:
        de_href = f'de/{slug}'

    desktop = f'''<div class="nav__lang">
      <span class="nav__lang-btn lang-active">EN</span>
      <span class="nav__lang-sep">|</span>
      <a href="{de_href}" class="nav__lang-btn">DE</a>
    </div>'''
    mobile = f'''<div class="mobile-lang">
      <span class="lang-active">EN</span>
      <a href="{de_href}">DE</a>
    </div>'''
    return desktop, mobile

def inject_switcher(content, desktop_sw, mobile_sw):
    """Remove old switcher, inject new desktop + mobile switcher."""
    # Remove old switcher divs
    content = re.sub(r'\s*<div class="nav__lang">.*?</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'\s*<div class="mobile-lang">.*?</div>', '', content, flags=re.DOTALL)

    # Remove old switcher CSS
    content = re.sub(r'\s*<style>\s*\.nav__lang\{.*?</style>', '', content, flags=re.DOTALL)

    # Inject desktop switcher after Order Now button
    content = re.sub(
        r'(class="nav__order-btn">[^<]+</a>)',
        f'\\1\n      {desktop_sw}',
        content
    )

    # Inject mobile switcher before closing </nav>
    content = content.replace('</nav>', f'  {mobile_sw}\n</nav>')

    # Inject CSS before </head>
    content = content.replace('</head>', SWITCHER_CSS + '\n</head>')

    return content

# ── Process all German pages ──────────────────────────────────────────────────
de_files = [(f.replace('\\','/'), False) for f in glob.glob('de/*.html')]
de_files += [(f.replace('\\','/'), True) for f in glob.glob('de/blog/*.html')]

print('=== Translating German pages ===')
for path, is_blog in de_files:
    slug = os.path.basename(path)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Apply translations (text-node aware)
    content = replace_text_nodes(content, TRANS)

    # Fix switcher
    desktop_sw, mobile_sw = build_switcher_de(slug, is_blog)
    content = inject_switcher(content, desktop_sw, mobile_sw)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  Translated: {path}')

# ── Update English pages with proper switcher ────────────────────────────────
en_files = [(f.replace('\\','/'), False) for f in glob.glob('*.html') if not f.startswith('de')]
en_files += [(f.replace('\\','/'), True) for f in glob.glob('blog/*.html')]

print()
print('=== Updating English page switchers ===')
for path, is_blog in en_files:
    slug = os.path.basename(path)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    desktop_sw, mobile_sw = build_switcher_en(slug, is_blog)
    content = inject_switcher(content, desktop_sw, mobile_sw)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  Updated: {path}')

print()
print('All done.')
