package com.example.falldetectorapp



data class FallEvent(
    val fecha: String,
    val hora: String,
    val direccion: String,
    val camara: String,
    val timestamp: String
)