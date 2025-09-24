<?php

namespace Database\Seeders;

use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;
use App\Models\Producto;

class ProductoSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        $productos = [
            ['id' => 1, 'nombre' => 'Salteña de carne', 'precio' => 5, 'categoria_id' => 1, 'stock' => 10, 'imagen' => 'productos/1.jpeg'],
            ['id' => 2, 'nombre' => 'Salteña de pollo', 'precio' => 5, 'categoria_id' => 1, 'stock' => 2, 'imagen' => 'productos/2.jpeg'],
            ['id' => 3, 'nombre' => 'Salteña de cerdo', 'precio' => 5, 'categoria_id' => 1, 'stock' => 5, 'imagen' => 'productos/3.jpeg'],
            ['id' => 4, 'nombre' => 'Salteña de queso', 'precio' => 5, 'categoria_id' => 1, 'stock' => 5, 'imagen' => 'productos/4.jpeg'],
            ['id' => 5, 'nombre' => 'Salteña de verduras', 'precio' => 5, 'categoria_id' => 1, 'stock' => 22, 'imagen' => 'productos/5.jpeg'],
            ['id' => 6, 'nombre' => 'Salteña picante', 'precio' => 6, 'categoria_id' => 1, 'stock' => 0, 'imagen' => 'productos/6.jpeg'],
            ['id' => 7, 'nombre' => 'Salteña con huevo', 'precio' => 6, 'categoria_id' => 1, 'stock' => 10, 'imagen' => 'productos/7.jpeg'],
            ['id' => 8, 'nombre' => 'Salteña de chorizo', 'precio' => 6, 'categoria_id' => 1, 'stock' => 28, 'imagen' => 'productos/8.jpeg'],
            ['id' => 9, 'nombre' => 'Salteña de atún', 'precio' => 6, 'categoria_id' => 1, 'stock' => 14, 'imagen' => 'productos/9.jpeg'],
            ['id' => 10, 'nombre' => 'Salteña especial', 'precio' => 6, 'categoria_id' => 1, 'stock' => 11, 'imagen' => 'productos/10.jpeg'],
            ['id' => 11, 'nombre' => 'Salteña de pavo', 'precio' => 7, 'categoria_id' => 1, 'stock' => 21, 'imagen' => 'productos/11.jpeg'],
            ['id' => 12, 'nombre' => 'Salteña con papas', 'precio' => 7, 'categoria_id' => 1, 'stock' => 30, 'imagen' => 'productos/12.jpeg'],
            ['id' => 13, 'nombre' => 'Salteña con champiñones', 'precio' => 7, 'categoria_id' => 1, 'stock' => 25, 'imagen' => 'productos/13.jpeg'],
            ['id' => 14, 'nombre' => 'Salteña de mariscos', 'precio' => 7, 'categoria_id' => 1, 'stock' => 22, 'imagen' => 'productos/14.jpeg'],
            ['id' => 15, 'nombre' => 'Salteña de espinacas', 'precio' => 7, 'categoria_id' => 1, 'stock' => 4, 'imagen' => 'productos/15.jpeg'],
            ['id' => 16, 'nombre' => 'Jugo de naranja', 'precio' => 15, 'categoria_id' => 2, 'stock' => 2, 'imagen' => 'productos/16.jpeg'],
            ['id' => 17, 'nombre' => 'Jugo de mango', 'precio' => 15, 'categoria_id' => 2, 'stock' => 49, 'imagen' => 'productos/17.jpeg'],
            ['id' => 18, 'nombre' => 'Jugo de manzana', 'precio' => 15, 'categoria_id' => 2, 'stock' => 48, 'imagen' => 'productos/18.jpg'],
            ['id' => 19, 'nombre' => 'Jugo de piña', 'precio' => 15, 'categoria_id' => 2, 'stock' => 3, 'imagen' => 'productos/19.jpeg'],
            ['id' => 20, 'nombre' => 'Jugo de uva', 'precio' => 15, 'categoria_id' => 2, 'stock' => 50, 'imagen' => 'productos/20.jpeg'],
            ['id' => 21, 'nombre' => 'Jugo de fresa', 'precio' => 16, 'categoria_id' => 2, 'stock' => 50, 'imagen' => 'productos/21.jpeg'],
            ['id' => 22, 'nombre' => 'Jugo de guanábana', 'precio' => 16, 'categoria_id' => 2, 'stock' => 4, 'imagen' => 'productos/22.jpg'],
            ['id' => 23, 'nombre' => 'Jugo de papaya', 'precio' => 16, 'categoria_id' => 2, 'stock' => 47, 'imagen' => 'productos/23.jpeg'],
            ['id' => 24, 'nombre' => 'Jugo de maracuyá', 'precio' => 16, 'categoria_id' => 2, 'stock' => 8, 'imagen' => 'productos/24.jpg'],
            ['id' => 25, 'nombre' => 'Jugo de cereza', 'precio' => 16, 'categoria_id' => 2, 'stock' => 49, 'imagen' => 'productos/25.jpg'],
            ['id' => 26, 'nombre' => 'Jugo de melón', 'precio' => 17, 'categoria_id' => 2, 'stock' => 48, 'imagen' => 'productos/26.jpeg'],
            ['id' => 27, 'nombre' => 'Jugo de kiwi', 'precio' => 17, 'categoria_id' => 2, 'stock' => 3, 'imagen' => 'productos/27.jpeg'],
            ['id' => 28, 'nombre' => 'Jugo de granada', 'precio' => 17, 'categoria_id' => 2, 'stock' => 50, 'imagen' => 'productos/28.jpeg'],
            ['id' => 29, 'nombre' => 'Jugo de durazno', 'precio' => 17, 'categoria_id' => 2, 'stock' => 50, 'imagen' => 'productos/29.jpeg'],
            ['id' => 30, 'nombre' => 'Jugo de coco', 'precio' => 17, 'categoria_id' => 2, 'stock' => 50, 'imagen' => 'productos/30.jpg'],
            ['id' => 31, 'nombre' => 'Torta de chocolate', 'precio' => 22, 'categoria_id' => 3, 'stock' => 30, 'imagen' => 'productos/31.jpg'],
            ['id' => 32, 'nombre' => 'Gelatina', 'precio' => 22, 'categoria_id' => 3, 'stock' => 3, 'imagen' => 'productos/32.jpeg'],
            ['id' => 33, 'nombre' => 'Cheesecake', 'precio' => 22, 'categoria_id' => 3, 'stock' => 20, 'imagen' => 'productos/33.jpg'],
            ['id' => 34, 'nombre' => 'Flan', 'precio' => 22, 'categoria_id' => 3, 'stock' => 7, 'imagen' => 'productos/34.jpeg'],
            ['id' => 35, 'nombre' => 'Panna cotta', 'precio' => 22, 'categoria_id' => 3, 'stock' => 20, 'imagen' => 'productos/35.jpg'],
            ['id' => 36, 'nombre' => 'Brownie', 'precio' => 23, 'categoria_id' => 3, 'stock' => 30, 'imagen' => 'productos/36.jpg'],
            ['id' => 37, 'nombre' => 'Mousse de chocolate', 'precio' => 23, 'categoria_id' => 3, 'stock' => 20, 'imagen' => 'productos/37.jpg'],
            ['id' => 38, 'nombre' => 'Tarta de manzana', 'precio' => 23, 'categoria_id' => 3, 'stock' => 2, 'imagen' => 'productos/38.jpg'],
            ['id' => 39, 'nombre' => 'Arroz con leche', 'precio' => 23, 'categoria_id' => 3, 'stock' => 37, 'imagen' => 'productos/39.jpeg'],
            ['id' => 40, 'nombre' => 'Tarta de limón', 'precio' => 23, 'categoria_id' => 3, 'stock' => 20, 'imagen' => 'productos/40.jpg'],
            ['id' => 41, 'nombre' => 'Crumble de frutas', 'precio' => 24, 'categoria_id' => 3, 'stock' => 20, 'imagen' => 'productos/41.jpeg'],
            ['id' => 42, 'nombre' => 'Cupcake', 'precio' => 24, 'categoria_id' => 3, 'stock' => 27, 'imagen' => 'productos/42.jpg'],
            ['id' => 43, 'nombre' => 'Tarta de queso', 'precio' => 24, 'categoria_id' => 3, 'stock' => 6, 'imagen' => 'productos/43.jpeg'],
            ['id' => 44, 'nombre' => 'Trufas de chocolate', 'precio' => 24, 'categoria_id' => 3, 'stock' => 30, 'imagen' => 'productos/44.jpg'],
            ['id' => 45, 'nombre' => 'Bizcocho de vainilla', 'precio' => 24, 'categoria_id' => 3, 'stock' => 5, 'imagen' => 'productos/45.jpeg']
        ];

        foreach ($productos as $producto) {
            Producto::create($producto);
        }
    }
}
