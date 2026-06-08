<?php
session_start();

// Load API key
$mollie_key = null;
$key_file = dirname($_SERVER['DOCUMENT_ROOT']) . '/mollie_key.php';
if (file_exists($key_file)) include $key_file;

$order_id = htmlspecialchars($_GET['order'] ?? '');
$lang     = ($_GET['lang'] ?? 'en') === 'de' ? 'de' : 'en';
$is_de    = ($lang === 'de');

// Load session order data
$order = $_SESSION['sw_order_' . $order_id] ?? null;

// Check payment status from Mollie
$status = 'unknown';
$payment_id = $order['payment_id'] ?? null;

if ($mollie_key && $payment_id) {
    $ch = curl_init('https://api.mollie.com/v2/payments/' . urlencode($payment_id));
    curl_setopt_array($ch, [
        CURLOPT_HTTPHEADER     => ['Authorization: Bearer ' . $mollie_key],
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT        => 10,
    ]);
    $resp    = curl_exec($ch);
    curl_close($ch);
    $payment = json_decode($resp, true) ?: [];
    $status  = $payment['status'] ?? 'unknown';

    // Merge metadata if session was lost
    if (!$order && !empty($payment['metadata'])) {
        $m = $payment['metadata'];
        $order = [
            'name'    => $m['name']   ?? '',
            'email'   => $m['email']  ?? '',
            'finish'  => $m['finish'] ?? '',
            'qty'     => $m['qty']    ?? 1,
            'total'   => (550 * ($m['qty'] ?? 1)) + 35,
            'order_id'=> $order_id,
        ];
    }
}

$paid       = ($status === 'paid');
$pending    = in_array($status, ['open', 'pending', 'authorized']);
$failed     = in_array($status, ['failed', 'canceled', 'expired']);

$product_url = $is_de ? 'de/product.html' : 'product.html';

$txt = $is_de ? [
    'paid_h'   => 'Bestellung bestätigt!',
    'paid_p'   => 'Vielen Dank für Ihre Bestellung. Sie erhalten in Kürze eine Bestätigungs-E-Mail. Lieferung in 3–5 Werktagen.',
    'pend_h'   => 'Zahlung wird verarbeitet',
    'pend_p'   => 'Ihre Zahlung wird verarbeitet. Sie erhalten eine Bestätigung, sobald sie abgeschlossen ist.',
    'fail_h'   => 'Zahlung nicht abgeschlossen',
    'fail_p'   => 'Ihre Zahlung wurde nicht abgeschlossen. Bitte versuchen Sie es erneut.',
    'retry'    => 'Erneut versuchen',
    'order_lbl'=> 'Bestellnummer',
    'name_lbl' => 'Name',
    'finish_lbl'=> 'Oberfläche',
    'qty_lbl'  => 'Anzahl',
    'total_lbl'=> 'Total',
    'home'     => 'Zurück zur Startseite',
] : [
    'paid_h'   => 'Order confirmed!',
    'paid_p'   => 'Thank you for your order. You will receive a confirmation email shortly. Delivery in 3–5 working days.',
    'pend_h'   => 'Payment processing',
    'pend_p'   => 'Your payment is being processed. You will receive a confirmation once it completes.',
    'fail_h'   => 'Payment not completed',
    'fail_p'   => 'Your payment was not completed. Please try again.',
    'retry'    => 'Try again',
    'order_lbl'=> 'Order number',
    'name_lbl' => 'Name',
    'finish_lbl'=> 'Finish',
    'qty_lbl'  => 'Quantity',
    'total_lbl'=> 'Total',
    'home'     => 'Back to homepage',
];
?>
<!DOCTYPE html>
<html lang="<?= $lang ?>">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title><?= $paid ? $txt['paid_h'] : ($pending ? $txt['pend_h'] : $txt['fail_h']) ?> — SunWave Switzerland</title>
  <meta name="robots" content="noindex">
  <link rel="icon" type="image/png" href="images/logo.webp">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
  <style>
    .ret-wrap { max-width:560px; margin:100px auto 80px; padding:0 24px; text-align:center; }
    .ret-icon { font-size:3rem; margin-bottom:20px; }
    .ret-h { font-size:1.8rem; font-weight:800; color:#1a1a24; margin-bottom:12px; }
    .ret-p { color:#666; line-height:1.7; margin-bottom:32px; }
    .ret-card { background:#f8f7f4; border:1px solid #e8e3db; border-radius:8px; padding:24px; text-align:left; margin-bottom:32px; }
    .ret-row { display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid #ebe7e0; font-size:0.88rem; }
    .ret-row:last-child { border-bottom:none; font-weight:700; font-size:1rem; }
    .ret-btn { display:inline-block; padding:14px 32px; background:var(--gold); color:#1a1a24; font-weight:700; border-radius:4px; text-decoration:none; font-family:inherit; }
    .ret-btn:hover { background:#e8c030; }
    .ret-link { display:block; margin-top:16px; color:#888; font-size:0.85rem; }
  </style>
</head>
<body>
<nav class="nav">
  <div class="nav__inner">
    <a href="<?= $is_de ? 'de/index.html' : 'index.html' ?>" class="nav__logo">
      <img src="images/logo.webp" alt="SunWave Switzerland" style="height:44px;display:block;border-radius:6px;">
    </a>
  </div>
</nav>

<div class="ret-wrap">
  <?php if ($paid): ?>
    <div class="ret-icon">✅</div>
    <h1 class="ret-h"><?= $txt['paid_h'] ?></h1>
    <p class="ret-p"><?= $txt['paid_p'] ?></p>
    <?php if ($order): ?>
    <div class="ret-card">
      <div class="ret-row"><span><?= $txt['order_lbl'] ?></span><span><?= htmlspecialchars($order['order_id']) ?></span></div>
      <div class="ret-row"><span><?= $txt['name_lbl'] ?></span><span><?= htmlspecialchars($order['name']) ?></span></div>
      <div class="ret-row"><span><?= $txt['finish_lbl'] ?></span><span><?= htmlspecialchars($order['finish']) ?></span></div>
      <div class="ret-row"><span><?= $txt['qty_lbl'] ?></span><span><?= intval($order['qty']) ?></span></div>
      <div class="ret-row"><span><?= $txt['total_lbl'] ?></span><span>CHF <?= number_format(floatval($order['total']), 0, '.', "'") ?></span></div>
    </div>
    <?php endif; ?>
    <a href="<?= $is_de ? 'de/index.html' : 'index.html' ?>" class="ret-btn"><?= $txt['home'] ?></a>

  <?php elseif ($pending): ?>
    <div class="ret-icon">⏳</div>
    <h1 class="ret-h"><?= $txt['pend_h'] ?></h1>
    <p class="ret-p"><?= $txt['pend_p'] ?></p>
    <a href="<?= $is_de ? 'de/index.html' : 'index.html' ?>" class="ret-btn"><?= $txt['home'] ?></a>

  <?php else: ?>
    <div class="ret-icon">❌</div>
    <h1 class="ret-h"><?= $txt['fail_h'] ?></h1>
    <p class="ret-p"><?= $txt['fail_p'] ?></p>
    <a href="<?= $product_url ?>" class="ret-btn"><?= $txt['retry'] ?></a>
    <a href="<?= $is_de ? 'de/index.html' : 'index.html' ?>" class="ret-link"><?= $txt['home'] ?></a>
  <?php endif; ?>
</div>
</body>
</html>
