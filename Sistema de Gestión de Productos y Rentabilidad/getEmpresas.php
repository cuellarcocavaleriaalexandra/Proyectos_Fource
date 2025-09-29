<?php
header('Content-Type: application/json');

// Establece la conexión a la base de datos
include 'db_conexion.php';

$sql = "SELECT id, nombre FROM Empresas";
$result = $conn->query($sql);
$empresas = array();
while ($row = $result->fetch_assoc()) {
    $empresas[] = $row;
}

// Cierra la conexión
$conn->close();

echo json_encode($empresas);
?>
