<?php

namespace App\Http\Controllers;

use App\Models\Cupon;
use Illuminate\Http\JsonResponse;

class CuponController extends Controller
{
    // En tu controlador de Laravel
    public function validarCupon($codigoCupon)
    {
        $cupon = Cupon::where('codigo', $codigoCupon)->first();

        if ($cupon) {
            return response()->json([
                'valido' => true,
                'descuento' => $cupon->descuento,
            ]);
        }

        return response()->json(['valido' => false], 404);
    }
}