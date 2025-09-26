package com.example.falldetectorapp
import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import androidx.core.content.ContextCompat
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.falldetectorapp.R
import org.json.JSONObject
import org.json.JSONArray
import android.app.NotificationChannel
import android.app.NotificationManager
import android.util.Log
import com.example.falldetectorapp.FallEvent
import kotlinx.coroutines.*
import java.io.BufferedReader
import java.io.InputStreamReader
import java.net.HttpURLConnection
import java.net.URL

class MainActivity : AppCompatActivity() {

    private val fallEvents = mutableListOf<FallEvent>()
    private lateinit var recyclerView: RecyclerView
    private lateinit var adapter: FallEventAdapter
    private val NOTIFICATION_ID = 1
    private val CHANNEL_ID = "fall_detection_channel"
    private val NOTIFICATION_PERMISSION_CODE = 123

    // CAMBIA ESTA IP POR LA DE TU SERVIDOR
    private val BASE_URL = "http://192.168.43.11:8000"
    private val ENDPOINT = "/notifications"

    private var pollingJob: Job? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        setupNotificationChannel()
        requestNotificationPermission()

        recyclerView = findViewById(R.id.recyclerView)
        adapter = FallEventAdapter(fallEvents)
        recyclerView.adapter = adapter
        recyclerView.layoutManager = LinearLayoutManager(this)

        // Iniciar el polling para obtener eventos del servidor
        startPollingForEvents()
    }

    private fun setupNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val name = "Fall Detection"
            val descriptionText = "Notifications for detected falls"
            val importance = NotificationManager.IMPORTANCE_HIGH
            val channel = NotificationChannel(CHANNEL_ID, name, importance).apply {
                description = descriptionText
                enableVibration(true)
            }
            val notificationManager: NotificationManager =
                getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            notificationManager.createNotificationChannel(channel)
        }
    }

    private fun requestNotificationPermission() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            if (ContextCompat.checkSelfPermission(
                    this,
                    Manifest.permission.POST_NOTIFICATIONS
                ) != PackageManager.PERMISSION_GRANTED
            ) {
                ActivityCompat.requestPermissions(
                    this,
                    arrayOf(Manifest.permission.POST_NOTIFICATIONS),
                    NOTIFICATION_PERMISSION_CODE
                )
            }
        }
    }

    private fun startPollingForEvents() {
        pollingJob = CoroutineScope(Dispatchers.Main).launch {
            while (true) {
                try {
                    val response = fetchFallEventsFromServer()
                    response?.let { processServerResponse(it) }
                } catch (e: Exception) {
                    Log.e("MainActivity", "Error en polling: ${e.message}")
                }
                delay(5000) // Consulta cada 5 segundos
            }
        }
    }

    private suspend fun fetchFallEventsFromServer(): String? {
        return withContext(Dispatchers.IO) {
            try {
                val url = URL("$BASE_URL$ENDPOINT")
                val connection = url.openConnection() as HttpURLConnection

                connection.requestMethod = "GET"
                connection.connectTimeout = 5000
                connection.readTimeout = 5000
                connection.setRequestProperty("Content-Type", "application/json")

                val responseCode = connection.responseCode
                if (responseCode == HttpURLConnection.HTTP_OK) {
                    val reader = BufferedReader(InputStreamReader(connection.inputStream))
                    val response = reader.readText()
                    reader.close()
                    Log.d("MainActivity", "Respuesta del servidor: $response")
                    response
                } else {
                    Log.e("MainActivity", "Error HTTP: $responseCode")
                    null
                }
            } catch (e: Exception) {
                Log.e("MainActivity", "Error de conexión: ${e.message}")
                null
            }
        }
    }

    private fun processServerResponse(response: String) {
        try {
            // Si el servidor devuelve un array de eventos
            if (response.trim().startsWith("[")) {
                val jsonArray = JSONArray(response)
                for (i in 0 until jsonArray.length()) {
                    val jsonObject = jsonArray.getJSONObject(i)
                    processEventJson(jsonObject)
                }
            }
            // Si el servidor devuelve un solo evento
            else if (response.trim().startsWith("{")) {
                val jsonObject = JSONObject(response)
                processEventJson(jsonObject)
            }
        } catch (e: Exception) {
            Log.e("MainActivity", "Error procesando respuesta del servidor: ${e.message}")
        }
    }

    private fun processEventJson(jsonObject: JSONObject) {
        val fecha = jsonObject.optString("echa", "N/A")
        val hora = jsonObject.optString("hora", "N/A")
        val direccion = jsonObject.optString("direccion", "N/A")
        val camara = jsonObject.optString("idCamara", "N/A")
        val timestamp = jsonObject.optString("timestamp", "N/A")
        val imageUrl = jsonObject.optString("image_url", "")

        val newEvent = FallEvent(fecha, hora, direccion, camara, timestamp)

        // Verificar si el evento ya existe (para evitar duplicados)
        val eventExists = fallEvents.any {
            it.timestamp == timestamp && it.camara == camara
        }

        if (!eventExists) {
            fallEvents.add(0, newEvent)
            adapter.notifyItemInserted(0)
            recyclerView.scrollToPosition(0)

            showNotification("¡Caída Detectada!", "Se detectó una caída en $direccion a las $hora")
            Log.d("MainActivity", "Nuevo evento de caída agregado: $direccion")
        }
    }

    private fun showNotification(title: String, content: String) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            if (ContextCompat.checkSelfPermission(
                    this,
                    Manifest.permission.POST_NOTIFICATIONS
                ) != PackageManager.PERMISSION_GRANTED
            ) {
                Log.e("MainActivity", "Notification permission not granted")
                return
            }
        }

        val builder = NotificationCompat.Builder(this, CHANNEL_ID)
            .setSmallIcon(android.R.drawable.ic_dialog_alert)
            .setContentTitle(title)
            .setContentText(content)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setAutoCancel(true)

        with(NotificationManagerCompat.from(this)) {
            notify(NOTIFICATION_ID, builder.build())
        }
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == NOTIFICATION_PERMISSION_CODE) {
            if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                Log.d("MainActivity", "Notification permission granted")
            } else {
                Log.e("MainActivity", "Notification permission denied")
            }
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        pollingJob?.cancel() // Cancelar el polling cuando se destruya la actividad
    }
}