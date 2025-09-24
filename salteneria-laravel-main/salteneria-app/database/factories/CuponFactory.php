<?php

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;
use App\Models\Cupon;
use Illuminate\Support\Str;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\Cupon>
 */
class CuponFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
     protected $model = Cupon::class;

    public function definition()
    {
        return [
            'codigo' => strtoupper(Str::random(6)),
            'descuento' => $this->faker->numberBetween(5, 50),
            'valido_hasta' => $this->faker->dateTimeBetween('+1 days', '+30 days'),
        ];
    }
}
