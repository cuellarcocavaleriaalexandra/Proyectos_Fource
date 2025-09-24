var boton_encriptar = document.querySelector(".boton_encriptador");
var boton_desencriptar = document.querySelector(".boton_desencriptador");
var munieco = document.querySelector(".contenedor_preview_resultado");
var contenedor_parrafo = document.querySelector(".contenedor_parrafo");
var resultado = document.querySelector(".texto_resultado");
var Contenedor_resultado = document.querySelector(".contenedor_resultado")

boton_encriptar.onclick = encriptar;
boton_desencriptar.onclick = desencriptar;



function encriptar() {
    const validacion = /^[a-z\s]+$/
    var Contenedor_caja_texto = recuperarTexto();
   
    
    if (!validacion.test(Contenedor_caja_texto)) {
        alert("El texto debe estar en minúsculas y no debe contener caracteres especiales.");
      }else{
        ocultarAdelante();
        var textoEncriptado = encriptarTexto(Contenedor_caja_texto);
        resultado.textContent = textoEncriptado;
      }

}

function encriptarTexto(mensaje) {
    var texto = mensaje;
    var textoFinal = "";

    for (var i = 0; i < texto.length; i++) {
        if (texto[i] === "a") {
            textoFinal = textoFinal + "ai";
        } else if (texto[i] === "e") {
            textoFinal = textoFinal + "enter";
        } else if (texto[i] === "i") {
            textoFinal = textoFinal + "imes";
        } else if (texto[i] === "o") {
            textoFinal = textoFinal + "ober";
        } else if (texto[i] === "u") {
            textoFinal = textoFinal + "ufat";
        } else {
            textoFinal = textoFinal + texto[i];
        }
    }

    return textoFinal;
}


function desencriptar() {
    ocultarAdelante();
    var Contenedor_caja_texto = recuperarTexto();
    var textoDesencriptado = desencriptarTexto(Contenedor_caja_texto);
    resultado.textContent = textoDesencriptado;
}

function desencriptarTexto(mensaje) {
    var texto = mensaje;
    var textoFinal = "";

    for (var i = 0; i < texto.length; i++) {
        if (texto[i] == "a" ) {
            textoFinal = textoFinal + "a";
            i++;
        } else if (texto[i] == "e" ) {
            textoFinal = textoFinal + "e";
            i+= 4;
        } else if (texto[i] == "i" ) {
            textoFinal = textoFinal + "i";
            i += 3;
        } else if (texto[i] == "o" ) {
            textoFinal = textoFinal + "o";
            i += 3;
        } else if (texto[i] == "u" ) {
            textoFinal = textoFinal + "u";
            i += 3;
        } else {
            textoFinal = textoFinal + texto[i];
        }
    }

    return textoFinal;
}

function ocultarAdelante() {
    munieco.classList.add("ocultar");
    contenedor_parrafo.classList.add("ocultar");
}

function ocultarCopia(){
    resultado.classList.add("ocultar")
}

function recuperarTexto() {
    var Contenedor_caja_texto = document.querySelector(".caja_texto");
    return Contenedor_caja_texto.value;
}

const botonCopiar = document.querySelector(".boton_copiar");
botonCopiar.addEventListener("click", copiar = () => {
    var contenido = document.querySelector(".texto_resultado").textContent;
    navigator.clipboard.writeText(contenido);
    console.log("hola");
});

