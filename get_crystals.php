<?php
header("Content-Type: application/json");

// создаём файл, если его нет
if (!file_exists("database.json")) {
    file_put_contents("database.json", "{}");
}

$db = json_decode(file_get_contents("database.json"), true);

$user_id = $_GET["user_id"] ?? null;

if (!$user_id) {
    echo json_encode(["error" => "No user id"]);
    exit;
}

$crystals = $db[$user_id] ?? 0;

echo json_encode([
    "crystals" => $crystals
]);
?>
