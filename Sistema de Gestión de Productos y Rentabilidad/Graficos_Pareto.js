//libreria para utilizar las gráficas
src="https://cdn.jsdelivr.net/npm/chart.js"

var data = [];
var paretoChart; // Variable para almacenar la instancia del gráfico de Pareto

document.getElementById('data-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    var gestion = document.getElementById('gestion').value;
    var mes = document.getElementById('mes').value;
    var articleNameValue = document.getElementById('articleName').value;
    var articleId = articleNameValue.split('|')[0];
    var articleName = articleNameValue.split('|')[1];
    var unidades = document.getElementById('unidades').value;
    var precio = document.getElementById('precio').value;
    var ventas = unidades * precio;
    
    // Validar si ya existe un objeto con el mismo año, mes y nombre de artículo
    var exists = data.some(function(el) {
        return el.gestion === gestion && el.mes === mes && el.articleName === articleName;
    });
    
    if (!exists) {
        data.push({gestion: gestion,
                   mes: mes,
                   articleId: articleId,
                   articleName: articleName,
                   unidades: unidades, 
                   precio: precio, 
                   ventas: ventas});
        
        addData();
    } else {
        alert('Ya has añadido datos para este artículo en el mismo mes y año. Por favor, cambia de artículo o de mes.');
    }
});

function addData() {
    var dataTable = document.getElementById('data-table');
    var resultsTable = document.getElementById('results-table');
    
    // Limpiar tablas
    dataTable.innerHTML = '<tr><th>Gestion</th><th>Mes</th><th>ID</th><th>Nombre</th><th>Unidades</th><th>Precio Unitario</th><th>Ventas</th></tr>';
    resultsTable.innerHTML = '<tr><th>ID</th><th>Nombre</th><th>Ventas Totales</th><th>Porcentaje Acumulado</th><th>Porcentaje Acumulado %</th></tr>';
    
    // Ordenar datos por ventas
    data.sort((a, b) => b.ventas - a.ventas);
    
    var totalVentas = data.reduce((total, item) => total + item.ventas, 0);
    var acumulado = 0;
    
    var nombres = [];
    var ventasTotales = [];
    var porcentajesAcumulados = [];
    
    // Reiniciar los arrays antes de agregar los nuevos datos
    for (var i = 0; i < data.length; i++) {
        // Añadir fila a la tabla de datos
        var dataRow = dataTable.insertRow(-1);
        
        dataRow.insertCell(0).innerHTML = data[i].gestion;
        dataRow.insertCell(1).innerHTML = data[i].mes;
        dataRow.insertCell(2).innerHTML = data[i].articleId;
        dataRow.insertCell(3).innerHTML = data[i].articleName;
        dataRow.insertCell(4).innerHTML = data[i].unidades;
        dataRow.insertCell(5).innerHTML = data[i].precio;
        dataRow.insertCell(6).innerHTML = data[i].ventas;
        
        // Calcular porcentaje acumulado
        acumulado += data[i].ventas;
        var porcentaje = acumulado / totalVentas * 100;
        
        // Añadir fila a la tabla de resultados
        var resultsRow = resultsTable.insertRow(-1);
        resultsRow.insertCell(0).innerHTML = data[i].articleId;
        resultsRow.insertCell(1).innerHTML = data[i].articleName;
        resultsRow.insertCell(2).innerHTML = data[i].ventas;
        resultsRow.insertCell(3).innerHTML = acumulado;
        resultsRow.insertCell(4).innerHTML = porcentaje.toFixed(2) + '%';
        
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

// Función para recoger los datos de la tabla
function getTableData(tableID) {
    var table = document.getElementById(tableID);
    var data = [];
    // Iterar sobre las filas de la tabla
    for (var i = 1; i < table.rows.length; i++) {
        var row = table.rows[i];
        var rowData = {};
        // Iterar sobre las celdas de la fila
        for (var j = 0; j < row.cells.length; j++) {
            var cell = row.cells[j];
            var header = table.rows[0].cells[j].innerText;
            rowData[header] = cell.innerText;
        }
        data.push(rowData);
    }
    return data;
}

document.getElementById('saveTable').addEventListener('click', function(event){
    event.preventDefault();

    // Recoger los datos de las tablas
    var dataTable = getTableData('data-table');
    var resultsTable = getTableData('results-table');

    // Crear un objeto FormData y añadir los datos de las tablas
    var formData = new FormData();
    formData.append('dataTable', JSON.stringify(dataTable));
    formData.append('results-Table', JSON.stringify(resultsTable));


    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'Insertar_Pareto.php', true);
    xhr.onload = function () {
        if (xhr.status === 200) {
            alert('Datos guardados correctamente');
        } else {
            alert('Un error ocurrió durante la operación');
        }
    };
    xhr.send(formData);
});