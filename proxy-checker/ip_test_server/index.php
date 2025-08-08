<?php
    header('Content-Type: application/json'); // Ensuring the content type is JSON
    header('Cache-Control: no-cache, must-revalidate'); // Prevent caching
    header('Expires: Mon, 26 Jul 1997 05:00:00 GMT');

    // Determining the client IP address. Most reliable: REMOTE_ADDR
    // HTTP_X_FORWARDED_FOR can be spoofed but is included for logging/debugging
    $client_ip = $_SERVER['REMOTE_ADDR'];

    // Get other headers
    $xff_header = isset($_SERVER['HTTP_X_FORWARDED_FOR']) ? $_SERVER['HTTP_X_FORWARDED_FOR'] : null;
    $user_agent = isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : 'N/A';

    $client_information = array(
        "ip" => $client_ip,
        "x_forwarded_for" => $xff_header,
        "user_agent" => $user_agent
    );

    echo json_encode($client_information, JSON_PRETTY_PRINT); // Display JSON data
?>