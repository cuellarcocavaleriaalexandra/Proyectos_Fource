import cv2
import numpy as np
import os
from pathlib import Path

def eliminar_lineas_imagen(imagen_path, output_path):
    """
    Elimina líneas horizontales y verticales de imágenes de números manuscritos
    """
    img = cv2.imread(str(imagen_path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"No se pudo cargar la imagen: {imagen_path}")
        return

    _, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel_horizontal = np.ones((1, 15), np.uint8)
    kernel_vertical = np.ones((15, 1), np.uint8)
    lineas_h = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel_horizontal, iterations=2)
    lineas_v = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel_vertical, iterations=2)
    lineas_totales = cv2.bitwise_or(lineas_h, lineas_v)
    mascara = cv2.bitwise_not(lineas_totales)
    resultado = cv2.bitwise_and(thresh, thresh, mask=mascara)
    resultado = cv2.bitwise_not(resultado)
    cv2.imwrite(str(output_path), resultado)

def procesar_recortes_finales_sucre(input_base, output_base):
    """
    Aplica la limpieza de líneas a cada imagen en cada subcarpeta de cada subcarpeta de input_base,
    guardando el resultado en la misma estructura bajo output_base.
    """
    input_base = Path(input_base)
    output_base = Path(output_base)
    extensiones_permitidas = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')

    # Iterar por cada subcarpeta de cada subcarpeta
    for subcarpeta in input_base.iterdir():
        if subcarpeta.is_dir():
            for subsubcarpeta in subcarpeta.iterdir():
                if subsubcarpeta.is_dir():
                    for archivo in subsubcarpeta.iterdir():
                        if archivo.suffix.lower() in extensiones_permitidas:
                            # Ruta de salida manteniendo la estructura
                            output_dir = output_base / subcarpeta.name / subsubcarpeta.name
                            output_dir.mkdir(parents=True, exist_ok=True)
                            output_path = output_dir / archivo.name
                            print(f"Procesando: {archivo} -> {output_path}")
                            eliminar_lineas_imagen(archivo, output_path)
    print("Procesamiento completado!")

# Configuración
INPUT_BASE = "Recortes_finales_Sucre"
OUTPUT_BASE = "Recortes_finales_sin_lineas"

if __name__ == "__main__":
    if not os.path.exists(INPUT_BASE):
        print(f"Error: La carpeta de entrada '{INPUT_BASE}' no existe.")
    else:
        procesar_recortes_finales_sucre(INPUT_BASE, OUTPUT_BASE)
        print(f"Imágenes procesadas guardadas en: {OUTPUT_BASE}")