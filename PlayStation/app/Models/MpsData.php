<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class MpsData extends Model
{
    public function mps()
{
    return $this->hasMany(Mps::class);
}
}
