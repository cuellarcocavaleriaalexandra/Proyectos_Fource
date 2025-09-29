<?php

include 'conexion_be.php';

    $nombre_completo = $_POST['nombre_completo'];
    $correo =$_POST['correo'];
    $usuario = $_POST['usuario'];
    $contrasena = $_POST['contrasena'];

    $query = "INSERT INTO usuarios(nombre_completo, correo, usuario, contrasena) 
    VALUES('$nombre_completo', '$correo', '$usuario','$contrasena')";

    //verificar que valores no se repitan
     $verificar_correo = mysqli_query($conn, "SELECT * FROM usuarios WHERE correo='$correo' ");

    if(mysqli_num_rows($verificar_correo) > 0){
        echo'
        <script>        
        alert("Este correo ya esta registrado");
        window.location="../index.php";        
        </script> 
        ';
        exit();

    }

    $verificar_usuario = mysqli_query($conn, "SELECT * FROM usuarios WHERE usuario='$usuario' ");

    if(mysqli_num_rows($verificar_usuario) > 0){
        echo'
        <script>        
        alert("Este usuario ya esta registrado");
        window.location="../index.php";        
        </script> 
        ';
        exit();

    }

    $ejecutar = mysqli_query($conn, $query);
    if($ejecutar){
        echo'
            <script>
             alert("Usuario almacenado exitosamente");
             window.location = "../index.php";
            </script>
        ';
    }else{
        echo'
        <script>
         alert("Intentalo de nuevo, Falla al almacenar");
         window.location = "../index.php";
        </script>
    ';
    }
    mysqli_close($conn);

?>