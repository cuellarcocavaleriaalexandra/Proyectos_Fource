<?php
// Aquí debes establecer la conexión con tu base de datos
include 'db_conexion.php';

header('Content-Type: application/json');
$empresaId = $_POST['empresaId'];
$productoId = $_POST['productoId'];
$gestionId = $_POST['gestionId'];
$calculoId = $_POST['calculoId'];

if ($calculoId == "pareto") {
    $sql = "SELECT mes, ingreso_venta, cantidad_unidades, precio_unitario FROM pareto WHERE id_producto = ? AND Gestion = ?";
} else if ($calculoId == "rentabilidad") {
    $sql = "SELECT mes, rentabilidad, indice_comerciabilidad, contribucion_utilitaria FROM rentabilidad WHERE id_producto = ? AND Gestion = ?";
}

// Utiliza consultas preparadas para mayor seguridad
$stmt = $conn->prepare($sql);
$stmt->bind_param("ii", $productoId, $gestionId);

if ($stmt->execute()) {
    $result = $stmt->get_result();
    $datos = $result->fetch_all(MYSQLI_ASSOC);
    echo json_encode($datos);
}

$stmt->close();
$conn->close();
?>