<?php

session_start();
include 'conexion_be.php';

    $correo =$_POST['correo'];
    $contrasena =$_POST['contrasena'];

    $validar_login = mysqli_query($conn, "SELECT * FROM usuarios WHERE correo='$correo'
    and contrasena='$contrasena'");

    if(mysqli_num_rows($validar_login)>0){
        $_SESSION['usuario']=$correo;
        header("location: ../menu.php");
        exit;
    }else{
        echo'
        
        <script>
        alert("Usuario no existe");
        window.location = "../index.php";
        </script>
        ';
        exit;

    }

?>