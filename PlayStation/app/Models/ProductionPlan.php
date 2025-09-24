<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class ProductionPlan extends Model
{
    protected $fillable = ['product_name', 'quantity', 'date'];
}
