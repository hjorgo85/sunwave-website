import re, json, os
from datetime import date

BASE = 'https://sunwaveswitzerland.com'
TODAY = date.today().isoformat()

# ── Page definitions ────────────────────────────────────────────────────────
PAGES = {
    'index.html': {
        'title': 'SunWave Switzerland — Ceramic Infrared Heating Panels',
        'desc':  "One of Switzerland's most independently tested ceramic infrared heating panels. BSRIA, Fraunhofer WKI, TU Dresden and Labor S.A. certified. MuKEn compliant. CHF 35 delivery.",
        'url':   BASE + '/',
        'og_image': BASE + '/images/hero-banner-1.webp',
        'og_type': 'website',
        'schema': [
            {
                '@context': 'https://schema.org',
                '@type': 'Organization',
                'name': 'SunWave Switzerland',
                'alternateName': 'Lumia Technologies GmbH',
                'url': BASE,
                'logo': BASE + '/images/logo.webp',
                'telephone': '+41767637490',
                'email': 'info@sunwaveswitzerland.com',
                'address': {
                    '@type': 'PostalAddress',
                    'streetAddress': 'Glaserbergstrasse 27',
                    'addressLocality': 'Basel',
                    'postalCode': '4056',
                    'addressCountry': 'CH'
                },
                'contactPoint': {
                    '@type': 'ContactPoint',
                    'telephone': '+41767637490',
                    'contactType': 'sales',
                    'areaServed': 'CH',
                    'availableLanguage': ['English', 'German', 'French']
                },
                'sameAs': ['https://sunwaveswitzerland.com']
            },
            {
                '@context': 'https://schema.org',
                '@type': 'FAQPage',
                'mainEntity': [
                    {
                        '@type': 'Question',
                        'name': 'Is infrared heating MuKEn-compliant in Switzerland?',
                        'acceptedAnswer': {
                            '@type': 'Answer',
                            'text': 'Electric infrared panels produce zero on-site combustion and operate on Switzerland\'s ~90% low-carbon electricity grid. They qualify as a compliant fossil fuel heating replacement under MuKEn 2014 Article 4.1 in all cantons that have adopted the provision — including Zurich, Bern, Basel, Vaud, and Aargau. No planning permission required in most cases.'
                        }
                    },
                    {
                        '@type': 'Question',
                        'name': 'How quickly can my boiler be replaced with infrared panels?',
                        'acceptedAnswer': {
                            '@type': 'Answer',
                            'text': 'SunWave Ceramica panels ship to all Swiss cantons with delivery in 3–5 working days. Panels connecting to standard sockets can be installed the same day they arrive — no electrician required for socket-connected panels. Hardwired installation requires a NIV-authorised electrician (typically 1 day).'
                        }
                    },
                    {
                        '@type': 'Question',
                        'name': 'What is the warranty on SunWave Ceramica panels?',
                        'acceptedAnswer': {
                            '@type': 'Answer',
                            'text': '5 years full manufacturer\'s warranty. The ceramic surface does not degrade — there are no moving parts, no filters, no gas components. The BSRIA 98-day continuous test confirmed stable performance with no output degradation throughout.'
                        }
                    },
                    {
                        '@type': 'Question',
                        'name': 'Can I use infrared panels in a rented apartment in Switzerland?',
                        'acceptedAnswer': {
                            '@type': 'Answer',
                            'text': 'Yes. Panels connecting to standard sockets do not require modification to the building and typically do not require landlord consent under Swiss tenancy law. They can be removed on departure with no permanent damage — mounting holes only.'
                        }
                    },
                    {
                        '@type': 'Question',
                        'name': 'Are the panels safe for children and allergy sufferers?',
                        'acceptedAnswer': {
                            '@type': 'Answer',
                            'text': 'Fraunhofer WKI certified VOC emissions at 0.043 mg/m³ TVOC — 23× below the limit. No combustion products. No forced air movement (no dust recirculation). The ceramic surface is chemically inert. Install on the upper wall out of direct reach of small children.'
                        }
                    }
                ]
            }
        ]
    },
    'product.html': {
        'title': 'SunWave Ceramica Infrared Panel | SunWave Switzerland',
        'desc':  'SunWave Ceramica: 650W ceramic infrared heating panel. BSRIA, TU Dresden, Fraunhofer WKI and Labor S.A. tested. Nine Swiss design finishes. CHF 490 incl. thermostat. Ships in 3–5 days.',
        'url':   BASE + '/product.html',
        'og_image': BASE + '/images/panel-imperial-marble.webp',
        'og_type': 'product',
        'schema': [
            {
                '@context': 'https://schema.org',
                '@type': 'Product',
                'name': 'SunWave Ceramica Infrared Heating Panel',
                'description': '650W ceramic infrared heating panel in 6mm fine porcelain stoneware. Independently tested by BSRIA, TU Dresden, Fraunhofer WKI and Labor S.A. Nine surface finishes. WiFi thermostat included.',
                'brand': {'@type': 'Brand', 'name': 'SunWave'},
                'image': BASE + '/images/panel-imperial-marble.webp',
                'sku': 'IR-PHP-D1',
                'mpn': 'IR-PHP-D1',
                'material': '6mm fine porcelain stoneware',
                'color': 'Imperial Marble, Alpine White, Tuscan Sand, Nordic Slate, Sandstone Edge, Desert Flow, Ivory Cloud, Walnut Stone, Timber Stone',
                'width': {'@type': 'QuantitativeValue', 'value': 120, 'unitCode': 'CMT'},
                'height': {'@type': 'QuantitativeValue', 'value': 60, 'unitCode': 'CMT'},
                'weight': {'@type': 'QuantitativeValue', 'value': 15, 'unitCode': 'KGM'},
                'offers': {
                    '@type': 'Offer',
                    'price': '490',
                    'priceCurrency': 'CHF',
                    'availability': 'https://schema.org/InStock',
                    'shippingDetails': {
                        '@type': 'OfferShippingDetails',
                        'shippingRate': {'@type': 'MonetaryAmount', 'value': '35', 'currency': 'CHF'},
                        'deliveryTime': {'@type': 'ShippingDeliveryTime', 'businessDays': {'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday','Tuesday','Wednesday','Thursday','Friday'], 'opens': '08:00', 'closes': '17:00'}, 'handlingTime': {'@type': 'QuantitativeValue', 'minValue': 1, 'maxValue': 2, 'unitCode': 'DAY'}, 'transitTime': {'@type': 'QuantitativeValue', 'minValue': 3, 'maxValue': 5, 'unitCode': 'DAY'}},
                        'shippingDestination': {'@type': 'DefinedRegion', 'addressCountry': 'CH'}
                    },
                    'hasMerchantReturnPolicy': {
                        '@type': 'MerchantReturnPolicy',
                        'returnPolicyCategory': 'https://schema.org/MerchantReturnFiniteReturnWindow',
                        'merchantReturnDays': 30,
                        'returnMethod': 'https://schema.org/ReturnByMail',
                        'returnFees': 'https://schema.org/FreeReturn'
                    },
                    'seller': {'@type': 'Organization', 'name': 'Lumia Technologies GmbH'}
                },
                'warranty': '5 years full manufacturer warranty'
            }
        ]
    },
    'research.html': {
        'title': 'Independent Test Reports | SunWave Ceramica',
        'desc':  '4 independent lab tests: BSRIA Report 105350/1, TU Dresden DIN EN IEC 60675-3, Fraunhofer WKI MAIC-2022-2428, and Labor S.A. EN 60335-2-30. Every claim independently verified.',
        'url':   BASE + '/research.html',
        'og_image': BASE + '/images/logo-bsria.webp',
        'og_type': 'website',
        'schema': [{'@context':'https://schema.org','@type':'WebPage','name':'Independent Test Reports — SunWave Ceramica','description':'4 independent laboratory test reports verifying the performance, safety and air quality of SunWave Ceramica infrared heating panels.','url': BASE+'/research.html','publisher':{'@type':'Organization','name':'SunWave Switzerland','url':BASE}}]
    },
    'contact.html': {
        'title': 'Contact SunWave Switzerland — Get a Free Quote',
        'desc':  'Request a personalised infrared heating quote for your Swiss home, hotel or office. Panel count, annual saving estimate, and payback period — sent within 24 hours.',
        'url':   BASE + '/contact.html',
        'og_image': BASE + '/images/hero-banner-1.webp',
        'og_type': 'website',
        'schema': [{'@context':'https://schema.org','@type':'ContactPage','name':'Contact SunWave Switzerland','url':BASE+'/contact.html','description':'Request a free personalised heating quote from SunWave Switzerland.'}]
    },
    'for-homes.html': {
        'title': 'Infrared Heating for Swiss Homes | SunWave Switzerland',
        'desc':  'Replace your gas boiler with SunWave Ceramica infrared panels. MuKEn 2014 compliant, 66% less energy than gas, zero maintenance, 30-year lifespan. Free savings estimate for Swiss homeowners.',
        'url':   BASE + '/for-homes.html',
        'og_image': BASE + '/images/homes-family-comfort.webp',
        'og_type': 'website',
        'schema': [{'@context':'https://schema.org','@type':'WebPage','name':'Infrared Heating for Swiss Homes','url':BASE+'/for-homes.html','description':'Replace your gas boiler with SunWave Ceramica infrared panels. MuKEn compliant, 66% less energy than gas.'}]
    },
    'for-hotels.html': {
        'title': 'Infrared Heating for Hotels | SunWave Switzerland',
        'desc':  'Silent ceramic infrared heating for Swiss hotels and chalets. No fan noise, no dust, individual room control, nine designer finishes. Up to 66% less energy than gas central heating.',
        'url':   BASE + '/for-hotels.html',
        'og_image': BASE + '/images/hotels-luxury-suite.webp',
        'og_type': 'website',
        'schema': [{'@context':'https://schema.org','@type':'WebPage','name':'Infrared Heating for Swiss Hotels','url':BASE+'/for-hotels.html','description':'Silent ceramic infrared heating for Swiss hotels. No fan noise, individual room control, designer finishes.'}]
    },
    'for-offices.html': {
        'title': 'Infrared Heating for Swiss Offices | SunWave Switzerland',
        'desc':  'Zone heating for Swiss offices and commercial spaces. Heat only occupied areas, zero dust circulation, 66% less energy vs gas, no boiler maintenance. Payback under 3 years.',
        'url':   BASE + '/for-offices.html',
        'og_image': BASE + '/images/offices-open-plan.webp',
        'og_type': 'website',
        'schema': [{'@context':'https://schema.org','@type':'WebPage','name':'Infrared Heating for Swiss Offices','url':BASE+'/for-offices.html','description':'Zone heating for Swiss offices. Heat only occupied areas, zero dust, 66% less energy than gas.'}]
    },
    'for-solar.html': {
        'title': 'Infrared Heating for Solar Installers | SunWave Switzerland',
        'desc':  'Pair SunWave Ceramica infrared panels with your PV installations. 650W load matches solar output, thermal mass storage, 66% energy reduction vs gas. MuKEn-compliant solar-heat package.',
        'url':   BASE + '/for-solar.html',
        'og_image': BASE + '/images/solar-rooftop-swiss.webp',
        'og_type': 'website',
        'schema': [{'@context':'https://schema.org','@type':'WebPage','name':'Infrared Heating for Swiss Solar Installers','url':BASE+'/for-solar.html','description':'Pair SunWave Ceramica with PV. 650W load, thermal mass storage, MuKEn compliant.'}]
    },
    'legal.html': {
        'title': 'Legal Notice | SunWave Switzerland — Lumia Technologies GmbH',
        'desc':  'Legal notice (Impressum) for SunWave Switzerland, operated by Lumia Technologies GmbH, Glaserbergstrasse 27, 4056 Basel. UID CHE-204.700.764. Swiss law. Jurisdiction: Basel-Stadt.',
        'url':   BASE + '/legal.html',
        'og_image': BASE + '/images/logo.webp',
        'og_type': 'website',
        'schema': [{'@context':'https://schema.org','@type':'WebPage','name':'Legal Notice — SunWave Switzerland','url':BASE+'/legal.html'}]
    },
    'terms.html': {
        'title': 'Terms & Conditions | SunWave Switzerland',
        'desc':  'General terms and conditions of sale for SunWave Ceramica infrared heating panels. 30-day returns, 5-year warranty, CHF 35 Swiss delivery, 3–5 day dispatch. Governed by Swiss law.',
        'url':   BASE + '/terms.html',
        'og_image': BASE + '/images/logo.webp',
        'og_type': 'website',
        'schema': [{'@context':'https://schema.org','@type':'WebPage','name':'Terms & Conditions — SunWave Switzerland','url':BASE+'/terms.html'}]
    },
    'returns.html': {
        'title': 'Returns Policy | SunWave Switzerland',
        'desc':  '30-day no-questions-asked return policy for SunWave Ceramica panels. Free return on faulty items. Full refund within 14 days. Panels must be uninstalled and in original packaging.',
        'url':   BASE + '/returns.html',
        'og_image': BASE + '/images/logo.webp',
        'og_type': 'website',
        'schema': [{'@context':'https://schema.org','@type':'WebPage','name':'Returns Policy — SunWave Switzerland','url':BASE+'/returns.html'}]
    },
    'shipping.html': {
        'title': 'Shipping & Delivery | SunWave Switzerland',
        'desc':  'CHF 35 flat-rate delivery to all Swiss cantons. SunWave Ceramica panels dispatched within 1–2 working days, delivered in 3–5 working days. Tracked shipping. Damage covered.',
        'url':   BASE + '/shipping.html',
        'og_image': BASE + '/images/logo.webp',
        'og_type': 'website',
        'schema': [{'@context':'https://schema.org','@type':'WebPage','name':'Shipping & Delivery — SunWave Switzerland','url':BASE+'/shipping.html'}]
    },
    'privacy.html': {
        'title': 'Privacy Policy | SunWave Switzerland',
        'desc':  'Privacy policy for sunwaveswitzerland.com. How Lumia Technologies GmbH collects and protects your data under Swiss nDSG law. No tracking cookies. No third-party data sharing.',
        'url':   BASE + '/privacy.html',
        'og_image': BASE + '/images/logo.webp',
        'og_type': 'website',
        'schema': [{'@context':'https://schema.org','@type':'WebPage','name':'Privacy Policy — SunWave Switzerland','url':BASE+'/privacy.html'}]
    },
    'blog/index.html': {
        'title': 'Infrared Heating Blog | SunWave Switzerland',
        'desc':  'Expert articles on infrared heating in Switzerland: MuKEn 2014 compliance, solar PV pairing, independent lab test results, and gas vs infrared cost comparisons.',
        'url':   BASE + '/blog/',
        'og_image': BASE + '/images/hero-banner-2.webp',
        'og_type': 'website',
        'schema': [{'@context':'https://schema.org','@type':'Blog','name':'SunWave Switzerland — Infrared Heating Blog','url':BASE+'/blog/','publisher':{'@type':'Organization','name':'SunWave Switzerland','url':BASE}}]
    },
    'blog/muken-2014-boiler-replacement-switzerland.html': {
        'title': "MuKEn 2014: Switzerland's Gas Boiler Replacement Law",
        'desc':  "MuKEn 2014 Article 4.1 requires end-of-life gas boilers to be replaced with renewable heating in Switzerland. Which cantons apply the rule and why infrared panels qualify as compliant replacements.",
        'url':   BASE + '/blog/muken-2014-boiler-replacement-switzerland.html',
        'og_image': BASE + '/images/hero-banner-3.webp',
        'og_type': 'article',
        'schema': [{'@context':'https://schema.org','@type':'BlogPosting','headline':"MuKEn 2014: Switzerland's Gas Boiler Replacement Law Explained",'datePublished':'2025-05-01','author':{'@type':'Organization','name':'SunWave Switzerland'},'publisher':{'@type':'Organization','name':'SunWave Switzerland','logo':{'@type':'ImageObject','url':BASE+'/images/logo.webp'}},'url':BASE+'/blog/muken-2014-boiler-replacement-switzerland.html','description':"Switzerland's MuKEn 2014 Article 4.1 requires end-of-life gas boilers to be replaced with renewable heating."}]
    },
    'blog/solar-infrared-heating-switzerland.html': {
        'title': 'Solar + Infrared Heating Switzerland | SunWave Switzerland',
        'desc':  'Why Swiss solar installers pair SunWave Ceramica infrared panels with PV systems. Load-matching, self-consumption uplift, thermal mass explained. The perfect MuKEn-compliant solar-heat package.',
        'url':   BASE + '/blog/solar-infrared-heating-switzerland.html',
        'og_image': BASE + '/images/solar-rooftop-swiss.webp',
        'og_type': 'article',
        'schema': [{'@context':'https://schema.org','@type':'BlogPosting','headline':'Solar + Infrared Heating in Switzerland: The Perfect PV Load','datePublished':'2025-04-01','author':{'@type':'Organization','name':'SunWave Switzerland'},'publisher':{'@type':'Organization','name':'SunWave Switzerland','logo':{'@type':'ImageObject','url':BASE+'/images/logo.webp'}},'url':BASE+'/blog/solar-infrared-heating-switzerland.html'}]
    },
    'blog/tu-dresden-infrared-test-results.html': {
        'title': 'TU Dresden DIN EN IEC 60675-3 Infrared Test Results',
        'desc':  'TU Dresden tested SunWave Ceramica to DIN EN IEC 60675-3 — the European infrared heater standard. Radiation efficiency, peak wavelength 8.52μm, and what the results mean for your heating.',
        'url':   BASE + '/blog/tu-dresden-infrared-test-results.html',
        'og_image': BASE + '/images/logo-tu-dresden.webp',
        'og_type': 'article',
        'schema': [{'@context':'https://schema.org','@type':'BlogPosting','headline':'TU Dresden DIN EN IEC 60675-3 Test: What the Results Mean','datePublished':'2025-03-01','author':{'@type':'Organization','name':'SunWave Switzerland'},'publisher':{'@type':'Organization','name':'SunWave Switzerland','logo':{'@type':'ImageObject','url':BASE+'/images/logo.webp'}},'url':BASE+'/blog/tu-dresden-infrared-test-results.html'}]
    },
    'blog/ceramic-vs-aluminium-infrared-panels.html': {
        'title': 'Ceramic vs Aluminium Infrared Panels | SunWave Switzerland',
        'desc':  'Fraunhofer WKI tested ceramic infrared panels: 0.043 mg/m³ TVOC — 23× below the limit. Why ceramic outperforms aluminium for indoor air quality, thermal mass, and longevity.',
        'url':   BASE + '/blog/ceramic-vs-aluminium-infrared-panels.html',
        'og_image': BASE + '/images/logo-fraunhofer.webp',
        'og_type': 'article',
        'schema': [{'@context':'https://schema.org','@type':'BlogPosting','headline':'Ceramic vs Aluminium Infrared Panels: The Fraunhofer WKI Study Explained','datePublished':'2025-02-01','author':{'@type':'Organization','name':'SunWave Switzerland'},'publisher':{'@type':'Organization','name':'SunWave Switzerland','logo':{'@type':'ImageObject','url':BASE+'/images/logo.webp'}},'url':BASE+'/blog/ceramic-vs-aluminium-infrared-panels.html'}]
    },
    'blog/gas-vs-infrared-heating-cost-switzerland.html': {
        'title': 'Gas vs Infrared Heating Cost in Switzerland 2025',
        'desc':  'Full cost comparison: gas heating vs SunWave Ceramica infrared in Switzerland. Capital cost, running cost, and payback using independent academic research and 2025 Swiss energy prices.',
        'url':   BASE + '/blog/gas-vs-infrared-heating-cost-switzerland.html',
        'og_image': BASE + '/images/hero-banner-1.webp',
        'og_type': 'article',
        'schema': [{'@context':'https://schema.org','@type':'BlogPosting','headline':'Gas vs Infrared Heating in Switzerland: A Full Cost Breakdown for 2025','datePublished':'2025-01-01','author':{'@type':'Organization','name':'SunWave Switzerland'},'publisher':{'@type':'Organization','name':'SunWave Switzerland','logo':{'@type':'ImageObject','url':BASE+'/images/logo.webp'}},'url':BASE+'/blog/gas-vs-infrared-heating-cost-switzerland.html'}]
    },
}

