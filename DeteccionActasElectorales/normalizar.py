import cv2
import os

# 🔹 Ruta de entrada (carpeta donde tienes las actas recortadas)
input_folder = r"ActasSucreProcesadas"

# 🔹 Ruta de salida (donde se guardarán las actas normalizadas)
output_folder = r"Nomalizadas_Sucre"
os.makedirs(output_folder, exist_ok=True)

# 🔹 Tamaño estándar
STANDARD_WIDTH = 2200
STANDARD_HEIGHT = 1500

def normalizar_acta(img_path, save_path):
    img = cv2.imread(img_path)

    if img is None:
        print(f"No se pudo leer la imagen {img_path}")
        return

    # Redimensionar al tamaño estándar
    img_resized = cv2.resize(img, (STANDARD_WIDTH, STANDARD_HEIGHT), interpolation=cv2.INTER_CUBIC)

    # Guardar imagen normalizada
    cv2.imwrite(save_path, img_resized)
    print(f"✅ Guardada normalizada: {save_path}")

# 🔹 Procesar todas las actas de la carpeta
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        normalizar_acta(input_path, output_path)
