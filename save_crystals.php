<?php
header("Content-Type: application/json");

$data = json_decode(file_get_contents("php://input"), true);

$user_id = $data["user_id"] ?? null;
$crystals = $data["crystals"] ?? null;

if (!$user_id || $crystals === null) {
    echo json_encode(["error" => "Invalid data"]);
    exit;
}

// загружаем базу
$db = json_decode(file_get_contents("database.json"), true);

// сохраняем
$db[$user_id] = $crystals;

// записываем обратно
file_put_contents("database.json", json_encode($db, JSON_PRETTY_PRINT));

echo json_encode(["status" => "saved"]);
?>
