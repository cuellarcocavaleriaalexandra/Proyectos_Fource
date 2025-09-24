@include('sidebar')

<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Venta</title>
    <meta name="csrf-token" content="{{ csrf_token() }}"> <!-- Meta token CSRF -->
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{{ asset('css/buscar.css') }}"> <!-- Agregar estilos CSS -->
</head>

<body>
    <div class="main-content">
        <h1>Buscar Productos</h1>

        <!-- Formulario para Buscar por Nombre -->
        <div class="search-container">
            <form id="search-form" method="GET" action="{{ route('buscar') }}">
                <input type="text" name="q" placeholder="Buscar por nombre" value="{{ request()->get('q') }}">
                <button type="submit">Buscar</button>
            </form>
        </div>

        <!-- Formulario para Filtrar por Categoría -->
        <div class="categories">
            <form id="category-form" method="GET" action="{{ route('buscar') }}">
                <button type="submit" name="categoria" value="" class="{{ request('categoria') ? '' : 'active' }}">
                    Todas las Categorías
                </button>

                @foreach ($categorias as $categoria)
                    <button type="submit" name="categoria" value="{{ $categoria->id }}"
                        class="{{ request('categoria') == $categoria->id ? 'active' : '' }}">
                        {{ $categoria->nombre }}
                    </button>
                @endforeach
            </form>
        </div>

        <h2>Resultados de la búsqueda:</h2>
        <div class="products">
            @forelse ($productos as $producto)
                <div class="product-card" data-product-id="{{ $producto->id }}" data-stock="{{ $producto->stock }}">
                    <img src="{{ asset($producto->imagen) }}" alt="{{ $producto->nombre }}">
                    <h3>{{ $producto->nombre }}</h3>
                    <p>Precio: BOB {{ $producto->precio }}</p>
                    <div class="quantity-control">
                        <button onclick="updateQuantity('{{ $producto->id }}', -1)">-</button>
                        <span id="quantity-{{ $producto->id }}">0</span>
                        <button onclick="updateQuantity('{{ $producto->id }}', 1)">+</button>
                    </div>
                    <button class="add-to-cart-btn"
                        onclick="addToCart('{{ $producto->id }}', '{{ $producto->nombre }}', {{ $producto->precio }})">
                        Agregar al carrito
                    </button>
                </div>
            @empty
                <p>No se encontraron productos.</p>
            @endforelse
        </div>
    </div>

    <div class="cart-summary">
        <div class="cart-summary-header" onclick="toggleCart()">
            <h3>Ticket de Venta</h3>
            <button class="toggle-cart">▲</button>
        </div>
        <div class="cart-content" style="display: none;">
            <div class="cart-items" id="cart-items"></div>
            <p id="total-amount">Total: BOB 0.00</p>
            <div class="cupon-input">
                <input type="text" id="codigo-cupon" placeholder="Código de cupón">
                <button onclick="aplicarCupon()">Aplicar Cupón</button>
            </div>
            <p id="descuento_cupon">Descuento Cupón: 0%</p>
            <div class="cupon-input">
                <input type="text" id="carnet_cliente" placeholder="Carnet del Cliente">
                <button onclick="aplicarCarnet()">Aplicar Descuento Cliente</button>
            </div>
            <p id="descuento_cliente">Descuento Cliente: 0%</p>
            <div class="cart-buttons">
                <button onclick="confirmPurchase()">Confirmar Compra</button>
                <button class="cancel" onclick="cancelPurchase()">Cancelar Compra</button>
            </div>
        </div>
    </div>
    <script src="{{ asset('js/buscar.js') }}"></script> <!-- Agregar script JS -->
</body>

</html>