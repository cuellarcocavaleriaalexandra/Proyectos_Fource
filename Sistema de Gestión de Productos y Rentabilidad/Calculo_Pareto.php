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
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script> <!-- Asegúrate de tener Chart.js -->
<head>
    <h1><?php echo $company['nombre']; ?></h1>
</head>
<body>

    <h2>Ingresar Datos</h2>
    <form id="data-form">
    
    <label class="right.align" for="Gestion">Gestion</label><br>
        <select class="right.align" name="Gestion" id="gestion">
            <option value="">Elegir Gestion</option>
            <option value="2019">2019</option>
            <option value="2020">2020</option>
            <option value="2021">2021</option>
            <option value="2022">2022</option>
            <option value="2023">2023</option>
            </select><br>

        <label class="right.align" for="Mes">Mes</label><br>
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
    
        <label class="right.align" for="nombre">Nombre del Artículo:</label><br>
    <?php
echo '<select name="articleName" id="articleName">';
echo '<option value="">Elegir un articulo</option>';
foreach ($products as $index => $product )  {
    echo '<option value="' . $product['id'] . '|' . $product['nombre'] . '">' . $product['nombre'] . '</option>';
}
echo '</select>';
  
echo '<script>';
echo 'var allArticles = ' . json_encode(array_column($products, 'nombre')) . ';';
echo '</script>';
  
  ?>
            <br>

        <label for="unidades">Unidades:</label><br>
        <input type="number" id="unidades" name="unidades"><br>
        <label for="precio">Precio Unitario:</label><br>
        <input type="number" id="precio" name="precio"><br>
     
        <input type="submit" value="Añadir datos">
        <button id="saveTable">Guardar tabla</button>

    </form>

<h2>Tabla de Datos</h2>
<table id="data-table">
  <tr>
    <th>Gestion</th>
    <th>Mes</th>
    <th>ID</th>
    <th>Nombre</th>
    <th>Unidades</th>
    <th>Precio Unitario</th>
    <th>Ventas</th>
  </tr>
</table>

<h2>Tabla de Resultados</h2>
<table id="results-table">
  <tr>
    <th>ID</th>
    <th>Nombre</th>
    <th>Ventas Totales</th>
    <th>Porcentaje Acumulado</th>
    <th>Porcentaje Acumulado %</th>
  </tr>
</table>


<!-- Gráfico de Pareto -->
<h2>Gráfico de Pareto</h2>
<canvas id="pareto-chart"></canvas>

<script src="Graficos_Pareto.js" charset="UTF-8"></script>

</body>
</html>
