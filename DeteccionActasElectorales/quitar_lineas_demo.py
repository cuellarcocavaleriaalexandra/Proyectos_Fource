import cv2
import numpy as np
import os
from pathlib import Path

def eliminar_lineas_imagen(imagen_path, output_path):
    """
    Elimina líneas horizontales y verticales de imágenes de números manuscritos
    """
    # Leer la imagen
    img = cv2.imread(imagen_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"No se pudo cargar la imagen: {imagen_path}")
        return
    
    # Aplicar umbral para binarizar la imagen
    _, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Crear kernels para detectar líneas
    kernel_horizontal = np.ones((1, 15), np.uint8)  # Para líneas horizontales
    kernel_vertical = np.ones((15, 1), np.uint8)    # Para líneas verticales
    
    # Detectar líneas horizontales
    lineas_h = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel_horizontal, iterations=2)
    
    # Detectar líneas verticales  
    lineas_v = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel_vertical, iterations=2)
    
    # Combinar todas las líneas detectadas
    lineas_totales = cv2.bitwise_or(lineas_h, lineas_v)
    
    # Crear máscara para eliminar las líneas
    mascara = cv2.bitwise_not(lineas_totales)
    
    # Aplicar la máscara a la imagen original
    resultado = cv2.bitwise_and(thresh, thresh, mask=mascara)
    
    # Invertir la imagen de vuelta al formato normal
    resultado = cv2.bitwise_not(resultado)
    
    # Guardar la imagen procesada
    cv2.imwrite(output_path, resultado)

def procesar_carpeta(input_folder, output_folder):
    """
    Procesa todas las imágenes en la carpeta de entrada y guarda en la de salida
    """
    # Crear carpeta de salida si no existe
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    # Obtener lista de archivos de imagen
    extensiones_permitidas = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')
    archivos = [f for f in os.listdir(input_folder) 
               if f.lower().endswith(extensiones_permitidas)]
    
    print(f"Procesando {len(archivos)} imágenes...")
    
    for i, archivo in enumerate(archivos):
        input_path = os.path.join(input_folder, archivo)
        output_path = os.path.join(output_folder, archivo)
        
        print(f"Procesando {i+1}/{len(archivos)}: {archivo}")
        eliminar_lineas_imagen(input_path, output_path)
    
    print("Procesamiento completado!")

# Configuración - CAMBIA ESTAS RUTAS SEGÚN TUS NECESIDADES
INPUT_FOLDER = "Recortes\mesa_4_2067031_recortada\celdas"    # Carpeta con las imágenes originales
OUTPUT_FOLDER = "cleaned_images" # Carpeta donde se guardarán las imágenes procesadas

if __name__ == "__main__":
    # Verificar que la carpeta de entrada existe
    if not os.path.exists(INPUT_FOLDER):
        print(f"Error: La carpeta de entrada '{INPUT_FOLDER}' no existe.")
        print("Por favor, crea la carpeta y coloca las imágenes allí.")
    else:
        procesar_carpeta(INPUT_FOLDER, OUTPUT_FOLDER)
        print(f"Imágenes procesadas guardadas en: {OUTPUT_FOLDER}")