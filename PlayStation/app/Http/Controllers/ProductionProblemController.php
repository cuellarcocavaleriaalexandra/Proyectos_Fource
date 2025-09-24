<?php

// app/Http/Controllers/ProductionProblemController.php
namespace App\Http\Controllers;

use App\Models\ProductionProblem;
use Illuminate\Http\Request;


class ProductionProblemController extends Controller
{
    public function index()
{
    $productionProblems = ProductionProblem::all();
    return view('admin.dashboard', compact('productionProblems'));
}

    public function batchUpdate(Request $request)
{
    $problemsData = $request->input('problems', []);

    foreach ($problemsData as $id => $data) {
        $problem = ProductionProblem::find($id);
        if ($problem) {
            $problem->frequency = $data['frequency'];
            $problem->percentage = $data['percentage'];
            $problem->save();
        }
    }

    return redirect()->route('production-problems.index')->with('success', 'Problemas actualizados correctamente.');
}

}