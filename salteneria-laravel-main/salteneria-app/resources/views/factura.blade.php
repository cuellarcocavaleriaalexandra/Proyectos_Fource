
<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Factura de Venta #{{ $venta->id }}</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{{ asset('css/factura.css') }}">
</head>

<body>
@include('sidebar')
    <div class="main-content">
        <h1>Factura de Venta #{{ $venta->id }}</h1>

        <div class="invoice-info">
            <div>
                <h3>Información del Cliente</h3>
                <p><strong>Nombre:</strong> {{ $venta->cliente->nombre ?? 'N/A' }}</p>
                <p><strong>Carnet:</strong> {{ $venta->cliente->carnet ?? 'N/A' }}</p>
            </div>
            <div>
                <h3>Detalles de la Venta</h3>
                <p><strong>Fecha:</strong> {{ $venta->created_at->format('d/m/Y') }}</p>
                <p><strong>Cupón Aplicado:</strong> {{ $venta->cupon->codigo ?? 'Ninguno' }}</p>
            </div>
        </div>

        <div class="product-list">
            <h2>Productos</h2>
            <table>
                <thead>
                    <tr>
                        <th>Producto</th>
                        <th>Cantidad</th>
                        <th>Precio Unitario (BOB)</th>
                        <th>Subtotal (BOB)</th>
                    </tr>
                </thead>
                <tbody>
                    @php
                        $totalBruto = 0;
                    @endphp
                    @foreach ($venta->detalles as $detalle)
                        @php
                            $subtotal = $detalle->precio * $detalle->cantidad;
                            $totalBruto += $subtotal;
                        @endphp
                        <tr>
                            <td>{{ $detalle->producto->nombre }}</td>
                            <td>{{ $detalle->cantidad }}</td>
                            <td>{{ number_format($detalle->precio, 2) }}</td>
                            <td>{{ number_format($subtotal, 2) }}</td>
                        </tr>
                    @endforeach
                </tbody>
            </table>
        </div>

        @php
            $descuentoCupon = $venta->cupon ? ($totalBruto * $venta->cupon->descuento / 100) : 0;
            $descuentoCliente = $venta->cliente ? ($totalBruto * $venta->cliente->obtener_descuento() / 100) : 0;
            $totalNeto = $totalBruto - $descuentoCupon - $descuentoCliente;
        @endphp

        <div class="total">
            <p><strong>Total Bruto:</strong> BOB {{ number_format($totalBruto, 2) }}</p>
            <p><strong>Descuento por Cupón:</strong> BOB {{ number_format($descuentoCupon, 2) }}</p>
            <p><strong>Descuento por Cliente:</strong> BOB {{ number_format($descuentoCliente, 2) }}</p>
            <p><strong>Total Neto:</strong> BOB {{ number_format($totalNeto, 2) }}</p>
        </div>

        <a href="{{ route('factura.pdf', $venta->id) }}" class="btn pdf-btn">Descargar PDF</a>
        <a href="{{ route('home') }}" class="btn">Volver al Inicio</a>

        <div class="footer">
            <p>Gracias por su compra. ¡Esperamos verlo pronto!</p>
        </div>
    </div>
</body>

</html>