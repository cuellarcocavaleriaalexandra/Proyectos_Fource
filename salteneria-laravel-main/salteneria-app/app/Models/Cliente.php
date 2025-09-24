<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Cliente extends Model
{
    /** @use HasFactory<\Database\Factories\ClienteFactory> */
    use HasFactory;

    protected $fillable = [
        'nombre',
        'carnet',
        'antiguedad',
    ];

    public function ventas()
    {
        return $this->hasMany(Venta::class);
    }

    public function obtener_descuento()
    {
        if ($this->antiguedad >= 3) {
            return 30.00;
        } elseif ($this->antiguedad >= 2) {
            return 20.00;
        } elseif ($this->antiguedad >= 1) {
            return 10.00;
        }
        return 0.00;
    }
}
