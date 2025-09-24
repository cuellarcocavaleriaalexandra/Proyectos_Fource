import cv2
import os

def dividir_en_celdas(img_path, output_dir):
    # Cargar la imagen en escala de grises
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    h, w = img.shape

    # Definir cortes verticales (3 celdas iguales: centenas, decenas, unidades)
    ancho_celda = w // 3

    # Crear carpeta de salida si no existe
    os.makedirs(output_dir, exist_ok=True)

    nombres = ["centenas", "decenas", "unidades"]

    for i in range(3):
        x_inicio = i * ancho_celda
        x_fin = (i + 1) * ancho_celda if i < 2 else w  # el último hasta el final
        recorte = img[:, x_inicio:x_fin]

        # Guardar recorte
        output_path = os.path.join(output_dir, f"{nombres[i]}.jpg")
        cv2.imwrite(output_path, recorte)

        print(f"Guardado: {output_path}")


# ================== EJEMPLO DE USO ==================
# Imagen de ejemplo (recorte de votos)
img_path = "Recortes\mesa_4_2067031_recortada\AP.png"   # aquí tu recorte original
output_dir = "Recortes\mesa_4_2067031_recortada\celdas"

dividir_en_celdas(img_path, output_dir)
