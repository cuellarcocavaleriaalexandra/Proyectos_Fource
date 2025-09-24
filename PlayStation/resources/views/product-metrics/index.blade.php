@extends('layouts.app') 

@section('content')
<div class="container mx-auto px-4 py-8">
    <!-- Botón para volver al dashboard -->
    <a href="{{ route('dashboard') }}" 
       class="inline-block mb-6 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">
       ← Volver al Dashboard
    </a>

    <h1 class="text-3xl font-bold mb-4">Indicadores de Producto</h1>

    <div class="overflow-x-auto">
        <table class="min-w-full bg-white shadow rounded-lg overflow-hidden">
            <thead class="bg-gray-100 text-gray-700">
                <tr>
                    <th class="px-4 py-2 text-left">ID</th>
                    <th class="px-4 py-2 text-left">Ingreso ($)</th>
                    <th class="px-4 py-2 text-left">Costos Totales ($)</th>
                    <th class="px-4 py-2 text-left">Rentabilidad (%)</th>
                    <th class="px-4 py-2 text-left">Comerciabilidad (%)</th>
                </tr>
            </thead>
            <tbody class="text-gray-800">
                @foreach($productMetrics as $metric)
                    <tr class="border-b hover:bg-gray-50">
                        <td class="px-4 py-2">{{ $metric->id }}</td>
                        <td class="px-4 py-2">${{ number_format($metric->income, 2) }}</td>
                        <td class="px-4 py-2">${{ number_format($metric->total_costs, 2) }}</td>
                        <td class="px-4 py-2">{{ number_format($metric->profitability, 2) }}%</td>
                        <td class="px-4 py-2">{{ number_format($metric->marketability, 2) }}%</td>
                    </tr>
                @endforeach
            </tbody>
        </table>
    </div>
</div>
@endsection
