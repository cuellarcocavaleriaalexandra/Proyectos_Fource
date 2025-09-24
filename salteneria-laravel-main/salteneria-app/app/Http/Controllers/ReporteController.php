<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Venta;
use Carbon\Carbon;
use Illuminate\Support\Collection;
use Barryvdh\DomPDF\Facade\Pdf;

class ReporteController extends Controller
{
    public function index(Request $request)
    {
        $filtro = $request->get('filtro', 'dia');
        $ventas_filtradas = $this->obtenerVentasFiltradas($filtro);

        return view('reportes', [
            'filtro' => $filtro,
            'ventas_filtradas' => $ventas_filtradas,
        ]);
    }

    private function obtenerVentasFiltradas($filtro)
    {
        $ventas = Venta::with(['detalles.producto', 'cupon', 'cliente'])->get();
    
        $ventas_filtradas = [];
    
        if ($filtro == 'dia') {
            $ventas_filtradas = $ventas->groupBy(fn($venta) => $venta->created_at->format('Y-m-d'));
        } elseif ($filtro == 'semana') {
            $ventas_filtradas = $ventas->groupBy(fn($venta) => $venta->created_at->format('W-Y'));
        } elseif ($filtro == 'mes') {
            $ventas_filtradas = $ventas->groupBy(fn($venta) => $venta->created_at->format('F Y'));
        }
    
        return $ventas_filtradas;
    }    

    public function generarPDF(Request $request)
    {
        $ventas = Venta::with('detalles.producto', 'cupon', 'cliente')->get();
    
        $filtro = $request->get('filtro', 'mes'); // Captura el filtro que estás aplicando
    
        $ventas_filtradas = $ventas->groupBy(fn($venta) => $venta->created_at->format('F Y'));
    
        $pdf = \PDF::loadView('reporte_pdf', compact('ventas_filtradas', 'filtro'));
    
        return $pdf->download('reporte_ventas.pdf');
    }    
}
