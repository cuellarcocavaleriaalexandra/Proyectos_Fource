package com.example.falldetectorapp

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.falldetectorapp.R // Add this import

class FallEventAdapter(private val events: List<FallEvent>) :
    RecyclerView.Adapter<FallEventAdapter.ViewHolder>() {

    class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val fechaText: TextView = view.findViewById(R.id.fechaText)
        val horaText: TextView = view.findViewById(R.id.horaText)
        val direccionText: TextView = view.findViewById(R.id.direccionText)
        val camaraText: TextView = view.findViewById(R.id.camaraText)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_fall_event, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val event = events[position]
        holder.fechaText.text = "Fecha: ${event.fecha}"
        holder.horaText.text = "Hora: ${event.hora}"
        holder.direccionText.text = "Dirección: ${event.direccion}"
        holder.camaraText.text = "Cámara: ${event.camara}"
    }

    override fun getItemCount() = events.size
}