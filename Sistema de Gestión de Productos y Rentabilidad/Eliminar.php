<?php
include 'db_conexion.php';

$companyId = $_GET['id'];

$stmt = $conn->prepare("DELETE FROM Productos WHERE id_empresa = ?");
$stmt->bind_param("i", $companyId);

if ($stmt->execute() === TRUE) {
    $stmt = $conn->prepare("DELETE FROM Empresas WHERE id = ?");
    $stmt->bind_param("i", $companyId);

    if ($stmt->execute() === TRUE) {
        echo "Empresa eliminada exitosamente";
    } else {
        echo "Error: " . $stmt->error;
    }
} else {
    echo "Error: " . $stmt->error;
}

$stmt->close();
$conn->close();
?>
