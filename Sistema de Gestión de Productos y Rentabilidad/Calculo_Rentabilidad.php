<?php
include 'db_conexion.php';

$companyId = $_GET['id'];

$sql = "SELECT nombre FROM Empresas WHERE id = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("i", $companyId);
$stmt->execute();
$result = $stmt->get_result();
$company = $result->fetch_assoc();

$sql = "SELECT id, nombre FROM Productos WHERE id_empresa = ?";
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
    <h1><?php echo $company['nombre']; ?></h1>
</head>
<body>
    <h2>Calculadora de Rentabilidad</h2>
    <form id="calculatorForm" method="POST" action="Insertar_Rentabilidad.php">

    <label class="right.align"  for="Gestion">Gestion</label><br>
        <select class="right.align" name="Gestion" id="gestion">
            <option value="">Elegir Gestion</option>
            <option value="2019">2019</option>
            <option value="2020">2020</option>
            <option value="2021">2021</option>
            <option value="2022">2022</option>
            <option value="2023">2023</option>
            </select><br>

        <label class="right.align"  for="Mes">Mes</label><br>
        <select class="right.align" name="Mes" id="mes">
            <option value="">Elegir Mes</option>
            <option value="Enero">Enero</option>
            <option value="Febrero">Febrero</option>
            <option value="Marzo">Marzo</option>
            <option value="Abril">Abril</option>
            <option value="Mayo">Mayo</option>
            <option value="Junio">Junio</option>
            <option value="Julio">Julio</option>
            <option value="Agosto">Agosto</option>
            <option value="Septiembre">Septiembre</option>
            <option value="Octubre">Octubre</option>
            <option value="Noviembre">Noviembre</option>
            <option value="Diciembre">Diciembre</option>
        </select><br>

        <label class="right.align" for="articleName">Nombre del Artículo:</label><br>
<?php
echo '<select name="articleName" id="articleName">';
echo '<option value="">Elegir un articulo</option>';
foreach ($products as $index => $product )  {
    echo '<option value="' . $product['id'] . '|' . $product['nombre'] . '">' . $product['nombre'] . '</option>';
}
echo '</select>';
?>
<br>
        <label for="salesIncome">Ingresos por Venta:</label><br>
        <input type="number" id="salesIncome" name="salesIncome"><br>
        <label for="fixedCosts">Costos Fijos:</label><br>
        <input type="number" id="fixedCosts" name="fixedCosts"><br>
        <label for="administrativeCosts">Costos Administrativos:</label><br>
        <input type="number" id="administrativeCosts" name="administrativeCosts"><br>
        <label for="commercialCosts">Costos Comerciales:</label><br>
        <input type="number" id="commercialCosts" name="commercialCosts"><br>
        <label for="variableCost">Costo Variable:</label><br>
        <input type="number" id="variableCost" name="variableCost"><br>

        <input type="submit" value="Calcular">
        <button id="saveTable">Guardar tabla</button>
   
    
    </form>
    <h2>Tabla de datos</h2>
    <table id="data-Table">
        <tr>
            <th>Gestion</th>
            <th>Mes</th>
            <th>ID</th>
            <th>Artículo</th>
            <th>Utilidades</th>
            <th>Ingresos por Venta</th>
            <th>Ingresos Totales por Venta</th>
            <th>Costo Total</th>

        </tr>
    </table>

    <h2>Resultados</h2>
    <table id="resultsTable">
        <tr>
            <th>ID</th>
            <th>Artículo</th>
            <th>Rentabilidad de Ventas</th>
            <th>Índice de Comerciabilidad</th>
            <th>Contribución Utilitaria</th>
            <th>Acciones</th>
        </tr>
    </table>

<script src="Rentabilidad.js" charset="UTF-8"></script>

</body>
</html>
