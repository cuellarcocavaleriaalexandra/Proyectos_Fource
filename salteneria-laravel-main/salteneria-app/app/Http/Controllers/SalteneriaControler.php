<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Producto;
use App\Models\Categoria;

class SalteneriaControler extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        //Obtiene los productos de la BD
        $productos = Producto::all();

        return view('home', compact('productos'));
    }

    public function notificaciones()
    {
        // Obtener productos con stock menor a 10
        $productosBajoStock = Producto::with('categoria')
            ->where('stock', '<', 10)
            ->get();

        // Retornar la vista y pasarle los productos como variable
        return view('notificaciones', ['productos' => $productosBajoStock]);
    }

    /**
     * Show the form for creating a new resource.
     */
    public function create()
    {
        //
    }

    /**
     * Store a newly created resource in storage.
     */
    public function store(Request $request)
    {
        //
    }

    /**
     * Display the specified resource.
     */
    public function show(string $id)
    {
        //
    }

    /**
     * Show the form for editing the specified resource.
     */
    public function edit(string $id)
    {
        //
    }

    /**
     * Update the specified resource in storage.
     */
    public function update(Request $request, string $id)
    {
        //
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy(string $id)
    {
        //
    }
}
