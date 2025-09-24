<?php

namespace App\Http\Controllers;

use App\Models\ProductionProblem; // Asegúrate que esté importado
use App\Models\ProductMetrics;
use App\Models\ProductionPlan;
use Illuminate\Support\Facades\Auth;

class AdminDashboardController extends Controller
{
    public function index()
    {
        $user = Auth::user();

        if (!$user) {
            abort(403, 'No autenticado');
        }

        if ($user->role === 'empleado') {
            $productMetrics = ProductMetrics::all();
            $productionPlans = ProductionPlan::all();

            return view('employee.dashboard', compact('productMetrics', 'productionPlans'));
        }

        if ($user->role === 'admin') {
            $productionProblems = ProductionProblem::all();

            return view('admin.dashboard', compact('productionProblems'));
        }

        abort(403, 'Rol no autorizado');
    }
}
