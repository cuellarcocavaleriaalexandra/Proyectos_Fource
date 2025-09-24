<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class PapController extends Controller
{
    public function index()
    {
        return view('pap.index'); 
    }

    public function show($tipo)
    {
        
        $data = match ($tipo) {
            'inventario-cero' => [
                'titulo' => 'Inventario Cero',
                'tabla' => [
                    ['mes' => 'Enero', 'demanda' => 3000, 'produccion' => 3000, 'contratacion' => 10, 'despidos' => 0, 'costo' => 16000],
                    ['mes' => 'Febrero', 'demanda' => 2500, 'produccion' => 2500, 'contratacion' => 0, 'despidos' => 5, 'costo' => 14500],
                    ['mes' => 'Marzo', 'demanda' => 4000, 'produccion' => 4000, 'contratacion' => 15, 'despidos' => 0, 'costo' => 19000],
                ],
                'costo_total' => 49500,
            ],
            'constante' => [
                'titulo' => 'Fuerza de Trabajo Constante',
                'tabla' => [
                    ['mes' => 'Enero', 'demanda' => 3000, 'produccion' => 3200, 'inventario' => 200, 'almacenamiento' => 200, 'costo' => 16500],
                    ['mes' => 'Febrero', 'demanda' => 2500, 'produccion' => 3200, 'inventario' => 900, 'almacenamiento' => 900, 'costo' => 15500],
                    ['mes' => 'Marzo', 'demanda' => 4000, 'produccion' => 3200, 'inventario' => 100, 'almacenamiento' => 100, 'costo' => 18000],
                ],
                'costo_total' => 50000,
            ],
            'subcontratacion' => [
                'titulo' => 'Subcontratación Parcial',
                'tabla' => [
                    ['mes' => 'Enero', 'demanda' => 3000, 'produccion' => 2000, 'subcontratacion' => 1000, 'costo_sub' => 3000, 'costo' => 15000],
                    ['mes' => 'Febrero', 'demanda' => 2500, 'produccion' => 2000, 'subcontratacion' => 500, 'costo_sub' => 1500, 'costo' => 14000],
                    ['mes' => 'Marzo', 'demanda' => 4000, 'produccion' => 2500, 'subcontratacion' => 1500, 'costo_sub' => 4500, 'costo' => 17000],
                ],
                'costo_total' => 46000,
            ],
            'contratar-despedir' => [
                'titulo' => 'Contratar/Despedir Según Necesidad',
                'tabla' => [
                    ['mes' => 'Enero', 'demanda' => 3000, 'contratacion' => 12, 'despidos' => 0, 'mano_obra' => 'Alta', 'costo' => 17000],
                    ['mes' => 'Febrero', 'demanda' => 2500, 'contratacion' => 0, 'despidos' => 6, 'mano_obra' => 'Media', 'costo' => 14500],
                    ['mes' => 'Marzo', 'demanda' => 4000, 'contratacion' => 15, 'despidos' => 0, 'mano_obra' => 'Alta', 'costo' => 20000],
                ],
                'costo_total' => 51500,
            ],
            'constancia-horas-extra' => [
                'titulo' => 'Constancia + Horas Extra',
                'tabla' => [
                    ['mes' => 'Enero', 'demanda' => 3000, 'produccion' => 2800, 'horas_extra' => 200, 'costo_extra' => 3000, 'costo' => 15500],
                    ['mes' => 'Febrero', 'demanda' => 2500, 'produccion' => 2700, 'horas_extra' => 0, 'costo_extra' => 0, 'costo' => 14000],
                    ['mes' => 'Marzo', 'demanda' => 4000, 'produccion' => 3200, 'horas_extra' => 800, 'costo_extra' => 6000, 'costo' => 18500],
                ],
                'costo_total' => 48000,
            ],
            default => abort(404),
        };

        return view('pap.alternativa', $data);
    }
}
