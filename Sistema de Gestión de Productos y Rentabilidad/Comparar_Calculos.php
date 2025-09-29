<?php
include 'db_conexion.php';

// Obtener empresas
$sqlEmpresas = "SELECT id, nombre FROM Empresas";
$resultEmpresas = $conn->query($sqlEmpresas);
$empresas = $resultEmpresas->fetch_all(MYSQLI_ASSOC);

// Cerrar conexión
$conn->close();
?>

<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" type="text/css" href="Style.css">

    <h1> Comparando datos </h1>

</head>
<!-- Agrega esto a tu HTML -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<body>

    <label >Empresas guardadas</label><br>
    <select id="empresa">
        <option>Seleccione una Empresa</option>
        <?php
        foreach ($empresas as $empresa) {
            echo "<option value='".$empresa['id']."'>".$empresa['nombre']."</option>";
        }
        ?>
    </select>
<br>

    <label>Productos:</label><br>
    <select id="producto">
        <option>Seleccione un producto</option>
    </select>
<br>

    <label >Comparación de calculos</label><br>
        <select class="right.align" name="calculos" id=comparación>
            <option value="">Elegir Tipo de comparación</option>
            <option value="pareto">Pareto</option>
            <option value="rentabilidad">Rentabilidad</option>
            </select><br>


    <label class="right.align" for="Gestion">Gestion: </label><br>
        <select class="right.align" name="Gestion" id="gestion">
            <option value="">Elegir Gestion</option>
            <option value="2019">2019</option>
            <option value="2020">2020</option>
            <option value="2021">2021</option>
            <option value="2022">2022</option>
            <option value="2023">2023</option>
            </select>
            <br>

    <button id="compare">Compare</button>
     <br>

    <table id="results">

    <!-- Results will be populated here -->
    </table>

    <h2>Gráfico de Barras Simple</h2>

<canvas id="myChart"></canvas>

<script>
document.addEventListener('DOMContentLoaded', function() {
    var empresaSelect = document.getElementById('empresa');
    var productoSelect = document.getElementById('producto');
    var gestionSelect = document.getElementById('gestion');
    var comparacionSelect = document.getElementById('comparación');
    var comparaButton = document.getElementById('compare');
    var resultsTable = document.getElementById('results');

    // Evento cuando se cambia la empresa seleccionada
    empresaSelect.addEventListener('change', function() {
        var empresaId = empresaSelect.value;
        var productoId = productoSelect.value
        var calculoId = comparacionSelect.value
        var gestionId = gestionSelect.value

        // Limpiar opciones de producto
        while (productoSelect.firstChild) {
            productoSelect.removeChild(productoSelect.firstChild);
        }

        // Si se seleccionó una empresa, obtener sus productos
        if (empresaId != "") {
            fetch('getProductos.php?empresa_id=' + empresaId)
                .then(response => response.json())
                .then(productos => {
                    // Llenar opciones de producto para la empresa seleccionada
                    productos.forEach(function(producto) {
                        var option = document.createElement('option');
                        option.value = producto.id;
                        option.textContent = producto.nombre;
                        productoSelect.appendChild(option);
                    });
                });
        }

    });

    // Evento cuando se hace clic en "Compara"
    comparaButton.addEventListener('click', function() {
        var empresaId = empresaSelect.value;
        var productoId = productoSelect.value;
        var comparacionId = comparacionSelect.value;
        var gestionId = gestionSelect.value;

        if (empresaId !== "" && productoId !== "" && comparacionId !== "" && gestionId !== "") {
            fetch('getDatos.php', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: '&empresaId=' + empresaId + '&productoId=' + productoId + '&gestionId=' + gestionId + '&calculoId=' + comparacionId
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(datos => {
                // Limpiar resultados anteriores
                while (resultsTable.firstChild) {
                    resultsTable.removeChild(resultsTable.firstChild);
                }

            // Crear fila de encabezado
            var headerRow = document.createElement('tr');
            var headerCell1 = document.createElement('th');
            var headerCell2 = document.createElement('th');
            var headerCell3 = document.createElement('th');
            var headerCell4 = document.createElement('th');
            headerCell1.textContent = "Mes";

            // Seleccionar el valor correcto según el tipo de comparación
            if (comparacionId === "pareto") {
                headerCell2.textContent = "Ingreso de Venta";
                headerCell3.textContent = "Cantidad de Unidades";
                headerCell4.textContent = "Precio Unitario";
            } else if (comparacionId === "rentabilidad") {
                headerCell2.textContent = "Rentabilidad";
                headerCell3.textContent = "Índice de Comerciabilidad";
                headerCell4.textContent = "Contribución Utilitaria";
            }

            headerRow.appendChild(headerCell1);
            headerRow.appendChild(headerCell2);
            headerRow.appendChild(headerCell3);
            headerRow.appendChild(headerCell4);
            resultsTable.appendChild(headerRow);

            var nombres = [];
            var valores = [];

                // Mostrar nuevos resultados en la tabla
                datos.forEach(function(dato) {
                    var row = document.createElement('tr');
                    var cell1 = document.createElement('td');
                    var cell2 = document.createElement('td');
                    var cell3 = document.createElement('td');
                    var cell4 = document.createElement('td');
                    cell1.textContent = dato.mes;
                    nombres.push(dato.mes);

                    // Seleccionar el valor correcto según el tipo de comparación
                    if (comparacionId === "pareto") {
                        cell2.textContent = dato.ingreso_venta;
                        cell3.textContent = dato.cantidad_unidades;
                        cell4.textContent = dato.precio_unitario;
                        valores.push(dato.ingreso_venta);
                    } else if (comparacionId === "rentabilidad") {
                        cell2.textContent = dato.rentabilidad;
                        cell3.textContent = dato.indice_comerciabilidad;
                        cell4.textContent = dato.contribucion_utilitaria;
                        valores.push(dato.rentabilidad);
                    }

                    row.appendChild(cell1);
                    row.appendChild(cell2);
                    row.appendChild(cell3);
                    row.appendChild(cell4);
                    resultsTable.appendChild(row);
                });



            // Crear gráfico
            var ctx = document.getElementById('myChart').getContext('2d');
            var myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: nombres,
                    datasets: [{
                        label: comparacionId === "pareto" ? 'Ingreso de Venta' : 'Rentabilidad',
                        data: valores,
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        })
            .catch(error => {
                console.error('Hubo un problema con la operación de fetch:', error);
            });
        }
    });
})
        
    </script>


</body>
</html>

