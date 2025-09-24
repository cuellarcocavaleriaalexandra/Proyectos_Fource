<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Añadir Producto</title>
    <link rel="stylesheet" href="{{ asset('css/almacen.css') }}">
</head>

<body>
    @include('sidebar')

    <div class="main-content">
        <h1>Añadir Producto</h1>
        <form method="POST" action="{{ route('almacen.guardar') }}" enctype="multipart/form-data">
            @csrf
            <label for="nombre">Nombre:</label>
            <input type="text" id="nombre" name="nombre" required>

            <label for="precio">Precio:</label>
            <input type="number" id="precio" name="precio" step="0.01" required>

            <label for="stock">Stock:</label>
            <input type="number" id="stock" name="stock" required>

            <label for="categoria_id">Categoría:</label>
            <select id="categoria_id" name="categoria_id" required>
                @foreach ($categorias as $categoria)
                    <option value="{{ $categoria->id }}">{{ $categoria->nombre }}</option>
                @endforeach
            </select>

            <button type="submit" class="btn">Guardar Producto</button>
        </form>
        <a href="{{ route('almacen') }}">Volver al Almacén</a>
    </div>
</body>

</html>