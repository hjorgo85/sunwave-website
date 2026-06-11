<?php
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    exit;
}

$to = 'info@sunwaveswitzerland.com';

$name    = strip_tags(trim($_POST['name'] ?? ''));
$email   = filter_var(trim($_POST['email'] ?? ''), FILTER_SANITIZE_EMAIL);
$phone   = strip_tags(trim($_POST['phone'] ?? ''));
$canton  = strip_tags(trim($_POST['canton'] ?? ''));
$type    = strip_tags(trim($_POST['type'] ?? ''));
$area    = strip_tags(trim($_POST['area'] ?? ''));
$system  = strip_tags(trim($_POST['system'] ?? ''));
$propertyType = strip_tags(trim($_POST['property_type'] ?? ''));
$rooms        = strip_tags(trim($_POST['rooms'] ?? ''));
$message = strip_tags(trim($_POST['message'] ?? ''));

$orderProduct  = strip_tags(trim($_POST['order_product'] ?? ''));
$orderFinish   = strip_tags(trim($_POST['order_finish'] ?? ''));
$orderQty      = strip_tags(trim($_POST['order_qty'] ?? ''));
$orderShipping = strip_tags(trim($_POST['order_shipping'] ?? ''));
$orderTotal    = strip_tags(trim($_POST['order_total'] ?? ''));

if (!$name || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Invalid input']);
    exit;
}

$subject = "SunWave Quote Request from $name";

$body  = "New quote request from sunwaveswitzerland.com\n";
$body .= str_repeat('-', 40) . "\n\n";

if ($orderProduct !== '') {
    $body .= "ORDER DETAILS\n";
    $body .= "Product:          $orderProduct\n";
    $body .= "Finish:           $orderFinish\n";
    $body .= "Quantity:         $orderQty\n";
    $body .= "Shipping:         " . ($orderShipping === '0' ? 'Free' : "CHF $orderShipping") . "\n";
    $body .= "Total (incl. VAT): CHF $orderTotal\n";
    $body .= str_repeat('-', 40) . "\n\n";
}

$body .= "Name:             $name\n";
$body .= "Email:            $email\n";
$body .= "Phone:            $phone\n";
$body .= "Canton:           $canton\n";
$body .= "Enquiry type:     $type\n";
$body .= "Floor area:       $area m²\n";
$body .= "Heating system:   $system\n";
$body .= "Property type:    $propertyType\n";
$body .= "Rooms to heat:    $rooms\n";
$body .= "\nMessage:\n$message\n";

$headers  = "From: noreply@sunwaveswitzerland.com\r\n";
$headers .= "Reply-To: $email\r\n";
$headers .= "X-Mailer: PHP/" . phpversion();

$sent = mail($to, $subject, $body, $headers);

header('Content-Type: application/json');
echo json_encode(['success' => $sent]);
