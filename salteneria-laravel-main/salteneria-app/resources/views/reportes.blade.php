@include('sidebar')

<!DOCTYPE html>
<html lang="es">

<head>
    <title>Reporte de Ventas</title>
    <link rel="stylesheet" href="{{ asset('css/reportes.css') }}">
</head>

<body>
    <div class="main-content">
        <h1>Reporte de Ventas</h1>
        <div class="filter-buttons">
            <a href="?filtro=dia" class="{{ request('filtro') == 'dia' ? 'active' : '' }}">Filtrar por Día</a>
            <a href="?filtro=semana" class="{{ request('filtro') == 'semana' ? 'active' : '' }}">Filtrar por Semana</a>
            <a href="?filtro=mes" class="{{ request('filtro') == 'mes' ? 'active' : '' }}">Filtrar por Mes</a>
        </div>

        @if ($filtro == 'dia')
        <h2>Ventas del Día</h2>
        @foreach ($ventas_filtradas as $dia => $ventas)
            <h3>{{ $dia }}</h3>
            <table>
                <thead>
                    <tr>
                        <th>Producto</th>
                        <th>Cantidad</th>
                        <th>Precio Unitario (BOB)</th>
                        <th>Subtotal (BOB)</th>
                        <th>Fecha</th>
                    </tr>
                </thead>
                <tbody>
                    @foreach ($ventas as $venta)
                        @php
                            $totalBruto = $venta->detalles->sum(fn($detalle) => $detalle->precio * $detalle->cantidad);
                            $descuentoCupon = $venta->cupon ? ($totalBruto * $venta->cupon->descuento / 100) : 0;
                            $descuentoCliente = $venta->cliente ? ($totalBruto * $venta->cliente->obtener_descuento() / 100) : 0;
                            $totalNeto = $totalBruto - $descuentoCupon - $descuentoCliente;
                        @endphp

                        <!-- Listar los productos de la venta -->
                        @foreach ($venta->detalles as $detalle)
                            <tr>
                                <td>{{ $detalle->producto->nombre }}</td>
                                <td>{{ $detalle->cantidad }}</td>
                                <td>{{ number_format($detalle->precio, 2) }}</td>
                                <td>{{ number_format($detalle->precio * $detalle->cantidad, 2) }} BOB</td>
                                <td>{{ $venta->created_at->format('d/m/Y') }}</td>
                            </tr>
                        @endforeach

                        <!-- Fila de totales para esta venta -->
                        <tr class="totales-venta">
                            <td colspan="3" style="text-align: right; font-weight: bold;">Total Bruto:</td>
                            <td colspan="2">{{ number_format($totalBruto, 2) }} BOB</td>
                        </tr>
                        <tr class="totales-venta">
                            <td colspan="3" style="text-align: right; font-weight: bold;">Descuento Cupón:</td>
                            <td colspan="2">{{ number_format($descuentoCupon, 2) }} BOB</td>
                        </tr>
                        <tr class="totales-venta">
                            <td colspan="3" style="text-align: right; font-weight: bold;">Descuento Cliente:</td>
                            <td colspan="2">{{ number_format($descuentoCliente, 2) }} BOB</td>
                        </tr>
                        <tr class="totales-venta">
                            <td colspan="3" style="text-align: right; font-weight: bold;">Total Neto:</td>
                            <td colspan="2">{{ number_format($totalNeto, 2) }} BOB</td>
                        </tr>

                        <!-- Espacio entre ventas para mejorar la legibilidad -->
                        <tr><td colspan="5" style="height: 10px;"></td></tr>
                    @endforeach
                </tbody>
            </table>
        @endforeach
        @elseif ($filtro == 'semana')
            <h2>Ventas por Semana</h2>
            @foreach ($ventas_filtradas as $semana => $ventas)
                <h3>Semana {{ $semana }}</h3>
                <table>
                    <thead>
                        <tr>
                            <th class="col-dia">Día</th>
                            <th class="col-total-dia">Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        @foreach ($ventas->groupBy(fn($venta) => $venta->created_at->format('l')) as $dia => $ventasDia)
                            @php
                                $totalBruto = $ventasDia->sum(fn($venta) => $venta->detalles->sum(fn($detalle) => $detalle->precio * $detalle->cantidad));
                                $totalDescuento = $ventasDia->sum(fn($venta) =>
                                    ($venta->cupon ? ($venta->detalles->sum(fn($detalle) => $detalle->precio * $detalle->cantidad) * $venta->cupon->descuento / 100) : 0) +
                                    ($venta->cliente ? ($venta->detalles->sum(fn($detalle) => $detalle->precio * $detalle->cantidad) * $venta->cliente->obtener_descuento() / 100) : 0)
                                );
                                $totalNeto = $totalBruto - $totalDescuento;
                            @endphp

                            <tr>
                                <td>{{ $dia }}</td>
                                <td>{{ number_format($totalNeto, 2) }} BOB</td>
                            </tr>
                        @endforeach
                    </tbody>
                </table>
            @endforeach
            @elseif ($filtro == 'mes')
            <h2>Ventas por Mes</h2>
            <a href="{{ route('reporte.pdf', ['filtro' => 'mes']) }}" class="btn-descargar-pdf">Descargar PDF</a>
            @foreach ($ventas_filtradas as $mes => $ventas)
                <h3>{{ $mes }}</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Día</th>
                            <th>Total del Día (BOB)</th>
                        </tr>
                    </thead>
                    <tbody>
                        @foreach ($ventas->groupBy(fn($venta) => $venta->created_at->format('d')) as $dia => $ventasDia)
                            @php
                                $totalBrutoDia = $ventasDia->sum(fn($venta) => 
                                    $venta->detalles->sum(fn($detalle) => $detalle->precio * $detalle->cantidad)
                                );

                                $totalDescuentoDia = $ventasDia->sum(fn($venta) =>
                                    ($venta->cupon ? ($venta->detalles->sum(fn($detalle) => $detalle->precio * $detalle->cantidad) * $venta->cupon->descuento / 100) : 0) +
                                    ($venta->cliente ? ($venta->detalles->sum(fn($detalle) => $detalle->precio * $detalle->cantidad) * $venta->cliente->obtener_descuento() / 100) : 0)
                                );

                                $totalNetoDia = $totalBrutoDia - $totalDescuentoDia;
                            @endphp

                            <tr>
                                <td>{{ $dia }}</td>
                                <td>{{ number_format($totalNetoDia, 2) }} BOB</td>
                            </tr>
                        @endforeach
                    </tbody>
                </table>
            @endforeach
        @endif
    </div>
</body>

</html>