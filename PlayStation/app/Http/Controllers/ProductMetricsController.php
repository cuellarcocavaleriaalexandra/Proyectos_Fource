<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\ProductMetric;

class ProductMetricsController extends Controller
{
    public function index()
    {
        $productMetrics = ProductMetric::all(); // singular aquí también
        return view('product-metrics.index', compact('productMetrics'));
    }
    
    public function batchUpdate(Request $request)
    {
        $products = $request->input('products', []);

        foreach ($products as $productData) {
            if (isset($productData['id'])) {
                $productMetric = ProductMetric::find($productData['id']);
                if ($productMetric) {
                    $productMetric->update([
                        'income' => $productData['income'],
                        'total_costs' => $productData['total_costs'],
                        'profitability' => $productData['profitability'],
                        'marketability' => $productData['marketability'],
                    ]);
                }
            }
        }

        return redirect()->route('employee.dashboard')->with('success', 'Métricas actualizadas correctamente.');
    }
}
