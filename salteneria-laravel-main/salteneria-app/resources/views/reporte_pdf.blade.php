<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <title>Reporte de Ventas - PDF</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }

        h2,
        h3 {
            text-align: center;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }

        th,
        td {
            border: 1px solid #3498db;
            padding: 10px;
            text-align: left;
        }

        th {
            background-color: #3498db;
            color: white;
        }

        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
    </style>
</head>

<body>
    <h2>Reporte de Ventas - {{ ucfirst($filtro) }}</h2>

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
                        // Cálculo del total bruto por día
                        $totalBrutoDia = $ventasDia->sum(fn($venta) => 
                            $venta->detalles->sum(fn($detalle) => $detalle->precio * $detalle->cantidad)
                        );

                        // Cálculo de los descuentos
                        $totalDescuentoDia = $ventasDia->sum(fn($venta) =>
                            ($venta->cupon ? ($venta->detalles->sum(fn($detalle) => $detalle->precio * $detalle->cantidad) * $venta->cupon->descuento / 100) : 0) +
                            ($venta->cliente ? ($venta->detalles->sum(fn($detalle) => $detalle->precio * $detalle->cantidad) * $venta->cliente->obtener_descuento() / 100) : 0)
                        );

                        // Total neto por día
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
</body>

</html>