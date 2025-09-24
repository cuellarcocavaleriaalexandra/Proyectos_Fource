@extends('layouts.app')

@section('content')
<div class="container mx-auto py-6">
    <h2 class="text-2xl font-bold mb-4">🧮 Alternativa: {{ $titulo }}</h2>

    <table class="table-auto w-full text-sm border mb-4">
        <thead class="bg-gray-100">
            <tr>
                @foreach(array_keys($tabla[0]) as $col)
                    <th class="p-2 border">{{ ucfirst(str_replace('_', ' ', $col)) }}</th>
                @endforeach
            </tr>
        </thead>
        <tbody>
            @foreach($tabla as $fila)
                <tr>
                    @foreach($fila as $valor)
                        <td class="p-2 border">{{ $valor }}</td>
                    @endforeach
                </tr>
            @endforeach
        </tbody>
    </table>

    <div class="text-right font-semibold text-lg">
        Costo Total: <span class="text-green-600">{{ number_format($costo_total, 0, ',', '.') }} Bs</span>
    </div>

    <div class="mt-6">
        <a href="{{ route('pap.index') }}" class="bg-gray-500 text-white px-4 py-2 rounded">⬅ Volver al resumen</a>
    </div>
</div>
@endsection
