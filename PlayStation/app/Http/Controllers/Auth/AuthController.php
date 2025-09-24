<?php

namespace App\Http\Controllers\Auth;

use App\Models\User;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;
class AuthController extends Controller
{
    public function showLoginForm()
    {
        return view('auth.login');
    }

 public function login(Request $request)
{
    $request->validate([
        'username' => 'required|string',
        'password' => 'required|string',
    ]);

    $credentials = $request->only('username', 'password');
    $remember = $request->has('remember');

    // Intento con bcrypt primero
    if (Auth::attempt($credentials, $remember)) {
        $request->session()->regenerate();
        
        return redirect()->intended(
            Auth::user()->role === 'admin' ? '/admin/dashboard' : '/employee/dashboard'
        );
    }

    // Intento con SHA1 (solo para migración)
    $user = User::where('username', $credentials['username'])->first();
    if ($user && sha1($credentials['password']) === $user->password) {
        $user->update(['password' => bcrypt($credentials['password'])]);
        Auth::login($user, $remember);
        $request->session()->regenerate();
        
        return redirect()->intended(
            $user->role === 'admin' ? '/admin/dashboard' : '/employee/dashboard'
        );
    }

    return back()->withErrors([
        'username' => 'Las credenciales no coinciden con nuestros registros.',
    ]);
}

    public function logout(Request $request)
    {
        Auth::logout();
        $request->session()->invalidate();
        $request->session()->regenerateToken();
        return redirect('/');
    }
}

