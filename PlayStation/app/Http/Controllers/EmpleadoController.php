<?php


namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\ProductionPlan;     
use App\Models\ProductMetric;      

class EmpleadoController extends Controller
{
   public function index()
{
    $productMetrics = ProductMetric::all();

    $totalIncome = $productMetrics->sum('income');

    foreach ($productMetrics as $product) {
        $product->profit = $product->income - $product->total_costs;

        $product->profitability = $product->income > 0
            ? ($product->profit / $product->income) * 100
            : 0;

        $product->marketability = $totalIncome > 0
            ? ($product->income / $totalIncome) * 100
            : 0;

        $product->contribution = $product->income > 0
            ? (($product->income - $product->total_costs) / $product->income) * 100
            : 0;

    }

    return view('employee.dashboard', compact('productMetrics'));
}

}
