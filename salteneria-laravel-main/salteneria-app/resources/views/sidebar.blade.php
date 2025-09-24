<!DOCTYPE html>
<html lang="es">

<head>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    <link rel="stylesheet" href="{{ asset('css/sidebar.css') }}">
</head>

<body>
    <div class="sidebar">
        <h2>{{ Auth::check() && Auth::user()->role === 'admin' ? 'Administrador' : 'Cajero' }}</h2>

        <div class="sidebar-links">
            <a href="{{ route('home') }}" class="{{ request()->routeIs('home') ? 'active' : '' }}">
                <i class="fas fa-home"></i> Inicio
            </a>

            @if (Auth::check() && Auth::user()->role === 'admin')
                <a href="{{ route('almacen') }}" class="{{ request()->routeIs('almacen') ? 'active' : '' }}">
                    <i class="fas fa-boxes"></i> Almacén
                </a>
                <a href="{{ route('reportes') }}" class="{{ request()->routeIs('reportes') ? 'active' : '' }}">
                    <i class="fas fa-chart-bar"></i> Reportes
                </a>
            @endif

            <a href="{{ route('notificaciones') }}" class="{{ request()->routeIs('notificaciones') ? 'active' : '' }}">
                <i class="fas fa-exclamation-triangle"></i> Bajo Stock
            </a>

            @if (Auth::check() && Auth::user()->role === 'cajero')
                <a href="{{ route('buscar') }}" class="{{ request()->routeIs('buscar') ? 'active' : '' }}">
                    <i class="fas fa-shopping-cart"></i> Crear venta
                </a>
            @endif

            <!-- Botón de Cerrar Sesión -->
            <form method="POST" action="{{ route('logout') }}" class="logout-form">
                @csrf
                <button type="submit" class="btn-logout">
                    <i class="fas fa-sign-out-alt"></i> Cerrar Sesión
                </button>
            </form>
        </div>
    </div>
</body>

</html>