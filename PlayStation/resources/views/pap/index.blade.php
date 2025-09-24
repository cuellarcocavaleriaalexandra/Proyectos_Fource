@extends('layouts.app')

@section('content')
<div class="container mx-auto py-6">
    <h1 class="text-2xl font-bold mb-4">📊 Plan Agregado de Producción</h1>

    <table class="w-full border mb-6 text-sm">
        <thead class="bg-gray-100">
            <tr>
                <th class="p-2 border">Alternativa</th>
                <th class="p-2 border">Costo Total (Bs)</th>
                <th class="p-2 border">Ver</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="p-2 border">Inventario Cero</td>
                <td class="p-2 border">49,500</td>
                <td class="p-2 border text-center">
                    <a href="{{ route('pap.alternativa', 'inventario-cero') }}" class="text-blue-500 underline">Ver</a>
                </td>
            </tr>
            <tr>
                <td class="p-2 border">Subcontratación Parcial</td>
                <td class="p-2 border">46,000</td>
                <td class="p-2 border text-center">
                    <a href="{{ route('pap.alternativa', 'subcontratacion') }}" class="text-blue-500 underline">Ver</a>
                </td>
            </tr>
        </tbody>
    </table>
</div>
@endsection
