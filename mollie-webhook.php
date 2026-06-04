<?php
// Mollie webhook — receives payment status updates server-to-server

$mollie_key = null;
$key_file = dirname($_SERVER['DOCUMENT_ROOT']) . '/mollie_key.php';
if (file_exists($key_file)) include $key_file;

if (!$mollie_key) { http_response_code(200); exit; }

$payment_id = $_POST['id'] ?? '';
if (!$payment_id) { http_response_code(200); exit; }

// Fetch payment details from Mollie
$ch = curl_init('https://api.mollie.com/v2/payments/' . urlencode($payment_id));
curl_setopt_array($ch, [
    CURLOPT_HTTPHEADER     => ['Authorization: Bearer ' . $mollie_key],
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_TIMEOUT        => 10,
]);
$resp    = curl_exec($ch);
curl_close($ch);
$payment = json_decode($resp, true) ?: [];

if (empty($payment['status'])) { http_response_code(200); exit; }

$status = $payment['status'];
$meta   = $payment['metadata'] ?? [];

// Send email notification when payment is paid
if ($status === 'paid') {
    $order_id = $meta['order_id']  ?? $payment_id;
    $name     = $meta['name']      ?? 'N/A';
    $email    = $meta['email']     ?? 'N/A';
    $phone    = $meta['phone']     ?? 'N/A';
    $address  = $meta['address']   ?? 'N/A';
    $city     = $meta['city']      ?? 'N/A';
    $postal   = $meta['postal']    ?? 'N/A';
    $canton   = $meta['canton']    ?? 'N/A';
    $finish   = $meta['finish']    ?? 'N/A';
    $qty      = $meta['qty']       ?? 1;
    $amount   = $payment['amount']['value']    ?? 'N/A';
    $currency = $payment['amount']['currency'] ?? 'CHF';

    $subject = "NEW ORDER {$order_id} — SunWave Switzerland";
    $body = "
NEW SUNWAVE ORDER
=================
Order ID : {$order_id}
Payment  : {$currency} {$amount}
Status   : PAID ✓

CUSTOMER
--------
Name     : {$name}
Email    : {$email}
Phone    : {$phone}

DELIVERY ADDRESS
----------------
{$address}
{$postal} {$city}
Canton   : {$canton}

PRODUCT
-------
Finish   : {$finish}
Quantity : {$qty} × SunWave Ceramica
";

    $headers = "From: orders@sunwaveswitzerland.com\r\nContent-Type: text/plain; charset=UTF-8";
    mail('hjorgo85@gmail.com', $subject, $body, $headers);
    mail('info@sunwaveswitzerland.com', $subject, $body, $headers);
}

http_response_code(200);
echo 'OK';