ORG_SCHEMA = {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    'name': 'SunWave Switzerland',
    'alternateName': 'Lumia Technologies GmbH',
    'url': BASE,
    'logo': BASE + '/images/logo.webp',
    'telephone': '+41767637490',
    'email': 'info@sunwaveswitzerland.com',
    'address': {
        '@type': 'PostalAddress',
        'streetAddress': 'Glaserbergstrasse 27',
        'addressLocality': 'Basel',
        'postalCode': '4056',
        'addressCountry': 'CH'
    }
}

def build_head_injection(page_key, data):
    is_blog = page_key.startswith('blog/')
    url = data['url']
    title = data['title']
    desc = data['desc']
    og_image = data['og_image']
    og_type = data['og_type']
    schemas = data.get('schema', [])

    # Add org schema to all pages except index (which has it)
    if page_key != 'index.html':
        schemas = [ORG_SCHEMA] + schemas

    schema_tags = '\n'.join(
        f'  <script type="application/ld+json">\n  {json.dumps(s, ensure_ascii=False, indent=2)}\n  </script>'
        for s in schemas
    )

    return f'''  <link rel="canonical" href="{url}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:type" content="{og_type}">
  <meta property="og:image" content="{og_image}">
  <meta property="og:site_name" content="SunWave Switzerland">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{og_image}">
{schema_tags}'''

