<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */


    public function up()
    {
        Schema::create('cupones', function (Blueprint $table) {
            $table->id(); 
            $table->string('codigo', 20)->unique();
            $table->decimal('descuento', 5, 2);
            $table->dateTime('valido_hasta');
            $table->timestamps();
        });
    }

    public function down()
    {
        Schema::dropIfExists('cupones');
    }

};
