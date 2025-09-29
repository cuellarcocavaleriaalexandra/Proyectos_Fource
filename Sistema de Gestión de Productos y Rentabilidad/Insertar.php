<?php
include 'db_conexion.php';

$companyName = $_POST['companyName'];
$products = json_decode($_POST['products']);

$stmt = $conn->prepare("INSERT INTO empresas (nombre) VALUES (?)");
$stmt->bind_param("s", $companyName);

if ($stmt->execute() === TRUE) {
    $id_empresa = $conn->insert_id;
    foreach ($products as $product) {
        $stmt = $conn->prepare("INSERT INTO Productos (id_empresa, nombre) VALUES (?, ?)");
        $stmt->bind_param("is", $id_empresa, $product);

        if ($stmt->execute() === TRUE) {
            echo "Nuevo producto creado exitosamente";
        } else {
            echo "Error: " . $stmt->error;
        }
    }
} else {
    echo "Error: " . $stmt->error;
}

$stmt->close();
$conn->close();
?>
