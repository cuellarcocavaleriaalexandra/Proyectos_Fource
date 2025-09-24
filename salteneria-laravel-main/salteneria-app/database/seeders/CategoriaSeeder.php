<?php

namespace Database\Seeders;

use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;
use App\Models\Categoria;

class CategoriaSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        $categorias = [
            ['id' => 1, 'nombre' => 'Salteñas'],
            ['id' => 2, 'nombre' => 'Jugos'],
            ['id' => 3, 'nombre' => 'Postres']
        ];

        foreach ($categorias as $categoria) {
            Categoria::create($categoria);
        }
    }
}
