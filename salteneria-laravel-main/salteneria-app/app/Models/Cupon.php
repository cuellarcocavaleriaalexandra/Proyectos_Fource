<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Cupon extends Model
{
    /** @use HasFactory<\Database\Factories\CuponFactory> */
    use HasFactory;
    protected $table = 'cupones';

    protected $fillable = [
        'codigo',
        'descuento',
        'valido_hasta',
    ];

    public function isValid()
    {
        return $this->valido_hasta >= now();
    }

    public function ventas()
    {
        return $this->hasMany(Venta::class);
    }
}
