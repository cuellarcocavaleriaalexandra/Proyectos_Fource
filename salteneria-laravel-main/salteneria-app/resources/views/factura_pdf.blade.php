<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <title>Factura de Venta #{{ $venta->id }}</title>
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            padding: 40px;
            background-color: #fff;
            color: #333;
            margin: 0;
        }

        h1 {
            text-align: center;
            color: #2c3e50;
            margin-bottom: 10px;
        }

        .invoice-info {
            display: flex;
            justify-content: space-between;
            margin-bottom: 20px;
        }

        .invoice-info div {
            width: 48%;
        }

        .invoice-info h3 {
            margin-bottom: 5px;
            color: #3498db;
        }

        .invoice-info p {
            margin: 0;
            font-size: 14px;
            color: #7f8c8d;
        }

        .product-list {
            margin-top: 20px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }

        th, td {
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }

        th {
            background-color: #3498db;
            color: white;
            font-weight: 700;
        }

        td {
            color: #2c3e50;
        }

        .total {
            text-align: right;
            margin-top: 10px;
            font-size: 20px;
            font-weight: bold;
            color: #2c3e50;
        }

        .footer {
            margin-top: 30px;
            text-align: center;
            font-size: 14px;
            color: #7f8c8d;
        }

        .footer-line {
            width: 100%;
            height: 1px;
            background-color: #ddd;
            margin: 20px 0;
        }
    </style>
</head>

<body>
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

    <div class="footer-line"></div>

    <div class="footer">
        <p>Gracias por su compra. ¡Esperamos verlo pronto!</p>
        <p>Generado automáticamente el {{ now()->format('d/m/Y H:i') }}</p>
    </div>
</body>

</html>