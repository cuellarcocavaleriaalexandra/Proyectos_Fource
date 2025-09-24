<?php

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;
use App\Models\Cliente;
use Illuminate\Support\Str;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\Cliente>
 */
class ClienteFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    protected $model = Cliente::class;

    public function definition()
    {
        return [
            'nombre' => $this->faker->name(),
            'carnet' => strtoupper(Str::random(8)),
            'antiguedad' => $this->faker->numberBetween(0, 5),
        ];
    }
}
