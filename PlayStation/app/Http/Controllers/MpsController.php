<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class MpsController extends Controller
{
    public function store(Request $request)
    {
        $data = $request->validate([
            'period' => 'required|string',
            'month' => 'nullable|string',
            'day' => 'nullable|date',
            'demand' => 'required|numeric',
            'production' => 'required|numeric',
            'subcontract' => 'required|numeric',
            'cost' => 'required|numeric',
        ]);

        // Simulación: guardar en sesión para demo
        session()->push('mps_entries', $data);

        return back()->with('success', 'Plan maestro guardado correctamente.');
    }
}
