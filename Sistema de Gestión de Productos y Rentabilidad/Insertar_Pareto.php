<?php
include 'db_conexion.php';

// Decodificar los datos de las tablas
$dataTable = json_decode($_POST['dataTable'], true);
$resultsTable = json_decode($_POST['results-Table'], true);

// Iterar sobre los datos de las tablas e insertarlos en la base de datos
foreach ($dataTable as $row) {
    $id_producto = $row['ID'];
    $nombre_producto = $row['Nombre'];
    $unidades = $row['Unidades'];
    $Precio_Unitario = $row['Precio Unitario'];
    $ingreso_venta = $row['Ventas'];
    $Gestion = $row['Gestion'];
    $Mes = $row['Mes'];

    // Buscar el correspondiente resultado para este producto en $resultsTable
    foreach ($resultsTable as $result) {
        if ($result['ID'] == $id_producto) {
            $ventas_totales = $result['Ventas Totales'];
            $porcentaje_acumulado = $result['Porcentaje Acumulado'];
            $porcentaje_acumulado_porcentaje = $result['Porcentaje Acumulado %'];
            break;
        }
    }

    $sql = "INSERT INTO pareto (id_producto, ingreso_venta, ingresos_totales_venta, porcentaje_acumulado, porcentaje_acumulado_porcentaje, Gestion, Mes, cantidad_unidades, precio_unitario)
    VALUES ('$id_producto', '$ingreso_venta', '$ventas_totales', '$porcentaje_acumulado', '$porcentaje_acumulado_porcentaje', '$Gestion', '$Mes', '$unidades', '$Precio_Unitario')";

    if ($conn->query($sql) === TRUE) {
      echo "New record created successfully";
    } else {
      echo "Error: " . $sql . "<br>" . $conn->error;
    }
}
$conn->close();
?>
