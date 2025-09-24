<?php

namespace App\Http\Controllers;

use App\Models\Cliente;
use Illuminate\Http\JsonResponse;

class ClienteController extends Controller
{
    public function validarCarnet($carnet): JsonResponse
    {
        $cliente = Cliente::where('carnet', $carnet)->first();

        if ($cliente) {
            $descuento = $cliente->obtener_descuento();
            return response()->json(['existe' => true, 'descuento' => $descuento]);
        }

        return response()->json(['existe' => false]);
    }
}