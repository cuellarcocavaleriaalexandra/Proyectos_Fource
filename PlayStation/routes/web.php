<?php

use Illuminate\Support\Facades\Route;
use Illuminate\Support\Facades\Auth;
use App\Http\Controllers\Auth\AuthController;
use App\Http\Controllers\AdminDashboardController;
use App\Http\Controllers\CompanyController;
use App\Http\Controllers\EmpleadoController;
use App\Http\Controllers\MpsController;
use App\Http\Controllers\ProductMetricsController;
use App\Http\Controllers\ProductionPlanController;
use App\Http\Controllers\ProductionProblemController;
use App\Http\Controllers\HomeController; // NUEVO CONTROLADOR PARA REDIRECCIÓN
use App\Http\Controllers\PapController;

// Redirigir la raíz a login
Route::redirect('/', '/login');

// Rutas públicas (sin autenticación)
Route::middleware('web')->group(function () {
    Route::get('/login', [AuthController::class, 'showLoginForm'])->name('login');
    Route::post('/login', [AuthController::class, 'login']);
    Route::post('/logout', [AuthController::class, 'logout'])->name('logout');
});

// Rutas protegidas por autenticación
Route::middleware(['web', 'auth'])->group(function () {

    // Redirige según rol al acceder a /dashboard
    Route::get('/dashboard', [HomeController::class, 'redirectUser'])->name('dashboard');

    // Dashboard de administrador
    Route::get('/admin/dashboard', [AdminDashboardController::class, 'index'])->name('admin.dashboard');

    // Dashboard de empleado
    Route::get('/employee/dashboard', [EmpleadoController::class, 'index'])->name('employee.dashboard');

    // Guardado de datos
    Route::post('/mps', [MpsController::class, 'store'])->name('mps.store');
    Route::post('/company', [CompanyController::class, 'store'])->name('company.store');

    // Actualizaciones por lote
    Route::put('/production-plans/update', [ProductionPlanController::class, 'batchUpdate'])->name('production-plans.batch-update');
    Route::put('production-problems/batch-update', [ProductionProblemController::class, 'batchUpdate'])->name('production-problems.batch-update');
    Route::put('product-metrics/batch-update', [ProductMetricsController::class, 'batchUpdate'])->name('product-metrics.batch-update');
    Route::put('/production-plan/batch-update', [ProductionPlanController::class, 'batchUpdate'])->name('production-plan.batch-update');
    Route::put('/production-plans/batch-update', [ProductionPlanController::class, 'batchUpdate'])->name('production-plan.batch-update');
    Route::post('/product-metrics/update', [ProductMetricsController::class, 'batchUpdate'])->name('product-metrics.batchUpdate');

    // Recursos
    Route::get('/production-plans', [ProductionPlanController::class, 'index']);
    Route::get('/admin/plan-agregado', [ProductionPlanController::class, 'index'])->name('admin.plan-agregado');
    Route::get('/pap', [PapController::class, 'index'])->name('pap.index');
    Route::get('/pap/alternativa/{tipo}', [PapController::class, 'show'])->name('pap.alternativa');
    
    Route::resource('product-metrics', ProductMetricsController::class)->only(['index', 'update']);
    Route::resource('production-plans', ProductionPlanController::class)->only(['index', 'update']);
    Route::resource('production-problems', ProductionProblemController::class)->only(['index', 'update']);
});
