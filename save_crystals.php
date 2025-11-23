<?php
header("Content-Type: application/json");
require "config.php";

$data = json_decode(file_get_contents("php://input"), true);

$user_id = intval($data["user_id"]);
$crystals = intval($data["crystals"]);

$conn->query(
    "INSERT INTO users (id, crystals) VALUES ($user_id, $crystals)
     ON DUPLICATE KEY UPDATE crystals = $crystals"
);

echo json_encode(["status" => "ok"]);
?>
