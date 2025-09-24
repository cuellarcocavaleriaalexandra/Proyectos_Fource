@extends('layouts.app')

@section('content')
<div class="bg-white rounded-lg shadow-md p-6 mb-6">
    <!-- Encabezado mejorado -->
    <div class="flex flex-col md:flex-row md:justify-between md:items-center mb-6 gap-4">
        <h2 class="text-2xl font-semibold text-gray-800">Plan Agregado de Producción</h2>
        
        <div class="flex flex-col sm:flex-row gap-2">
            
            <a href="{{ route('dashboard') }}" 
               class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-md text-center transition-colors duration-200">
                Volver al Dashboard
            </a>
            <a href="{{ route('pap.index') }}" 
               class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-md text-center transition-colors duration-200">
                Ver alternativas
</a>
        </div>
    </div>

    <!-- Vista de visualización -->
    <div id="productionPlanView">
        <div class="overflow-x-auto">
            <table class="w-full min-w-max">
                <thead>
                    <tr class="bg-playstation-blue text-white">
                        <th class="p-3 text-left">Alternativa</th>
                        <th class="p-3 text-left">Costo Total (Bs)</th>
                        <th class="p-3 text-left">Ventajas</th>
                        <th class="p-3 text-left">Desventajas</th>
                    </tr>
                </thead>
                <tbody>
                    @foreach($productionPlans as $plan)
                    <tr class="border-b hover:bg-gray-50 transition-colors duration-150">
                        <td class="p-3">{{ $plan->alternative_name }}</td>
                        <td class="p-3">{{ number_format($plan->total_cost, 2) }}</td>
                        <td class="p-3">{{ $plan->advantages }}</td>
                        <td class="p-3">{{ $plan->disadvantages }}</td>
                    </tr>
                    @endforeach
                </tbody>
            </table>
        </div>
    </div>
    
    <!-- Vista de edición (oculta inicialmente) -->
    <div id="productionPlanEdit" class="hidden mt-6">
        <form method="POST" action="{{ route('production-plans.batch-update') }}">
            @csrf
            @method('PUT')
            
            <div class="overflow-x-auto">
                <table class="w-full min-w-max">
                    <thead>
                        <tr class="bg-playstation-blue text-white">
                            <th class="p-3 text-left">Alternativa</th>
                            <th class="p-3 text-left">Costo Total (Bs)</th>
                            <th class="p-3 text-left">Ventajas</th>
                            <th class="p-3 text-left">Desventajas</th>
                        </tr>
                    </thead>
                    <tbody>
                        @foreach($productionPlans as $index => $plan)
                        <tr class="border-b hover:bg-gray-50 transition-colors duration-150">
                            <td class="p-3">{{ $plan->alternative_name }}</td>
                            <input type="hidden" name="plans[{{ $index }}][id]" value="{{ $plan->id }}">
                            
                            <td class="p-3">
                                <input type="number" step="0.01" 
                                       name="plans[{{ $index }}][total_cost]" 
                                       value="{{ $plan->total_cost }}" 
                                       class="w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-playstation-blue focus:border-transparent">
                            </td>
                            <td class="p-3">
                                <input type="text" 
                                       name="plans[{{ $index }}][advantages]" 
                                       value="{{ $plan->advantages }}" 
                                       class="w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-playstation-blue focus:border-transparent">
                            </td>
                            <td class="p-3">
                                <input type="text" 
                                       name="plans[{{ $index }}][disadvantages]" 
                                       value="{{ $plan->disadvantages }}" 
                                       class="w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-playstation-blue focus:border-transparent">
                            </td>
                        </tr>
                        @endforeach
                    </tbody>
                </table>
            </div>
            
            <div class="mt-6 flex justify-end space-x-3">
                <button type="button" 
                        onclick="toggleEdit('productionPlan')" 
                        class="bg-gray-500 hover:bg-gray-600 text-white px-5 py-2 rounded-md transition-colors duration-200">
                    Cancelar
                </button>
                <button type="submit" 
                        class="bg-green-500 hover:bg-green-600 text-white px-5 py-2 rounded-md transition-colors duration-200">
                    Guardar Cambios
                </button>
            </div>
        </form>
    </div>
</div>

<script>
function toggleEdit(section) {
    const viewElement = document.getElementById(`${section}View`);
    const editElement = document.getElementById(`${section}Edit`);
    
    viewElement.classList.toggle('hidden');
    editElement.classList.toggle('hidden');
    
    // Si se está mostrando el formulario, hacer scroll a la sección
    if (!editElement.classList.contains('hidden')) {
        editElement.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}
</script>
@endsection