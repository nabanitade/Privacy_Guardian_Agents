<?php
// PHP test file with privacy violations
$userEmail = "test@example.com";
$userSSN = "123-45-6789";
$userPhone = "555-123-4567";

function processUserData($user) {
    echo "Processing user: " . $user['email']; // PII in console log
    return array(
        'id' => $user['id'],
        'email' => $user['email'],
        'ssn' => $user['ssn'] // Sensitive data
    );
}

$apiKey = "sk-1234567890abcdef"; // API key
$userData = array(
    'name' => 'John Doe',
    'email' => 'john@example.com',
    'phone' => '555-987-6543',
    'address' => '123 Main Street, Anytown, CA 90210'
);
?> 