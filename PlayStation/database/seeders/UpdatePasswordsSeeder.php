<?php

namespace Database\Seeders;

use App\Models\User;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;

class UpdatePasswordsSeeder extends Seeder
{
    public function run()
    {
        User::where('username', 'admin')->update([
            'password' => Hash::make('admin') // Cambia 'admin' por tu contraseña
        ]);

        User::where('username', 'dario')->update([
            'password' => Hash::make('dario')
        ]);

        User::where('username', 'user1')->update([
            'password' => Hash::make('password123')
        ]);

        $this->command->info('Contraseñas actualizadas correctamente!');
    }
}