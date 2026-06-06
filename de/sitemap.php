<?php
header('Content-Type: application/xml; charset=UTF-8');
header('Cache-Control: no-cache, no-store, must-revalidate');
header('X-LiteSpeed-Cache-Control: no-store');
$today = date('Y-m-d');
$base = 'https://sunwaveswitzerland.com/de';
$pages = [
    ['/', '1.0', 'weekly'],
    ['/product.html', '0.9', 'monthly'],
    ['/research.html', '0.9', 'monthly'],
    ['/contact.html', '0.8', 'monthly'],
    ['/for-homes.html', '0.8', 'monthly'],
    ['/for-hotels.html', '0.8', 'monthly'],
    ['/for-offices.html', '0.8', 'monthly'],
    ['/for-solar.html', '0.8', 'monthly'],
    ['/blog/', '0.7', 'weekly'],
    ['/blog/infrarotheizung-schweiz-ratgeber.html', '0.8', 'monthly'],
    ['/blog/elektroheizung-verbot-schweiz.html', '0.8', 'monthly'],
    ['/blog/gasheizung-ersetzen-schweiz.html', '0.8', 'monthly'],
    ['/blog/infrarotheizung-decke-schweiz.html', '0.8', 'monthly'],
    ['/blog/infrarotheizung-badezimmer-schweiz.html', '0.8', 'monthly'],
    ['/blog/muken-2014-boiler-replacement-switzerland.html', '0.7', 'monthly'],
    ['/blog/solar-infrared-heating-switzerland.html', '0.7', 'monthly'],
    ['/blog/tu-dresden-infrared-test-results.html', '0.7', 'monthly'],
    ['/blog/ceramic-vs-aluminium-infrared-panels.html', '0.7', 'monthly'],
    ['/blog/gas-vs-infrared-heating-cost-switzerland.html', '0.7', 'monthly'],
    ['/legal.html', '0.3', 'yearly'],
    ['/terms.html', '0.3', 'yearly'],
    ['/returns.html', '0.4', 'yearly'],
    ['/shipping.html', '0.4', 'yearly'],
    ['/privacy.html', '0.3', 'yearly'],
];
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
foreach ($pages as $p) {
    echo "  <url>\n";
    echo "    <loc>{$base}{$p[0]}</loc>\n";
    echo "    <lastmod>{$today}</lastmod>\n";
    echo "    <changefreq>{$p[2]}</changefreq>\n";
    echo "    <priority>{$p[1]}</priority>\n";
    echo "  </url>\n";
}
echo '</urlset>';
