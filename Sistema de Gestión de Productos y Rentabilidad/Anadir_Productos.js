
var productCount = 0;
var products = [];
document.getElementById('companyForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    productCount++;
    var product = document.getElementById('product').value;
    products.push(product);

var row = document.createElement('tr');
row.innerHTML = '<td>' + productCount 
         + '</td><td>' + product ;
document.getElementById('productTable').appendChild(row);
});

document.getElementById('save').addEventListener('click', function(event) {
    event.preventDefault();

    var companyName = document.getElementById('companyName').value;
    if (confirm('¿Estás seguro de que quieres guardar esta empresa y sus productos?')) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "Insertar.php", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onload = function () {
        if (xhr.readyState == 4 && xhr.status == "200") {
            alert("Empresa guardada exitosamente");
            location.reload();
        } else {
            alert("Error al guardar la empresa");
        }
        }
    xhr.send("companyName=" + companyName + "&products=" + JSON.stringify(products));
    }
});