def update_file(fname, page_key, data):
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix title
    content = re.sub(r'<title>.*?</title>', f'<title>{data["title"]}</title>', content)

    # Fix meta description
    content = re.sub(
        r'<meta name="description"\s+content="[^"]*">',
        f'<meta name="description" content="{data["desc"]}">',
        content
    )

    # Remove existing canonical/og/twitter/schema tags to avoid duplicates
    content = re.sub(r'\s*<link rel="canonical"[^>]*>', '', content)
    content = re.sub(r'\s*<meta property="og:[^"]*"[^>]*>', '', content)
    content = re.sub(r'\s*<meta name="twitter:[^"]*"[^>]*>', '', content)
    content = re.sub(r'\s*<script type="application/ld\+json">.*?</script>', '', content, flags=re.DOTALL)

    # Inject before </head>
    injection = build_head_injection(page_key, data)
    content = content.replace('</head>', injection + '\n</head>')

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Updated: {fname}')

# ── Run ──────────────────────────────────────────────────────────────────────
for page_key, data in PAGES.items():
    update_file(page_key, page_key, data)

# ── sitemap.xml ──────────────────────────────────────────────────────────────
sitemap_urls = [
    (BASE + '/', '1.0', 'weekly'),
    (BASE + '/product.html', '0.9', 'monthly'),
    (BASE + '/research.html', '0.9', 'monthly'),
    (BASE + '/contact.html', '0.8', 'monthly'),
    (BASE + '/for-homes.html', '0.8', 'monthly'),
    (BASE + '/for-hotels.html', '0.8', 'monthly'),
    (BASE + '/for-offices.html', '0.8', 'monthly'),
    (BASE + '/for-solar.html', '0.8', 'monthly'),
    (BASE + '/blog/', '0.7', 'weekly'),
    (BASE + '/blog/muken-2014-boiler-replacement-switzerland.html', '0.7', 'monthly'),
    (BASE + '/blog/solar-infrared-heating-switzerland.html', '0.7', 'monthly'),
    (BASE + '/blog/tu-dresden-infrared-test-results.html', '0.7', 'monthly'),
    (BASE + '/blog/ceramic-vs-aluminium-infrared-panels.html', '0.7', 'monthly'),
    (BASE + '/blog/gas-vs-infrared-heating-cost-switzerland.html', '0.7', 'monthly'),
    (BASE + '/legal.html', '0.3', 'yearly'),
    (BASE + '/terms.html', '0.3', 'yearly'),
    (BASE + '/returns.html', '0.4', 'yearly'),
    (BASE + '/shipping.html', '0.4', 'yearly'),
    (BASE + '/privacy.html', '0.3', 'yearly'),
]

sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for url, priority, freq in sitemap_urls:
    sitemap += f'  <url>\n    <loc>{url}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>{freq}</changefreq>\n    <priority>{priority}</priority>\n  </url>\n'
sitemap += '</urlset>'

with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(sitemap)
print('Created: sitemap.xml')

# ── robots.txt ───────────────────────────────────────────────────────────────
robots = f"""User-agent: *
Allow: /

Sitemap: {BASE}/sitemap.xml
"""
with open('robots.txt', 'w', encoding='utf-8') as f:
    f.write(robots)
print('Created: robots.txt')

print('\nDone. All pages updated with canonical, OG, schema, sitemap and robots.txt.')
