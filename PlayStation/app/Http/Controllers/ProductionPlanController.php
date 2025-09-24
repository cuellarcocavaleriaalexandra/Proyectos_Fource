<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\ProductionPlan;

class ProductionPlanController extends Controller
{
     public function index()
    {
        $productionPlans = ProductionPlan::all();
        return view('production-plans.index', compact('productionPlans'));
    }
    
    public function batchUpdate(Request $request)
    {
        $plans = $request->input('plans', []);

        foreach ($plans as $planData) {
            if (isset($planData['id'])) {
                $plan = ProductionPlan::find($planData['id']);
                if ($plan) {
                    $plan->update([
                        'total_cost' => $planData['total_cost'],
                        'advantages' => $planData['advantages'],
                        'disadvantages' => $planData['disadvantages'],
                    ]);
                }
            }
        }

        return redirect()->route('employee.dashboard')->with('success', 'Plan agregado actualizado correctamente.');
    }
}
