var data=[];
var dataresults=[];
var totalSalesIncome =0;
document.getElementById('calculatorForm').addEventListener('submit', function(event) {
  event.preventDefault();

  var gestion = document.getElementById('gestion').value;
  var mes = document.getElementById('mes').value;
  var articleNameValue = document.getElementById('articleName').value;
  var articleId = articleNameValue.split('|')[0];
  var articleName = articleNameValue.split('|')[1];
  var fixedCosts = parseFloat(document.getElementById('fixedCosts').value);
  var administrativeCosts = parseFloat(document.getElementById('administrativeCosts').value);
  var commercialCosts = parseFloat(document.getElementById('commercialCosts').value);
  var salesIncome = parseFloat(document.getElementById('salesIncome').value);
  var variableCost = parseFloat(document.getElementById('variableCost').value);
  
    // Calcular las utilidades
    var utilities = salesIncome - (fixedCosts + variableCost + administrativeCosts + commercialCosts);

    // Añadir los ingresos por venta al total de ingresos por venta
    totalSalesIncome += salesIncome;
  
    var Costototal = fixedCosts + variableCost + administrativeCosts + commercialCosts ; 

// Validar si ya existe un objeto con el mismo año, mes y nombre de artículo
var exists = data.some(function(el) {
  return el.gestion === gestion && el.mes === mes && el.articleName === articleName;
});
if (!exists) {
    data.push({gestion: gestion,
               mes: mes,
               articleId: articleId,
               articleName: articleName,
               utilities: utilities,
               salesIncome: salesIncome,
               totalSalesIncome: totalSalesIncome,
               Costototal: Costototal});
    addData();
} else {
    alert('Ya has añadido datos para este artículo en el mismo mes y año. Por favor, cambia de artículo o de mes.');
}

  // Calcular la rentabilidad de ventas, el índice de comerciabilidad y la contribución utilitaria
  var salesProfitability = utilities / salesIncome;
  var tradeIndex = salesIncome / totalSalesIncome;
  var utilityContribution = (salesIncome - variableCost) / salesIncome;

  var conclusion = '';
  if(salesProfitability > 0.6 && tradeIndex > 0.6 && utilityContribution > 0.6) {
    conclusion = 'Excelente rendimiento';
  } else if(salesProfitability > 0.3 && tradeIndex > 0.3 && utilityContribution > 0.3) {
    conclusion = 'Buen rendimiento';
  } else {
    conclusion = 'Rendimiento necesita mejorar';
  }

  dataresults.push({articleId: articleId, articleName: articleName,salesProfitability: salesProfitability, tradeIndex: tradeIndex, utilityContribution: utilityContribution, conclusion: conclusion});

  addDataResults();
  updateTradeIndex(); 

});
  
function addData(){
  var dataTable = document.getElementById('data-Table');
  dataTable.innerHTML = '<tr><th>Gestion</th><th>Mes</th><th>ID</th><th>Artículo</th><th>Utilidades</th><th>Ingreso por Venta</th><th>Ingresos Totales por Venta</th><th>Costo Total</th></tr>';
    // Reiniciar los arrays antes de agregar los nuevos datos
    for (var i = 0; i < data.length; i++) {
        // Añadir fila a la tabla de datos
        var dataRow = dataTable.insertRow(-1);
        dataRow.insertCell(0).innerHTML = data[i].gestion;
        dataRow.insertCell(1).innerHTML = data[i].mes;
        dataRow.insertCell(2).innerHTML = data[i].articleId;
        dataRow.insertCell(3).innerHTML = data[i].articleName;
        dataRow.insertCell(4).innerHTML = data[i].utilities;
        dataRow.insertCell(5).innerHTML = data[i].salesIncome;
        dataRow.insertCell(6).innerHTML = totalSalesIncome; // Actualizar el 'Ingreso Total por Venta' para todos los productos
        dataRow.insertCell(7).innerHTML = data[i].Costototal;
      }
  }
function addDataResults(){
    var dataTable = document.getElementById('resultsTable');
    dataTable.innerHTML = '<tr><th>ID</th><th>Artículo</th><th>Rentabilidad de Ventas</th><th>Índice de Comerciabilidad</th><th>Contribución Utilitaria</th><th>Acciones</th></tr>';
      // Reiniciar los arrays antes de agregar los nuevos datos
      for (var i = 0; i < dataresults.length; i++) {
        // Añadir fila a la tabla de datos
        var dataRow = dataTable.insertRow(-1);
        dataRow.insertCell(0).innerHTML = dataresults[i].articleId;
        dataRow.insertCell(1).innerHTML = dataresults[i].articleName;
        dataRow.insertCell(2).innerHTML = dataresults[i].salesProfitability;
        dataRow.insertCell(3).innerHTML = dataresults[i].tradeIndex;
        dataRow.insertCell(4).innerHTML = dataresults[i].utilityContribution;
        dataRow.insertCell(5).innerHTML = dataresults[i].conclusion;
    }
  }

  function updateTradeIndex() {
  // Calcular e insertar el índice de comerciabilidad actualizado para cada producto
  var dataTable = document.getElementById('resultsTable');
  for (var i = 0; i < data.length; i++) {
    var tradeIndex = data[i].salesIncome / totalSalesIncome;
    dataTable.rows[i + 1].cells[3].innerHTML = tradeIndex.toFixed(2);
  }
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
    var dataTable = getTableData('data-Table');
    var resultsTable = getTableData('resultsTable');

    // Crear un objeto FormData y añadir los datos de las tablas
    var formData = new FormData();
    formData.append('dataTable', JSON.stringify(dataTable));
    formData.append('resultsTable', JSON.stringify(resultsTable));


    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'Insertar_Rentabilidad.php', true);
    xhr.onload = function () {
        if (xhr.status === 200) {
            alert('Datos guardados correctamente');
        } else {
            alert('Un error ocurrió durante la operación');
        }
    };
    xhr.send(formData);
});

function getTableData(tableID) {
    var table = document.getElementById(tableID);
    var data = [];
    // Check if table exists
    if (!table) {
        console.error('Table with ID ' + tableID + ' does not exist.');
        return data;
    }
    // Iterar sobre las filas de la tabla
    for (var i = 1; i < table.rows.length; i++) {
        var row = table.rows[i];
        var rowData = {};
        // Iterar sobre las celdas de la fila
        for (var j = 0; j < row.cells.length; j++) {
            var cell = row.cells[j];
            // Check if header cell exists
            if (!table.rows[0].cells[j]) {
                console.error('Header cell at index ' + j + ' does not exist.');
                continue;
            }
            var header = table.rows[0].cells[j].innerText;
            rowData[header] = cell.innerText;
        }
        data.push(rowData);
    }
    return data;
}
