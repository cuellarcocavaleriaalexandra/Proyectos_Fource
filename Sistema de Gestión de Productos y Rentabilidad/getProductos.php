<?php
include 'db_conexion.php';

// Obtener id de la empresa
$empresaId = $_GET['empresa_id'];

// Obtener productos de la empresa
$sqlProductos = "SELECT id, nombre FROM Productos WHERE id_empresa = $empresaId";
$resultProductos = $conn->query($sqlProductos);
$productos = $resultProductos->fetch_all(MYSQLI_ASSOC);

// Cerrar conexión
$conn->close();

// Devolver productos en formato JSON
echo json_encode($productos);
?>
