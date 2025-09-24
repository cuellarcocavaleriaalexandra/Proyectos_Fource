<?php

$server = "localhost";
$user = "root";
$password = "";
$db = "empresas";

// Crear conexión
$conn = new mysqli($server, $user, $password, $db);

// Verificar conexión
/* if ($conn->connect_errno) {
  die("Conexión fallida: " . $conn->connect_errno);
} else{
  echo "conectado";
}*/

?>
