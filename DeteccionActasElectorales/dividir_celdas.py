import cv2
import os
from pathlib import Path

def dividir_en_celdas(img_path, output_dir):
    img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"⚠️ No se pudo leer la imagen: {img_path}")
        return
    h, w = img.shape
    ancho_celda = w // 3
    nombres = ["centenas", "decenas", "unidades"]

    os.makedirs(output_dir, exist_ok=True)

    for i in range(3):
        x_inicio = i * ancho_celda
        x_fin = (i + 1) * ancho_celda if i < 2 else w
        recorte = img[:, x_inicio:x_fin]
        output_path = os.path.join(output_dir, f"{nombres[i]}.jpg")
        cv2.imwrite(output_path, recorte)
        print(f"Guardado: {output_path}")

def procesar_subcarpetas_sucre(sucre_dir, salida_base):
    sucre_dir = Path(sucre_dir)
    salida_base = Path(salida_base)
    for subcarpeta in sucre_dir.iterdir():
        if subcarpeta.is_dir():
            for img_path in subcarpeta.glob("*.jpg"):
                if img_path.stem == "codigo_mesa":
                    continue
                # Carpeta de salida: Recortes_finales_Sucre/<subcarpeta>/<nombre_imagen_sin_extensión>
                output_dir = salida_base / subcarpeta.name / img_path.stem
                dividir_en_celdas(img_path, output_dir)

# ================== EJEMPLO DE USO ==================
# Carpeta principal de Sucre
sucre_dir = "Recortes_secciones_Sucre"
salida_base = "Recortes_finales_Sucre"
procesar_subcarpetas_sucre(sucre_dir, salida_base)