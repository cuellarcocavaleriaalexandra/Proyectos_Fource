<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class ProductMetric extends Model
{
    protected $fillable = [
        'income',
        'total_costs',
        'profitability',
        'marketability',
        // otros campos que necesites actualizar por mass assignment
    ];
}
