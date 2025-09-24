<?php
include 'db_conexion.php';

$sql = "SELECT id, nombre FROM Empresas";
$result = $conn->query($sql);
?>

<!DOCTYPE html>
<html>
    <link rel="stylesheet" type="text/css" href="Style.css">

<head>
    <title>Biblioteca de empresas</title>
</head>
<body>
    <!--<h1>Bienvenido 'Nombre de Usuario': Biblioteca de empresas</h1>-->
    <h1>Bienvenido: Biblioteca de empresas</h1>
    <table>
        <tr>
            <th>Nombre empresa</th>
            <th>Ver</th>
         
            <th>Eliminar</th>
        </tr>
        <?php
        if ($result->num_rows > 0) {
            while($row = $result->fetch_assoc()) {
                echo "<tr>";
                echo "<td>" . $row["nombre"] . "</td>";
                echo "<td><button class='ver' data-id='" . $row["id"] . "'>Ver</button></td>";
               
                echo "<td><button class='eliminar' action='Eliminar.php' data-id='" . $row["id"] . "'>Eliminar</button></td>";
                echo "</tr>";
            }
        } else {
            echo "0 resultados";
        }
        $conn->close();
        ?>
    </table>
    <button id="createCompany">Crear nueva empresa</button>
    <script src="Funciones_Menu.js" charset="UTF-8"></script>
</body>
</html>
