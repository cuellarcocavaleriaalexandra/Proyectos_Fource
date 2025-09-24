// Función para mostrar el modal de eliminación
function confirmarEliminacion(productoId) {
    const form = document.getElementById("formEliminar");
    form.action = `/almacen/eliminar/${productoId}`;
    document.getElementById("modalEliminar").style.display = "flex";
}

// Función para cerrar el modal de eliminación
function cerrarModal() {
    document.getElementById("modalEliminar").style.display = "none";
}

// Función para reiniciar el campo de búsqueda
function resetSearchInput() {
    document.getElementById("searchInput").value = "";
}

// Función para reiniciar la selección de categoría
function resetCategory() {
    document.getElementById("categoriaSelect").value = "";
}

// Evento para cerrar el modal al hacer clic fuera del cuadro
document.addEventListener("click", function (event) {
    const modal = document.getElementById("modalEliminar");
    if (event.target === modal) {
        cerrarModal();
    }
});
