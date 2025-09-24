<?php

$server = "localhost";
$user = "root";
$password = "";
$db = "empresas";

// Crear conexión
$conn = new mysqli($server, $user, $password, $db);

// Verificar conexión
if ($conn->connect_errno) {
  die("Conexión fallida: " . $conn->connect_errno);
}else{
  echo "conectado";
}

//$conn = mysqli_connect("localhost", "root", "", "login_register_db");

//comprobacion de la base de datos
/*
if($conexion){
    echo 'Conectado exitosamente a la Base de Datos';
}else{
    echo 'No se ha podido conectar a la Base de Datos';
}
*/

?>