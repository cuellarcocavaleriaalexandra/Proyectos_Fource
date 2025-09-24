<?php

namespace App\Http\Controllers;

use App\Models\Producto;
use App\Models\Categoria;
use App\Models\Venta;
use App\Models\DetalleVenta;
use App\Models\Cupon;
use App\Models\Cliente;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Barryvdh\DomPDF\Facade\Pdf;

class VentaController extends Controller
{
    public function index(Request $request)
    {
        // Obtener todos las categorías para mostrar en la vista.
        $categorias = Categoria::all();

        // Obtener los parámetros de búsqueda del request.
        $query = $request->input('q');
        $categoriaId = $request->input('categoria');

        // Inicializamos la consulta base para los productos.
        $productos = Producto::query();

        // Solo uno de los filtros se aplicará.
        if ($query) {
            // Si hay un término de búsqueda, ignoramos la categoría.
            $productos->where('nombre', 'like', '%' . $query . '%');
        } elseif ($categoriaId) {
            // Si no hay término de búsqueda, pero se seleccionó una categoría.
            $productos->where('categoria_id', $categoriaId);
        }

        // Ejecutamos la consulta para obtener los productos filtrados.
        $productos = $productos->get();

        // Retornamos la vista con los productos y categorías.
        return view('buscar', [
            'categorias' => $categorias,
            'productos' => $productos,
            'query' => $query,
        ]);
    }

    public function confirmarVenta(Request $request)
    {
        DB::beginTransaction();

        try {
            $productosSeleccionados = $request->input('productos', []);
            $cantidades = $request->input('cantidades', []);
            $codigoCupon = $request->input('codigoCupon');
            $carnetCliente = $request->input('carnetCliente');

            $total = 0;
            $descuentoCupon = 0;
            $descuentoCliente = 0;

            // Validar cupón
            $cupon = $codigoCupon
                ? Cupon::where('codigo', $codigoCupon)
                    ->where('valido_hasta', '>=', now())
                    ->first()
                : null;
            if ($codigoCupon && !$cupon) {
                return response()->json([
                    'success' => false,
                    'error' => 'Cupón no válido o expirado',
                ]);
            }

            // Validar cliente
            $cliente = $carnetCliente
                ? Cliente::where('carnet', $carnetCliente)->first()
                : null;
            if ($carnetCliente && !$cliente) {
                return response()->json([
                    'success' => false,
                    'error' => 'Carnet de cliente no válido',
                ]);
            }

            // Crear venta
            $venta = Venta::create([
                'total' => 0, // Se actualizará después
                'cupon_id' => $cupon->id ?? null,
                'cliente_id' => $cliente->id ?? null,
            ]);

            // Procesar productos
            foreach ($productosSeleccionados as $productoId) {
                $producto = Producto::find($productoId);

                if (!$producto) {
                    return response()->json([
                        'success' => false,
                        'error' => "Producto con ID $productoId no encontrado.",
                    ]);
                }

                $cantidad = $cantidades[$productoId] ?? 1;

                // Verificar si hay suficiente stock
                if ($producto->stock < $cantidad) {
                    return response()->json([
                        'success' => false,
                        'error' => "No hay suficiente stock para el producto: {$producto->nombre}.",
                    ]);
                }

                // Reducir el stock del producto
                $producto->stock -= $cantidad;
                $producto->save();

                // Registrar el detalle de la venta
                DetalleVenta::create([
                    'venta_id' => $venta->id,
                    'producto_id' => $producto->id,
                    'cantidad' => $cantidad,
                    'precio' => $producto->precio,
                    'total' => $producto->precio * $cantidad,
                ]);
            }                    

            // Aplicar descuentos
            if ($cupon) {
                $total -= $total * ($cupon->descuento / 100);
            }
            if ($cliente) {
                $total -= $total * ($cliente->descuento / 100);
            }

            // Guardar total de la venta
            $venta->total = $total;
            $venta->save();

            DB::commit();

            return response()->json([
                'success' => true,
                'venta_id' => $venta->id,
            ]);
        } catch (\Exception $e) {
            DB::rollback();
            \Log::error('Error al confirmar la venta: ' . $e->getMessage());
        
            return response()->json([
                'success' => false,
                'error' => 'Ocurrió un error al procesar la venta. Por favor, intenta nuevamente.',
            ], 500);
        }        
    }

    public function mostrarFactura($id)
    {
        $venta = Venta::with('detalles.producto', 'cliente', 'cupon')->findOrFail($id);
    
        return view('factura', ['venta' => $venta]);
    }    

    public function generarFacturaPDF($id)
    {
        // Buscar la venta y cargar las relaciones necesarias
        $venta = Venta::with(
            'detalles.producto',
            'cliente',
            'cupon'
        )->findOrFail($id);

        // Generar el PDF con la vista 'factura'
        $pdf = Pdf::loadView('factura_pdf', ['venta' => $venta]);

        // Retornar el PDF para que se descargue
        return $pdf->download('factura_' . $venta->id . '.pdf');
    }
}
