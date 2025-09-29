import cv2
import os
from pathlib import Path

# 📂 Carpeta de entrada (donde están las actas normalizadas)
input_folder = r"Nomalizadas_Sucre"

# 📂 Carpeta de salida
output_folder = r"Recortes_secciones_Sucre"
os.makedirs(output_folder, exist_ok=True)

# 🔹 Diccionario de coordenadas (x1, y1, x2, y2)
coordenadas = {
    "codigo_mesa": (885, 211, 1013, 252),

    "AP": (667, 434, 798, 478),
    "LYP_ADN": (668, 488, 797, 535),
    "APB_SUMATE": (667, 545, 797, 591),
    "LIBRE": (667, 656, 798, 702),
    "FP": (667, 713, 798, 756),
    "MAS_IPSP": (668, 769, 798, 811),
    "UNIDAD": (665, 877, 797, 923),
    "PDC": (666, 934, 798, 979),

    "validos": (667, 1025, 798, 1069),
    "blancos": (667, 1123, 798, 1169),
    "nulos": (667, 1180, 798, 1224),
}

def recortar_y_guardar(img, save_dir, nombre, coords):
    """Recorta una región y la guarda en archivo JPG"""
    x1, y1, x2, y2 = coords
    recorte = img[y1:y2, x1:x2]
    save_path = os.path.join(save_dir, f"{nombre}.jpg")
    cv2.imwrite(save_path, recorte)

def procesar_acta(img_path, output_folder):
    """Procesa una sola acta: crea subcarpeta y guarda recortes"""
    img_name = Path(img_path).stem  # nombre sin extensión
    save_dir = os.path.join(output_folder, img_name)
    os.makedirs(save_dir, exist_ok=True)

    img = cv2.imread(img_path)
    if img is None:
        print(f"⚠️ No se pudo leer la imagen {img_path}")
        return

    for nombre, coords in coordenadas.items():
        recortar_y_guardar(img, save_dir, nombre, coords)

    print(f"✅ Procesada y recortada: {img_name}")

def main():
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            img_path = os.path.join(input_folder, filename)
            procesar_acta(img_path, output_folder)

if __name__ == "__main__":
    main()
