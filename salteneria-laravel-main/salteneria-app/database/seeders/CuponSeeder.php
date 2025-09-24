<?php

namespace Database\Seeders;

use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;
use App\Models\Cupon;

class CuponSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run()
    {
        Cupon::factory()->count(50)->create();
    }
}
