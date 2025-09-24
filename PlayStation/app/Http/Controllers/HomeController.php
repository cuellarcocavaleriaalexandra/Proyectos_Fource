<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Auth;

class HomeController extends Controller
{
    public function redirectUser()
    {
        $user = Auth::user();

        if (!$user) {
            abort(403, 'No autenticado');
        }

        if ($user->role === 'admin') {
            return redirect()->route('admin.dashboard');
        }

        if ($user->role === 'empleado') {
            return redirect()->route('employee.dashboard');
        }

        abort(403, 'Rol no autorizado');
    }
}
