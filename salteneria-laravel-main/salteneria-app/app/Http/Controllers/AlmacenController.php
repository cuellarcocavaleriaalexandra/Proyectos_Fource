<?php

namespace App\Http\Controllers;

use App\Models\Producto;
use App\Models\Categoria;
use Illuminate\Http\Request;

class AlmacenController extends Controller
{
    public function index(Request $request)
    {
        $query = $request->get('q');
        $categoriaId = $request->get('categoria');

        $productos = Producto::when($query, function ($q) use ($query) {
            return $q->where('nombre', 'like', "%$query%");
        })->when($categoriaId, function ($q) use ($categoriaId) {
            return $q->where('categoria_id', $categoriaId);
        })->with('categoria')->get();

        $categorias = Categoria::all();

        return view('almacen', compact('productos', 'categorias'));
    }

    public function crear()
    {
        $categorias = Categoria::all();
        return view('crear_producto', compact('categorias'));
    }
    
    public function guardar(Request $request)
    {
        Producto::create($request->all());
        return redirect()->route('almacen')->with('success', 'Producto añadido correctamente.');
    }
    
    public function editar($id)
    {
        $producto = Producto::findOrFail($id);
        $categorias = Categoria::all();
        return view('editar_producto', compact('producto', 'categorias'));
    }
    
    public function actualizar(Request $request, $id)
    {
        $producto = Producto::findOrFail($id);
        $producto->update($request->all());
        return redirect()->route('almacen')->with('success', 'Producto actualizado correctamente.');
    }
    
    public function eliminar($id)
    {
        $producto = Producto::findOrFail($id);
        $producto->delete();
        return redirect()->route('almacen')->with('success', 'Producto eliminado correctamente.');
    }    
}