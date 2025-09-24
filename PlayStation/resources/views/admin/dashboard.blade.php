@extends('layouts.app')
    
@section('content')
<div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-6">Dashboard Administrador</h1>
    
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Diagrama de Pareto -->
        <div class="bg-white rounded-lg shadow-md p-6 lg:col-span-2">
            <h2 class="text-xl font-semibold mb-4">Diagrama de Pareto - Problemas en Producción</h2>
            <canvas id="paretoChart" height="300"></canvas>
            
            <div class="mt-6">
                <button onclick="toggleEdit('pareto')" class="bg-blue-500 text-white px-4 py-2 rounded">
                    Editar Datos
                </button>
                
                <div id="paretoEdit" class="hidden mt-4">
                    <form method="POST" action="{{ route('production-problems.batch-update') }}">
                        @csrf
                        @method('PUT')
                        <table class="w-full">
                            <thead>
                                <tr class="bg-gray-100">
                                    <th class="p-2">Problema</th>
                                    <th class="p-2">Frecuencia</th>
                                    <th class="p-2">% Sobre Total</th>
                                </tr>
                            </thead>
                            <tbody>
                                @foreach($productionProblems as $problem)
                                <tr>
                                    <td class="p-2 border">{{ $problem->problem_name }}</td>
                                    <td class="p-2 border">
                                        <input type="number" name="problems[{{ $problem->id }}][frequency]" 
                                               value="{{ $problem->frequency }}" class="w-full px-2 py-1 border rounded">
                                    </td>
                                    <td class="p-2 border">
                                        <input type="number" step="0.01" name="problems[{{ $problem->id }}][percentage]" 
                                               value="{{ $problem->percentage }}" class="w-full px-2 py-1 border rounded">
                                    </td>
                                </tr>
                                @endforeach
                            </tbody>
                        </table>
                        <div class="mt-4 flex justify-end space-x-2">
                            <button type="button" onclick="toggleEdit('pareto')" class="bg-gray-500 text-white px-4 py-2 rounded">
                                Cancelar
                            </button>
                            <button type="submit" class="bg-green-500 text-white px-4 py-2 rounded">
                                Guardar
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        
        <!-- Accesos Rápidos -->
        <div class="bg-white rounded-lg shadow-md p-6">
            <h2 class="text-xl font-semibold mb-4">Accesos Rápidos</h2>
            <div class="space-y-3">
                <a href="{{ route('product-metrics.index') }}" class="block p-3 bg-blue-100 hover:bg-blue-200 rounded-lg">
                    Indicadores de Productos
                </a>
                <a href="{{ route('production-plans.index') }}" class="block p-3 bg-green-100 hover:bg-green-200 rounded-lg">
                    Plan Agregado de Producción
                </a>
                <a href="{{ route('production-problems.index') }}" class="block p-3 bg-purple-100 hover:bg-purple-200 rounded-lg">
                    Problemas de Producción
                </a>
                <a href="{{ route('pap.index') }}" class="block p-3 bg-purple-100 hover:bg-grey-200 rounded-lg">
                    Ver Plan Agregado de Producción</a>
        
            </div>
            
            <!-- Gráfico de Flujo -->
            <div class="mt-6">
                <h3 class="text-lg font-medium mb-2">Flujo de Producción</h3>
                <canvas id="flowChart" height="200"></canvas>
            </div>
        </div>
    </div>
</div>

<!-- Incluir Chart.js -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
// Diagrama de Pareto
const paretoCtx = document.getElementById('paretoChart').getContext('2d');
const paretoChart = new Chart(paretoCtx, {
    type: 'bar',
    data: {
        labels: @json($productionProblems->pluck('problem_name')),
        datasets: [
            {
                label: 'Frecuencia',
                data: @json($productionProblems->pluck('frequency')),
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            },
            {
                label: '% Acumulado',
                data: @json($productionProblems->pluck('cumulative_percentage')),
                type: 'line',
                borderColor: 'rgba(255, 99, 132, 1)',
                backgroundColor: 'rgba(255, 99, 132, 0.1)',
                fill: true,
                yAxisID: 'y1'
            }
        ]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Frecuencia'
                }
            },
            y1: {
                position: 'right',
                beginAtZero: true,
                max: 100,
                title: {
                    display: true,
                    text: '% Acumulado'
                },
                grid: {
                    drawOnChartArea: false
                }
            }
        }
    }
});

// Gráfico de Flujo
const flowCtx = document.getElementById('flowChart').getContext('2d');
const flowChart = new Chart(flowCtx, {
    type: 'line',
    data: {
        labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
        datasets: [{
            label: 'Producción Mensual',
            data: [1200, 1900, 1700, 2100, 2300, 2500],
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: false
            }
        }
    }
});

function toggleEdit(section) {
    document.getElementById(section + 'Edit').classList.toggle('hidden');
}
</script>
@endsection