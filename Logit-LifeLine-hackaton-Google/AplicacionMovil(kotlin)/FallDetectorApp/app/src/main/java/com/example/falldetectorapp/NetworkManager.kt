package com.example.falldetectorapp

import android.util.Log
import kotlinx.coroutines.*
import java.io.BufferedReader
import java.io.InputStreamReader
import java.net.HttpURLConnection
import java.net.URL

class NetworkManager {

    companion object {
        // CAMBIA ESTA IP POR LA IP DE TU SERVIDOR
        private const val BASE_URL = "http://192.168.43.11:8000" // Ejemplo de IP local
        private const val ENDPOINT = "/notifications" // Endpoint de tu API

        // Función para obtener eventos de caída del servidor
        suspend fun getFallEvents(): String? {
            return withContext(Dispatchers.IO) {
                try {
                    val url = URL("$BASE_URL$ENDPOINT")
                    val connection = url.openConnection() as HttpURLConnection

                    connection.requestMethod = "GET"
                    connection.connectTimeout = 5000
                    connection.readTimeout = 5000

                    val responseCode = connection.responseCode
                    if (responseCode == HttpURLConnection.HTTP_OK) {
                        val reader = BufferedReader(InputStreamReader(connection.inputStream))
                        val response = reader.readText()
                        reader.close()
                        response
                    } else {
                        Log.e("NetworkManager", "Error HTTP: $responseCode")
                        null
                    }
                } catch (e: Exception) {
                    Log.e("NetworkManager", "Error de red: ${e.message}")
                    null
                }
            }
        }

        // Función para hacer polling continuo (opcional)
        fun startPolling(onNewEvent: (String) -> Unit) {
            CoroutineScope(Dispatchers.Main).launch {
                while (true) {
                    val response = getFallEvents()
                    response?.let { onNewEvent(it) }
                    delay(2000) // Consulta cada 5 segundos
                }
            }
        }
    }
}