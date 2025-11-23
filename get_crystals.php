<?php
header("Content-Type: application/json");
require "config.php";

$user_id = intval($_GET["user_id"]);

$result = $conn->query("SELECT crystals FROM users WHERE id = $user_id");

if ($result->num_rows === 0) {
    // создаём пользователя
    $conn->query("INSERT INTO users (id, crystals) VALUES ($user_id, 0)");
    echo json_encode(["crystals" => 0]);
    exit;
}

$row = $result->fetch_assoc();
echo json_encode(["crystals" => intval($row["crystals"])]);
?>
