<?php
include 'db_conexion.php';

$companyId = $_GET['id'];

$sql = "SELECT nombre FROM Empresas WHERE id = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("i", $companyId);
$stmt->execute();
$result = $stmt->get_result();
$company = $result->fetch_assoc();

$sql = "SELECT nombre FROM Productos WHERE id_empresa = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("i", $companyId);
$stmt->execute();
$result = $stmt->get_result();
$products = $result->fetch_all(MYSQLI_ASSOC);

$stmt->close();
$conn->close();

?>

<!DOCTYPE html>
<html>
    <link rel="stylesheet" type="text/css" href="Style.css">
<head>
    <title>Descripcion empresa</title>
</head>
<body>
   
<h1><?php echo $company['nombre']; ?></h1>

    <table>
        <tr>
            <th>ID</th>
            <th>Producto</th>
        </tr>
       
        <?php
        foreach ($products as $index => $product) {
            echo "<tr>";
            echo "<td>" . ($index + 1) . "</td>";
            echo "<td>" . $product['nombre'] . "</td>";
            echo "</tr>";
        }
        ?>

    </table>
    <h2>Que desea calcular?</h2>
    <button id="pareto" data-id="<?php echo $companyId; ?>">Pareto</button>
    <p>Pareto identifica el 20% de los factores que causan el 80% de los resultados, ayudando a priorizar eficientemente.</p>
    <button id="profitability" data-id="<?php echo $companyId; ?>">Rentabilidad y desempeño financiero</button>
    <p>La rentabilidad del producto, índice de comerciabilidad, contribución utilitaria.</p>
 
 <script src="Funciones_Calculos.js" charset="UTF-8"></script>
</body>
</html>

