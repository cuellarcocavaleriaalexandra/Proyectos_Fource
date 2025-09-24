<?php

protected $routeMiddleware = [
    'auth' => \App\Http\Middleware\Authenticate::class,
    'can' => \App\Http\Middleware\Authorize::class,
    // ...
];