<?php
session_start();

// ── API key: loaded from outside the web root (never in git) ─────────────
$mollie_key = null;
$key_file = dirname($_SERVER['DOCUMENT_ROOT']) . '/mollie_key.php';
if (file_exists($key_file)) include $key_file; // sets $mollie_key

// ── Mollie API helper ─────────────────────────────────────────────────────
function mollie_post($key, $data) {
    $ch = curl_init('https://api.mollie.com/v2/payments');
    curl_setopt_array($ch, [
        CURLOPT_HTTPHEADER     => ['Authorization: Bearer '.$key, 'Content-Type: application/json'],
        CURLOPT_POST           => true,
        CURLOPT_POSTFIELDS     => json_encode($data),
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT        => 20,
    ]);
    $r = curl_exec($ch);
    curl_close($ch);
    return json_decode($r, true) ?: [];
}

// ── Handle POST: create payment ───────────────────────────────────────────
$post_error = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!$mollie_key) {
        $post_error = 'Payment system not yet configured. Please email info@sunwaveswitzerland.com to order.';
    } else {
        $name    = trim($_POST['name']    ?? '');
        $email   = trim($_POST['email']   ?? '');
        $phone   = trim($_POST['phone']   ?? '');
        $address = trim($_POST['address'] ?? '');
        $city    = trim($_POST['city']    ?? '');
        $postal  = trim($_POST['postal']  ?? '');
        $canton  = trim($_POST['canton']  ?? '');
        $finish  = trim($_POST['finish']  ?? 'Imperial Marble');
        $qty     = max(1, min(50, intval($_POST['qty'] ?? 1)));
        $lang    = ($_POST['lang'] ?? 'en') === 'de' ? 'de' : 'en';

        if (!$name || !filter_var($email, FILTER_VALIDATE_EMAIL) || !$address || !$city || !$postal || !$canton) {
            $post_error = $lang === 'de'
                ? 'Bitte füllen Sie alle Pflichtfelder aus.'
                : 'Please fill in all required fields.';
        } else {
            $subtotal  = 550 * $qty;
            $shipping  = 35;
            $total     = $subtotal + $shipping;
            $order_id  = 'SW-' . date('Ymd') . '-' . strtoupper(substr(uniqid(), -5));
            $base      = 'https://sunwaveswitzerland.com';

            $payment = mollie_post($mollie_key, [
                'amount'      => ['currency' => 'CHF', 'value' => number_format($total, 2, '.', '')],
                'description' => 'SunWave Ceramica ×' . $qty . ' (' . $finish . ')',
                'redirectUrl' => $base . '/payment-return.php?order=' . urlencode($order_id) . '&lang=' . $lang,
                'webhookUrl'  => $base . '/mollie-webhook.php',
                'locale'      => $lang === 'de' ? 'de_CH' : 'en_US',
                'metadata'    => compact('order_id','name','email','phone','address','city','postal','canton','finish','qty','lang'),
            ]);

            if (!empty($payment['_links']['checkout']['href'])) {
                $_SESSION['sw_order_' . $order_id] = [
                    'name'       => $name,
                    'email'      => $email,
                    'finish'     => $finish,
                    'qty'        => $qty,
                    'total'      => $total,
                    'order_id'   => $order_id,
                    'payment_id' => $payment['id'],
                ];
                header('Location: ' . $payment['_links']['checkout']['href']);
                exit;
            } else {
                $post_error = $lang === 'de'
                    ? 'Fehler beim Erstellen der Zahlung. Bitte versuchen Sie es erneut.'
                    : 'Payment creation failed. Please try again.';
            }
        }
    }
}

// ── GET parameters ─────────────────────────────────────────────────────────
$qty    = max(1, min(50, intval($_GET['qty'] ?? $_POST['qty'] ?? 1)));
$finish = htmlspecialchars($_GET['finish'] ?? $_POST['finish'] ?? 'Imperial Marble', ENT_QUOTES);
$lang   = (($_GET['lang'] ?? $_POST['lang'] ?? 'en') === 'de') ? 'de' : 'en';
$is_de  = ($lang === 'de');

