<!DOCTYPE html>
<html>

<head>
    <link rel="stylesheet" type="text/css" href="Style.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <h1>Calculadora de Pareto</h1>
</head>

<body>

    <label class="right-align" for="nombre">Nombre del Artículo:</label><br>
    <input type="text" id="nombre" name="nombre"><br>

    <label for="unidades">Unidades:</label><br>
    <input type="number" id="unidades" name="unidades"><br>
    
    <label for="precio">Precio Unitario:</label><br>
    <input type="number" id="precio" name="precio"><br>

    <input type="submit" value="Calcular" id="calcular">

    <!-- Tabla de Datos -->
    <h2>Tabla de Datos</h2>
    <table id="data-table">
        <tr>
            <th>Nombre</th>
            <th>Unidades</th>
            <th>Precio Unitario</th>
            <th>Ventas</th>
        </tr>
    </table>

    <!-- Tabla de Resultados -->
    <h2>Tabla de Resultados</h2>
    <table id="results-table">
        <tr>
            <th>Nombre</th>
            <th>Ventas Totales</th>
            <th>Porcentaje Acumulado</th>
            <th>Porcentaje Acumulado %</th>
        </tr>
    </table>

    <!-- Gráfico de Pareto -->
    <h2>Gráfico de Pareto</h2>
    <canvas id="pareto-chart"></canvas>

    <script>
        var data = [];
        var paretoChart; // Variable para almacenar la instancia del gráfico de Pareto

        document.getElementById('calcular').addEventListener('click', function () {
            var articleName = document.getElementById('nombre').value;
            var unidades = parseInt(document.getElementById('unidades').value);
            var precio = parseFloat(document.getElementById('precio').value);

            if (articleName && !isNaN(unidades) && !isNaN(precio)) {
                var ventas = unidades * precio;
                data.push({
                    articleName: articleName,
                    unidades: unidades,
                    precio: precio,
                    ventas: ventas
                });

                updateTables();
            } else {
                alert('Por favor, ingresa datos válidos.');
            }
        });

        function updateTables() {
            var dataTable = document.getElementById('data-table');
            var resultsTable = document.getElementById('results-table');

            // Limpiar tablas
            dataTable.innerHTML = '<tr><th>Nombre</th><th>Unidades</th><th>Precio Unitario</th><th>Ventas</th></tr>';
            resultsTable.innerHTML = '<tr><th>Nombre</th><th>Ventas Totales</th><th>Porcentaje Acumulado</th><th>Porcentaje Acumulado %</th></tr>';

            // Ordenar datos por ventas
            data.sort((a, b) => b.ventas - a.ventas);

            var totalVentas = data.reduce((total, item) => total + item.ventas, 0);
            var acumulado = 0;

            var nombres = [];
            var ventasTotales = [];
            var porcentajesAcumulados = [];

            for (var i = 0; i < data.length; i++) {
                // Añadir fila a la tabla de datos
                var dataRow = dataTable.insertRow(-1);
                dataRow.insertCell(0).innerHTML = data[i].articleName;
                dataRow.insertCell(1).innerHTML = data[i].unidades;
                dataRow.insertCell(2).innerHTML = data[i].precio;
                dataRow.insertCell(3).innerHTML = data[i].ventas;

                // Calcular porcentaje acumulado
                acumulado += data[i].ventas;
                var porcentaje = (acumulado / totalVentas) * 100;

                // Añadir fila a la tabla de resultados
                var resultsRow = resultsTable.insertRow(-1);
                resultsRow.insertCell(0).innerHTML = data[i].articleName;
                resultsRow.insertCell(1).innerHTML = data[i].ventas;
                resultsRow.insertCell(2).innerHTML = acumulado;
                resultsRow.insertCell(3).innerHTML = porcentaje.toFixed(2) + '%';

                // Añadir datos para el gráfico
                nombres.push(data[i].articleName);
                ventasTotales.push(data[i].ventas);
                porcentajesAcumulados.push(porcentaje);
            }

            // Si el gráfico de Pareto ya existe, destrúyelo antes de crear uno nuevo
            if (paretoChart) {
                paretoChart.destroy();
            }

            // Crear gráfico de Pareto
            var ctx = document.getElementById('pareto-chart').getContext('2d');
            paretoChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: nombres,
                    datasets: [{
                        label: 'Ventas Totales',
                        data: ventasTotales,
                        backgroundColor: 'rgba(75, 192, 192, 0.2)', 
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }, {
                        label: 'Porcentaje Acumulado',
                        data: porcentajesAcumulados,
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1,
                        type: 'line',
                        fill: false,
                        yAxisID: 'y-axis-2'
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        },
                        'y-axis-2': {
                            type: 'linear',
                            display: true,
                            position: 'right',
                            beginAtZero: true
                        }
                    }
                }
            });
        }
    </script>

</body>

</html>
