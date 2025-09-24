package com.example.pedidosapp

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.Button
import android.widget.Toast
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.pedidosapp.databinding.ActivityAdminBinding
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.GoogleAuthProvider
import com.google.firebase.firestore.FirebaseFirestore
import java.util.ArrayList
import com.example.pedidosapp.AuthActivity

class AdminActivity : AppCompatActivity() {

    val db = FirebaseFirestore.getInstance()
    private lateinit var binding : ActivityAdminBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityAdminBinding.inflate(layoutInflater)
        setContentView(binding.root)



        val guardarDatos = findViewById<Button>(R.id.buttonGuardar) as Button
        val borrarProducto = findViewById<Button>(R.id.buttonEliminar) as Button

        //val VerEmail = findViewById<Button>(R.id.buttonVerEmail) as Button
        val VerTodosProductos = findViewById<Button>(R.id.buttonVerTodosProductos) as Button


        guardarDatos.setOnClickListener(){
            agregarDatos()
        }

        borrarProducto.setOnClickListener(){
            eliminarProducto()
        }
        VerTodosProductos.setOnClickListener {
            val i = Intent(this, VerTodosProductosActivity::class.java)
            startActivity(i)
        }
        binding.buttonVerTodosPedidos.setOnClickListener{
            val i = Intent(this, VerTodosPedidosActivity::class.java)
            startActivity(i)
        }



        //para el boton insertar nuevo producto
        binding.buttonInsertaProducto.setOnClickListener {

            binding.cardViewInsertarP.visibility = View.VISIBLE
            binding.buttonInsertaProducto.visibility = View.GONE
        }
        binding.buttonCerrarInertP.setOnClickListener {

            binding.cardViewInsertarP.visibility = View.GONE
            binding.buttonInsertaProducto.visibility = View.VISIBLE
        }
        //para el boton insertar nuevo producto

        //para el boton Eliminar producto por su codigo
        binding.buttonEliminarProductoCode.setOnClickListener {

            binding.cardViewElimCP.visibility = View.VISIBLE
            //binding.buttonEliminarProductoCode.visibility = View.GONE
        }
        binding.buttonCerrarElimP.setOnClickListener {

            binding.cardViewElimCP.visibility = View.GONE
            //binding.buttonEliminarProductoCode.visibility = View.VISIBLE
        }
        //para el boton Eliminar producto por su codigo





        //verrecycler()
        //llamarrecyclerview()

//        VerEmail.setOnClickListener {
//
//            val user = FirebaseAuth.getInstance().currentUser       //para obtener el usuario actual
//            val correoElectronico = user?.email                     //para obtener el email
//            Toast.makeText(this, "aqui se ve el email $correoElectronico", Toast.LENGTH_LONG).show()
//
//        }
    }

