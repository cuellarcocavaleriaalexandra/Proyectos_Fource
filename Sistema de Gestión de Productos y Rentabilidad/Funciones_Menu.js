document.getElementById('createCompany').addEventListener('click', function() {
    window.location.href = 'crear_empresa.php';
});

var verButtons = document.getElementsByClassName('ver');
for (var i = 0; i < verButtons.length; i++) {
    verButtons[i].addEventListener('click', function() {
        var companyId = this.getAttribute('data-id');
        window.location.href = 'Opciones_Calculo.php?id=' + companyId;
    });
}

var editarButtons = document.getElementsByClassName('editar');
for (var i = 0; i < editarButtons.length; i++) {
    editarButtons[i].addEventListener('click', function() {
        var companyId = this.getAttribute('data-id');
        window.location.href = 'editar_empresa.php?id=' + companyId;
    });
}

var eliminarButtons = document.getElementsByClassName('eliminar');
for (var i = 0; i < eliminarButtons.length; i++) {
    eliminarButtons[i].addEventListener('click', function() {
        var companyId = this.getAttribute('data-id');
        if (confirm('¿Estás seguro de que quieres eliminar esta empresa?')) {
            var xhr = new XMLHttpRequest();
            xhr.open("GET", "Eliminar.php?id=" + companyId, true);
            xhr.onload = function () {
                if (xhr.readyState == 4 && xhr.status == "200") {
                    alert("Empresa eliminada exitosamente");
                    location.reload();
                } else {
                    alert("Error al eliminar la empresa");
                }
            }
            xhr.send(null);
        }
    });
}