$subtotal = 550 * $qty;
$shipping = 35;
$total    = $subtotal + $shipping;

$product_url  = $is_de ? 'de/product.html'  : 'product.html';
$logo_url     = 'images/logo.webp';
$css_url      = 'css/style.css';

$txt = $is_de ? [
    'page_title'  => 'Bestellung — SunWave Switzerland',
    'heading'     => 'Zur Kasse',
    'contact_h'   => 'Kontaktdaten',
    'f_name'      => 'Vor- und Nachname *',
    'f_email'     => 'E-Mail-Adresse *',
    'f_phone'     => 'Telefon',
    'delivery_h'  => 'Lieferadresse',
    'f_address'   => 'Strasse und Hausnummer *',
    'f_city'      => 'Ort *',
    'f_postal'    => 'Postleitzahl *',
    'f_canton'    => 'Kanton *',
    'order_h'     => 'Bestellübersicht',
    'product_lbl' => 'SunWave Ceramica',
    'finish_lbl'  => 'Oberfläche',
    'qty_lbl'     => 'Anzahl',
    'subtotal'    => 'Zwischensumme',
    'delivery'    => 'Lieferung (Swiss Post)',
    'total'       => 'Total (inkl. MwSt.)',
    'pay_btn'     => 'Jetzt bezahlen →',
    'secure'      => 'Sichere Zahlung via Mollie',
    'methods'     => 'TWINT · PostFinance · Visa · Mastercard · Apple Pay',
    'back'        => '← Zurück zum Produkt',
    'incl_thermo' => 'inkl. WLAN-Thermostat · 5 Jahre Garantie',
    'per_panel'   => 'CHF 550 × ' . $qty,
] : [
    'page_title'  => 'Checkout — SunWave Switzerland',
    'heading'     => 'Checkout',
    'contact_h'   => 'Contact details',
    'f_name'      => 'Full name *',
    'f_email'     => 'Email address *',
    'f_phone'     => 'Phone number',
    'delivery_h'  => 'Delivery address',
    'f_address'   => 'Street address *',
    'f_city'      => 'City *',
    'f_postal'    => 'Postal code *',
    'f_canton'    => 'Canton *',
    'order_h'     => 'Order summary',
    'product_lbl' => 'SunWave Ceramica',
    'finish_lbl'  => 'Finish',
    'qty_lbl'     => 'Quantity',
    'subtotal'    => 'Subtotal',
    'delivery'    => 'Delivery (Swiss Post)',
    'total'       => 'Total (incl. VAT)',
    'pay_btn'     => 'Pay now →',
    'secure'      => 'Secure payment via Mollie',
    'methods'     => 'TWINT · PostFinance · Visa · Mastercard · Apple Pay',
    'back'        => '← Back to product',
    'incl_thermo' => 'incl. WiFi thermostat · 5-year warranty',
    'per_panel'   => 'CHF 550 × ' . $qty,
];
?>
<!DOCTYPE html>
<html lang="<?= $lang ?>">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title><?= $txt['page_title'] ?></title>
  <meta name="robots" content="noindex">
  <link rel="icon" type="image/png" href="<?= $logo_url ?>">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="<?= $css_url ?>">
  <style>
    .ck-wrap { max-width:960px; margin:0 auto; padding:40px 24px 80px; display:grid; grid-template-columns:1fr 380px; gap:40px; align-items:start; }
    @media(max-width:700px){ .ck-wrap{ grid-template-columns:1fr; } .ck-summary{ order:-1; } }
    .ck-form-box { background:#fff; border:1px solid #e8e3db; border-radius:8px; padding:32px; }
    .ck-form-box h2 { font-size:1rem; font-weight:700; letter-spacing:0.06em; text-transform:uppercase; color:#888; margin:0 0 20px; }
    .ck-form-box h2:not(:first-child) { margin-top:32px; }
    .ck-field { display:flex; flex-direction:column; gap:6px; margin-bottom:16px; }
    .ck-field label { font-size:0.82rem; font-weight:600; color:#444; }
    .ck-field input, .ck-field select { padding:11px 14px; border:1.5px solid #ddd; border-radius:4px; font-family:inherit; font-size:0.9rem; color:#1a1a24; transition:border-color .2s; }
    .ck-field input:focus, .ck-field select:focus { outline:none; border-color:#1a1a24; }
    .ck-row2 { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
    .ck-summary { background:#f8f7f4; border:1px solid #e8e3db; border-radius:8px; padding:28px; position:sticky; top:84px; }
    .ck-summary h3 { font-size:0.82rem; font-weight:700; letter-spacing:0.06em; text-transform:uppercase; color:#888; margin:0 0 20px; }
    .ck-prod-name { font-size:1.1rem; font-weight:700; color:#1a1a24; margin-bottom:4px; }
    .ck-prod-sub { font-size:0.78rem; color:#888; margin-bottom:20px; }
    .ck-line { display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid #ebe7e0; font-size:0.88rem; color:#555; }
    .ck-line:last-of-type { border-bottom:none; }
    .ck-total { display:flex; justify-content:space-between; align-items:center; margin-top:16px; padding-top:16px; border-top:2px solid #1a1a24; font-weight:800; font-size:1.1rem; color:#1a1a24; }
    .ck-pay-btn { display:block; width:100%; padding:16px; background:var(--gold); color:#1a1a24; border:none; border-radius:4px; font-family:inherit; font-size:1rem; font-weight:800; cursor:pointer; margin-top:20px; transition:background .2s, transform .15s; letter-spacing:0.01em; }
    .ck-pay-btn:hover { background:#e8c030; transform:translateY(-1px); }
    .ck-secure { text-align:center; font-size:0.75rem; color:#888; margin-top:10px; }
    .ck-methods { text-align:center; font-size:0.72rem; color:#aaa; margin-top:4px; }
    .ck-back { display:inline-block; font-size:0.82rem; color:#888; text-decoration:none; margin-bottom:24px; }
    .ck-back:hover { color:#1a1a24; }
    .ck-error { background:#fee; border:1px solid #f99; border-radius:4px; padding:12px 16px; color:#c00; font-size:0.85rem; margin-bottom:20px; }
    .ck-finish-tag { display:inline-block; background:#eee8de; color:#666; font-size:0.75rem; padding:3px 10px; border-radius:20px; margin-bottom:16px; }
  </style>
</head>
<body>

<nav class="nav" id="nav">
  <div class="nav__inner">
    <a href="<?= $is_de ? 'de/index.html' : 'index.html' ?>" class="nav__logo">
      <img src="<?= $logo_url ?>" alt="SunWave Switzerland" style="height:44px;display:block;border-radius:6px;">
    </a>
    <div class="nav__links"></div>
    <div class="nav__right">
      <a href="<?= $product_url ?>" class="nav__order-btn"><?= $is_de ? 'Zurück' : 'Back' ?></a>
    </div>
  </div>
</nav>

<div style="padding-top:64px; background:#f8f7f4; min-height:100vh;">
  <div class="ck-wrap">

    <!-- LEFT: Form -->
    <div>
      <a href="<?= $product_url ?>" class="ck-back"><?= $txt['back'] ?></a>

      <?php if ($post_error): ?>
        <div class="ck-error"><?= htmlspecialchars($post_error) ?></div>
      <?php endif; ?>

      <form method="POST" action="checkout.php">
        <input type="hidden" name="finish" value="<?= $finish ?>">
        <input type="hidden" name="qty"    value="<?= $qty ?>">
        <input type="hidden" name="lang"   value="<?= $lang ?>">

        <div class="ck-form-box">
          <h2><?= $txt['contact_h'] ?></h2>
          <div class="ck-field">
            <label for="name"><?= $txt['f_name'] ?></label>
            <input type="text" id="name" name="name" autocomplete="name" required
                   value="<?= htmlspecialchars($_POST['name'] ?? '', ENT_QUOTES) ?>">
          </div>
          <div class="ck-row2">
            <div class="ck-field">
              <label for="email"><?= $txt['f_email'] ?></label>
              <input type="email" id="email" name="email" autocomplete="email" required
                     value="<?= htmlspecialchars($_POST['email'] ?? '', ENT_QUOTES) ?>">
            </div>
            <div class="ck-field">
              <label for="phone"><?= $txt['f_phone'] ?></label>
              <input type="tel" id="phone" name="phone" autocomplete="tel"
                     value="<?= htmlspecialchars($_POST['phone'] ?? '', ENT_QUOTES) ?>">
            </div>
          </div>

          <h2><?= $txt['delivery_h'] ?></h2>
          <div class="ck-field">
            <label for="address"><?= $txt['f_address'] ?></label>
            <input type="text" id="address" name="address" autocomplete="street-address" required
                   value="<?= htmlspecialchars($_POST['address'] ?? '', ENT_QUOTES) ?>">
          </div>
          <div class="ck-row2">
            <div class="ck-field">
              <label for="postal"><?= $txt['f_postal'] ?></label>
              <input type="text" id="postal" name="postal" autocomplete="postal-code"
                     pattern="[0-9]{4}" maxlength="4" required
                     value="<?= htmlspecialchars($_POST['postal'] ?? '', ENT_QUOTES) ?>">
            </div>
            <div class="ck-field">
              <label for="city"><?= $txt['f_city'] ?></label>
              <input type="text" id="city" name="city" autocomplete="address-level2" required
                     value="<?= htmlspecialchars($_POST['city'] ?? '', ENT_QUOTES) ?>">
            </div>
          </div>
          <div class="ck-field">
            <label for="canton"><?= $txt['f_canton'] ?></label>
            <select id="canton" name="canton" required>
              <option value="">— <?= $is_de ? 'Bitte wählen' : 'Please select' ?> —</option>
              <?php
              $cantons = ['AG','AI','AR','BE','BL','BS','FR','GE','GL','GR','JU','LU','NE','NW','OW','SG','SH','SO','SZ','TG','TI','UR','VD','VS','ZG','ZH'];
              $sel = $_POST['canton'] ?? '';
              foreach ($cantons as $c) echo '<option value="'.$c.'"'.($sel===$c?' selected':'').'>'.$c.'</option>';
              ?>
            </select>
          </div>
        </div>

        <!-- Mobile: summary shown here via CSS order -->
        <div class="ck-summary" style="display:none;" id="mobile-summary-placeholder"></div>

        <button type="submit" class="ck-pay-btn"><?= $txt['pay_btn'] ?></button>
        <p class="ck-secure">🔒 <?= $txt['secure'] ?></p>
        <p class="ck-methods"><?= $txt['methods'] ?></p>
      </form>
    </div>

    <!-- RIGHT: Order summary -->
    <div class="ck-summary">
      <h3><?= $txt['order_h'] ?></h3>
      <div class="ck-prod-name"><?= $txt['product_lbl'] ?></div>
      <div class="ck-prod-sub"><?= $txt['incl_thermo'] ?></div>
      <span class="ck-finish-tag"><?= $finish ?></span>
      <div class="ck-line">
        <span><?= $txt['per_panel'] ?></span>
        <span>CHF <?= number_format($subtotal, 0, '.', "'") ?></span>
      </div>
      <div class="ck-line">
        <span><?= $txt['delivery'] ?></span>
        <span>CHF <?= $shipping ?></span>
      </div>
      <div class="ck-total">
        <span><?= $txt['total'] ?></span>
        <span>CHF <?= number_format($total, 0, '.', "'") ?></span>
      </div>
    </div>

  </div>
</div>

<script>
window.addEventListener('scroll', () => {
  document.querySelector('.nav')?.classList.toggle('scrolled', window.scrollY > 20);
});
</script>
</body>
</html>
