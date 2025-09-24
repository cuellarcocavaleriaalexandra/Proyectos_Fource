<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Almacén</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{{ asset('css/almacen.css') }}">
    <script src="{{ asset('js/almacen.js') }}"></script>
</head>

<body>
    @include('sidebar')

    <div class="main-content">
        <h1>Almacén</h1>

        <form method="GET" action="{{ route('almacen') }}">
            <input type="text" id="searchInput" name="q" placeholder="Buscar productos..." 
                   value="{{ request()->get('q') }}" oninput="resetCategory()">

            <select name="categoria" id="categoriaSelect" onchange="resetSearchInput()">
                <option value="">Todas las Categorías</option>
                @foreach ($categorias as $categoria)
                    <option value="{{ $categoria->id }}" {{ request('categoria') == $categoria->id ? 'selected' : '' }}>
                        {{ $categoria->nombre }}
                    </option>
                @endforeach
            </select>

            <button type="submit">Buscar</button>
        </form>

        <div class="actions-container">
            <a href="{{ route('almacen.crear') }}" class="btn btn-anadir">
                <i class="fas fa-plus-circle"></i> Añadir Producto
            </a>
        </div>

        <table>
            <thead>
                <tr>
                    <th>Nombre</th>
                    <th>Precio</th>
                    <th>Stock</th>
                    <th>Categoría</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                @forelse ($productos as $producto)
                    <tr>
                        <td>{{ $producto->nombre }}</td>
                        <td>{{ number_format($producto->precio, 2) }} BOB</td>
                        <td>{{ $producto->stock }}</td>
                        <td>{{ $producto->categoria->nombre }}</td>
                        <td>
                            <a href="{{ route('almacen.editar', $producto->id) }}" class="btn btn-editar">
                                <i class="fas fa-edit"></i> Editar
                            </a>
                            <button class="btn btn-eliminar" onclick="confirmarEliminacion('{{ $producto->id }}')">
                                <i class="fas fa-trash"></i> Eliminar
                            </button>
                        </td>
                    </tr>
                @empty
                    <tr>
                        <td colspan="5" style="text-align: center;">No se encontraron productos.</td>
                    </tr>
                @endforelse
            </tbody>
        </table>

        <!-- Modal de Confirmación para Eliminar Producto -->
        <div id="modalEliminar" class="modal" style="display: none;">
            <div class="modal-content">
                <span class="close" onclick="cerrarModal()">&times;</span>
                <h2>Confirmar Eliminación</h2>
                <p>¿Estás seguro de que deseas eliminar este producto?</p>
                <form id="formEliminar" method="POST">
                    @csrf
                    @method('DELETE')
                    <button type="submit" class="btn btn-eliminar">
                        <i class="fas fa-trash"></i> Eliminar
                    </button>
                    <button type="button" class="btn btn-cancelar" onclick="cerrarModal()">
                        Cancelar
                    </button>
                </form>
            </div>
        </div>
    </div>

    <script>
        function confirmarEliminacion(productoId) {
            const form = document.getElementById('formEliminar');
            form.action = `/almacen/eliminar/${productoId}`;
            abrirModal();
        }

        function abrirModal() {
            document.getElementById('modalEliminar').style.display = 'flex';
        }

        function cerrarModal() {
            document.getElementById('modalEliminar').style.display = 'none';
        }

        function resetSearchInput() {
            document.getElementById('searchInput').value = '';
        }

        function resetCategory() {
            document.getElementById('categoriaSelect').value = '';
        }
    </script>
</body>

</html>