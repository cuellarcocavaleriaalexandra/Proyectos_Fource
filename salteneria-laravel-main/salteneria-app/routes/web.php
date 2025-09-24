<?php

use App\Http\Controllers\AuthController;
use App\Http\Controllers\SalteneriaControler;
use App\Http\Controllers\VentaController;
use App\Http\Controllers\ReporteController;
use App\Http\Controllers\AlmacenController;
use App\Http\Controllers\CuponController;
use App\Http\Controllers\ClienteController;
use Illuminate\Support\Facades\Route;

// Ruta de inicio
Route::get('/', [SalteneriaControler::class, 'index'])->name('home');

// Rutas de autenticación
Route::get('/login', [AuthController::class, 'showLogin'])->name('login');
Route::post('/login', [AuthController::class, 'login']);
Route::post('/logout', [AuthController::class, 'logout'])->name('logout');

// Rutas del sistema
Route::get('/buscar', [VentaController::class, 'index'])->name('buscar');
Route::post('/confirmar', [VentaController::class, 'confirmarVenta'])->name('confirmar');
Route::get('/notificaciones', [SalteneriaControler::class, 'notificaciones'])->name('notificaciones');
Route::get('/reportes', [ReporteController::class, 'index'])->name('reportes');
Route::get('/almacen', [AlmacenController::class, 'index'])->name('almacen');
Route::get('/almacen/crear', [AlmacenController::class, 'crear'])->name('almacen.crear');
Route::post('/almacen/guardar', [AlmacenController::class, 'guardar'])->name('almacen.guardar');
Route::get('/almacen/editar/{id}', [AlmacenController::class, 'editar'])->name('almacen.editar');
Route::put('/almacen/actualizar/{id}', [AlmacenController::class, 'actualizar'])->name('almacen.actualizar');
Route::delete('/almacen/eliminar/{id}', [AlmacenController::class, 'eliminar'])->name('almacen.eliminar');
Route::get('/validar-cupon/{codigoCupon}', [CuponController::class, 'validarCupon'])->name('validar-cupon');
Route::get('/validar-carnet/{carnet}', [ClienteController::class, 'validarCarnet'])->name('validar-carnet');
Route::get('/factura/{id}', [VentaController::class, 'mostrarFactura'])->name('factura');
Route::get('/factura/{id}/pdf', [VentaController::class, 'generarFacturaPDF'])->name('factura.pdf');
Route::get('/reporte/pdf', [ReporteController::class, 'generarPDF'])->name('reporte.pdf');