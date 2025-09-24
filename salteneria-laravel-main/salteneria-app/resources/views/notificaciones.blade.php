<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Notificaciones</title>
    <link rel="stylesheet" href="{{ asset('css/notificaciones.css') }}" />
</head>

<body>
    @include('sidebar')

    <div class="main-content">
        <h1>Productos con Bajo Stock</h1>
        <div class="notifications">
            @foreach ($productos as $producto)
                <div class="notification-card">
                    <h3>{{ $producto->nombre }}</h3>
                    <p>Categoría: {{  $producto->categoria->nombre }}</p>
                    <p class="stock">Stock: {{ $producto->stock }} unidades</p>
                    <!-- <button class="notify-btn">Reportar</button>-->
                </div>
            @endforeach
        </div>
    </div>
</body>

</html>