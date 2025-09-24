<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
    <link rel="stylesheet" href="{{ asset('css/home.css') }}">
</head>

<body>
    @include('sidebar')
    <div class="main-content">
        <h1>Productos Disponibles</h1>
        <div class="product-list">
            @foreach ($productos as $producto)
                <div class="product-card">
                    <h3>{{ $producto->nombre }}</h3>
                    <p>Precio: {{ $producto->precio }}</p>
                    <p class="stock">Stock: {{ $producto->stock }}</p>
                </div>
            @endforeach
        </div>
    </div>
</body>

</html>