<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Eliminar Producto</title>
    <link rel="stylesheet" href="{{ asset('css/almacen.css') }}">
</head>

<body>
    @include('sidebar')

    <div class="main-content">
        <h1>Eliminar Producto</h1>
        <p>¿Estás seguro de que deseas eliminar el producto "{{ $producto->nombre }}"?</p>
        <form method="POST" action="{{ route('almacen.eliminar', $producto->id) }}">
            @csrf
            @method('DELETE')

            <button type="submit" class="btn btn-eliminar">Eliminar</button>
            <a href="{{ route('almacen') }}" class="btn btn-cancelar">Cancelar</a>
        </form>
    </div>
</body>

</html>