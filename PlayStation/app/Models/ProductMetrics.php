<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class ProductMetrics extends Model
{
    //class ProductMetric extends Model

    protected $fillable = ['income', 'total_costs', 'profitability', 'marketability'];

}
