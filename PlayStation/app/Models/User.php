<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    use Notifiable;

    protected $table = 'users';
    public $timestamps = false; // Si tu tabla no tiene timestamps

    protected $fillable = [
        'username', 'password', 'role'
    ];
    public function getAuthPassword()
{
    return $this->password;
}
}