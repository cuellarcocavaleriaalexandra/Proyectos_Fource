<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class CompanyController extends Controller
{
    public function store(Request $request)
    {
        // Validación simple
        $data = $request->validate([
            'metric_name' => 'required|string',
            'metric_value' => 'required|string',
        ]);

        // Simulación: guardar en sesión para demo
        session()->push('company_metrics', $data);

        return back()->with('success', 'Datos empresariales guardados correctamente.');
    }
}