//    private fun llamarrecyclerview() {
//
//        producList = ArrayList()
//        adapterproduct = Adapterproductos(producList)
//        db.collection("Productos")
//            .orderBy("Nombre del producto")
//            .get()
//            .addOnSuccessListener { documets ->
//                for(document in documets){
//                    val wallItem = document.toObject(ItemProduct::class.java)
//                    wallItem.idProduct = document.id
//                    wallItem.nomProduct = document["Nombre del producto"].toString()
//                    wallItem.tipProduct = document["Tipo del producto"].toString()
//                    wallItem.preProduct = document["Precio del producto"].toString().toInt()
//                    wallItem.nitProduct = document["Codigo del producto"].toString()
//                    wallItem.imgProduct = document["Imagen del producto"].toString()
//
//                    binding.recyclerssProduct.adapter = adapterproduct
//                    binding.recyclerssProduct.layoutManager = LinearLayoutManager(this)
//                    producList.add(wallItem)
//                }
//            }
//
//    }


    private fun agregarDatos() {

        if( binding.DatoProducto.text.toString().isBlank()
            or binding.DatoDescripcion.text.toString().isBlank()
            or binding.DatoTipo.text.toString().isBlank()
            or binding.DatoMarca.text.toString().isBlank()
            or binding.DatoUnidad.text.toString().isBlank()
            or binding.DatoPrecio.text.toString().isBlank()
            or binding.DatoUrlImagen.text.toString().isBlank()) {
            Toast.makeText(this, "Por favor rellene los campos", Toast.LENGTH_LONG).show()
        }

        else{
            val user = hashMapOf(

                "Nombre" to binding.DatoProducto.text.toString(),
                "Descripcion" to binding.DatoDescripcion.text.toString(),
                "Tipo" to binding.DatoTipo.text.toString(),
                "Marca" to binding.DatoMarca.text.toString(),
                "Unidad" to binding.DatoUnidad.text.toString(),
                "Precio" to binding.DatoPrecio.text.toString().toInt(),
                "Imagen del producto" to binding.DatoUrlImagen.text.toString()

            )
            db.collection("Productos")
                .add(user)
                .addOnSuccessListener {  documentReference ->
                    Toast.makeText(this, "Producto agregado correctamente", Toast.LENGTH_LONG).show()
                    println("agregado correctamente xd")

                    /*producList.add(ItemProduct(documentReference.id, binding.DatoProducto.text.toString(),
                                                                    binding.DatoTipo.text.toString(),
                                                                    binding.DatoPrecio.text.toString().toInt(),
                                                                    binding.DatoNitProducto.text.toString(),
                                                                    "https://waifus.wiki/wp-content/uploads/2021/07/Es2oz-LW4AEqdmd.jpg"))*/
                    //llamarrecyclerview()

                    //adapterproduct.notifyDataSetChanged()
                }
                .addOnFailureListener {e-> Log.w("Tag","Error $e")}

//prueba
            binding.DatoProducto.text.clear()
            binding.DatoDescripcion.text.clear()
            binding.DatoTipo.text.clear()
            binding.DatoMarca.text.clear()
            binding.DatoUnidad.text.clear()
            binding.DatoPrecio.text.clear()
            binding.DatoUrlImagen.text.clear()


        }
    }
    private fun eliminarProducto() {

        val datoBuscar =binding.DatoBuscarProducto.text.toString()
       // val docRef = db.collection("Productos").document( binding.DatoBuscarProducto.text.toString()).toString()

        if(binding.DatoBuscarProducto.text.toString().isBlank() ){
            Toast.makeText(this, "No puso el Codigo de producto", Toast.LENGTH_LONG).show()
        }
        else{

                db.collection("Productos").document( binding.DatoBuscarProducto.text.toString())
                    .delete()
                    .addOnSuccessListener { Log.d("Tag","se Elimino correctamente $datoBuscar") }
                    .addOnFailureListener {e-> Log.w("Tag","Error al borrar el documento $e")}
                Toast.makeText(this, "Se elimino correctamente $datoBuscar", Toast.LENGTH_LONG).show()
                binding.DatoBuscarProducto.text.clear()

               //llamarrecyclerview()
                //adapterproduct.notifyDataSetChanged()

        }
    }




   /* private fun verrecycler() {
        adapterproduct= Adapterproductos(cargarlista())
        binding.recyclerssProduct.adapter = adapterproduct
        binding.recyclerssProduct.layoutManager = LinearLayoutManager(this)
    }

    private fun cargarlista(): MutableList<ItemProduct> {
        val lista = mutableListOf<ItemProduct>()

        lista.add(ItemProduct("1","Arroz","Integral",50, "123455","https://somoskudasai.com/wp-content/uploads/2023/04/portada_go-toubun-no-hanayome-170.jpg"))
        lista.add(ItemProduct("1","Arroz","Integral",50, "123456","https://somoskudasai.com/wp-content/uploads/2023/04/portada_go-toubun-no-hanayome-170.jpg"))
        lista.add(ItemProduct("1","Arroz","Integral",50, "123457","https://somoskudasai.com/wp-content/uploads/2023/04/portada_go-toubun-no-hanayome-170.jpg"))
        lista.add(ItemProduct("1","Arroz","Integral",50, "123457","https://somoskudasai.com/wp-content/uploads/2023/04/portada_go-toubun-no-hanayome-170.jpg"))
        lista.add(ItemProduct("1","Arroz","Integral",50, "123457","https://somoskudasai.com/wp-content/uploads/2023/04/portada_go-toubun-no-hanayome-170.jpg"))
        lista.add(ItemProduct("1","Arroz","Integral",50, "123457","https://somoskudasai.com/wp-content/uploads/2023/04/portada_go-toubun-no-hanayome-170.jpg"))

        return lista

    }*/



    //ejemplo



}