<?php
//solicitar el archivo de conexión a la base de datos
include 'db_conexion.php';
?>

<!DOCTYPE html>
<html>
    <link rel="stylesheet" type="text/css" href="Style.css">

<head>
    <title>Creando nueva empresa</title>
</head>
<body>
    <h1>Creando nueva empresa</h1>
    <form id="companyForm" action="Insertar.php" method="POST">

        <label for="companyName">Nombre de la empresa:</label><br>
        <input type="text" id="companyName" name="companyName"><br>
        <label for="products">Productos:</label><br>
        <input type="text" id="product" name="product"><br>
        <input type="submit" value="Añadir producto"><br>
        <button type="button" id="save">Guardar</button>

    </form>
    <table id="productTable">
        <tr>
            <th>No.</th>
            <th>Producto</th>
        </tr>
    </table>
    <script src="Anadir_Productos.js" charset="UTF-8"></script>. 

</body>
</html>
