<?php
// Bypass LiteSpeed cache and serve sitemap with correct headers
header('Content-Type: application/xml; charset=UTF-8');
header('Cache-Control: no-cache, no-store, must-revalidate');
header('X-LiteSpeed-Cache-Control: no-store');
header('X-Robots-Tag: noindex');
echo file_get_contents(__DIR__ . '/sitemap.xml');
