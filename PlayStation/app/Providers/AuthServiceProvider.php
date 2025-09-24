<?php

namespace App\Providers;

use Illuminate\Foundation\Support\Providers\AuthServiceProvider as ServiceProvider;
use Illuminate\Support\Facades\Gate;

class AuthServiceProvider extends ServiceProvider
{

public function boot()
{
    $this->registerPolicies();

    \Log::info('AuthServiceProvider cargado');

    Gate::define('admin', function ($user) {
        return $user->role === 'admin';
    });
}

}
