@extends('layouts.app')

@section('content')
<div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-6">Dashboard Empleado</h1>
    
    <!-- Indicadores de Productos -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-8">
        
        <h2 class="text-xl font-semibold mb-4 flex justify-between items-center">
            <span>Indicadores de Productos</span>
            <button onclick="toggleEdit('productMetrics')" class="bg-blue-500 text-white px-3 py-1 rounded text-sm">
                Editar
            </button>
        </h2>
        
        <div id="productMetricsView">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                @foreach($productMetrics as $product)
                <div class="border rounded-lg p-4">
                    <h3 class="font-medium">{{ $product->product_name }}</h3>
                    <div class="mt-2 space-y-1 text-sm">
                        <p>Ingresos: ${{ number_format($product->income, 2) }}</p>
                        <p>Utilidad: ${{ number_format($product->profit, 2) }}</p>
                        <p>Rentabilidad: {{ $product->profitability }}%</p>
                    </div>
                </div>
                @endforeach
            </div>
        </div>
            
       <div id="productMetricsEdit" class="hidden">
    <form action="{{ route('product-metrics.batch-update') }}" method="POST">
        @csrf
        @method('PUT')
        <table class="w-full">
    <thead>
        <tr class="bg-gray-100">
            <th class="p-2">Producto</th>
            <th class="p-2">Ingresos</th>
            <th class="p-2">Costos</th>
            <th class="p-2">Rentabilidad</th>
            <th class="p-2">Comerciabilidad</th>
        </tr>
    </thead>
    <tbody>
        @foreach($productMetrics as $index => $product)
        <tr>
            <td class="p-2 border">{{ $product->product_name }}</td>

            <!-- Campo oculto con el ID -->
            <input type="hidden" name="products[{{ $index }}][id]" value="{{ $product->id }}">

            <td class="p-2 border">
                <input type="number" step="0.01" name="products[{{ $index }}][income]" 
                       value="{{ $product->income }}" class="w-full px-2 py-1 border rounded">
            </td>
            <td class="p-2 border">
                <input type="number" step="0.01" name="products[{{ $index }}][total_costs]" 
                       value="{{ $product->total_costs }}" class="w-full px-2 py-1 border rounded">
            </td>
            <td class="p-2 border">
                <input type="number" step="0.01" name="products[{{ $index }}][profitability]" 
                       value="{{ $product->profitability }}" class="w-full px-2 py-1 border rounded">
            </td>
            <td class="p-2 border">
                <input type="number" step="0.01" name="products[{{ $index }}][marketability]" 
                       value="{{ $product->marketability }}" class="w-full px-2 py-1 border rounded">
            </td>
        </tr>
        @endforeach
    </tbody>
</table>
<div class="mt-4 flex justify-end space-x-2">
            <button type="button" onclick="toggleEdit('productMetrics')" class="bg-gray-500 text-white px-4 py-2 rounded">Cancelar</button>
            <button type="submit" class="bg-green-500 text-white px-4 py-2 rounded">Guardar</button>
        </div>
    </form>
</div>
    
    <!-- Plan Agregado de Producción -->
    <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold mb-4 flex justify-between items-center">
            <span>Plan de Producción</span>
            
        </h2>
        
        <div id="productionPlanView">
            <table class="w-full">
    <thead>
        <tr class="bg-gray-100">
            <th class="p-2">Producto</th>
            <th class="p-2">Utilidad (Bs)</th>
            <th class="p-2">Rentabilidad (%)</th>
            <th class="p-2">Comerciabilidad (%)</th>
            <th class="p-2">Contribución a la utilidad (%)</th>
        </tr>
    </thead>
    <tbody>
        @foreach($productMetrics as $product)
        <tr>
            <td class="p-2 border">{{ $product->product_name }}</td>
            <td class="p-2 border">{{ number_format($product->profit, 2) }}</td>
            <td class="p-2 border">{{ number_format($product->profitability, 2) }}%</td>
            <td class="p-2 border">{{ number_format($product->marketability, 2) }}%</td>
            <td class="p-2 border">{{ number_format($product->contribution, 2) }}%</td>
        </tr>
        @endforeach
    </tbody>
</table>
        </div>
         </div>
</div>

<script>
function toggleEdit(section) {
    document.getElementById(section + 'View').classList.toggle('hidden');
    document.getElementById(section + 'Edit').classList.toggle('hidden');
}
</script>
@endsection